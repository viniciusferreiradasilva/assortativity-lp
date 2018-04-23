#!/usr/bin/env python
# -*- coding: utf-8 -*-

from igraph import *

class GraphLoader():

    # Method that loads a unipartite undirected .ncol network.
    def load_unipartite_undirected_ncol(self, file):
        graph = Graph.Read_Ncol(file, directed=False)
        graph['successors'] = range(graph.vcount())
        graph['level'] = 0
        graph = self.remove_self_edges(graph)
        return graph

    # Method that loads a unipartite undirected .ncol network.
    def load_unipartite_undirected_gml(self, file):
        graph = Graph.Read_GML(file)
        graph['successors'] = range(graph.vcount())
        graph['level'] = 0
        graph = self.remove_self_edges(graph)
        return graph


    # Method that loads a unipartite undirected .ncol network.
    def load_unipartite_pajek(self, file):
        graph = Graph.Read_Pajek(file)
        graph['successors'] = range(graph.vcount())
        graph['level'] = 0
        graph = self.remove_self_edges(graph)
        return graph


    # Method that loads a unipartite undirected .ncol network.
    def load_unipartite_directed_ncol(self, file):
        graph = Graph.Read_Ncol(file, directed=True)
        graph['successors'] = range(graph.vcount())
        graph['level'] = 0
        graph = self.remove_self_edges(graph)
        return graph

    def remove_self_edges(self, graph):
        graph.delete_edges([edge for edge in graph.es if (edge.source == edge.target)])
        return graph

