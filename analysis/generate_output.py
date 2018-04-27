#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This code generates a .csv output file containing all the results for all datasets in output folder.

import numpy as np
from os import listdir, path

root = "../output/"

print "Generating output files..."
output_dir = root + "output.csv"
output_file = open((output_dir), "w")
header = False

for dataset in listdir(root):
    print "dataset:", dataset
    # Tests if the file is a directory.
    if(path.isdir(root + dataset)):
        dataset_dir = root + dataset
        for similarity_method in listdir(dataset_dir + "/"):
                print "similarity_method:", similarity_method
                # Open the auc file.
                auc_file = open(("../output/"+ dataset_dir.split("/")[2] + "/" + similarity_method + "/auc.csv"), "r")
                # # Open the precision file.
                pr_file = open(("../output/"+ dataset_dir.split("/")[2] + "/" + similarity_method + "/pr.csv"), "r")

                auc_matrix = np.loadtxt(auc_file, delimiter=",", skiprows=0, dtype=float)
                auc_means = [auc_matrix[1:].mean(0)]
                auc_sds = [auc_matrix[1:].std(0)]

                pr_matrix = np.loadtxt(pr_file, delimiter=",", skiprows=0, dtype=float)
                pr_means = [pr_matrix[1:].mean(0)]
                pr_sds = [pr_matrix[1:].std(0)]

                # Tests if the reader was already writen.
                if (not header):
                    header = True
                    file_header = "dataset, similarity_method, "
                    # Write the pr header values.
                    file_header += "auc_" + str(int(auc_matrix[0])) + "_mean, "
                    file_header += "auc_" + str(int(auc_matrix[0])) + "_sd, "
                    file_header += "pr_" + str(int(pr_matrix[0])) + "_mean, "
                    file_header += "pr_" + str(int(pr_matrix[0])) + "_sd, "
                    file_header += "\n"
                    output_file.write(file_header)

                # Writes the values
                line = dataset + ", " + similarity_method + ", "
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

                line += "\n"
                output_file.write(line)

                auc_file.close()
                pr_file.close()

output_file.close()
print "Finished..."
