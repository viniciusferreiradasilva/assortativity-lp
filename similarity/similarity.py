#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import math
import numpy as np
from numpy.linalg import inv


############################
# Local Similarity Indices #
############################

# Implementation of common neighbors similarity index for link prediction.
def common_neighbors(graph, adjlist, i, j):
    return len(adjlist[i].intersection(adjlist[j]))


# Implementation of jaccard similarity index for link prediction.
def jaccard_index(graph, adjlist, i, j):
    isect = len(adjlist[i].intersection(adjlist[j]))
    union = (len(adjlist[i]) + len(adjlist[j]) - isect)
    # Tests if the union of the two sets is not empty.
    if (union == 0):
        return 0
    else:
        return (isect / union)


# Implementation of salton similarity index for link prediction.
def salton_index(graph, adjlist, i, j):
    product = float(graph.degree(i) * graph.degree(j))
    if product == 0.0:
        return 0.0
    isect = len(adjlist[i].intersection(adjlist[j]))
    return isect / math.sqrt(product)


# Implementation of sorensen similarity index for link prediction.
def sorensen_index(graph, adjlist, i, j):
    _sum = float(graph.degree(i)) * float(graph.degree(j))
    if _sum == 0.0:
        return 0.0
    isect = 2 * len(adjlist[i].intersection(adjlist[j]))
    return isect / _sum


# Implementation of hub depressed similarity index for link prediction.
def leicht_holme_newman(graph, adjlist, i, j):
    product = float(graph.degree(i)) * float(graph.degree(j))
    if product == 0.0:
        return 0.0
    isect = len(adjlist[i].intersection(adjlist[j]))
    return isect / product


# Implementation of hub promoted similarity index for link prediction.
def hub_promoted(graph, adjlist, i, j):
    minimum = min(float(graph.degree(i)), float(graph.degree(j)))
    if minimum == 0.0:
        return 0.0
    isect = len(adjlist[i].intersection(adjlist[j]))
    return isect / minimum


# Implementation of hub depressed similarity index for link prediction.
def hub_depressed(graph, adjlist, i, j):
    maximum = max(float(graph.degree(i)), float(graph.degree(j)))
    if maximum == 0.0:
        return 0.0
    isect = len(adjlist[i].intersection(adjlist[j]))
    return isect / maximum


# Implementation of preferential attachment similarity index for link prediction.
def preferential_attachment(graph, adjlist, i, j):
    return graph.degree(i) * graph.degree(j)


# Implementation of resource allocation similarity index for link prediction.
def resource_allocation(graph, adjlist, i, j):
    score = 0.0
    for isect in adjlist[i].intersection(adjlist[j]):
        degree = graph.degree(isect)
        if degree != 0:
            score += 1 / degree
    return score


# Implementation of adamic adar similarity index for link prediction.
def adamic_adar(graph, adjlist, i, j):
    score = 0.0
    for isect in adjlist[i].intersection(adjlist[j]):
        degree = graph.degree(isect)
        if degree != 0 and degree != 1:
            score += 1 / math.log(degree)
    return score


#############################
# Global Similarity Indices #
#############################

# Implementation of standard katz similarity index for link prediction. (Uses too much memory)
def katz_index(graph, katz_matrix, i, j, beta=0.5):
    # If any object is different, the katz matrix must be calculated. In a positive case, katz similarity must
    # be recalculated.
    if katz_matrix is None:
        # Gets the adjacency matrix of the graph as a numpy object.
        adj_matrix = np.array(graph.get_adjacency().data)
        idn = np.identity(graph.vcount())
        katz_matrix = inv((idn - beta * adj_matrix)) - idn
    return katz_matrix[i, j]


# Implementation of simrank index for link prediction.
def simrank(graph, adjlist, i, j, it=5):
    return 0


# Implementation of page rank for link prediction.
def pagerank(graph, adjlist, i, j, it=5, df = .85):
    return 0
