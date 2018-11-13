#! /usr/bin/python
import os
import argparse
from math import sqrt
import matplotlib.pyplot as plt


def convert_float(x):
    if x != '':
        try:
            x = float(x)
            return x
        except (TypeError, ValueError):
            return x


### GIVES A DICT OF ALL OF THE FEATURES
def read_data(dataname):
    with open('../data/' + dataname) as f:
        lis=[line for line in f]
        nb_features = len(lis[0].split(','))-1
        feature_list = lis[0].strip().split(',')[1:]
        first_student = lis[1].strip().split(',')[1:]
        first_float = []
        for f in range(len(first_student)):
            first_float.append(convert_float(first_student[f]))
        feature_dico = dict((k, [l]) for k, l in zip(feature_list, first_float))
        for i in range(2, len(lis)):
            student = lis[i].strip().split(',')[1:]
            for f in range(len(feature_list)):
                feature_dico[feature_list[f]].append(convert_float(student[f]))
        return feature_dico, feature_list

### Data Analysis
def Count(lis):
    c = 0
    for i in lis:
        if i:
            c+=1
    return c

def Mean(lis):
    m = 0
    try:
        lis2 = [float(l) for l in lis if l]
        for i in lis2:
            m += i
        m = m / len(lis2)
    except (TypeError, ValueError, ZeroDivisionError):
        m = 'Not numerical'
    return m

def Std(lis):
    n = len(lis)
    try:
        lis2 = [float(l) for l in lis if l] # remove empty strings + converts to floats (not necessary anymore)
        lis3 =  [(l - Mean(lis2))**2 for l in lis2]
        sd = sqrt(sum(lis3)/(n -1)) # unbiaised
    except (TypeError, ValueError):
        sd = 'Not numerical'
    return sd

def Quartile(lis, p):
    n = len(lis)
    try:
        lis2 = [float(l) for l in lis if l]
        lis2 = sorted(lis2)
        if p == 1:
            quart = lis2[-1] # if we want the max
        else:
            quart = lis2[int(n*p)]
    except (TypeError, ValueError):
        quart = 'Not numerical'
    return quart

class dataframe:
    def __init__(self, dataname):
        self.dataname = dataname

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Dataset you want to describe')
    parser.add_argument('set', type = str, help = 'Name of the file to read')
    args = parser.parse_args()
    feature_dico, feature_list = read_data(args.set)

    res = ['Feature', 'Count', 'Mean', 'Std', 'Min', '0.25%', '0.5%', 'O.75%', 'Max']
    print ('%s' % '\t'.join([str(x) for x in res]))

    for feature in feature_list:
        res = [feature]
        list_no_nas = [item for item in feature_dico[feature] if item]
        res.append(Count(list_no_nas))
        res.append(Mean(list_no_nas))
        res.append(Std(list_no_nas))
        for i in [0, 0.25, 0.5, 0.75, 1]:
            res.append(Quartile(list_no_nas, i))
        if res.count('Not numerical') < 3:
            print ('%s' % '\t'.join([str(x) for x in res]))
