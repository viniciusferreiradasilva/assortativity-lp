#!/usr/bin/env python
# -*- coding: utf-8 -*-
import operator
import os
from tempfile import gettempdir
from itertools import islice, cycle
from random import shuffle
import heapq


# Class that handles the input/output files that are used by this software. Ranking files, precision/auc/time files, etc.
class IOHandler():

    def __init__(self):
        self.input_file = None
        self.input_file_path = None
        self.output_file = None
        self.output_file_path = None

    # Method that loads a input file.
    def load_input_file(self, input_file_path):
        self.input_file = open(input_file_path, "r")
        self.input_file_path = input_file_path

    # Method that loads a output file.
    def load_output_file(self, output_file_path):
        self.output_file = open(output_file_path, "w")
        self.output_file_path = output_file_path

    # Method that closes the input/output files.
    def close_files(self):
        if (self.input_file):
            self.input_file.close()
        if(self.output_file):
            self.output_file.close()

    # Method that removes an input file.
    def remove_input_file(self):
        os.remove(self.input_file_path)

    # Method that removes an output file.
    def remove_output_file(self):
        os.remove(self.output_file_path)

    # Methods that writes the predicted edges in the output file.
    def write_predicted_edges(self, predicted_edges):
        for predicted_edge in predicted_edges:
            self.output_file.write("%i %i %f\n" % (predicted_edge[0], predicted_edge[1], predicted_edges[predicted_edge]))

    # Methods that loads the predicted edges from the input file.
    def load_predicted_edges(self):
        # Set the pointer to the begining.
        self.input_file.seek(0, 0)
        predicted_edges = {}
        for line in self.input_file:
            values = line.split(" ")
            predicted_edges[(int(values[0]), int(values[1]))] = float(values[2])
        return predicted_edges

    # Methods that writes one predicted edge in the output file. (For performance proposes)
    def write_predicted_edge(self, predicted_edge, weight):
        self.output_file.write("%i %i %s\n" % (predicted_edge[0], predicted_edge[1], weight))

    # Methods that writes one predicted edge in the output file. (For performance proposes)
    def load_predicted_edge(self):
        return self.input_file.readline()

    # Methods that writes the probe edges in the output file.
    def write_probe_edges(self, probe_edges):
        for probe_edge in probe_edges:
            self.output_file.write("%i %i %f\n" % (probe_edge[0], probe_edge[1], probe_edges[probe_edge]))

    # Methods that loads the predicted edges from the input file.
    def load_probe_edges(self):
        # Set the pointer to the begining.
        self.input_file.seek(0, 0)
        probe_edges = {}
        for line in self.input_file:
            values = line.split(" ")
            probe_edges[(int(values[0]), int(values[1]))] = float(values[2])
        return probe_edges


    # Write the edges in the output file.
    def write_results(self, result):
        self.output_file.write("%s\n" % (result))

    ############################
    #       Batch handling     #
    ############################

    # Sorts a huge files for statistical confidence in metrics calculation.
    def batch_sort(self, key=None, buffer_size=32000000, tempdirs=None):
        if tempdirs is None:
            tempdirs = []
        if not tempdirs:
            tempdirs.append(gettempdir())
        chunks = []
        try:
            with open(self.input_file_path, 'rb', 64 * 1024) as input_file:
                input_iterator = iter(input_file)
                for tempdir in cycle(tempdirs):
                    current_chunk = list(islice(input_iterator, buffer_size))
                    if not current_chunk:
                        break
                    # Lambda function allows the last attribute (edge weight) be used as the value for sorting.
                    current_chunk = sorted(current_chunk, key=lambda x: float(x.split(" ")[2]), reverse=True)

                    output_chunk = open(os.path.join(tempdir, '%06i' % len(chunks)), 'w+b', 64 * 1024)
                    chunks.append(output_chunk)
                    output_chunk.writelines(current_chunk)
                    output_chunk.flush()
                    output_chunk.seek(0)
            with open(self.input_file_path, 'wb', 64 * 1024) as output_file:
                output_file.writelines(self.merge(key, *chunks))
        finally:
            for chunk in chunks:
                try:
                    chunk.close()
                    os.remove(chunk.name)
                except Exception:
                    pass

    # Shuffles a huge files for statistical confidence in metrics calculation.
    def batch_shuffle(self, key=None, buffer_size=32000000, tempdirs=None):
        if tempdirs is None:
            tempdirs = []
        if not tempdirs:
            tempdirs.append(gettempdir())

        chunks = []
        try:
            with open(self.input_file_path, 'rb', 64 * 1024) as input_file:
                input_iterator = iter(input_file)
                for tempdir in cycle(tempdirs):
                    current_chunk = list(islice(input_iterator, buffer_size))
                    if not current_chunk:
                        break
                    # Method that shuffles the chunk.
                    shuffle(current_chunk)
                    output_chunk = open(os.path.join(tempdir, '%06i' % len(chunks)), 'w+b', 64 * 1024)
                    chunks.append(output_chunk)
                    output_chunk.writelines(current_chunk)
                    output_chunk.flush()
                    output_chunk.seek(0)
            with open(self.input_file_path, 'wb', 64 * 1024) as output_file:
                output_file.writelines(self.merge(key, *chunks))
        finally:
            for chunk in chunks:
                try:
                    chunk.close()
                    os.remove(chunk.name)
                except Exception:
                    pass

    # Method that merges chunks of predicted edges.
    def merge(self, key=None, *iterables):
        for element in heapq.merge(*iterables):
            yield element


