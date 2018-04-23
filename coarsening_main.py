#!//env python
# -*- coding: utf-8 -*-
import argparse

from loader.iohandler import IOHandler
from similarity.similarity import Similarity
from linkprediction.link_predictor import LinkPredictor
from linkprediction.metric_calculator import MetricCalculator
from linkprediction.sampler import Sampler
from loader.graph_loader import GraphLoader
import random
import os

def print_graph(graph):
    print "Vertices:", range(graph.vcount())
    print "Edges:", graph.get_edgelist()

def print_predicted(predicted_edges):
    for predicted_edge in predicted_edges:
        print predicted_edge,":",predicted_edges[predicted_edge]

def print_graph_status(graph):
    print "Vertices:", graph.vcount(), "Edges:", graph.ecount()

# Parse options command line
parser = argparse.ArgumentParser(description="Link prediction")
# Define the arguments that the user will pass to the software.
parser.add_argument('-f', '--filename', action='store', dest='filename', help='A file name that contains a .ncol network.', type = str)
parser.add_argument('-k', '--k', action='store', dest='k', help='Number of folds to cross validation.', type = int, default = 10)
parser.add_argument('-s', '--similarity', action='store', dest='similarity_method', help='Similarity measure used for link prediction. [0 - CN, 1 - JAC, 2 - SAL, 3 - AA, 4 - PA, 5 - KATZ].', type = int, default = 0)

# Parses the arguments.
args = parser.parse_args()

if args.filename is None:
	parser.error("required -f [filename] arg.")
graph_loader = GraphLoader()
if("ncol" in args.filename):
    graph = graph_loader.load_unipartite_undirected_ncol(args.filename)
elif("gml" in args.filename):
    graph = graph_loader.load_unipartite_undirected_gml(args.filename)
else:
    graph = graph_loader.load_unipartite_pajek(args.filename)


link_predictor = LinkPredictor()
similarity = Similarity()
metric_calculator = MetricCalculator()
sampler = Sampler()

# Number of folds of the set.
k = args.k
# Similarity method.
s = args.similarity_method
# Solves the dataset name.
dataset_name = (args.filename.split("/")[len(args.filename.split("/")) - 1]).split(".")[0]
print "Executing for dataset =",dataset_name,"k =",k,"s =",s,

# Gets the edgelist and shuffles this list.
edgelist = random.sample(graph.get_edgelist(), graph.ecount())
auc_io_handler = IOHandler()
pr_io_handler = IOHandler()

# Size of Ls that will be analised.
ls = [10]

dir = "output/" + dataset_name + "/" + similarity.similarities_array[s].__name__ + "/"
if(not os.path.exists(dir)):
    os.makedirs(dir)

# Loading output files.
auc_io_handler.load_output_file(dir + "auc.csv")
pr_io_handler.load_output_file(dir + "pr.csv")
# Writes the reader in each file.
auc_io_handler.write_results(",".join(map(str, ls)))
pr_io_handler.write_results(",".join(map(str, ls)))

for i in range(k):
    print "Calculating for (",(i+1),"/",k,") folds..."
    # Creates the probe edges by k-fold.
    probe_edges = sampler.create_k_edges_probe_list(graph, edgelist, i, k)

    # Delete the edges from the graph.
    sampler.delete_edges(graph, probe_edges)

    predicted_edges = link_predictor.link_prediction_by_similarity(graph, similarity.similarities_array[s])

    aucs = [None] * len(ls)
    prs = [None] * len(ls)
    # L values to calculate auc and precision.
    for j in range(len(ls)):
        # Calculates auc with 10% of the edges.
        aucs[j] = metric_calculator.calculate_auc(predicted_edges, probe_edges, int(len(predicted_edges) * 0.1))
        # Calculates p@L with 10% of the edges.
        prs[j] = metric_calculator.calculate_precision(predicted_edges, probe_edges, int(len(predicted_edges) * 0.1))
    # Writes the auc results.
    auc_io_handler.write_results(",".join(map(str, aucs)))
    # Writes the precision results.
    pr_io_handler.write_results(",".join(map(str, prs)))

    # Re-adds the edges to the network.
    sampler.readd_edges(graph, probe_edges)

auc_io_handler.close_files()
pr_io_handler.close_files()
