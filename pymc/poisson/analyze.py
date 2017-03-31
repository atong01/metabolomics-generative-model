import operator
import read
import csv
from collections import defaultdict
data_path = '../data/'
hil_neg = data_path + 'HilNeg 0324 -- Data.csv'
hil_pos = data_path + 'HilPos 0324 -- Data.csv'
syn_neg = data_path + 'SynNeg 0324 -- Data.csv'

def get_metabolite_sets():
    """ Gets the sets of observed metabolites """
    path_dict   = read.get_model(data_path + 'model2.csv')
    pathways    = path_dict.keys()
    features    = read.get_metabolites(path_dict)
    cofactors   = read.get_cofactors(data_path + 'cofactors')
    paths = (hil_neg, hil_pos, syn_neg)
    metlin  = []
    hmdb    = []
    metfrag = []
    for path in paths:
        metlin.append(read.metlin(path))
        hmdb.append(read.hmdb(path))
        metfrag.append(set(read.metfrag_with_scores(path, keep_zero_scores = False).keys()))
    # remove non-features & cofactors
    for i in range(len(paths)):
        metlin[i] = (metlin[i] & features) - cofactors
        hmdb[i] = (hmdb[i] & features) - cofactors
        metfrag[i] = (metfrag[i] & features) - cofactors
    all = []
    for db in [metlin, hmdb, metfrag]:
        all.append(reduce(lambda x, y: x | y, db))
    return all

def summarize(pathway):
    path_dict   = read.get_model(data_path + 'model2.csv')
    pathways    = path_dict.keys()
    features    = read.get_metabolites(path_dict)
    cofactors   = read.get_cofactors(data_path + 'cofactors')
    paths = (hil_neg, hil_pos, syn_neg)
    metlin  = []
    hmdb    = []
    metfrag = []
    for path in paths:
        metlin.append(read.metlin(path))
        hmdb.append(read.hmdb(path))
        metfrag.append(set(read.metfrag_with_scores(path, keep_zero_scores = False).keys()))
    # remove non-features & cofactors
    for i in range(len(paths)):
        metlin[i] = (metlin[i] & features) - cofactors
        hmdb[i] = (hmdb[i] & features) - cofactors
        metfrag[i] = (metfrag[i] & features) - cofactors
    all = []
    for db in [metlin, hmdb, metfrag]:
        all.append(reduce(lambda x, y: x | y, db))
    def stats(pathway, metlin, hmdb, metfrag = set()):
        cge = path_dict[pathway]
        observed = ((metlin | hmdb | metfrag) & features) - cofactors
        reverse_path_dict = read.reverse_dict(path_dict)
        for compound in observed & cge:
            print (compound, len(reverse_path_dict[compound]))
    compounds = path_dict[pathway]
    #print ("Prob(C05381)", read.metfrag_with_scores(list(paths))['C05381'])
    print (pathway, len(compounds - cofactors))
    print ("Unobserved:")
    stats(pathway, compounds - cofactors, set())
    print ("Full Stats:")
    stats(pathway, all[0], all[1], all[2])
    print ("Hard Stats:")
    stats(pathway, all[0], all[1], set())
    return all

def summarize_compound(compound):
    path_dict   = read.get_model(data_path + 'model2.csv')
    reverse_path_dict = read.reverse_dict(path_dict)
    print ("Compound", compound, "has pathways:")
    for path in sorted(reverse_path_dict[compound]):
        print (path)


#POST ANALYZE
class Posterior():
    def __init__(self, path):
        self.cge = {}
        self.int = {}
        self.mets = {}
        MAPPING = {'p_' : self.cge, 'b' : self.int, 'g' : self.mets }
        with open(path, 'r') as f:
            reader = csv.reader(f)
            data = []
            for i, row in enumerate(reader):
                data.append([r.strip() for r in row])
            for row in data:
                for name, key in MAPPING.iteritems():
                    if row[0].startswith(name):
                        key[row[0]] = float(row[1 if name != 'b' else 2])
                        continue
    def compare_pathway_probs(self, other):
        diffs = {}
        for pathway, mean in self.cge.iteritems():
            other_mean = other.cge[pathway]
            diffs[pathway] = abs(mean - other_mean)
        sorted_diffs = sorted(diffs.items(), key=operator.itemgetter(1), reverse=True)
        for pathway, diff in sorted_diffs[:10]:
            print (pathway, self.cge[pathway], other.cge[pathway])
        return sorted_diffs

def list_range(l):
    return max(l) - min(l)

def construct_union(posteriors):
    all_paths = defaultdict(list)
    all_mets = defaultdict(list)
    for p in posteriors:
        for pathway, mean in p.cge.iteritems():
            all_paths[pathway].append(mean)
        for met, mean in p.mets.iteritems():
            all_mets[met].append(mean)
    return all_paths, all_mets

def dict_sort_by_value(d, reverse=False):
    return sorted(d.items(), key=operator.itemgetter(1), reverse=reverse)

def compare_pathway_probs(posteriors, threshold = 0.5):
    """ Takes a list of posterior objects and performs analysis on their pathway
        probabilities.
    """
    all_paths = construct_union(posteriors)[0]
    all_ranges = {k : list_range(l) for k,l in all_paths.iteritems()}
    top_ranges = dict_sort_by_value(all_ranges, reverse=True)
    print ("top ranges")
    to_return = []
    for p,r in top_ranges:
        if r > threshold:
            to_return.append((p, r))
            print (p, r)
    return all_paths, to_return

if __name__ == '__main__':
    #summarize('cge00524')
    #summarize('cge00010')
    summarize('cge00020')
    #summarize('cge01230')
    #summarize('cge00561')
    #summarize('cge00052')
    #summarize('cge00350')
    #p5 = Posterior('results/5.csv') 
    #p6 = Posterior('results/6.csv')
    #p5.compare_pathway_probs(p6)

    #summarize_compound('C00158')
    #summarize_compound('C00025')

