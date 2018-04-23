#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scipy.sparse

class LinkPredictor():

    def __init__(self):
        self.predictors_array = [self.link_prediction_by_similarity, self.link_prediction_by_similarity_to_file, self.link_prediction_by_similarity_non_zero]

    # Method that predict links in without consider self edges.
    def link_prediction_by_similarity(self, graph, similarity):
        predicted_edges = {}
        adjlist = map(set, graph.get_adjlist())
        for v in range(graph.vcount()):
            for u in range((v + 1), graph.vcount()):
                # A 0 value in a adjacency matrix position means that not exist a edge.
                # Also, this function doesn't considerate self links.
                if(graph[v, u] == 0):
                    predicted_value = similarity(graph, adjlist, i = v, j = u)
                    predicted_edges[(v, u)] = predicted_value
        return predicted_edges


    # Method that predict links in without consider self edges. The output is saved in a outputfile to do not overload the memory.
    def link_prediction_by_similarity_to_file(self, graph, similarity, io_handler):
        adjlist = map(set, graph.get_adjlist())
        for v in range(graph.vcount()):
            for u in range((v + 1), graph.vcount()):
                # A 0 value in a adjacency matrix position means that not exist a edge.
                # Also, this function doesn't considerate self links.
                if (graph[v, u] == 0):
                    io_handler.write_predicted_edge((v, u), str(similarity(graph, adjlist, v, u)))


    # Method that predict links without consider self edges. This method does not save edges with a zero value.
    def link_prediction_by_similarity_non_zero(self, graph, similarity, threshold = 0.00005):
        predicted_edges = {}
        adjlist = map(set, graph.get_adjlist())
        for v in range(graph.vcount()):
            for u in range((v + 1), graph.vcount()):
                # A 0 value in a adjacency matrix position means that not exist a edge.
                # Also, this function doesn't considerate self links.
                if (graph[v, u] == 0):
                    # print "Predicted:", (v,u)
                    sim = similarity(graph, adjlist, i=v, j=u)
                    if (sim > threshold):
                        predicted_edges[(v, u)] = sim
                        print "Size: ", len(predicted_edges), "Sim:", sim
        return predicted_edges
