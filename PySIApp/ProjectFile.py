'''
 Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
 Unpublished Copyright (c) 2015-2017 Peter J. Pupalaikis and Teledyne LeCroy,
 All Rights Reserved.

 Explicit license in accompanying README.txt file.  If you don't have that file
 or do not agree to the terms in that file, then you are not licensed to use
 this material whatsoever.
'''
from ProjectFileBase import XMLConfiguration,XMLPropertyDefaultFloat,XMLPropertyDefaultString,XMLPropertyDefaultInt,XMLPropertyDefaultBool
from ProjectFileBase import ProjectFileBase,XMLProperty

import os
import sys

class PartPropertyConfiguration(XMLConfiguration):
    def __init__(self):
        XMLConfiguration.__init__(self)
        self.dict['Keyword']=XMLPropertyDefaultString('Keyword')
        self.dict['PropertyName']=XMLPropertyDefaultString('PropertyName')
        self.dict['Description']=XMLPropertyDefaultString('Description')
        self.dict['Value']=XMLPropertyDefaultString('Value')
        self.dict['Hidden']=XMLPropertyDefaultBool('Hidden')
        self.dict['Visible']=XMLPropertyDefaultBool('Visible')
        self.dict['KeywordVisible']=XMLPropertyDefaultBool('KeywordVisible')
        self.dict['Type']=XMLPropertyDefaultString('Type')
        self.dict['Unit']=XMLPropertyDefaultString('Unit')

class PartPictureConfiguration(XMLConfiguration):
    def __init__(self):
        XMLConfiguration.__init__(self)
        self.dict['ClassNames']=XMLProperty('ClassNames',[XMLPropertyDefaultString('ClassName') for _ in range(0)],'array')
        self.dict['Selected']=XMLPropertyDefaultBool('Selected',False)
        self.dict['Origin']=XMLPropertyDefaultString('Origin')
        self.dict['Orientation']=XMLPropertyDefaultInt('Orientation')
        self.dict['MirroredVertically']=XMLPropertyDefaultBool('MirroredVertically',False)
        self.dict['MirroredHorizontally']=XMLPropertyDefaultBool('MirroredHorizontally',False)

class DeviceConfiguration(XMLConfiguration):
    def __init__(self):
        XMLConfiguration.__init__(self)
        self.dict['ClassName']=XMLPropertyDefaultString('ClassName')
        self.dict['PartPicture']=PartPictureConfiguration()
        self.dict['PartProperties']=XMLProperty('PartProperties',[PartPropertyConfiguration() for _ in range(0)],'array')

class VertexConfiguration(XMLConfiguration):
    def __init__(self):
        XMLConfiguration.__init__(self)
        self.dict['Vertex']=XMLPropertyDefaultString('Vertex')

class WireConfiguration(XMLConfiguration):
    def __init__(self):
        XMLConfiguration.__init__(self)
        self.dict['Vertices']=XMLProperty('Vertices',[XMLPropertyDefaultString() for _ in range(0)],'array')

class DrawingPropertiesConfiguration(XMLConfiguration):
    def __init__(self):
        XMLConfiguration.__init__(self)
        self.dict['Grid']=XMLPropertyDefaultInt('Grid',32)
        self.dict['Originx']=XMLPropertyDefaultInt('Originx',1)
        self.dict['Originy']=XMLPropertyDefaultInt('Originy',4)
        self.dict['Width']=XMLPropertyDefaultInt('Width',711)
        self.dict['Height']=XMLPropertyDefaultInt('Height',318)
        self.dict['Geometry']=XMLPropertyDefaultString('Geometry','711x363+27+56')

class SchematicConfiguration(XMLConfiguration):
    def __init__(self):
        XMLConfiguration.__init__(self)
        self.dict['Devices']=XMLProperty('Devices',[DeviceConfiguration() for _ in range(0)],'array')
        self.dict['Wires']=XMLProperty('Wires',[WireConfiguration() for _ in range(0)],'array')

class DrawingConfiguration(XMLConfiguration):
    def __init__(self):
        XMLConfiguration.__init__(self)
        self.dict['DrawingProperties']=DrawingPropertiesConfiguration()
        self.dict['Schematic']=SchematicConfiguration()

class CalculationPropertiesConfiguration(XMLConfiguration):
    def __init__(self):
        XMLConfiguration.__init__(self)
        self.dict['EndFrequency']=XMLPropertyDefaultFloat('EndFrequency',20e9)
        self.dict['FrequencyPoints']=XMLPropertyDefaultInt('FrequencyPoints',2000)
        self.dict['UserSampleRate']=XMLPropertyDefaultFloat('UserSampleRate',40e9)

class ProjectFile(ProjectFileBase):
    def __init__(self):
        ProjectFileBase.__init__(self,os.path.basename(__file__).split('.')[0])
        self.dict['Drawing']=DrawingConfiguration()
        self.dict['CalculationProperties']=CalculationPropertiesConfiguration()

