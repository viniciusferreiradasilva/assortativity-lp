# assortativity-lp
assortativity-lp is a fast python implementation of topological similarity-based algorithms for link prediction. I used igraph python module because it is really fast to extract basic characteristics of the networks like degree, adjacency matrices and a sort of coefficients. If you need to add/remove vertices and edges frequently, igraph may not be the right network python module for you. The usage of the module is:

# python main.py -f <FILE> -k <K> -s <SIMILARITY>

The FILE argument refers to the network file. This module allows you to load graphs in three different formats: ncol, gml, and pajek. You can implement your own methods to load graphs in the loader/graph_loader.py. I remove all the self-edges because regular link prediction literature does not consider this kind of edge.

The K argument refers to the number of folds that will be used to extract performance measures from the link prediction results. The main.py file contains a code to extract a complete link prediction ranking from the network and also extracts AUC/Precision values. K is an argument that sets the number of folds to calculate AUC/Precision via k-fold-cross-validation or k-random-folds. 

SIMILARITY stands for the similarity algorithm that will be used to extract the prediction. The file similarity/similarity.py contains several local and global similarities algorithms. You can implement your own in this file but do not forget to add the method to the similarities array. 

The datasets folder contains a lot of networks datasets that can be used as benchmark. The link prediction results for those datasets are in the output folder. An example of use:

# python main.py -f "datasets/ncol/netscience/netscience.ncol" -k 10 -s 0

This example will produce AUC and Precision files in the output folder for the results of the netscience dataset with a 10-fold-cross-validation, using Common Neighbors as the link prediction algorithm.
