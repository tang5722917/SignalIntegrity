'''
 Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
 Unpublished Copyright (c) 2015-2016 Peter J. Pupalaikis and Teledyne LeCroy,
 All Rights Reserved.

 Explicit license in accompanying README.txt file.  If you don't have that file
 or do not agree to the terms in that file, then you are not licensed to use
 this material whatsoever.
'''
from ProjectFile import DeviceNetListConfiguration,DeviceNetListKeywordConfiguration

class DeviceNetListLine(DeviceNetListConfiguration):
    def __init__(self,devicename=None,partname=None,showReference=True,showports=True,values=None):
        DeviceNetListConfiguration.__init__(self)
        if devicename is None:
            self.SetValue('DeviceName','device')
        else:
            self.SetValue('DeviceName',devicename)
        self.SetValue('PartName',partname)
        self.SetValue('ShowReference',showReference)
        self.SetValue('ShowPorts',showports)
        if not values is None:
            self.SetValue('Values',[DeviceNetListKeywordConfiguration() for _ in range(len(values))])
            for vi in range(len(values)):
                (kw,show)=values[vi]
                self.GetValue('Values')[vi].SetValue('Keyword',kw)
                self.GetValue('Values')[vi].SetValue('ShowKeyword',show)
    def NetListLine(self,device):
        returnstring=self.GetValue('DeviceName')
        if self.GetValue('ShowReference'):
            if not returnstring=='':
                returnstring=returnstring+' '
            returnstring=returnstring+device['ref'].PropertyString(stype='raw')
        if self.GetValue('ShowPorts'):
            if not returnstring=='':
                returnstring=returnstring+' '
            returnstring=returnstring+device['ports'].PropertyString(stype='raw')
        if not self.GetValue('PartName') is None:
            if not returnstring=='':
                returnstring=returnstring+' '
            returnstring=returnstring+self.GetValue('PartName')
        for kwc in self.GetValue('Values'):
            if not returnstring=='':
                returnstring=returnstring+' '
            if kwc.GetValue('ShowKeyword'):
                returnstring=returnstring+kwc.GetValue('Keyword')+' '
            returnstring=returnstring+device[kwc.GetValue('Keyword')].PropertyString(stype='raw')
        return returnstring
