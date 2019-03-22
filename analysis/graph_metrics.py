#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np


def vertex_number(graph):
    return graph.vcount()


def edge_number(graph):
    return graph.ecount()


def global_transitivity(graph):
    return graph.transitivity_undirected()


def vertices_mean_degree(graph):
    return np.mean(graph.degree())


def assortativity(graph):
    return graph.assortativity_degree(directed=False)


def heterogeneity(graph):
    mean_degree_quad = 0.
    for v in range(graph.vcount()):
        mean_degree_quad += np.power(graph.degree(v), 2)
    mean_degree_quad = mean_degree_quad / graph.vcount()
    return mean_degree_quad / np.power(np.mean(graph.degree()), 2)


def density(graph):
    return graph.ecount()/((graph.vcount() * (graph.vcount()-1))/2)