from PySIApp import TheApp
class App(TheApp):
    def __init__(self):
        TheApp.__init__(self,False)
    def ConvertOldProjectToNew(self,oldfilename,newfilename):
        import xml.etree.ElementTree as et
        tree=et.parse(oldfilename)
        root=tree.getroot()
        for child in root:
            if child.tag == 'drawing':
                self.Drawing.InitFromXml(child)
            elif child.tag == 'calculation_properties':
                self.calculationProperties.InitFromXml(child, self)

        project=ProjectFile()
        project.SetValue('Drawing.DrawingProperties.Grid',self.Drawing.grid)
        project.SetValue('Drawing.DrawingProperties.Originx',self.Drawing.originx)
        project.SetValue('Drawing.DrawingProperties.Originy',self.Drawing.originy)
        project.SetValue('Drawing.DrawingProperties.Width',self.Drawing.canvas.winfo_width())
        project.SetValue('Drawing.DrawingProperties.Height',self.Drawing.canvas.winfo_height())
        project.SetValue('Drawing.DrawingProperties.Geometry',self.root.geometry())
        project.SetValue('Drawing.Schematic.Devices',[DeviceConfiguration() for _ in range(len(self.Drawing.schematic.deviceList))])
        for d in range(len(project.GetValue('Drawing.Schematic.Devices'))):
            deviceProject=project.GetValue('Drawing.Schematic.Devices')[d]
            device=self.Drawing.schematic.deviceList[d]
            deviceProject.SetValue('ClassName',device.__class__.__name__)
            partPictureProject=deviceProject.GetValue('PartPicture')
            partPicture=device.partPicture
            partPictureProject.SetValue('ClassNames',[XMLPropertyDefaultString('ClassName',name) for name in partPicture.partPictureClassList])
            partPictureProject.SetValue('Selected',partPicture.partPictureSelected)
            partPictureProject.SetValue('Origin',partPicture.current.origin)
            partPictureProject.SetValue('Orientation',partPicture.current.orientation)
            partPictureProject.SetValue('MirroredVertically',partPicture.current.mirroredVertically)
            partPictureProject.SetValue('MirroredHorizontally',partPicture.current.mirroredHorizontally)
            deviceProject.SetValue('PartProperties',[PartPropertyConfiguration() for _ in range(len(device.propertiesList))])
            for p in range(len(deviceProject.GetValue('PartProperties'))):
                partPropertyProject=deviceProject.GetValue('PartProperties')[p]
                partProperty=device.propertiesList[p]
                partPropertyProject.SetValue('Keyword',partProperty.keyword)
                partPropertyProject.SetValue('PropertyName',partProperty.propertyName)
                partPropertyProject.SetValue('Description',partProperty.description)
                partPropertyProject.SetValue('Value',partProperty.PropertyString(stype='raw'))
                partPropertyProject.SetValue('Hidden',partProperty.hidden)
                partPropertyProject.SetValue('Visible',partProperty.visible)
                partPropertyProject.SetValue('KeywordVisible',partProperty.keywordVisible)
                partPropertyProject.SetValue('Type',partProperty.type)
                partPropertyProject.SetValue('Unit',partProperty.unit)
        project.SetValue('Drawing.Schematic.Wires',[WireConfiguration() for _ in range(len(self.Drawing.schematic.wireList))])
        for w in range(len(project.GetValue('Drawing.Schematic.Wires'))):
            wireProject=project.GetValue('Drawing.Schematic.Wires')[w]
            wire=self.Drawing.schematic.wireList[w]
            wireProject.SetValue('Vertices',[XMLPropertyDefaultString('Vertex',str(vertex.coord)) for vertex in wire])
        project.SetValue('CalculationProperties.EndFrequency',self.calculationProperties.endFrequency)
        project.SetValue('CalculationProperties.FrequencyPoints',self.calculationProperties.frequencyPoints)
        project.SetValue('CalculationProperties.UserSampleRate',self.calculationProperties.userSampleRate)
        project.Write(newfilename)
        project.Read(newfilename)
        project.Write(newfilename)
        pass
            
 
if __name__ == '__main__':
    App().ConvertOldProjectToNew('RLCTest2.xml', 'NewFile.xml')
    
    
    
    
    
    
    
    
    
    
#     installdir=os.path.dirname(os.path.abspath(__file__))
#     if len(sys.argv) < 3:
#         print 'no project file provided'
#         raise
#     
#     oldProjectFileName=sys.argv[1]
#     newProjectFileName=sys.argv[2]
#     
#     pf=ProjectFile().Read(installdir+'\\'+projectFileName)
#     pf.PrintFullInformation()
#     #pf.OutputXML()
#     pf.Write(installdir+'\\'+projectFileName)
    #print pf.GetValue('Instrument.AWG.SerialNumber')