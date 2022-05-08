\ Model nealClique
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
- C0 - C1 - C2 - C3 - C4 - C5
Subject To
 R0: C0 + C2 - V0 <= 1
 R1: C0 + C3 - V1 <= 1
 R2: C0 + C4 - V2 <= 1
 R3: C1 + C4 - V3 <= 1
 R4: C2 + C4 - V4 <= 1
 R5: C1 + C5 - V5 <= 1
 R6: C2 + C5 - V6 <= 1
 R7: C3 + C5 - V7 <= 1
 R8: V0 + V1 + V2 + V3 + V4 + V5 + V6 + V7 = 2
Bounds
Binaries
 C0 C1 C2 C3 C4 C5 V0 V1 V2 V3 V4 V5 V6 V7
End
