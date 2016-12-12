"""
Provides helper functions for reading in data
"""
import numpy as np
import csv
from collections import defaultdict

def get_model(model_path, keep_full_path=False, cofactors = set()):
    with open(model_path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
        data = np.array([row for row in reader])
    path_dict = defaultdict(set)
    for line in data[1:]:
        path = line[0]
        compounds = set(line[5].split()).union(set(line[6].split()))
        compounds -= cofactors
        path_dict[path].update(compounds)
    if not keep_full_path:
        del path_dict['cge01100']
    return path_dict

def reverse_dict(d):
    to_return = defaultdict(list)
    for k, v in d.iteritems():
        for c in v:
            to_return[c].append(k)
    return to_return

def get_metabolites(path_dict):
    mets = set()
    for p in path_dict.values():
        mets |= p
    return mets

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

def get_cofactors(path):
    with open(path, 'rb') as cof_file:
        reader = csv.reader(cof_file)
        cofactors = set(["C" + row[0].zfill(5) for row in reader])
    return cofactors

hmdb    = lambda path: get_column_set(path, 5)
metlin  = lambda path: get_column_set(path, 7)
metfrag = lambda path: get_column_set(path, 9)

def metfrag_with_scores(path, keep_zero_scores = True):
    """
        Returns dict: Compound --> Score
        Score is calculated as 1 - prod(1 - p) for p in scores
    """
    scores = defaultdict(list)
    to_return = defaultdict(float)
    with open(path, 'rb') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i < 3:
                continue
            for c, score in zip(*(row[9].split(','), row[10].split(','))):
                scores[c].append(score.strip())
        del scores['']
    for c, score_list in scores.iteritems():
        tot = 1
        for s in score_list:
            tot *= (1 - float(s))
        to_return[c] = 1 - tot

    if not keep_zero_scores:
        to_return = dict((k,v) for k, v in to_return.iteritems() if v != 0)
    return to_return


if __name__ == "__main__":
    data = '../data/HilNeg 0324 -- Data.csv'
    d = get_model('../data/model2.csv')
    mets = get_metabolites(d)
    print len(metfrag_with_scores(data))
    print len(metfrag_with_scores(data, keep_zero_scores = False))
    #print sorted(list((hmdb(data) | metlin(data)) & mets))
