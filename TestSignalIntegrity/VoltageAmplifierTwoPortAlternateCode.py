import SignalIntegrity as si

sdp=si.p.SystemDescriptionParser()
sdp.AddLines(['device DV 3','device G 1 ground',
    'port 1 DV 1 2 DV 2',
    'connect DV 3 G 1'])
ssps=si.sd.SystemSParametersSymbolic(sdp.SystemDescription(),True,True)
DV=si.sy.VoltageAmplifier(3,'\\alpha','Z_i','Z_o')
ssps.AssignSParameters('DV',DV)
ssps.LaTeXBlockSolutionBiggest().Emit()
