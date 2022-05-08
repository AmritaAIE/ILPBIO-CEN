import numpy as np
import gurobipy as gp
import time
import pandas as pd
import json

from formulations import findMaximalClique, findAllMaximalCliques, findNearClique, findAllNearCliques, invNearClique, findAllInvNearCliques

meta = {}

#########################################################################
# Exp 1: Yeast Adjacency Matrix : 209 Nodes (Warming Up)
########################################################################
print("Yeast Adjacency Matrix (209 Nodes)......")
print("Reading Matrix......")
with open("./yeastAdjMatrix") as f:
    mat = []
    for line in f:
        lne = []
        for char in line:
            if char != '\n':
                lne.append(int(char))
        mat.append(lne)
mat = np.array(mat)
print("Finding All Maximal Cliques....")
start = time.time()
C = findAllMaximalCliques(mat, sharing='allow')
end = time.time()
print(f"Found {C.shape[0]} Cliques in {end-start}s")


res = {"n_cliques": C.shape[0],
       "time": end-start,
       }
meta["Yeast_209"] = res
#############################################################
# Exp 2: Maximal Cliqus on Random Graphs
############################################################
print("Maximal Cliques on Random Graphs...........")
print("Reading data..............")
df1 = pd.read_excel("./100_05.xlsx", header=None)
df2 = pd.read_excel("./300_25.xlsx", header=None)
df3 = pd.read_excel("./500_25.xlsx", header=None)

exp_name = ["Random_100_05", "Random_300_25", "Random_500_25"]
T = []

print(exp_name[0]+"...........................")
model = gp.Model(exp_name[0])
start = time.time()
findMaximalClique(df1.to_numpy(), model=model)
end = time.time()
T.append(end-start)
print(exp_name[1]+"...........................")
model = gp.Model(exp_name[1])
start = time.time()
findMaximalClique(df2.to_numpy(), model=model)
end = time.time()
T.append(end-start)
print(exp_name[2]+"...........................")
model = gp.Model(exp_name[2])
start = time.time()
findMaximalClique(df3.to_numpy(), model=model)
end = time.time()
T.append(end-start)


for exp_n, t in zip(exp_name, T):
    res = {"time": t}
    meta[exp_n] = res

##########################################################
# Exp 3: Maximal Cliques on Complete Yeast Dataset
##########################################################
print("Maximal Cliques on Complete Dataset ......................")
print("Reading Data............")
nodes = []
with open("./Spoke_TAP_format.txt") as f:
    for line in f:
        edge = line.strip().split("\t")
        if edge[0] not in nodes:
            nodes.append(edge[0])
        if edge[1] not in nodes:
            nodes.append(edge[1])

N = len(nodes)
Adj = np.zeros((N, N))

with open("./Spoke_TAP_format.txt") as f:
    for line in f:
        edge = line.strip().split("\t")

        n1_idx = nodes.index(edge[0])
        n2_idx = nodes.index(edge[1])

        Adj[n1_idx, n2_idx] = 1
        Adj[n2_idx, n1_idx] = 1

print(f"Graph with {Adj.shape[0]} Nodes and {int(Adj.sum()/2)} Edges")


nodes = np.array(nodes)
np.savetxt("MIPS_nodeList.csv", nodes, delimiter=",", fmt='%s')
print("Node List saved in MIPS_nodeList.csv")

print("Finding Maximal Cliques............")
start = time.time()
C = findAllMaximalCliques(Adj, sharing='allow')
end = time.time()
t = end-start
print(f"Total of {C.shape[0]} Maximal Cliques Found in {t}s.")

C = np.array(C)

np.savetxt("MIPS_Maximal_Cliques.csv", C, delimiter=",")
print("All Maximal cliques saved to MIPS_Maximal_Cliques.csv")

res = {"n_cliques": C.shape[0],
       "time": t}

meta["MIPS_Maximal_Cliques"] = res

##############################################
# Exp 4: Predicting Edges
##############################################
print("Predicting Edges...........")
Ks = np.unique(C.sum(axis=1))
extra_nodes = np.arange(1, 8)


results = {}
nk = len(Ks)
for ix, k in enumerate(Ks):
    for d in extra_nodes:
        print(f"Completing clique for k={k} and d={d}......")
        start = time.time()
        clqs, Vs, idx = findAllInvNearCliques(Adj, k, d, sharing='allow')
        end = time.time()
        res = {"Cliques": clqs.tolist(),
               "Vs": Vs.tolist(),
               "idx": idx.tolist(),
               "time": end-start}
        results[k, d] = res
        print(f"Found {clqs.shape[0]}  cliques in {end-start}s")
    print(f"K: {ix}/nk")

try:
    with open('MIPS_Pred.txt', 'w') as f:
        f.write(json.dumps(results))
except:
    np.savetxt("clqs.csv", clqs, delimiter=",")
    np.savetxt("Vs", Vs, delimiter=",")
    np.savetxt("idx", idx, delimiter=",")


with open('meta.txt', 'w') as f:
    f.write(json.dumps(meta))
