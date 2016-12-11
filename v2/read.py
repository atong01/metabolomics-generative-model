"""
Provides helper functions for reading in data
"""
import numpy as np
import csv

def get_model(model_path, keep_full_path=False):
    with open(model_path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
        data = np.array([row for row in reader])
    path_dict = {}
    for line in data[1:]:
        path = line[0]
        if path not in path_dict:
            path_dict[path] = set()
        path_dict[path].update(line[5].split())
        path_dict[path].update(line[6].split())
    if not keep_full_path:
        del path_dict['cge01100']
    return path_dict

def get_column_set(path, col):
    """ Gets set of comma separated strings in column """
    to_return = set()
    data = []
    with open(path, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            data.extend([c.strip() for c in row[col].split(',')])
    for d in data[3:]:
        to_return.add(d)
    to_return.remove('')
    return to_return

def metlin(path):
    return get_column_set(path, 7)

def hmdb(path):
    return get_column_set(path, 5)

if __name__ == "__main__":
    data = 'HilNeg 0324 -- Data.csv'
    d = get_model('../data/model2.csv')
    for k,v in d.iteritems():
        print k, len(v)
