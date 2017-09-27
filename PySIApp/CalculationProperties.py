'''
 Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
 Unpublished Copyright (c) 2015-2016 Peter J. Pupalaikis and Teledyne LeCroy,
 All Rights Reserved.

 Explicit license in accompanying README.txt file.  If you don't have that file
 or do not agree to the terms in that file, then you are not licensed to use
 this material whatsoever.
'''
# This is the legacy calculation properties to be removed eventually

class CalculationProperties(object):
    def __init__(self,parent,endFrequency=20e9,frequencyPoints=400,userSampleRate=40e9):
        self.parent=parent
        self.schematic=parent.Drawing.schematic
        self.endFrequency=endFrequency
        self.frequencyPoints=frequencyPoints
        self.userSampleRate=userSampleRate
        self.CalculateOthersFromBaseInformation()
    def CalculateOthersFromBaseInformation(self):
        self.baseSampleRate=self.endFrequency*2
        self.timePoints=self.frequencyPoints*2
        self.frequencyResolution=self.endFrequency/self.frequencyPoints
        self.impulseLength=1./self.frequencyResolution
    def InitFromXml(self,calculationPropertiesElement,parent):
        endFrequency=20e9
        frequencyPoints=400
        userSampleRate=40e9
        for calculationProperty in calculationPropertiesElement:
            if calculationProperty.tag == 'end_frequency':
                endFrequency=float(calculationProperty.text)
            elif calculationProperty.tag == 'frequency_points':
                frequencyPoints=int(calculationProperty.text)
            elif calculationProperty.tag == 'user_samplerate':
                userSampleRate = float(calculationProperty.text)
        self.__init__(parent,endFrequency,frequencyPoints,userSampleRate)
