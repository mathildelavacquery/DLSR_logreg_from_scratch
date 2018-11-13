import csv
import argparse
import math
from describe import Mean
from matrix_class import Matrix, read_data3
from logreg_train import preprocess, write_csv

def index_max(liste):
    m = 0
    index = 0
    for i in range(len(liste)):
        if liste[i] > m :
            m = liste[i]
            index = i
    return index

def predict(X, theta, house_dico):
    result_all = Matrix(X.dot(theta))
    result = Matrix([[1/float(1+math.exp(-z)) for z in row] for row in result_all]) # We need to apply dot by dot in the matrix

    # Selecting the best house
    col_result = Matrix([[0] for i in range(X.nrow)])
    for i in range(result.nrow):
        col_result[i][0] = house_dico[index_max(result[i])]
    return col_result

def return_predict(X, res):
    X_test = read_data3(X)
    for i in range(X_test.nrow - 1):
        X_test[i+1][1] = res[i][0]
    return X_test

def assess_result(Y, res, house_dico):
    true_pred = 0
    Y_true_col = Matrix([[0] for i in range(Y.nrow)])
    for i in range(Y.nrow):
        Y_true_col[i][0] = house_dico[index_max(Y[i])]
        if res[i][0] == Y_true_col[i][0]:
            true_pred += 1
    Y_train_res = Y_true_col.append_col(res.to_list())
    accuracy = float(true_pred) / float(Y.nrow)
    write_csv(Matrix(Y_train_res), ['Y_true', 'Y_pred'], 'result_train')
    return accuracy

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Dataset you want to describe')
    parser.add_argument('set', type = str, help = 'Name of the file to read')
    parser.add_argument('theta', type = str, help = 'Weights of the features')
    parser.add_argument('count', type = str, nargs = '?', help = 'If you want to assess your prediction of train set', default =  'False')
    args = parser.parse_args()

    X, Y, features, y_name = preprocess(args.set)
    all_theta = read_data3(args.theta)

    houses = all_theta[0]
    houses = [h.split('_')[1] for h in houses]
    house_dico = dict((i, houses[i]) for i in range(len(houses)))
    all_theta = Matrix(all_theta[1:]).to_float()

    res = predict(X, all_theta, house_dico)
    if args.count == 'True':
        accuracy = assess_result(Y, res, house_dico)
        print (accuracy)
    else:
        X_test = return_predict(args.set, res)
        write_csv(Matrix(X_test[1:]), X_test[0], 'result_test')
