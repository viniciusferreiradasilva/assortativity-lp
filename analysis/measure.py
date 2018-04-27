#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np

def summary(graph, complete = False, subgraph = False):
    summary = [
        ("level", graph['level']),
        ("vertex number", graph.vcount()),
        ("edge number", graph.ecount()),
        ("global transitivity", graph.transitivity_undirected()),
        ("vertices mean degree", np.mean(graph.degree())),
        ("assortativity", graph.assortativity_degree(directed=False)),
        ("heterogeneity", heterogeneity(graph)),
        ("density", density(graph))
    ]

    print "graph summary:"
    for tuple in summary:
        print tuple
    print "-" * 75



def heterogeneity(graph):
    mean_degree_quad = 0.
    for v in range(graph.vcount()):
        mean_degree_quad += np.power(graph.degree(v), 2)
    mean_degree_quad = mean_degree_quad / graph.vcount()
    return mean_degree_quad / np.power(np.mean(graph.degree()), 2)

def density(graph):
    return graph.ecount()/((graph.vcount() * (graph.vcount()-1))/2)
