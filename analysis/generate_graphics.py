#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import matplotlib.pyplot as plt
import os
from os import listdir
import re

root = "../output/"

plot_dir = "../output/plots/bymethod/"
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)

# Generate the graphs for auc and pr between the levels by method.
for database in [x for x in listdir(root) if(".csv" in x)]:
    for metric in ["auc", "pr"]:
        # Cleans the plot tool.
        plt.clf()
        # Plotting the auc graphs.
        with open((root+database), 'rb') as csvfile:
            filename = database.split("_")[0]
            print "Generating by method ", metric," graphs for:", filename
            if not os.path.exists(plot_dir+filename+"/"+metric+"/"):
                os.makedirs(plot_dir+filename+"/"+metric+"/")

            # Opens the reading object.
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            # Loads the header from the file.
            header = next(csv_reader)
            old_row = None
            # For each row of the file.
            for row in csv_reader:
                # First reading line.
                if(old_row is None):
                    old_row = row
                    old_ml_method = old_row[0]
                    old_matching_method = old_row[1]
                    old_similarity_method = old_row[2]
                    old_level = old_row[3]
                ml_method = row[0]
                matching_method = row[1]
                similarity_method = row[2]
                level = row[3]
                if(old_ml_method != ml_method or old_matching_method != matching_method or old_similarity_method != similarity_method):
                    plt.title(re.sub('_', '', old_ml_method)  + "_" + re.sub('_', '', old_matching_method) + " " + re.sub('_', '', old_similarity_method))
                    plt.legend(loc='lower right', prop={'size': 5})
                    plt.xlabel('comparisons')
                    plt.ylabel(metric)
                    # Saves the old graph and creates a new one.
                    plt.savefig(plot_dir+filename+ "/" + metric + "/" + old_ml_method + "_" + old_matching_method + "_" + old_similarity_method + '_' + metric+ ".eps", format='eps')
                    plt.clf()
                # Adds the subplot.
                indexes = [header.index(x) for x in header if (metric in x and "mean" in x)]
                y = [float(row[x]) for x in indexes]
                x = [int(x.split("_")[1]) for x in header if (metric in x and "mean" in x)]
                # Plotting the curve.
                plt.plot(x, y,  marker = 'o', label = level)
                axes = plt.gca()
                axes.set_xlim([x[0], x[len(x) - 1]])
                # Updating the old values.
                old_row = row
                old_ml_method = old_row[0]
                old_matching_method = old_row[1]
                old_similarity_method = old_row[2]
                old_level = old_row[3]

plot_dir = "../output/plots/bylevel/"

for database in [x for x in listdir(root) if(".csv" in x)]:
    for metric in ["auc", "pr"]:
        # Cleans the plot tool.
        plt.clf()
        with open((root+database), 'rb') as csvfile:
            filename = database.split("_")[0]
            if not os.path.exists(plot_dir+filename+"/"+metric+"/"):
                os.makedirs(plot_dir+filename+"/"+metric+"/")

            filename = database.split("_")[0]
            print "Generating by level", metric," graphs for:", filename
            if not os.path.exists(plot_dir+filename+"/"):
                os.makedirs(plot_dir+filename+"/")


            # Opens the reading object.
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            # Loads the header from the file.
            header = next(csv_reader)
            level_index = [header.index(x) for x in header if ("level" in x)][0]

            data_by_level = {}

            for row in csv_reader:
                if(row[level_index] in data_by_level):
                    data_by_level[row[level_index]].append(row)
                else:
                    data_by_level[row[level_index]] = [row]

            indexes = [header.index(x) for x in header if (metric in x and "mean" in x)]
            # Calculates the average of the level 0 values for the plot.
            for level in [x for x in data_by_level.keys() if('level0' in x)]:
                avgs = [.0] * len(indexes)
                for row in data_by_level[level]:
                    avgs = [x+y for x,y in zip(avgs, [float(row[x]) for x in indexes])]
                avgs = [x / len(data_by_level[level]) for x in avgs]

            # Plots the curves of levels > 0.
            for level in [x for x in data_by_level.keys() if('level0' not in x)]:
                x = [int(x.split("_")[1]) for x in header if (metric in x and "mean" in x)]
                plt.plot(x, avgs, label="level0")
                axes = plt.gca()
                axes.set_xlim([x[0], x[len(x) - 1]])

                # Plots the graph for that level.
                for row in data_by_level[level]:

                    ml_method = row[0]
                    matching_method = row[1]
                    similarity_method = row[2]
                    y = [float(row[x]) for x in indexes]
                    x = [int(x.split("_")[1]) for x in header if (metric in x and "mean" in x)]
                    plt.plot(x, y,  marker = 'o', label = re.sub('_', '', ml_method)  + "_" + re.sub('_', '', matching_method) + "_" + re.sub('_', '', similarity_method))
                    axes = plt.gca()
                    axes.set_xlim([x[0], x[len(x) - 1]])

                plt.title(level)
                plt.legend(loc='lower right', prop={'size': 5})
                plt.xlabel('comparisons')
                plt.ylabel(metric)
                # Saves the old graph and creates a new one.
                plt.savefig(plot_dir+filename+ "/" + metric + "/" + level.replace(' ', '') + ".eps", format='eps')
                plt.clf()


plot_dir = "../output/plots/time/"

for database in [x for x in listdir(root) if(".csv" in x)]:
    # Cleans the plot tool.
    plt.clf()
    with open((root+database), 'rb') as csvfile:
        filename = database.split("_")[0]
        if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)

        print "Generating by level time graphs for:", filename

        # Opens the reading object.
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        # Loads the header from the file.
        header = next(csv_reader)

        level_index = [header.index(x) for x in header if("level" in x)][0]
        mean_time_index = [header.index(x) for x in header if("mean" in x and "time" in x)][0]

        x = []
        y = []
        old_row = None
        for row in csv_reader:
            if("0" in row[level_index] and x and y):
                plt.plot(x, y, marker = 'o', label=(old_row[0] + "_" + old_row[1] + "_" + old_row[2]))
                axes = plt.gca()
                axes.set_xlim([x[0], x[len(x) - 1]])
                x = []
                y = []

            y.append(float(row[mean_time_index]))
            x.append(int((row[level_index].split("level")[1])))
            old_row = row

        plt.plot(x, y, marker='o', label=(old_row[0] + "_" + old_row[1] + "_" + old_row[2]))
        axes = plt.gca()
        axes.set_xlim([x[0], x[len(x) - 1]])

        plt.title("times(s)  for " + filename)
        plt.legend(loc='upper right', prop={'size': 5})
        plt.xlabel('levels')
        plt.ylabel('time')
        # Saves the old graph and creates a new one.
        plt.savefig(plot_dir+filename + "_time.eps", format='eps')
        plt.clf()









