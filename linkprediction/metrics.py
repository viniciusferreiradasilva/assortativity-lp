#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from itertools import izip


# Method that calculates the precision score for a link prediction ranking, a edges probe set and a depth L.
# This method considers that the predicted edges ranking is already sorted by the value.
def calculate_precision(self, predicted_edges, edges_probe_set, l=100):
    l = min(l, len(edges_probe_set))
    lr = 0
    for edge in sorted(predicted_edges, key=predicted_edges.get, reverse=True)[:l]:
        # Verifies if the first L edges in the sorted ranking are in the probe set.
        if edge in edges_probe_set:
            lr += 1
    return lr / l


# # Method that calculates the AUC score for a link prediction ranking, a edges probe set and n comparisons.
# def calculate_auc(self, predicted_edges, probe_edges_set, n = 100):
#     # Tests if the n is bigger than the sets sizes.
#     if n > len(predicted_edges) or n > len(probe_edges_set):
#         n = min(len(predicted_edges), len(probe_edges_set))
#     # Creates a n size sample of the sets for n comparisons.
#     predicted_edges_sample = random.sample(predicted_edges.keys(), n)
#     probe_edges_set_sample = random.sample(probe_edges_set.keys(), n)
#     n_line = 0
#     n_twolines = 0
#     # For each one of the comparisons, the value of predicted weight is compared with a probe value.
#     for predicted_edge, probe_edge in izip(predicted_edges_sample,__future__ probe_edges_set_sample):
#         # There are n_line times the missing link having a higher score and n_twolines times they have the same
#         # score.
#         if predicted_edges[probe_edge] > predicted_edges[predicted_edge]:
#             n_line += 1
#         elif predicted_edges[probe_edge] == predicted_edges[predicted_edge]:
#             n_twolines += 1
#     return (n_line + 0.5 * n_twolines)/n

