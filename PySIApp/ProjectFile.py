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
        self.dict['ClassNames']=XMLProperty('ClassNames',[XMLPropertyDefaultString('ClassName') for _ in range(0)],'string')
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
        self.dict['PartProperties']=XMLProperty('PartProperties',[PartPropertyConfiguration() for _ in range(0)])

class VertexConfiguration(XMLConfiguration):
    def __init__(self):
        XMLConfiguration.__init__(self)
        self.dict['Coord']=XMLPropertyDefaultString('Coord')
        self.dict['Selected']=XMLPropertyDefaultBool('Selected',False)

class WireConfiguration(XMLConfiguration):
    def __init__(self):
        XMLConfiguration.__init__(self)
        self.dict['Vertex']=XMLProperty('Vertex',[VertexConfiguration() for _ in range(0)],'string')

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
        self.dict['Devices']=XMLProperty('Devices',[DeviceConfiguration() for _ in range(0)])
        self.dict['Wires']=XMLProperty('Wires',[WireConfiguration() for _ in range(0)])

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
        self.dict['BaseSampleRate']=XMLPropertyDefaultFloat('BaseSampleRate')
        self.dict['TimePoints']=XMLPropertyDefaultInt('TimePoints')
        self.dict['FrequencyResolution']=XMLPropertyDefaultFloat('FrequencyResolution')
        self.dict['ImpulseResponseLength']=XMLPropertyDefaultFloat('ImpulseResponseLength')

class ProjectFile(ProjectFileBase):
    def __init__(self):
        ProjectFileBase.__init__(self,os.path.basename(__file__).split('.')[0],'pysi_project')
        self.dict['Drawing']=DrawingConfiguration()
        self.dict['CalculationProperties']=CalculationPropertiesConfiguration()

    def Read(self, filename,drawing):
        ProjectFileBase.Read(self, filename)
        # calculate certain calculation properties
        self.SetValue('CalculationProperties.BaseSampleRate', self.GetValue('CalculationProperties.EndFrequency')*2)
        self.SetValue('CalculationProperties.TimePoints',self.GetValue('CalculationProperties.FrequencyPoints')*2)
        self.SetValue('CalculationProperties.FrequencyResolution', self.GetValue('CalculationProperties.EndFrequency')/self.GetValue('CalculationProperties.FrequencyPoints'))
        self.SetValue('CalculationProperties.ImpulseResponseLength',1./self.GetValue('CalculationProperties.FrequencyResolution'))
        drawing.InitFromProject(self)
        return self

    def Write(self,filename,app):
        self.SetValue('Drawing.DrawingProperties.Grid',app.Drawing.grid)
        self.SetValue('Drawing.DrawingProperties.Originx',app.Drawing.originx)
        self.SetValue('Drawing.DrawingProperties.Originy',app.Drawing.originy)
        self.SetValue('Drawing.DrawingProperties.Width',app.Drawing.canvas.winfo_width())
        self.SetValue('Drawing.DrawingProperties.Height',app.Drawing.canvas.winfo_height())
        self.SetValue('Drawing.DrawingProperties.Geometry',app.root.geometry())
        self.SetValue('Drawing.Schematic.Devices',[DeviceConfiguration() for _ in range(len(app.Drawing.schematic.deviceList))])
        for d in range(len(self.GetValue('Drawing.Schematic.Devices'))):
            deviceProject=self.GetValue('Drawing.Schematic.Devices')[d]
            device=app.Drawing.schematic.deviceList[d]
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
        ProjectFileBase.Write(self,filename)
        return self

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
            wireProject.SetValue('Vertex',[VertexConfiguration() for vertex in wire])
            for v in range(len(wireProject.GetValue('Vertex'))):
                vertexProject=wireProject.GetValue('Vertex')[v]
                vertex=wire[v]
                vertexProject.SetValue('Vertex',vertex.coord)
        project.SetValue('CalculationProperties.EndFrequency',self.calculationProperties.endFrequency)
        project.SetValue('CalculationProperties.FrequencyPoints',self.calculationProperties.frequencyPoints)
        project.SetValue('CalculationProperties.UserSampleRate',self.calculationProperties.userSampleRate)
        project.Write(newfilename)
        project.Read(newfilename)
        project.Write(newfilename)
        #project.PrintFullInformation()
            
 
