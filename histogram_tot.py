#! /usr/bin/python

import argparse
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from describe import Quartile, Count
from histogram import convert_float, read_data2, freq_per_house, plot_hist


def hist_tot(feature_dico, feature_list, b, house_colors):
    l = 0
    m = 0
    fig = plt.figure(figsize = (20,10), dpi = 100)
    grid = gridspec.GridSpec(4,4)
    for k in range(len(feature_list)):
        xy_dico = freq_per_house(feature_dico[feature_list[k]], b)
        if k <4:
            l = k
        else:
            m = k//4
            l = k - 4*m
        plt.subplot(grid[m, l])
        plot_hist(feature_dico, feature_list[k], b, house_colors)
        plt.title(feature_list[k])
        plt.legend(ncol = 2, fontsize = 'x-small')
    plt.tight_layout()
    plt.show(block = True)
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Dataset you want to describe')
    parser.add_argument('set', type = str, help = 'Name of the file to read')
    args = parser.parse_args()

    house_colors = {'Ravenclaw': 'blue', 'Slytherin': 'green', 'Gryffindor' : 'red', 'Hufflepuff' : 'yellow'}

    feature_dico, feature_list = read_data2(args.set)

    hist_tot(feature_dico, feature_list, 20, house_colors)
