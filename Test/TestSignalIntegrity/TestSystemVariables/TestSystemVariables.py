"""
TestSystemVariables.py
"""

# Copyright (c) 2018 Teledyne LeCroy, Inc.
# All rights reserved worldwide.
#
# This file is part of SignalIntegrity.
#
# SignalIntegrity is free software: You can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation, either
# version 3 of the License, or any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>

import os
import unittest

import SignalIntegrity.Lib as si
import SignalIntegrity.App as siapp

class TestSystemVariablesTest(unittest.TestCase,
        si.test.SParameterCompareHelper,si.test.SignalIntegrityAppTestHelper):
    relearn=True
    plot=False
    debug=False
    checkPictures=True
    epsilon=50e-12
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.cwd=os.getcwd()
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        #si.test.SignalIntegrityAppTestHelper.forceWritePictures=True
        from SignalIntegrity.App.SignalIntegrityAppHeadless import SignalIntegrityAppHeadless
        import SignalIntegrity.App.Project
        pysi=SignalIntegrityAppHeadless()
        self.UseSinX=SignalIntegrity.App.Preferences['Calculation.UseSinX']
        SignalIntegrity.App.Preferences['Calculation.UseSinX']=False
        SignalIntegrity.App.Preferences.SaveToFile()
        pysi=SignalIntegrityAppHeadless()
        SignalIntegrity.App.Preferences['Calculation'].ApplyPreferences()
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        os.chdir(self.cwd)
        from SignalIntegrity.App.SignalIntegrityAppHeadless import SignalIntegrityAppHeadless
        import SignalIntegrity.App.Project
        pysi=SignalIntegrityAppHeadless()
        SignalIntegrity.App.Preferences['Calculation.UseSinX']=self.UseSinX
        SignalIntegrity.App.Preferences.SaveToFile()
        pysi=SignalIntegrityAppHeadless()
        SignalIntegrity.App.Preferences['Calculation'].ApplyPreferences()
    def __init__(self, methodName='runTest'):
        si.test.SParameterCompareHelper.__init__(self)
        unittest.TestCase.__init__(self,methodName)
        si.test.SignalIntegrityAppTestHelper.__init__(self,os.path.dirname(os.path.realpath(__file__)))
    def RelayTest(self,route):
        app=siapp.SignalIntegrityAppHeadless()
        app.OpenProjectFile('RelayTest.si',{'Route':route})
        filename='RelayTest'+str(route)+'.si'
        app.SaveProjectToFile(filename)
        return filename
    def testRelayTest1(self):
        self.SParameterResultsChecker(self.RelayTest(1))
    def testRelayTest2(self):
        self.SParameterResultsChecker(self.RelayTest(2))
    def testRelayTest3(self):
        self.SParameterResultsChecker(self.RelayTest(3))
    def RelayTestSimulation(self,route,source):
        app=siapp.SignalIntegrityAppHeadless()
        app.OpenProjectFile('RelayTestSimulation.si',{'Route':route,'Source':source})
        filename='RelayTestSimulation'+str(route)+str(source)+'.si'
        app.SaveProjectToFile(filename)
        return filename
    def testRelayTestSimulation11(self):
        self.SimulationResultsChecker(self.RelayTestSimulation(1,1))
    def testRelayTestSimulation21(self):
        self.SimulationResultsChecker(self.RelayTestSimulation(2,1))
    def testRelayTestSimulation31(self):
        self.SimulationResultsChecker(self.RelayTestSimulation(3,1))
    def testRelayTestSimulation12(self):
        self.SimulationResultsChecker(self.RelayTestSimulation(1,2))
    def testRelayTestSimulation22(self):
        self.SimulationResultsChecker(self.RelayTestSimulation(2,2))
    def testRelayTestSimulation32(self):
        self.SimulationResultsChecker(self.RelayTestSimulation(3,2))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()