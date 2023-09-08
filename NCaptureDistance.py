import ROOT as rt
import numpy as np
import math
import os

def NCapDistance_Calculate(InputName):
    NewFile = rt.TFile("/junofs/users/junopublic3/output/NearestNCapDist_to_{}.root".format(InputName), "RECREATE")
    hist = rt.TH1F("hist", "NearestNCapDist_to_{}".format(InputName), 300, 0, 3000)

    for EvtNum in range(0, 5001):
        if (os.path.isfile('/junofs/users/wangyg/Simulation/TeLS/data/QGSP_BERT_HP/output/evt-muon-{0}.root'.format(EvtNum))):
            ReadFile = rt.TFile("/junofs/users/wangyg/Simulation/TeLS/data/QGSP_BERT_HP/output/evt-muon-" + str(EvtNum) + ".root", "READ")
            Process_num = ReadFile.process.GetEntries()
            Evt_count = 0
            NotEvt_count = 0

            for Process_entry_num in range(Process_num):
                
                ReadFile.process.GetEntry(Process_entry_num)
                EventID = ReadFile.process.EventID
                ProName = ReadFile.process.ProductName
                NCapDistance = []
                
                if InputName in ProName:
                    IsoPosX = ReadFile.process.ProductGenPosX[0]
                    IsoPosY = ReadFile.process.ProductGenPosY[0]
                    IsoPosZ = ReadFile.process.ProductGenPosZ[0]
                    
                    for Num in range(Process_num):
                        ReadFile.process.GetEntry(Num)
                        if ReadFile.process.EventID == EventID:
                            if ReadFile.process.ProcessName == "nCapture":
                                NCapPosX = ReadFile.process.ProductGenPosX[0]
                                NCapPosY = ReadFile.process.ProductGenPosY[0]
                                NCapPosZ = ReadFile.process.ProductGenPosZ[0]

                                DistX = NCapPosX - IsoPosX
                                DistY = NCapPosY - IsoPosY
                                DistZ = NCapPosZ - IsoPosZ

                                Distance = math.sqrt(DistX**2 + DistY**2 + DistZ**2)
                                # print(Distance)
                                NCapDistance.append(Distance)
                    if len(NCapDistance) != 0:
                        Evt_count = Evt_count + 1
                        Distance_min = np.min(NCapDistance)
                        # print(Distance_min)
                        hist.Fill(Distance_min)
                    if len(NCapDistance) == 0:
                        NotEvt_count = NotEvt_count + 1
                        
    NewFile.cd()
    hist.Write()
    NewFile.Close()
    print(InputName, "Evt_count:", Evt_count, "; NotEvt_count: ", NotEvt_count)

NCapDistance_Calculate("C10")
NCapDistance_Calculate("B12")
NCapDistance_Calculate("He6")
NCapDistance_Calculate("Li8")
