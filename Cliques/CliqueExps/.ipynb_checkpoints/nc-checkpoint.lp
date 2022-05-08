\ Model nealClique
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  C[0] + C[1] + C[2] + C[3] + C[4] + C[5]
Subject To
 R0: C[0] + C[2] - V[0] <= 1
 R1: C[0] + C[3] - V[1] <= 1
 R2: C[0] + C[4] - V[2] <= 1
 R3: C[1] + C[4] - V[3] <= 1
 R4: C[2] + C[4] - V[4] <= 1
 R5: C[1] + C[5] - V[5] <= 1
 R6: C[2] + C[5] - V[6] <= 1
 R7: C[3] + C[5] - V[7] <= 1
 R8: V[0] + V[1] + V[2] + V[3] + V[4] + V[5] + V[6] + V[7] = 2
Bounds
Binaries
 C[0] C[1] C[2] C[3] C[4] C[5] V[0] V[1] V[2] V[3] V[4] V[5] V[6] V[7]
End
