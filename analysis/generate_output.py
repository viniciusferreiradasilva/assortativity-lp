#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from os import listdir, path
import re

root = "../output/"

print "Generating output files..."
for database in listdir(root):
    # Tests if the file is a directory.
    if(path.isdir(root + database)):
        output_dir = root + database

        output_file = open((output_dir + "_output.csv"), "w")
        header = False

        # Gets the mlp_method.
        for mlp_method in listdir(output_dir+"/"):
            # Gets the matching method.
            for matching_method in listdir(output_dir + "/" + mlp_method + "/"):
                # Gets similarity method
                for similarity_method in listdir(output_dir + "/" + mlp_method + "/" + matching_method + "/"):
                    # Gets the level and tests if it is a directory.
                    levels = [x for x in listdir(output_dir + "/" + mlp_method + "/" + matching_method + "/" + similarity_method)
                              if path.isdir(output_dir + "/" + mlp_method + "/" + matching_method + "/" + similarity_method + "/" + x)]

                    levels_numbers = [None] * len(levels)
                    for i in range(len(levels)):
                        levels_numbers[i] = int(re.match(r"([a-z]+)([0-9]+)", levels[i], re.I).groups()[1])
                    # Get the matrices.
                    for i in sorted(range(len(levels_numbers)), key=lambda k: levels_numbers[k]):
                        # Open the auc file.
                        auc_file = open(("../output/"+ output_dir.split("/")[2] + "/" + mlp_method + "/" + matching_method + "/" + similarity_method + "/" + levels[i] + "/auc.csv"), "r")
                        # # Open the precision file.
                        pr_file = open(("../output/"+ output_dir.split("/")[2] + "/" + mlp_method + "/" + matching_method + "/" + similarity_method + "/" + levels[i] + "/pr.csv"), "r")
                        # # Open the time file.
                        time_file = open(("../output/"+ output_dir.split("/")[2] + "/" + mlp_method + "/" + matching_method + "/" + similarity_method + "/" + levels[i] + "/time.csv"), "r")

                        auc_matrix = np.loadtxt(auc_file, delimiter=",", skiprows=0)
                        auc_means = auc_matrix[1:].mean(0)
                        auc_sds = auc_matrix[1:].std(0)

                        pr_matrix = np.loadtxt(pr_file, delimiter=",", skiprows=0)
                        pr_means = pr_matrix[1:].mean(0)
                        pr_sds = pr_matrix[1:].std(0)

                        time_matrix = np.loadtxt(time_file, delimiter=",", skiprows=0)
                        time_means = time_matrix.mean(0)
                        time_sds = time_matrix.std(0)

                        # Tests if the reader was already writen.
                        if(not header):
                            header = True
                            file_header = "mlp_method, matching_method, similarity_method, level, "
                            # Write the pr header values.
                            for j in range(auc_matrix.shape[1]):
                                file_header += "auc_" + str(int(auc_matrix[0][j])) + "_mean, "

                            # Write the pr header values.
                            for j in range(auc_matrix.shape[1]):
                                file_header += "auc_" + str(int(auc_matrix[0][j])) + "_sd, "

                            for j in range(pr_matrix.shape[1]):
                                file_header += "pr_" + str(int(pr_matrix[0][j])) + "_mean, "

                            for j in range(pr_matrix.shape[1]):
                                file_header += "pr_" + str(int(pr_matrix[0][j])) + "_sd, "

                            file_header += "time_mean, time_sd\n"
                            output_file.write(file_header)

                        # Writes the values
                        line = mlp_method + ", " + matching_method + ", " + similarity_method + ", " + levels[i] + ", "
                        # Write the auc means values.
                        for value in auc_means:
                            line += str(value) + ", "

                        # Write the auc header values.
                        for value in auc_sds:
                            line += str(value) + ", "

                        # Write the pr means values.
                        for value in pr_means:
                            line += str(value) + ", "

                        # Write the pr header values.
                        for value in pr_sds:
                            line += str(value) + ", "

                        line += str(time_means) + ", " + str(time_sds) + "\n"

                        output_file.write(line)

                        # auc_file.close()
                        pr_file.close()
                        time_file.close()

        output_file.close()
print "Finished..."