if __name__ == '__main__':

    filesList=[
        '/home/peterp/Work/PySI/TestPySIApp/FilterTest.xml',
        '/home/peterp/Work/PySI/TestPySIApp/FourPortTLineTest.xml',
        '/home/peterp/Work/PySI/TestPySIApp/Devices.xml',
        '/home/peterp/Work/PySI/TestPySIApp/TestVRM.xml',
        '/home/peterp/Work/PySI/TestPySIApp/OpenStub.xml',
        '/home/peterp/Work/PySI/PowerIntegrity/TestVRMIstvan2.xml',
        '/home/peterp/Work/PySI/PowerIntegrity/VP/Measure.xml',
        '/home/peterp/Work/PySI/PowerIntegrity/VP/Calculate.xml',
        '/home/peterp/Work/PySI/PowerIntegrity/VP/Compare.xml',
        '/home/peterp/Work/PySI/PowerIntegrity/TestVRMIstvan.xml',
        '/home/peterp/Work/PySI/PowerIntegrity/TestVRMEquiv.xml',
        '/home/peterp/Work/PySI/PowerIntegrity/VRMWaveformCompare.xml',
        '/home/peterp/Work/PySI/PowerIntegrity/TestCNaturalResponse.xml',
        '/home/peterp/Work/PySI/PowerIntegrity/TestVRMModel.xml',
        '/home/peterp/Work/PySI/PowerIntegrity/VPSteady/FeedbackNetwork.xml',
        '/home/peterp/Work/PySI/PowerIntegrity/VPSteady/Measure5.xml',
        '/home/peterp/Work/PySI/PowerIntegrity/VPSteady/Measure.xml',
        '/home/peterp/Work/PySI/PowerIntegrity/VPSteady/Measure2.xml',
        '/home/peterp/Work/PySI/PowerIntegrity/VPSteady/Measure4.xml',
        '/home/peterp/Work/PySI/PowerIntegrity/VPSteady/Measure3.xml',
        '/home/peterp/Work/PySI/PowerIntegrity/VPSteady/Measure6.xml',
        '/home/peterp/Work/PySI/PowerIntegrity/LoadResistanceBWL.xml',
        '/home/peterp/Work/PySI/PowerIntegrity/TestVRMEquivAC.xml',
        '/home/peterp/Work/PySI/PowerIntegrity/TestVRM.xml',
        '/home/peterp/Work/PySI/TestSignalIntegrity/TestCurrentSense.xml',
        '/home/peterp/Work/PySI/TestSignalIntegrity/TestVRMParasitics.xml',
        '/home/peterp/Work/PySI/TestSignalIntegrity/TestVRM.xml',
        '/home/peterp/Work/PySI/PySIApp/FourPortTests/DifferentialTransmissionLineComparesMixedMode.xml',
        '/home/peterp/Work/PySI/PySIApp/FourPortTests/Mutual.xml',
        '/home/peterp/Work/PySI/PySIApp/FourPortTests/telegrapherFourPortTwoElements.xml',
        '/home/peterp/Work/PySI/PySIApp/FourPortTests/telegrapherFourPortCircuitOneSection.xml',
        '/home/peterp/Work/PySI/PySIApp/FourPortTests/DifferentialTransmissionLineCompares.xml',
        '/home/peterp/Work/PySI/PySIApp/FourPortTests/telegrapherFourPortElement.xml',
        '/home/peterp/Work/PySI/PySIApp/FourPortTests/TL_test_Circuit1_Pete.xml',
        '/home/peterp/Work/PySI/PySIApp/FourPortTests/telegrapherFourPort10000Elements.xml',
        '/home/peterp/Work/PySI/PySIApp/FourPortTests/DimaWay.xml',
        '/home/peterp/Work/PySI/PySIApp/FourPortTests/telegrapherFourPortCircuitTwoSections.xml',
        '/home/peterp/Work/PySI/PySIApp/Examples/XRAYTest.xml',
        '/home/peterp/Work/PySI/PySIApp/Examples/RLCTest.xml',
        '/home/peterp/Work/PySI/PySIApp/Examples/telegrapherFourPort.xml',
        '/home/peterp/Work/PySI/PySIApp/Examples/SParameterExample.xml',
        '/home/peterp/Work/PySI/PySIApp/Examples/RC.xml',
        '/home/peterp/Work/PySI/PySIApp/Examples/telegrapherTestFourPort.xml',
        '/home/peterp/Work/PySI/PySIApp/Examples/SParameterExample/SParameterGenerationExample.xml',
        '/home/peterp/Work/PySI/PySIApp/Examples/DeembedCableFilter.xml',
        '/home/peterp/Work/PySI/PySIApp/Examples/PulseGeneratorTest.xml',
        '/home/peterp/Work/PySI/PySIApp/Examples/SimulationExample/SimulatorExample.xml',
        '/home/peterp/Work/PySI/PySIApp/Examples/SimulationExample/InvCheby_8.xml',
        '/home/peterp/Work/PySI/PySIApp/Examples/SimulationExample/BMYcheby.xml',
        '/home/peterp/Work/PySI/PySIApp/Examples/SimulationExample/BMYchebySParameters.xml',
        '/home/peterp/Work/PySI/PySIApp/Examples/XRAYTest2.xml',
        '/home/peterp/Work/PySI/PySIApp/Examples/telegrapherTestTwoPort.xml',
        '/home/peterp/Work/PySI/PySIApp/Examples/VirtualProbingExample/VirtualProbeExampleSimulation2.xml',
        '/home/peterp/Work/PySI/PySIApp/Examples/VirtualProbingExample/VirtualProbeExampleSimulation.xml',
        '/home/peterp/Work/PySI/PySIApp/Examples/VirtualProbingExample/VirtualProbeExampleCompare.xml',
        '/home/peterp/Work/PySI/PySIApp/Examples/VirtualProbingExample/VirtualProbeExample.xml',
        '/home/peterp/Work/PySI/PySIApp/Examples/RLC.xml',
        '/home/peterp/Work/PySI/PySIApp/Examples/CascCableFilter.xml',
        #'/home/peterp/Work/PySI/PySIApp/Examples/RCNetwork.xml',
        '/home/peterp/Work/PySI/PySIApp/Examples/StepGeneratorTest.xml',
        '/home/peterp/Work/PySI/PySIApp/Examples/RLCTest2.xml',
        '/home/peterp/Work/PySI/PySIApp/VirtualProbeTests/comparison.xml',
        '/home/peterp/Work/PySI/PySIApp/VirtualProbeTests/Example2.xml',
        '/home/peterp/Work/PySI/PySIApp/VirtualProbeTests/SimpleCaseExample1.xml',
        '/home/peterp/Work/PySI/PySIApp/VirtualProbeTests/Example3DegreeOfFreedom.xml',
        '/home/peterp/Work/PySI/PySIApp/VirtualProbeTests/SimpleCase.xml',
        '/home/peterp/Work/PySIBook/TransmissionLines/TerminationDifferentialCenterTapUnbalanced.xml',
        '/home/peterp/Work/PySIBook/TransmissionLines/FourPortMixedModeModelCompareTlines.xml',
        '/home/peterp/Work/PySIBook/TransmissionLines/TerminationMixedMode.xml',
        '/home/peterp/Work/PySIBook/TransmissionLines/MixedModeSimulation.xml',
        '/home/peterp/Work/PySIBook/TransmissionLines/MixedModeConverterSymbol.xml',
        '/home/peterp/Work/PySIBook/TransmissionLines/FourPortMixedModeModelCompareTelegrapher.xml',
        '/home/peterp/Work/PySIBook/TransmissionLines/TerminationDifferentialCenterTapACCoupled.xml',
        '/home/peterp/Work/PySIBook/TransmissionLines/TerminationDifferentialTee.xml',
        '/home/peterp/Work/PySIBook/TransmissionLines/TerminationDifferentialCenterTap.xml',
        '/home/peterp/Work/PySIBook/TransmissionLines/SimulationTerminationDifferentialTee.xml',
        '/home/peterp/Work/PySIBook/TransmissionLines/BalancedFourPortTelegrapherMixedMode.xml',
        '/home/peterp/Work/PySIBook/TransmissionLines/TerminationDifferentialOnly.xml',
        '/home/peterp/Work/PySIBook/TransmissionLines/DifferentialTelegrapher.xml',
        '/home/peterp/Work/PySIBook/TransmissionLines/DifferentialTelegrapherBalancede.xml',
        '/home/peterp/Work/PySIBook/TransmissionLines/TerminationDifferentialPi.xml',
        '/home/peterp/Work/PySIBook/TransmissionLines/BalancedFourPortModelMixedMode.xml',
        '/home/peterp/Work/PySIBook/TransmissionLines/MixedModeConverterVoltageSymbol.xml',
        '/home/peterp/Work/PySIBook/TransmissionLines/MixedModeSimulationPi.xml',
        '/home/peterp/Work/PySIBook/TransmissionLines/MixedModeSimulationTee.xml',
        '/home/peterp/Work/PySIBook/SParameters/Mutual.xml',
        '/home/peterp/Work/PySIBook/Simulation/SimulationCircuitSchematic2.xml',
        '/home/peterp/Work/PySIBook/Simulation/SimulationCircuitBlockDiagram.xml',
        '/home/peterp/Work/PySIBook/Simulation/SimulationCircuitSchematic.xml',
        '/home/peterp/Work/PySIBook/WaveformProcessing/TransferMatricesProcessing.xml',
        '/home/peterp/Work/PySIBook/SymbolicDeviceSolutions/FourPortVoltageAmplifierVoltageSeriesFeedbackCircuit.xml',
        '/home/peterp/Work/PySIBook/SymbolicDeviceSolutions/TransistorThreePortCircuit.xml',
        '/home/peterp/Work/PySIBook/VirtualProbing/VirtualProbingSimpleExample.xml',
        '/home/peterp/Work/PySIBook/VirtualProbing/VirtualProbingTwoVoltageExample.xml',
        '/home/peterp/Work/PySIBook/VirtualProbing/VirtualProbingDifferentialExample.xml',
        '/home/peterp/Work/PySIBook/VirtualProbing/VirtualProbingProbeDeembeddingExample.xml',
        '/home/peterp/Work/PySIBook/NetworkParameters/ShuntImpedanceInstrumentedZ.xml',
        '/home/peterp/Work/PySIBook/NetworkParameters/FileDevice.xml',
        '/home/peterp/Work/PySIBook/NetworkParameters/YParametersSchematic.xml',
        '/home/peterp/Work/PySIBook/NetworkParameters/SimpleCircuitAnalysisExampleNetwork.xml',
        '/home/peterp/Work/PySIBook/NetworkParameters/ArbitraryCircuitInstrumentedZ.xml',
        '/home/peterp/Work/PySIBook/NetworkParameters/ClassicNetworkParameterDevice.xml',
        '/home/peterp/Work/PySIBook/NetworkParameters/CascABCD.xml',
        '/home/peterp/Work/PySIBook/NetworkParameters/SeriesImpedanceInstrumentedZ.xml',
        '/home/peterp/Work/PySIBook/NetworkParameters/SeriesImpedanceInstrumentedY.xml',
        '/home/peterp/Work/PySIBook/NetworkParameters/ZParametersSchematic.xml',
        '/home/peterp/Work/PySIBook/NetworkParameters/SimpleCircuitAnalysisExampleCircuit.xml',
        '/home/peterp/Work/PySIBook/Sources/Amplifiers/OperationalAmplifierSymbol.xml',
        '/home/peterp/Work/PySIBook/Sources/Amplifiers/VoltageAmplifierTwoPortSymbol.xml',
        '/home/peterp/Work/PySIBook/Sources/Amplifiers/CurrentAmplifierFourPortCircuit.xml',
        '/home/peterp/Work/PySIBook/Sources/Amplifiers/VoltageAmplifierTwoPortCircuit.xml',
        '/home/peterp/Work/PySIBook/Sources/Amplifiers/OperationalAmplifierCircuit.xml',
        '/home/peterp/Work/PySIBook/Sources/Amplifiers/VoltageAmplifierFourPortSymbol.xml',
        '/home/peterp/Work/PySIBook/Sources/Amplifiers/VoltageAmplifierThreePortCircuit.xml',
        '/home/peterp/Work/PySIBook/Sources/Amplifiers/VoltageAmplifierFourPortCircuit.xml',
        '/home/peterp/Work/PySIBook/Sources/IdealTransformer/testIdealTransformer.xml',
        '/home/peterp/Work/PySIBook/Sources/IdealTransformer/IdealTransformerSP.xml',
        '/home/peterp/Work/PySIBook/Sources/IdealTransformer/IdealTransformerCircuit.xml',
        '/home/peterp/Work/PySIBook/Sources/IdealTransformer/IdealTransformerSymbol.xml',
        '/home/peterp/Work/PySIBook/Sources/DependentSources/DependentSources.xml',
        '/home/peterp/Work/TempProject/SenseResistorVirtualProbe.xml',
        '/home/peterp/Work/TempProject/SenseResistorMeasurement.xml',
        '/home/peterp/Work/TempProject/SenseResistorSimple.xml'
    ]

    app=App()
    for file in filesList:
        oldfile=file
        newfile=file.split('.')[0]+'.pysi_project'
        
        print 'oldfile: '+oldfile+' -> newfile: '+newfile
        app.ConvertOldProjectToNew(oldfile,newfile)
    
    
    
    
    
    
    
    
    
    
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