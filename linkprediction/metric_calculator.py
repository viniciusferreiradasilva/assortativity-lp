#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import random
from itertools import izip

# Class with methods that calculates the metrics for test link predictors accuracy.
class MetricCalculator():

    def __init__(self):
        pass

    ########################
    #       Precision      #
    ########################


    # Method that calculates the precision score for a link prediction ranking, a edges probe set and a depth L.
    # This method considers that the predicted edges ranking is already sorted by the value.
    def calculate_precision(self, predicted_edges, edges_probe_set, L=100):
        L = min(L, len(edges_probe_set))
        Lr = 0
        for edge in sorted(predicted_edges, key=predicted_edges.get, reverse=True)[:L]:
            # Verifies if the first L edges in the sorted ranking are in the probe set.
            if(edge in edges_probe_set):
                Lr += 1
        return (Lr / L)

    # Method that calculates the precision score for a link prediction ranking, a edges probe set and a depth L.
    # This method considers that the predicted edges ranking is already batch sorted by the value. This method also
    # works for batched files.
    def calculate_precision_from_file(self, edges_probe_set, iohandler, L=100):
        iohandler.input_file.seek(0, 0)
        Lr = 0
        # Reads the first L predicted edges from the ranking.
        for i in range(L):
                values = iohandler.load_predicted_edge()
                if(values):
                    values = values.split(" ")
                    predicted_edge = (int(values[0]), int(values[1]))
                    if(predicted_edge in edges_probe_set):
                        Lr += 1
        return (Lr / L)


    ########################
    # Area Under ROC Curve #
    ########################

    # Method that calculates the AUC score for a link prediction ranking, a edges probe set and n comparisons.
    def calculate_auc(self, predicted_edges, probe_edges_set, n = 100):
        # Tests if the n is biggers than the sets sizes.
        if(n > len(predicted_edges) or n > len(probe_edges_set)):
            n = min(len(predicted_edges), len(probe_edges_set))
        # Creates a n size sample of the sets for n comparisons.
        predicted_edges_sample = random.sample(predicted_edges.keys(), n)
        probe_edges_set_sample = random.sample(probe_edges_set.keys(), n)
        n_line = 0
        n_twolines = 0
        # For each one of the comparisons, the value of predicted weight is compared with a probe value.
        for predicted_edge, probe_edge in izip(predicted_edges_sample, probe_edges_set_sample):
            # There are n_line times the missing link having a higher score and n_twolines times they have the same
            # score.
            if(predicted_edges[probe_edge] > predicted_edges[predicted_edge]):
                n_line += 1
            elif(predicted_edges[probe_edge] == predicted_edges[predicted_edge]):
                n_twolines += 1
        return ((n_line + 0.5 * n_twolines)/n)


    # Method that calculates the precision score for a link prediction ranking, a edges probe set and a depth L.
    # This method considers that the predicted edges ranking is already batch sorted by the value. This method also
    # works for batched files.
    def calculate_auc_from_file(self, edges_probe_set, iohandler, n=100):
        iohandler.input_file.seek(0, 0)
        n_line = 0
        n_twolines = 0
        # Stack of readed probe edges.
        probe_stack = []
        # Stack of readed predicted.
        predicted_stack = []
        # Adjusts the n parameter.
        n = min(n, len(edges_probe_set))
        # Recovers the values from the ranking file.
        while(not (len(probe_stack) == n and len(predicted_stack) == n)):
            values = iohandler.load_predicted_edge()
            if(values):
                values = values.split(" ")
                if ((int(values[0]), int(values[1])) in edges_probe_set and len(probe_stack) < n):
                    probe_stack.append(float(values[2]))
                elif(len(predicted_stack) < n):
                    predicted_stack.append(float(values[2]))
        # Making the comparisons between the probe and predicted edges.
        while(probe_stack and predicted_stack):
            probe_edge_value = probe_stack.pop()
            predicted_edge_value = predicted_stack.pop()
            # There are n_line times the missing link having a higher score and n_twolines times they have the same score.
            if (probe_edge_value > predicted_edge_value):
                n_line += 1
            elif (probe_edge_value == predicted_edge_value):
                n_twolines += 1

        return ((n_line + 0.5 * n_twolines) / n)


    # Method that calculates the AUC score for a link prediction ranking, a edges probe set and n comparisons. This
    # method considers a ranking that only contains non-zero predictions (To do such thing, the way that the edges are
    # randomizes is different from the standard method.
    def calculate_auc_non_zero(self, vcount, predicted_edges, probe_edges_set, n=100):
        # Tests if the n is biggers than the sets sizes.
        if (n > len(probe_edges_set)):
            n = len(probe_edges_set)
        # predicted_edges_sample = random.sample(predicted_edges.keys(), n)
        probe_edges_set_sample = random.sample(probe_edges_set.keys(), n)
        n_line = 0
        n_twolines = 0
        comparisons = 0
        # For each one of the comparisons, the value of predicted weight is compared with a probe value.
        for probe_edge in probe_edges_set_sample:
            # Gets a random predicted edge that is not in the probe edges set.
            predicted_edge_from = random.randint(0, vcount - 2)
            predicted_edge_to = random.randint(predicted_edge_from + 1, vcount - 1)

            while((predicted_edge_from, predicted_edge_to) in probe_edges_set):
                predicted_edge_from = random.randint(0, vcount - 2)
                predicted_edge_to = random.randint(predicted_edge_from + 1, vcount - 1)

            # Gets the predicted edge value.
            if((predicted_edge_from, predicted_edge_to) in predicted_edges):
                predicted_edge_value = predicted_edges[(predicted_edge_from, predicted_edge_to)]
            else:
                predicted_edge_value = 0

            # Tests if the predicted edge has a value greater than zero and exists in the set of predicted edges.
            if(probe_edge in predicted_edges):
                probe_edge_value = predicted_edges[probe_edge]
            else:
                probe_edge_value = 0

            # There are n_line times the missing link having a higher score and n_twolines times they have the same score.
            if (probe_edge_value > predicted_edge_value):
                n_line += 1
            elif (probe_edge_value == predicted_edge_value):
                n_twolines += 1

        return ((n_line + 0.5 * n_twolines) / n)

    # Metric that calculates how many examples of the first ranking exists in the second ranking as well. The first
    # L entries of the ordered ranking are tested.
    def calculate_ranking_compare(self, test_ranking, probe_ranking, L):
        hits = 0
        probe_ranking = sorted(probe_ranking, key=probe_ranking.get, reverse=True)[:L]

        for entry in sorted(test_ranking, key=test_ranking.get, reverse=True)[:L]:
            if(entry in probe_ranking):
                hits += 1
        return (hits/len(test_ranking))