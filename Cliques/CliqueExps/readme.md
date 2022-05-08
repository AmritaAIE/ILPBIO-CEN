# Formulations for Clique Problems in ILP

This folder contains files required to run the formulations for Clique problems in ILP.There are 3 main Clique Problem Adressed.

1. Maximal Clique
2. Near Clique
3. Inverse Near Clique

Details of these are explained in the formulations.ipynb

This Folder Contains:

1. 100_05.xlsx,300_25.xlsx,500_25.xlsx : Data Files for testing maximal clique formulation. 100_05 is a Random Graph of 100 nodes and probablity of edge being 0.5. Similarly 300_25,500_25 shall extend
2. Formulations.ipynb: Conatains all the formulations in a Sequential Order. 
3. Gurobi-Python3-Howto.pdf: Short Installation Guide on how to install gurobi for python.
4. Spoke_Tap_format.txt: MIPS yeast dataset, on which prediction algorithm is applied. 
5. yeastAdjMatrix: 209x209 Yeast Adjacency Matrix

Misc: All other Files(If Any) are Output Files. 

### Dependencies

Before Installing the dependency, Gurobi should be installed with academic liscence or otherwise.Process of Installing Gurobi and adding license is described in `Gurobi-Python3-How-to.pdf` (source: http://matthiaswalter.org/intpm/Gurobi-Python3-Howto.pdf).

Once Gurobi is up and running, 
dependencies can be installed by

`pip install -r requirements.txt`

### Running the Experiments.

The package is supposed to run 4 Experiments
1.Yeast Adjacency Matrix : 209 Nodes
2. Maximal Cliqus on Random Graphs
3. Maximal Cliques on Complete Yeast Dataset
4. Exp 4: Predicting Edges

All the experiments can be run by running the `experiments.py`. From the terminal, run `python experiments.py`. 

The Following output files are expected to be generated
1. MIPS_nodeList.csv
2. MIPS_Maximal_Cliques.csv
3. MIPS_Pred.txt
4. meta.txt
However, if there is trouble writing MIPS_Pred.txt, Additional 3 files will be generated. 