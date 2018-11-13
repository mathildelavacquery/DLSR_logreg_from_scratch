#! /usr/bin/python

import argparse
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from describe import Quartile, Count
from histogram import convert_float, read_data2, freq_per_house, plot_hist
from scatter_plot import scatter_plot


house_colors = {'Ravenclaw': 'blue', 'Slytherin': 'green', 'Gryffindor' : 'red', 'Hufflepuff' : 'yellow'}

def pair_plot(feature_dico, feature_list, house_colors):
    n = len(feature_list)
    fig = plt.figure(figsize = (15, 15), dpi = 100)
    grid = gridspec.GridSpec(n,n)
    for k in range(n):
        for l in range(n):
            plt.subplot(grid[k,l]) 
            if k == l:
                plot_hist(feature_dico, feature_list[k], 20, house_colors)
                if k == 0:
                    plt.legend(ncol = 2, fontsize = 'x-small')
            else:
                plot = scatter_plot(feature_dico, feature_list[k], feature_list[l], house_colors)
            if k == 0:
                plt.title(feature_list[l])
            if l == 0:
                plt.ylabel(feature_list[k])
    plt.tight_layout()
    plt.show(block = True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Dataset to plot')
    parser.add_argument('set', type = str, help = 'Name of the file to read')
    args = parser.parse_args()
    feature_dico, feature_list = read_data2(args.set)
    houses = list(feature_dico[feature_list[0]].keys())

    feature_list2 = feature_list[:5]

    pair_plot(feature_dico, feature_list2, house_colors)
