"""
meta.py

Produces venn diagram plots of the metadata. This is useful in visualizing the
structure of the data.

"""

from matplotlib import pyplot as plt
from matplotlib_venn import venn3
import read

data_path = '../data/'
hil_neg = data_path + 'HilNeg 0324 -- Data.csv'
hil_pos = data_path + 'HilPos 0324 -- Data.csv'
syn_neg = data_path + 'SynNeg 0324 -- Data.csv'
path_dict   = read.get_model(data_path + 'model2.csv')
pathways    = path_dict.keys()
features    = read.get_metabolites(path_dict)
cofactors   = read.get_cofactors(data_path + 'cofactors')

def plot_hil_neg():
    observation_file = hil_neg
    metlin      = read.metlin(observation_file)
    hmdb        = read.hmdb(observation_file)
    metfrag     = set(read.metfrag_with_scores(observation_file).keys())
    metfrag_no_zeros = set(read.metfrag_with_scores(observation_file, keep_zero_scores = False).keys())
    feature_compounds = set([f for f in features if str.startswith(f, 'C')])

    """
    PLOTTING
    """
    figure, axes = plt.subplots(2, 3)
    venn3([features, metlin, hmdb], ('features', 'metlin', 'hmdb'), ax = axes[0][0])
    venn3([features, cofactors, metlin | hmdb], ('features', 'cofactors', 'observed'), ax = axes[0][1])
    venn3([cofactors, metlin, hmdb], ('cofactors', 'metlin', 'hmdb'), ax = axes[0][2])
    venn3([metfrag_no_zeros, cofactors, features], ('metfrag_no_zeros', 'cofactors', 'features'), ax = axes[1][0])
    venn3([metfrag - cofactors, (metlin | hmdb) - cofactors, features - cofactors], ('metfrag_with_zeros', 'observed', 'features'), ax = axes[1][1])
    venn3([metfrag_no_zeros - cofactors, (metlin | hmdb) - cofactors, features - cofactors], ('metfrag', 'observed', 'features'), ax = axes[1][2])

    axes[0][0].set_title('hard_evidence')
    axes[0][1].set_title('hard evidence cofactor analysis vs features')
    axes[0][2].set_title('hard evidence cofactor analysis')
    axes[1][0].set_title('metfrag cofactor analysis')
    axes[1][1].set_title('metfrag with zero scores (exclude cofactors)')
    axes[1][2].set_title('metfrag without zero scores (exclude cofactors)')

    plt.show()

def cge20(metlin, hmdb, metfrag):
    cge20 = path_dict['cge00020']
    observed = ((metlin | hmdb | metfrag) & features) - cofactors
    reverse_path_dict = read.reverse_dict(path_dict)
    print observed & cge20
    for compound in observed & cge20:
        print compound, len(reverse_path_dict[compound])
def plot_all():
    paths = (hil_neg, hil_pos, syn_neg)
    metlin  = []
    hmdb    = []
    metfrag = []
    for path in paths:
        metlin.append(read.metlin(path))
        hmdb.append(read.hmdb(path))
        metfrag.append(set(read.metfrag_with_scores(path, keep_zero_scores = False).keys()))
    # remove non-features & cofactors
    if False:
        for i in range(len(paths)):
            metlin[i] = (metlin[i] & features) - cofactors
            hmdb[i] = (hmdb[i] & features) - cofactors
            metfrag[i] = (metfrag[i] & features) - cofactors

    all = []
    for db in [metlin, hmdb, metfrag]:
        all.append(reduce(lambda x, y: x | y, db))
    cge20(*all)
    """
    figure, axes = plt.subplots(2, 3)
    venn3(all, ('metlin', 'hmdb', 'metfrag'), ax = axes[0][0])
    venn3((all[0] | all[1], all[2], features), ('observed', 'metfrag', 'features'), ax = axes[0][1])


    venn3(metlin, ('hilneg', 'hilpos', 'synneg'), ax = axes[1][0])
    venn3(hmdb, ('hilneg', 'hilpos', 'synneg'), ax = axes[1][1])
    venn3(metfrag, ('hilneg', 'hilpos', 'synneg'), ax = axes[1][2])
    axes[0][0].set_title('All')
    axes[1][0].set_title('Metlin')
    axes[1][1].set_title('HMDB')
    axes[1][2].set_title('MetFrag')
    """
    venn3((all[0] | all[1], all[2], features), ('observed', 'metfrag', 'KEGG'))

    plt.show()

if __name__ == '__main__':
    plot_all()
