#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from linkprediction.link_predictor import LinkPredictor
from similarity.similarity import Similarity

class MultilevelLinkPredictor():

    def __init__(self):
        # Array that contains all the available multilevel link predictors implemented in this class.
        self.predictors_array = [self.predict_by_edge_replication, self.predict_by_edge_replication_to_file,
                                 self.predict_by_weighted_edge_replication, self.predict_by_weighted_edge_replication_to_file]

    # Method that receives a coarsed graph and the predicted links generated by this graph and generate
    # the predicted links for the original graph (level 0) by replicating the predicted edges for all
    # the vertices inside a supervertex. Receives the original graph, to check the original edges,
    # the coarsed graph (in any level) and the coarsed predicted edges (generated by a link prediction
    # algorithm in the coarsed graph). ER - Edge Replication.
    def predict_by_edge_replication(self, original_graph, coarsed_graph, coarsed_predicted_edges):
        original_predicted_edges = {}
        for v in range(original_graph.vcount()):
            for u in range((v + 1), original_graph.vcount()):
                # Tests if the edge doesn't exists in the original graph. (The edge must be predicted)
                if(original_graph[v, u] == 0):
                    v_successor = coarsed_graph['successors'][v]
                    u_successor = coarsed_graph['successors'][u]
                    # Tests if the edge exists in between the supervertices.
                    if(coarsed_graph[v_successor, u_successor] != 0):
                        original_predicted_edges[(v, u)] = coarsed_graph[v_successor, u_successor]
                    # Tests if the edge exists in between the supervertices.
                    elif (coarsed_graph[u_successor, v_successor] != 0):
                        original_predicted_edges[(v, u)] = coarsed_graph[u_successor, v_successor]
                    # Tests if the vertices are in the same supervertex.
                    elif(v_successor == u_successor):
                        original_predicted_edges[(v, u)] = 1
                    # Tests if there is an edge between the supervertices.
                    elif((v_successor, u_successor) in coarsed_predicted_edges):
                        original_predicted_edges[(v, u)] = coarsed_predicted_edges[(v_successor, u_successor)]
                    # Tests if there is an edge between the supervertices.
                    elif((u_successor, v_successor) in coarsed_predicted_edges):
                        original_predicted_edges[(v, u)] = coarsed_predicted_edges[(u_successor, v_successor)]
        return original_predicted_edges

    # Method that receives a coarsed graph and the predicted links generated by this graph and generate
    # the predicted links for the original graph (level 0) by replicating the predicted edges for all
    # the vertices inside a supervertex. Receives the original graph, to check the original edges,
    # the coarsed graph (in any level) and the coarsed predicted edges (generated by a link prediction
    # algorithm in the coarsed graph). ER - Edge Replication.
    def predict_by_edge_replication_to_file(self, original_graph, coarsed_graph, coarsed_predicted_edges, io_handler):
        original_predicted_edges = {}
        for v in range(original_graph.vcount()):
            for u in range((v + 1), original_graph.vcount()):
                # Tests if the edge doesn't exists in the original graph. (The edge must be predicted)
                if(original_graph[v, u] == 0):
                    v_successor = coarsed_graph['successors'][v]
                    u_successor = coarsed_graph['successors'][u]
                    # Tests if the edge exists in between the supervertices.
                    if(coarsed_graph[v_successor, u_successor] != 0):
                        io_handler.write_predicted_edge((v, u), str(coarsed_graph[v_successor, u_successor]))
                    # Tests if the edge exists in between the supervertices.
                    elif (coarsed_graph[u_successor, v_successor] != 0):
                        io_handler.write_predicted_edge((v, u), str(coarsed_graph[u_successor, v_successor]))
                    # Tests if the vertices are in the same supervertex.
                    elif(v_successor == u_successor):
                        io_handler.write_predicted_edge((v, u), str(1))
                    # Tests if there is an edge between the supervertices.
                    elif((v_successor, u_successor) in coarsed_predicted_edges):
                        io_handler.write_predicted_edge((v, u), str(coarsed_predicted_edges[(v_successor, u_successor)]))
                    # Tests if there is an edge between the supervertices.
                    elif((u_successor, v_successor) in coarsed_predicted_edges):
                        io_handler.write_predicted_edge((v, u), str(coarsed_predicted_edges[(u_successor, v_successor)]))

    # Method that receives a coarsed graph and the predicted links generated by this graph and generate
    # the predicted links for the original graph (level 0) by replicating the predicted edges for all
    # the vertices inside a supervertex. Differently from the method above, this method weights the edges
    # that are inside the supervertex. WER - Weighted Edge Replication.
    def predict_by_weighted_edge_replication(self, original_graph, coarsed_graph, coarsed_predicted_edges):
        original_predicted_edges = {}
        # Calculates the sizes of the super-vertices of the network.
        super_vertices_sizes = {}
        for super_vertice in coarsed_graph['successors']:
            if(super_vertice in super_vertices_sizes):
                super_vertices_sizes[super_vertice] += 1
            else:
                super_vertices_sizes[super_vertice] = 1
        for v in range(original_graph.vcount()):
            for u in range((v + 1), original_graph.vcount()):
                # Tests if the edge doesn't exists in the original graph. (The edge must be predicted)
                if(original_graph[v, u] == 0):
                    v_successor = coarsed_graph['successors'][v]
                    u_successor = coarsed_graph['successors'][u]
                    # Tests if the edge exists in between the supervertices.
                    if(coarsed_graph[v_successor, u_successor] != 0):
                        original_predicted_edges[(v, u)] = (coarsed_graph[v_successor, u_successor] / (super_vertices_sizes[v_successor] * super_vertices_sizes[u_successor]))
                    # Tests if the edge exists in between the supervertices.
                    elif (coarsed_graph[u_successor, v_successor] != 0):
                        original_predicted_edges[(v, u)] = (coarsed_graph[u_successor, v_successor] / (super_vertices_sizes[v_successor] * super_vertices_sizes[u_successor]))
                    # Tests if the vertices are in the same supervertex.
                    elif(v_successor == u_successor):
                        original_predicted_edges[(v, u)] = (1 / super_vertices_sizes[v_successor])
                    # Tests if there is an edge between the supervertices.
                    elif((v_successor, u_successor) in coarsed_predicted_edges):
                        original_predicted_edges[(v, u)] = coarsed_predicted_edges[(v_successor, u_successor)]
                    # Tests if there is an edge between the supervertices.
                    elif((u_successor, v_successor) in coarsed_predicted_edges):
                        original_predicted_edges[(v, u)] = coarsed_predicted_edges[(u_successor, v_successor)]
        return original_predicted_edges


    # Method that receives a coarsed graph and the predicted links generated by this graph and generate
    # the predicted links for the original graph (level 0) by replicating the predicted edges for all
    # the vertices inside a supervertex. Differently from the method above, this method weights the edges
    # that are inside the supervertex. WER - Weighted Edge Replication.
    def predict_by_weighted_edge_replication_to_file(self, original_graph, coarsed_graph, coarsed_predicted_edges, io_handler):
        original_predicted_edges = {}
        # Calculates the sizes of the super-vertices of the network.
        super_vertices_sizes = {}
        for super_vertice in coarsed_graph['successors']:
            if (super_vertice in super_vertices_sizes):
                super_vertices_sizes[super_vertice] += 1
            else:
                super_vertices_sizes[super_vertice] = 1
        for v in range(original_graph.vcount()):
            for u in range((v + 1), original_graph.vcount()):
                # Tests if the edge doesn't exists in the original graph. (The edge must be predicted)
                if (original_graph[v, u] == 0):
                    v_successor = coarsed_graph['successors'][v]
                    u_successor = coarsed_graph['successors'][u]
                    # Tests if the edge exists in between the supervertices.
                    if (coarsed_graph[v_successor, u_successor] != 0):
                        io_handler.write_predicted_edge((v, u), str((coarsed_graph[v_successor, u_successor] / (
                        super_vertices_sizes[v_successor] * super_vertices_sizes[u_successor]))))
                    # Tests if the edge exists in between the supervertices.
                    elif (coarsed_graph[u_successor, v_successor] != 0):
                        io_handler.write_predicted_edge((v, u), str((coarsed_graph[u_successor, v_successor] / (
                        super_vertices_sizes[v_successor] * super_vertices_sizes[u_successor]))))
                    # Tests if the vertices are in the same supervertex.
                    elif (v_successor == u_successor):
                        io_handler.write_predicted_edge((v, u), str((1 / super_vertices_sizes[v_successor])))

                    # Tests if there is an edge between the supervertices.
                    elif ((v_successor, u_successor) in coarsed_predicted_edges):
                        io_handler.write_predicted_edge((v, u), str(coarsed_predicted_edges[(v_successor, u_successor)]))

                    # Tests if there is an edge between the supervertices.
                    elif ((u_successor, v_successor) in coarsed_predicted_edges):
                        io_handler.write_predicted_edge((v, u), str(coarsed_predicted_edges[(u_successor, v_successor)]))


    # Method that predicts edges for each subgraph generated by supervertices.
    def predict_inside_super_vertex(self, coarsed_graph, similarity):
        predicted_edges = {}
        # Tests if the graph has any super-vertex.
        if(coarsed_graph['level'] != 0):
            print coarsed_graph['successors']
            return predicted_edges
        else:
            print "graph has no super-vertices."
