import numpy as np
import gurobipy as gp
from gurobipy import GRB


def findMaximalClique(Adj, model, xp=None, sharing=None):
    """
    Finds Maximal Clique for given Adjacency Matrixl 

    Params:
    Adj: Adjacency matrix

    model: GurobiPi Model instance

    xp : binary numpy array, denoting previous clique.

    sharing: `'none'` to not include any nodes that are included from xp. `'allow'` to allow sharing of nodes from previous c
    clique xp

    Returns:
    C: tupleDict containing indices and corresponding values. if C[i] is 1, then 
    node `i` is included in clique K.
    """

    n_nodes = Adj.shape[0]

    idxs = np.argwhere(
        (np.tril(Adj, -1)+np.triu(np.ones((n_nodes, 1))*np.ones((1, n_nodes)))) == 0)

    C = model.addMVar(n_nodes, vtype=GRB.BINARY, name="C")
    constraints = model.addConstrs((C[i] + C[j] <= 1) for i, j in idxs)
    if xp is not None:
        if sharing == 'none':
            print('here')
            xp_idxs = np.argwhere(np.array(xp) == 1)
            constraints2 = model.addConstr(C[xp_idxs].sum() == 0)

        elif sharing == 'allow':
            xp_idxs = np.argwhere(np.array(xp) == 0)
            constraints2 = model.addConstr(C[xp_idxs].sum() >= 1)

        else:
            raise ValueError(
                "Please Specify a valid value for `sharing` parameter. See function signature for more information")

    model.setObjective(gp.quicksum(C), GRB.MAXIMIZE)
    model.optimize()

    return C


def findAllMaximalCliques(Adj, sharing='none'):
    """
    Finds all maximal cliques given From a graph given by Adj.

    Params:

    Adj: Adjacency matrix of the graph

    sharing: `'none'` to not include any nodes that are included from xp. `'allow'` to allow sharing of nodes from previous c
    clique xp

    Returns:

    Cliques: MxN array, where M is hte number of cliques found, and N is the number of Nodes. 

    """
    N = Adj.shape[0]
    a = np.array([1])
    xp = np.zeros(N)
    cliques = []

    while True:
        print("Finding Another Maximal Clique....")
        # Build Gurobi Model
        model = gp.Model('maximalClique')
        a = findMaximalClique(Adj, model, xp, sharing='allow')

        xp = xp+a.x
        print(".....................................")

        if a.x.sum() <= 2:
            break
        cliques.append(a.x)
        print(f"Clique of size {a.x.sum()} found")
        print(".....................................")

    return np.array(cliques)


def findNearClique(Adj, model, N, xp=None, sharing=None):
    """
    Finds Near Clique for given adjacency matrix.

    Params:
    --------------
    Adj: numpy arrya of adjaceny matrix

    model: Gurobipy model

    N: Maximum number of edges that should be added

     xp : binary numpy array, denoting previous clique.

    sharing: `'none'` to not include any nodes that are included from xp. 
    `'allow'` to allow sharing of nodes from previous clique xp

    Returns:
    C: Binary Vairable denoting the clique K

    V: Binary Variables coresponding to formation of edges

    idx: Kx2 where K is the number of constraints. Gives edges corresponding to each of the binary variable in V
    -------------
    """

    n_nodes = Adj.shape[0]

    idxs = np.argwhere(
        (np.tril(Adj, -1)+np.triu(np.ones((n_nodes, 1))*np.ones((1, n_nodes)))) == 0)
    n_constraints = idxs.shape[0]

    C = model.addMVar(n_nodes, vtype=GRB.BINARY, name="C")
    V = model.addMVar(n_constraints, vtype=GRB.BINARY, name="V")

    constraints1 = model.addConstrs(
        (C[i] + C[j] - V[idx] <= 1) for idx, (i, j) in enumerate(idxs))
    constraints2 = model.addConstr(V.sum() == N)

    if xp is not None:
        if sharing == 'none':

            xp_idxs = np.argwhere(np.array(xp) == 1)
            constraints3 = model.addConstr(C[xp_idxs].sum() == 0)

        elif sharing == 'allow':
            xp_idxs = np.argwhere(np.array(xp) == 0)
            constraints3 = model.addConstr(C[xp_idxs].sum() >= 1)

        else:
            raise ValueError(
                "Please Specify a valid value for `sharing` parameter. See function signature for more information")

    model.setObjective(gp.quicksum(C), GRB.MAXIMIZE)
    model.optimize()
    return C, V, idxs


