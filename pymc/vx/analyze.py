import read
import csv
data_path = '../data/'
hil_neg = data_path + 'HilNeg 0324 -- Data.csv'
hil_pos = data_path + 'HilPos 0324 -- Data.csv'
syn_neg = data_path + 'SynNeg 0324 -- Data.csv'

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
            print compound, len(reverse_path_dict[compound])
    compounds = path_dict[pathway]
    print "Prob(C05381)", read.metfrag_with_scores(list(paths))['C05381']
    print pathway, len(compounds - cofactors)
    print "Unobserved:"
    stats(pathway, compounds - cofactors, set())
    print "Full Stats:"
    stats(pathway, all[0], all[1], all[2])
    print "Hard Stats:"
    stats(pathway, all[0], all[1], set())

def summarize_compound(compound):
    path_dict   = read.get_model(data_path + 'model2.csv')
    reverse_path_dict = read.reverse_dict(path_dict)
    print "Compound", compound, "has pathways:", reverse_path_dict[compound]


#POST ANALYZE
class Posterior():
    def __init__(self, path):
        self.cge = []
        with open(path, 'rb') as f:
            reader = csv.reader(f)
            data = []
            for i, row in enumerate(reader):
                data.append([r.strip() for r in row])
            for row in data:
                if row[0].startswith('cge'):
                    self.cge.append(row)
        for row in self.cge:
            print row[0], row[1]

if __name__ == '__main__':
    #summarize('cge00524')
    #summarize('cge00020')
    summarize('cge01230')
    #Posterior('quick/0.csv')
    #summarize_compound('C00158')
