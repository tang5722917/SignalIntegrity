'''
 Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
 Unpublished Copyright (c) 2015-2016 Peter J. Pupalaikis and Teledyne LeCroy,
 All Rights Reserved.

 Explicit license in accompanying README.txt file.  If you don't have that file
 or do not agree to the terms in that file, then you are not licensed to use
 this material whatsoever.
'''
from numpy import linalg

from SignalIntegrity.Conversions import S2T
from SignalIntegrity.Conversions import T2S
from SignalIntegrity.SParameters.SParameters import SParameters

class TLineDifferentialRLGCApproximate(SParameters):
    def __init__(self,f, Rp, Rsep, Lp, Gp, Cp, dfp,
                         Rn, Rsen, Ln, Gn, Cn, dfn,
                         Cm, dfm, Gm, Lm, Z0, K):
        self.m_K=K
        # pragma: silent exclude
        from SignalIntegrity.Devices import SeriesG
        from SignalIntegrity.Devices import SeriesZ
        from SignalIntegrity.Devices import TerminationG
        import SignalIntegrity.SParameters.Devices as dev
        from SignalIntegrity.SystemDescriptions.SystemSParametersNumeric import SystemSParametersNumeric
        from SignalIntegrity.Parsers.SystemDescriptionParser import SystemDescriptionParser
        # pragma: include
        sdp=SystemDescriptionParser().AddLines([
        'device rsep 2','device rp 2','device lp 2','device gp 1','device cp 1',
        'device rsen 2','device rn 2','device ln 2','device gn 1','device cn 1',
        'device lm 4','device gm 2','device cm 2',
         'connect rp 2 rsep 1','connect rsep 2 lp 1',
         'connect rn 2 rsen 1','connect rsen 2 ln 1',
         'connect lp 2 lm 1','connect ln 2 lm 3',
         'connect lm 2 gp 1 cp 1 gm 1 cm 1','connect lm 4 gn 1 cn 1 gm 2 cm 2',
         'port 1 rp 1 2 lm 2 3 rn 1 4 lm 4'])
        self.m_sspn=SystemSParametersNumeric(sdp.SystemDescription())
        self.m_sspn.AssignSParameters('rp',SeriesZ(Rp/K,Z0))
        self.m_sspn.AssignSParameters('gp',TerminationG(Gp/K,Z0))
        self.m_sspn.AssignSParameters('rn',SeriesZ(Rn/K,Z0))
        self.m_sspn.AssignSParameters('gn',TerminationG(Gn/K,Z0))
        self.m_sspn.AssignSParameters('gm',SeriesG(Gm/K,Z0))
        self.m_spdl=[('rsep',dev.SeriesRse(f,Rsep/K,Z0)),
            ('lp',dev.SeriesL(f,Lp/K,Z0)),('cp',dev.TerminationC(f,Cp/K,Z0,dfp)),
            ('rsen',dev.SeriesRse(f,Rsen/K,Z0)),('ln',dev.SeriesL(f,Ln/K,Z0)),
            ('cn',dev.TerminationC(f,Cn/K,Z0,dfn)),('lm',dev.Mutual(f,Lm/K,Z0)),
            ('cm',dev.SeriesC(f,Cm/K,Z0,dfm))]
        SParameters.__init__(self,f,None,Z0)
    def __getitem__(self,n):
        for ds in self.m_spdl:
            self.m_sspn.AssignSParameters(ds[0],ds[1][n])
        sp=self.m_sspn.SParameters()
        if sp == 1: return sp
        lp=[1,3]; rp=[2,4]
        return T2S(linalg.matrix_power(S2T(sp,lp,rp),self.m_K),lp,rp)