def findAllNearCliques(Adj, n, sharing='none'):
    """
    Completes all near cliques from a graph given by Adj. 

    Params:
    Adj: Adjacency Matrix of the graph

    n: Number of edges that can be added

    sharing: `'none'` denotes none of the nodes from the previous cliques can be shared, `'allow'` denotes allow  sharing 
    between nodes of the previous cliques.

    Returns:

    Cliques: NDArray of Cliques. It is MxN matrix, where M is the number of lciques found and N is the number of nodes in
    the graph.

    Vs: ND array of MxE,  where E is the cardinality of the set `Not(E)`. M is the number of cliques found.

    idx: NDArray of size Ex2, where E is the cardinaluity of the set `not(E)`. 

    idx[Vs[i,:]==1] Gives the edges that are added in ith Clique. 

    """
    N = Adj.shape[0]
    a = np.array([1])
    xp = np.zeros(N)
    cliques = []
    Vs = []
    idxs = []

    while True:
        print("Completing Another Near Clique....")
        # Build Gurobi Model
        model = gp.Model('nearClique')
        a, V, idx = findNearClique(Adj, model, n, xp, sharing=sharing)

        xp = xp+a.x
        print(".....................................")

        if a.x.sum() <= 2 or sum(xp) > N:
            break
        cliques.append(a.x)
        Vs.append(V.x)
        # idxs.append(idx)
        print(f"Clique of size {a.x.sum()} found")
        print(".....................................")

    return np.array(cliques), np.array(Vs), np.array(idx)


def invNearClique(Adj, model, k, d, xp=None, sharing=None):
    """
    Given a graph G(E,V) and it has a maximal clique of size
    k, Inverse clique problem is to find the minimum number of
    edges to be added to G, so that the maximal clique is of size
    atleast k+d , for some positive integer d

    Params:
    --------------
    Adj: numpy arrya of adjaceny matrix

    model: Gurobipy model

    N: Maximum number of edges that should be added

     xp : binary numpy array, denoting previous clique.

    sharing: `'none'` to not include any nodes that are included from xp. `'allow'` to allow sharing of nodes from previous c
    clique xp

    Returns:
    C: Binary Vairable denoting the clique K

    V: Binary Variables coresponding to formation of edges

    idx: Kx2 where K is the number of constraints. Gives edges corresponding to each of the binary variable in V
    -------------
    """

    n_nodes = Adj.shape[0]

    idxs = np.argwhere(
        (np.tril(Adj, -1)+np.triu(np.ones((n_nodes, 1))*np.ones((1, n_nodes)))) == 0)
    n_constraints = idxs.shape[0]

    C = model.addMVar(n_nodes, vtype=GRB.BINARY, name="C")
    V = model.addMVar(n_constraints, vtype=GRB.BINARY, name="V")
    W = model.addMVar(1, vtype=GRB.INTEGER, name="W")
    print("setting up constraints...")
    constraints1 = model.addConstrs(
        (C[i] + C[j] - V[idx] <= 1) for idx, (i, j) in enumerate(idxs))
    constraints2 = model.addConstr(C.sum() >= k+d)
   # print(W.shape)
    constraints3 = model.addConstr(V.sum() <= W.sum())

    if xp is not None:
        if sharing == 'none':

            xp_idxs = np.argwhere(np.array(xp) == 1)
            constraints4 = model.addConstr(C[xp_idxs].sum() == 0)

        elif sharing == 'allow':
            xp_idxs = np.argwhere(np.array(xp) == 0)
            constraints4 = model.addConstr(C[xp_idxs].sum() >= 1)

        else:
            raise ValueError(
                "Please Specify a valid value for `sharing` parameter. See function signature for more information")

    model.setObjective(W.sum(), GRB.MINIMIZE)
    print("optimizing....")
    model.optimize()
    return C, V, idxs


def findAllInvNearCliques(Adj, k, d, sharing='none'):
    """
    Completes all near cliques from a graph given by Adj. 

    Params:
    Adj: Adjacency Matrix of the graph

    k:

    d:

    sharing: `'none'` denotes none of the nodes from the previous cliques can be shared, `'allow'` denotes allow  sharing 
    between nodes of the previous cliques.

    Returns:

    Cliques: NDArray of Cliques. It is MxN matrix, where M is the number of lciques found and N is the number of nodes in
    the graph.

    Vs: ND array of MxE,  where E is the cardinality of the set `Not(E)`. M is the number of cliques found.

    idx: NDArray of size Ex2, where E is the cardinaluity of the set `not(E)`. 

    idx[Vs[i,:]==1] Gives the edges that are added in ith Clique. 

    """
    N = Adj.shape[0]
    a = np.array([1])
    xp = np.zeros(N)
    cliques = []
    Vs = []
    idxs = []

    while True:
        print("Completing Another Near Clique....")
        # Build Gurobi Model
        model = gp.Model('invnearClique')
        a, V, idx = invNearClique(Adj, model, k, d, xp, sharing=sharing)

        xp = xp+a.x
        print(".....................................")

        if a.x.sum() <= 2 or sum(xp) > N:
            break
        cliques.append(a.x)
        Vs.append(V.x)
        # idxs.append(idx)
        print(f"Clique of size {a.x.sum()} found")
        print(".....................................")

    return np.array(cliques), np.array(Vs), np.array(idx)
