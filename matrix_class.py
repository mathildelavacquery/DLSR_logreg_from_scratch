import csv
import argparse
import math
from describe import Mean


class Matrix(list):
    def __init__(self, mat):
        super(Matrix, self).__init__(mat)

    @property
    def nrow(self):
        return len(self)

    @property
    def ncol(self):
        return len(self[0])

    def product(self,scalar):
        return Matrix([[row[i]*scalar for i in range(self.ncol)] for row in self])

    def Exp(self):
        return Matrix([[math.exp(row[i]) for i in range(self.ncol)] for row in self])

    def dot(self,mat2):
        if self.ncol == mat2.nrow:
            mat = [[0]*mat2.ncol for i in range(self.nrow)]
            for i in range(self.nrow):
                for j in range(mat2.ncol):
                    mat[i][j] = sum([self[i][k]*mat2[k][j] for k in range(self.ncol)])
        else:
            raise TypeError('The matrix are not compatible for multiplication')
        return Matrix(mat)

    def add(self, mat2):
        if (self.ncol == mat2.ncol) and (self.nrow == mat2.nrow):
            mat = [[0]*self.ncol for i in range(self.nrow)]
            for i in range(self.nrow):
                for j in range(mat2.ncol):
                    mat[i][j] = self[i][j] + mat2[i][j]
        else:
            raise TypeError('The matrix dont have the same size')
        return Matrix(mat)

    def sub(self, mat2):
        if (self.ncol == mat2.ncol) and (self.nrow == mat2.nrow):
            mat = [[0]*self.ncol for i in range(self.nrow)]
            for i in range(self.nrow):
                for j in range(mat2.ncol):
                    mat[i][j] = self[i][j] - mat2[i][j]
        else:
            raise TypeError('The matrix dont have the same size')
        return Matrix(mat)

    def transpose(self):
        return Matrix([[row[i] for row in self] for i in range(self.ncol)])

    def show(self):
        for row in self:
            print ('%s' % '\t'.join([str(x) for x in row]))

    def append_col(self, col): # col should be a list here
        if self.nrow == len(col):
            for i in range(self.nrow):
                self[i].append(col[i])
        else:
            raise TypeError('Cannot append column of different size')
        return Matrix(self)

    def col(self,i):
        return Matrix([[row[i]] for row in self])

    def row(self,i):
        return Matrix([self[i]])

    def drop(self, k_list, axis):
        if axis == 0: # rows
            mat = Matrix([self[i] for i in [k for k in range(self.nrow) if k not in k_list]])
        elif axis == 1: # columns
            mat = Matrix([[row[i] for i in [k for k in range(self.ncol) if k not in k_list]] for row in self])
        return mat

    def to_float(self):
        return Matrix([[float(row[i]) if row[i].replace('-','',1).replace('.', '',1).isdigit() else row[i] for i in range(self.ncol)] for row in self])

    def unique(self, i, axis):
        unique_values = []
        if axis == 0:
            for k in range(self.ncol):
                if self[i][k] not in unique_values:
                    unique_values.append(self[i][k])
        elif axis == 1:
            for k in range(self.nrow):
                if self[k][i] not in unique_values:
                    unique_values.append(self[k][i])
        return unique_values

    def count_null(self):
        null_dico = dict((k, 0) for k in range(self.ncol))
        for i in range(self.ncol):
            for j in range(self.nrow):
                if self[j][i] == '':
                    null_dico[i] +=1
        return null_dico


    def standardize(self):
        mat = [[0]*self.ncol for i in range(self.nrow)]
        for j in range(self.ncol):
            mean_col = Mean([row[j] for row in self])
            std_col = math.sqrt(sum([(row[j] - mean_col)**2 for row in self])/float(self.nrow -1))
            for i in range(self.nrow):
                mat[i][j] = (self[i][j] - mean_col)/ float(std_col)
        return Matrix(mat)

    def to_list(self):
        return list([item for sublist in self for item in sublist])


def read_data3(dataname):
    with open('../data/' + dataname) as f:
        return Matrix([line.strip().split(',') for line in f])
