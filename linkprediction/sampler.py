#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

# Class that creates samples, removes samples from the network, re-adds the samples of edges in the network for saving memory.

class Sampler():

    def __init__(self):
        pass

    # Method that removes the edges in the probe list from the graph. The edge list must be a dictionary which the key is a edge
    # and the value is the weight.
    def delete_edges(self, graph, edges_probe_list):
        graph.delete_edges(edges_probe_list.keys())

    # Method that re-adds the edges in the probe list to the graph. The edge list must be a dictionary which the key is a edge
    # and the value is the weight.
    def readd_edges(self, graph, edges_probe_list):
        for edge in edges_probe_list:
            graph[edge[0], edge[1]] = edges_probe_list[edge]

    # Method that creates the edge probe list from graph according to the proportion.
    def create_random_edges_probe_list(self, graph, proportion):
        edges_probe_list = {}
        # Creates a sample according to the proportion size.
        sample = random.sample(graph.get_edgelist(), int(len(graph.get_edgelist()) * proportion))
        # The edges are added to the probe list with their weights.
        for edge in sample:
            weight = graph[edge[0], edge[1]]
            edges_probe_list[edge] = weight
        return edges_probe_list

    # Method that creates the edge probe list from graph according to the proportion. The edgelist is a parameter
    # because it can be shuffled before the function call, generating a random sorted list of edges.
    def create_k_edges_probe_list(self, graph, edgelist, i, k):
        edges_probe_list = {}
        from_i = i * (graph.ecount() / k)
        to_i = from_i + ((graph.ecount() / k))
        # The i partition of the edge is recovered.
        sample = edgelist[from_i: to_i]
        # The edges are added to the probe list with their weights.
        for edge in sample:
            weight = graph[edge[0], edge[1]]
            edges_probe_list[edge] = weight
        return edges_probe_list