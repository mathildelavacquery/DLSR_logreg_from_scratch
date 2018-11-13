#! /usr/bin/python

import argparse
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from describe import Quartile, Count


### Quel cours de Poudlard a une repartition des notes homogenes entre les 4 maisons ?
def convert_float(x):
    if x != '':
        try:
            x = float(x)
            return x
        except (TypeError, ValueError):
            return x


def read_data2(dataname):
    with open('../data/' + dataname) as f:
        lis=[line for line in f]
        feature_list = lis[0].strip().split(',')[6:] # only the subjects features
        nb_subjects = len(feature_list)
        feature_dico = dict((k,dict()) for k in feature_list)
        for student in lis[1:]:
            house = student.strip().split(',')[1]
            grades = student.strip().split(',')[6:]
            for i in range(nb_subjects):
                if house in feature_dico[feature_list[i]].keys():
                    feature_dico[feature_list[i]][house].append(convert_float(grades[i]))
                else:
                    feature_dico[feature_list[i]][house] = [convert_float(grades[i])]
        return feature_dico, feature_list

def anova4(x, y, z, t):
    x = [float(l) for l in x if l]
    y = [float(l) for l in y if l]
    z = [float(l) for l in z if l]
    t = [float(l) for l in t if l]
    tot = x + y +z + t
    tot_nest = [x, y, z, t]
    SSbetween = - sum(tot)**2/float(len(tot))
    for i in range(4):
        SSbetween += sum(tot_nest[i])**2/float(len(tot_nest[i]))
    SSwithin  = sum([l**2 for l in tot]) - sum(tot)**2/float(len(tot))
    dfb = len(tot_nest) - 1
    dfw = len(tot)- len(tot_nest)
    MSbetween = SSbetween / dfb
    MSwithin = SSwithin / dfw
    F = MSbetween / MSwithin
    return F

def homogen_fonction(feature_dico, feature_list, F_real):
    houses = list(feature_dico[feature_list[0]].keys())
    homogen_features = []
    for feature in feature_list:
        X = feature_dico[feature]
        F = anova4(X[houses[0]],X[houses[1]], X[houses[2]], X[houses[3]])
        if F <= F_real:
            homogen_features.append(feature)
    return homogen_features

def freq_per_house(feature, b): # a dictionnary / b = nb of bins, an integer
    # distribution of the grades for everyone
    houses = feature.keys()
    all_grades = []
    for house in houses:
        all_grades += feature[house]
    mini = Quartile(all_grades, 0) #min
    maxi = Quartile(all_grades, 1) #max
    grade_list = [mini + (maxi-mini)/b*i for i in range(b+1)]
    xy_dico = dict((house, dict()) for house in houses)
    for house in houses:
        xy_dico[house]['x'] = [mini]
        xy_dico[house]['y'] = [0]
        lis = [float(l) for l in feature[house] if l]
        nb_student = Count(lis) # nb of students per house enrolled in the class
        for i in range(1,b+1):
            lis2 = [l for l in lis if (l <= grade_list[i] and l > grade_list[i-1])]
            freq = Count(lis2)/float(nb_student)
            xy_dico[house]['x'].extend((grade_list[i-1], grade_list[i]))
            xy_dico[house]['y'].extend((freq, freq))
        xy_dico[house]['x'].append(grade_list[b]) # pour refermer le graph
        xy_dico[house]['y'].append(0)
    return xy_dico


def plot_hist(feature_dico, feature, b, house_colors):
    xy_dico = freq_per_house(feature_dico[feature], b)
    for house in house_colors.keys():
        x = xy_dico[house]['x']
        y = xy_dico[house]['y']
        plt.fill(x, y, color= house_colors[house], linewidth=2, label = house, alpha = 0.5)
    plt.xlim(Quartile(x,0),)
    plt.ylim(Quartile(y,0),)

def plot_homogen_hist(feature_dico, homogen_features, house_colors):
    k = 0
    fig = plt.figure(figsize = (20,10), dpi = 100)
    grid = gridspec.GridSpec(1, len(homogen_features))
    for feature in homogen_features:
        plt.subplot(grid[0, k])
        plot_hist(feature_dico, feature, 20, house_colors)
        plt.title(feature)
        plt.legend(ncol = 2, fontsize = 'x-small')
        k += 1
    plt.tight_layout()
    plt.show(block = True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Dataset you want to describe')
    parser.add_argument('set', type = str, help = 'Name of the file to read')
    args = parser.parse_args()
    feature_dico, feature_list = read_data2(args.set)

    house_colors = {'Ravenclaw': 'blue', 'Slytherin': 'green', 'Gryffindor' : 'red', 'Hufflepuff' : 'yellow'}

    # ANOVA F stat with confidence alpha = 0.05
    # grade repartition is homogeneous if F <= F_3_1550
    # we test H0: the distributions are homogeneous against H1: they are not
    F_3_1550 = 2.6
    homogen_features = homogen_fonction(feature_dico, feature_list, F_3_1550)

    plot_homogen_hist(feature_dico, homogen_features, house_colors)
