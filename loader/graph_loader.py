#!/usr/bin/env python
# -*- coding: utf-8 -*-
from igraph import Graph
from loader.graph_operations import delete_self_edges


# Method that loads a unipartite undirected .ncol network.
def load_unipartite_undirected_ncol(file):
    graph = Graph.Read_Ncol(file, directed=False)
    graph = delete_self_edges(graph)
    return graph


# Method that loads a unipartite undirected .ncol network.
def load_unipartite_undirected_gml(file):
    graph = Graph.Read_GML(file)
    graph = delete_self_edges(graph)
    return graph


# Method that loads a unipartite undirected .ncol network.
def load_unipartite_pajek(file):
    graph = Graph.Read_Pajek(file)
    graph = delete_self_edges(graph)
    return graph

