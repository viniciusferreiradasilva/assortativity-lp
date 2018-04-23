#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import math
import numpy as np
from numpy.linalg import inv

class Similarity():

    def __init__(self):
        # Matrix that stores the katz measure to avoid re-calculations.
        self.katz_matrix = None
        # Dict that stores the katz similarities to avoid re-calculations.
        self.katz_similarities = {}
        self.katz_length = None
        self.katz_beta = None
        self.last_i = -1
        # Array that contains all the available similarities measures implemented in this class.
        self.similarities_array = [self.common_neighbors, self.jaccard_index, self.salton_index, self.adamic_adar,
                                   self.preferential_attachment, self.resource_allocation, self.sorensen_index,
                                   self.hub_promoted, self.hub_depressed, self.leicht_holme_newman,
                                   self.lowmem_katz_index]

    ############################
    # Local Similarity Indices #
	############################

    # Implementation of common neighbors similarity index for link prediction.
    def common_neighbors(self, graph, adjlist, i, j):
        return len(adjlist[i].intersection(adjlist[j]))

    # Implementation of jaccard similarity index for link prediction.
    def jaccard_index(self, graph, adjlist, i, j):
        isect = len(adjlist[i].intersection(adjlist[j]))
        union = (len(adjlist[i]) + len(adjlist[j]) - isect)
        # Tests if the union of the two sets is not empty.
        if (union == 0):
            return 0
        else:
            return (isect / union)

    # Implementation of salton similarity index for link prediction.
    def salton_index(self, graph, adjlist, i, j):
        product = float(graph.degree(i) * graph.degree(j))
        if product == 0.0:
            return 0.0
        isect = len(adjlist[i].intersection(adjlist[j]))
        return isect / math.sqrt(product)

    # Implementation of sorensen similarity index for link prediction.
    def sorensen_index(self, i, j):
        _sum = float(self.graph.degree(i)) * float(self.graph.degree(j))
        if _sum == 0.0:
            return 0.0
        isect = 2 * len(self.adjlist[i].intersection(self.adjlist[j]))
        return isect / _sum

    # Implementation of hub depressed similarity index for link prediction.
    def leicht_holme_newman(self, i, j):
        product = float(self.graph.degree(i)) * float(self.graph.degree(j))
        if product == 0.0:
            return 0.0
        isect = len(self.adjlist[i].intersection(self.adjlist[j]))
        return isect / product

    # Implementation of hub promoted similarity index for link prediction.
    def hub_promoted(self, i, j):
        minimum = min(float(self.graph.degree(i)), float(self.graph.degree(j)))
        if minimum == 0.0:
            return 0.0
        isect = len(self.adjlist[i].intersection(self.adjlist[j]))
        return isect / minimum

    # Implementation of hub depressed similarity index for link prediction.
    def hub_depressed(self, i, j):
        maximum = max(float(self.graph.degree(i)), float(self.graph.degree(j)))
        if maximum == 0.0:
            return 0.0
        isect = len(self.adjlist[i].intersection(self.adjlist[j]))
        return isect / maximum

    # Implementation of preferential attachment similarity index for link prediction.
    def preferential_attachment(self, graph, adjlist, i, j):
        return graph.degree(i) * graph.degree(j)

    # Implementation of resource allocation similarity index for link prediction.
    def resource_allocation(self, i, j):
        score = 0.0
        for isect in self.adjlist[i].intersection(self.adjlist[j]):
            degree = self.graph.degree(isect)
            if degree != 0:
                score += 1 / degree
        return score

    # Implementation of adamic adar similarity index for link prediction.
    def adamic_adar(self, graph, adjlist, i, j):
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
	def katz_index(self, graph, adjlist, i, j, beta=0.5):
		# If any object is different, the katz matrix must be calculated. In a positive case, katz similarity must
        # be recalculated.
		if (self.katz_matrix is None):
			# Gets the adjacency matrix of the graph as a numpy object.
			adj_matrix = np.array(graph.get_adjacency().data)
			I = np.identity(graph.vcount())
			self.katz_matrix = inv((I - beta * adj_matrix)) - I
		return (self.katz_matrix[i, j])

	# Implementation of a iterative katz similarity index for link prediction. (Uses less memory.)
	def lowmem_katz_index(self, graph, adjlist, i, j, l=3, beta=0.5):
		# If the parameters are different, the entire matrix must be recalculated.
		if((self.katz_length != l) or (self.katz_beta != beta) or (self.last_i != i)):
			self.katz_length = l
			self.katz_beta = beta
			self.last_i = i

			constant = beta
			# Creates the array of adjacency for the vertex v.
			v_adjacency = [1 if (x in adjlist[i]) else 0 for x in range(graph.vcount())]
			# Array that stores the katz similarities. Similarities starts with (beta * adjacency), as iteration 1.
			self.katz_similarities = np.dot(constant, v_adjacency)

			for cont in range(2, (l + 1)):
				# Updates the product constant value.
				constant *= beta
				product = np.empty([graph.vcount()])
				for k in range(graph.vcount()):
					product[k] = 0
					for neighbor in adjlist[k]:
						if(v_adjacency[neighbor] != 0):
							product[k] += 1
					# Updates the similarities values.
					self.katz_similarities[k] += constant * product[k]
				v_adjacency = product

		return self.katz_similarities[j]


	# Implementation of simrank index for link prediction.
	def simrank(self, graph, adjlist, i, j, it=5):
		return 0

	# Implementation of page rank for link prediction.
	def pagerank(self, graph, adjlist, i, j, it=5, df = .85):
		return 0
