#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Method that predict links in without consider self edges.
def link_prediction_by_similarity(self, graph, similarity):
    predicted_edges = {}
    adjlist = map(set, graph.get_adjlist())
    for v in range(graph.vcount()):
        for u in range((v + 1), graph.vcount()):
            # A 0 value in a adjacency matrix position means that not exist a edge.
            # Also, this function doesn't considerate self links.
            if graph[v, u] == 0:
                predicted_value = similarity(graph, adjlist, i=v, j=u)
                predicted_edges[(v, u)] = predicted_value
    return predicted_edges
