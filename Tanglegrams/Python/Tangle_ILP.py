import re
import gurobipy as gp
from ete3 import Tree
import time


def Tanglegram_solver(Tree_1,Tree_2):
    start = time.time()

    # make an ete3 object using the given tree
    t1 = Tree(Tree_1)
    print("First tree : \n",t1,"\n")

    # find the nodes and their positions
    temp = re.findall(r'\d+', Tree_1)
    res_1 = list(map(int, temp))
    # print(res_1)
    positions_1 = {r:res_1.index(r) for r in res_1}

    # Performing same operations for tree 2
    t2 = Tree(Tree_2)
    print("Second Tree : \n",t2,"\n")
    temp = re.findall(r'\d+', Tree_2)
    res_2 = list(map(int, temp))
    positions_2 = {r:res_2.index(r) for r in res_2}

    # Number of nodes in the tree and the maximum number of variables needed during formulation (tot)
    n = len(res_1)
    tot = n*(n-1)/2

    # creating a gurobipy model and adding the varibles
    Tangle = gp.Model()
    R1 = Tangle.addMVar(int(tot),vtype = gp.GRB.BINARY,name="R1")
    R2 = Tangle.addMVar(int(tot),vtype = gp.GRB.BINARY,name="R2")
    X1 = Tangle.addMVar(Tree_1.count("("),vtype = gp.GRB.BINARY,name="X1")
    X2 = Tangle.addMVar(Tree_2.count("("),vtype = gp.GRB.BINARY,name="X2")
    C = Tangle.addMVar(int(tot),vtype = gp.GRB.BINARY,name="C")

    # OBJECTIVE FUNCTION ( to be minimized )
    Tangle.setObjective(sum(C),gp.GRB.MINIMIZE)

    # adding the constraints
    Tangle.addConstr(C-R1+R2>=0,name="c1")
    Tangle.addConstr(C-R2+R1>=0,name="c2")

    # dictionaries to store the positions of the Least Common Ancestor of nodes (i,j)
    Xs1 = dict()
    Xs2 = dict()

    # function to get the position of the node configuration in the Array Variables ( R1,R2 )
    def get_num(m,n):
        return int(len(res_1)*(m-1)+n-m*(m+1)/2-1)

    global x1 , x2
    x1 , x2 = 0 , 0
    tangles = 0
    # function to find the least common ancestor of i,j and return the position of it in X1,X2
    def get_xpos(i,j):
        global x1,x2
        if (t1.get_common_ancestor(str(i),str(j)) not in Xs1.keys()):
            Xs1[t1.get_common_ancestor(str(i),str(j))] = x1
            xpos = x1
            x1 = x1+1
        else:
            xpos = Xs1[t1.get_common_ancestor(str(i),str(j))]

        if (t2.get_common_ancestor(str(i),str(j)) not in Xs2.keys()):
            Xs2[t2.get_common_ancestor(str(i),str(j))] = x2
            xpos2 = x2
            x2 = x2+1
        else:
            xpos2 = Xs2[t2.get_common_ancestor(str(i),str(j))]

        return xpos,xpos2


    for i in range(1,len(res_1)+1):                                 # traversing the trees and determining the constraints
        for j in range(i+1,len(res_1)+1):
            xpos , xpos2 = get_xpos(i,j)
            num = get_num(i,j)

            # if they are in order
            if positions_1[i]<positions_1[j]:
                Tangle.addConstr(R1[num]+X1[xpos] == 1)
                # print(f"R1({num+1   })+X1({xpos+1}) == 1")
                c1 = 1
            # if they are out of order
            else:
                Tangle.addConstr(R1[num]-X1[xpos] == 0)
                # print(f"R1({num+1})-X1({xpos+1}) == 0")
                c1 =0

            # similar operations for nodes of tree 2
            if positions_2[i]<positions_2[j]:
                Tangle.addConstr(R2[num] + X2[xpos2] == 1)
                # print(f"R2({num+1})+X2({xpos2+1}) == 1")
                c2 = 1
            else:
                Tangle.addConstr(R2[num] - X2[xpos2] == 0)
                # print(f"R2({num+1})-X2({xpos2+1}) == 0")
                c2 = 0

            if c1!=c2:
                tangles = tangles + 1

    after_add = time.time()
    print("\n \n Constarints are completely added at : ",after_add,"\n \n")

    # optimise
    Tangle.optimize()
    T = time.time()
    print("The time taken to solve the problem using gurobi optimiser is : ",round(T-after_add,8),"\n \n")
    swapped1 = list()
    swapped2 = list()

    for i in range(1,len(res_1)+1):
        for j in range(i+1,len(res_2)+1):
            xpos , xpos2 = get_xpos(i,j)
            if Tangle.getVarByName(f"X1[{xpos}]").x == 1 and t1.get_common_ancestor(str(i),str(j)) not in swapped1:
                t1.get_common_ancestor(str(i),str(j)).swap_children()
                swapped1.append(t1.get_common_ancestor(str(i),str(j)))


            if Tangle.getVarByName(f"X2[{xpos2}]").x == 1 and t2.get_common_ancestor(str(i),str(j)) not in swapped2:
                t2.get_common_ancestor(str(i),str(j)).swap_children()
                swapped2.append(t2.get_common_ancestor(str(i),str(j)))


    print("The Exchanged Trees are : \n \n","Tree 1")
    print(t1)
    print("\n \n Tree 2 \n")
    print(t2,"\n \n")
    print("The number of Tangles are : ",C.sum().getValue() , f"Reduced from {tangles} number of tangles")

    choice = input("would you like to print the results ? (Y - yes ) : ")
    if choice == 'Y':
        # printing the solution
        for v in Tangle.getVars():
            print('%s=%g' % (v.varName, v.x))


Tanglegram_solver("((4,6),((1,5),(2,3)));","((4,(2,(1,5))),(3,6));")