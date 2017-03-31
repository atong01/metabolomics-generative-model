"""
Provides helper functions for reading in data
"""
import numpy as np
import csv
from collections import defaultdict

def get_model(model_path, keep_full_path=False, cofactors = set()):
    """ returns (dict) pathway : set(compounds) """
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
    if type(path) == list:
        return reduce(lambda x, y: x | y, [get_column_set(p, col) for p in path])
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

def or_scores(scores):
    to_return = defaultdict(float)
    for c, score_list in scores.iteritems():
        tot = 1
        for s in score_list:
            tot *= (1 - float(s))
        to_return[c] = 1 - tot
    return to_return

def metfrag_with_scores(path, keep_zero_scores = True):
    """
        Returns dict: Compound --> Score
        Score is calculated as 1 - prod(1 - p) for p in scores
    """
    scores = defaultdict(list)
    to_return = defaultdict(float)
    if type(path) == list:
        dicts = [metfrag_with_scores(p, keep_zero_scores) for p in path]
        for d in dicts:
            for k, v in d.iteritems():
                scores[k].append(v)
        return or_scores(scores)
    with open(path, 'rb') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i < 3:
                continue
            for c, score in zip(*(row[9].split(','), row[10].split(','))):
                scores[c].append(score.strip())
        del scores['']
    to_return = or_scores(scores)

    if not keep_zero_scores:
        to_return = dict((k,v) for k, v in to_return.iteritems() if v != 0)
    return to_return

def clean_sets():
    """ Gets cleaned sets of evidence and metfrag """
    data_path = '../data/'
    observation_file = data_path + 'HilNeg 0324 -- Data.csv'
    cofactors = get_cofactors(data_path + 'cofactors')
    path_dict = get_model(data_path + 'model2.csv', cofactors = cofactors)
    pathways = path_dict.keys()
    features = get_metabolites(path_dict)
    evidence = metlin(observation_file)
    evidence |= hmdb(observation_file)
    evidence -= cofactors
    features -= cofactors
    evidence &= features
    reverse_path_dict = reverse_dict(path_dict)
    mf = metfrag(observation_file)
    metfrag_evidence = dict_of_set(metfrag_with_scores(observation_file, keep_zero_scores = False), mf & features - cofactors - evidence)
    return evidence, metfrag_evidence

def get_all_sets():
    data_path = '../data/'
    observation_file = data_path + 'HilNeg 0324 -- Data.csv'
    cofactors = get_cofactors(data_path + 'cofactors')
    path_dict = get_model(data_path + 'model2.csv', cofactors = cofactors)
    pathways = path_dict.keys()
    features = get_metabolites(path_dict)
    evidence = metlin(observation_file)
    evidence |= hmdb(observation_file)
    evidence -= cofactors
    features -= cofactors
    evidence &= features
    reverse_path_dict = reverse_dict(path_dict)
    mf = metfrag(observation_file)
    metfrag_evidence = dict_of_set(metfrag_with_scores(observation_file, keep_zero_scores = False), mf & features - cofactors - evidence)
    evidence = {e : 1 for e in evidence}
    return pathways, features, path_dict, reverse_path_dict, evidence, metfrag_evidence

def dict_of_set(d, s):
    """ Returns a dict with keys in set """
    return dict((k,v) for k, v in d.iteritems() if k in s)

if __name__ == "__main__":
    data = '../data/HilNeg 0324 -- Data.csv'
    d = get_model('../data/model2.csv')
    mets = get_metabolites(d)
    #print len(metfrag_with_scores(data))
    #print len(metfrag_with_scores(data, keep_zero_scores = False))
    #print sorted(list((hmdb(data) | metlin(data)) & mets))
