#!/bin/env python

loopnames =[
"L1D1PN",
"L1D2MN",
"L2D1MN",
"L2D2PN",
"L3D1MN",
"L3D2PN",
"L3D3MN",
"L3D4PN",
"L4D1PN",
"L4D2MN",
"L4D3PN",
"L4D4MN",
"L1D1MF",
"L1D2PF",
"L2D1PF",
"L2D2MF",
"L3D1PF",
"L3D2MF",
"L3D3PF",
"L3D4MF",
"L4D1MF",
"L4D2PF",
"L4D3MF",
"L4D4PF"]

hcs = ["Bp","Bm"]

outputFile = "HVTempMap.txt"
fout = open(outputFile,"w")

for loopname in loopnames:

    for ihc in hcs:
        alias = "PixelBarrel_"

        if ("N" in loopname):
            alias = alias + ihc + "I_"

        if ("F" in loopname):
            alias = alias + ihc + "O_"

        if ("L1D1" in loopname):
            fout.write(alias + "S1_LAY1" + ":" + loopname + "\n")
            fout.write(alias + "S2_LAY1" + ":" + loopname + "\n")
            fout.write(alias + "S3_LAY1" + ":" + loopname + "\n")
            fout.write(alias + "S4_LAY1" + ":" + loopname + "\n")

        if ("L1D2" in loopname):
            fout.write(alias + "S5_LAY1" + ":" + loopname + "\n")
            fout.write(alias + "S6_LAY1" + ":" + loopname + "\n")
            fout.write(alias + "S7_LAY1" + ":" + loopname + "\n")
            fout.write(alias + "S8_LAY1" + ":" + loopname + "\n")

        if ("L2D1" in loopname):
            fout.write(alias + "S1_LAY2" + ":" + loopname + "\n")
            fout.write(alias + "S2_LAY2" + ":" + loopname + "\n")
            fout.write(alias + "S3_LAY2" + ":" + loopname + "\n")
            fout.write(alias + "S4_LAY2" + ":" + loopname + "\n")

        if ("L2D2" in loopname):
            fout.write(alias + "S5_LAY2" + ":" + loopname + "\n")
            fout.write(alias + "S6_LAY2" + ":" + loopname + "\n")
            fout.write(alias + "S7_LAY2" + ":" + loopname + "\n")
            fout.write(alias + "S8_LAY2" + ":" + loopname + "\n")

        if ("L3D1" in loopname):
            fout.write(alias + "S1_LAY3" + ":" + loopname + "\n")
            fout.write(alias + "S2_LAY3" + ":" + loopname + "\n")

        if ("L3D2" in loopname):
            fout.write(alias + "S3_LAY3" + ":" + loopname + "\n")
            fout.write(alias + "S4_LAY3" + ":" + loopname + "\n")

        if ("L3D3" in loopname):
            fout.write(alias + "S5_LAY3" + ":" + loopname + "\n")
            fout.write(alias + "S6_LAY3" + ":" + loopname + "\n")

        if ("L3D4" in loopname):
            fout.write(alias + "S7_LAY3" + ":" + loopname + "\n")
            fout.write(alias + "S8_LAY3" + ":" + loopname + "\n")

        if ("L4D1" in loopname):
            fout.write(alias + "S1_LAY4" + ":" + loopname + "\n")
            fout.write(alias + "S2_LAY4" + ":" + loopname + "\n")

        if ("L4D2" in loopname):
            fout.write(alias + "S3_LAY4" + ":" + loopname + "\n")
            fout.write(alias + "S4_LAY4" + ":" + loopname + "\n")

        if ("L4D3" in loopname):
            fout.write(alias + "S5_LAY4" + ":" + loopname + "\n")
            fout.write(alias + "S6_LAY4" + ":" + loopname + "\n")

        if ("L4D4" in loopname):
            fout.write(alias + "S7_LAY4" + ":" + loopname + "\n")
            fout.write(alias + "S8_LAY4" + ":" + loopname + "\n")

fout.close()
