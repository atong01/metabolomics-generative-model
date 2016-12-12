"""
meta.py

Produces venn diagram plots of the metadata. This is useful in visualizing the
structure of the data.

"""

from matplotlib import pyplot as plt
from matplotlib_venn import venn3
import read
data_path = '../data/'
observation_file = data_path + 'HilNeg 0324 -- Data.csv'
path_dict   = read.get_model(data_path + 'model2.csv')
pathways    = path_dict.keys()
features    = read.get_metabolites(path_dict)
metlin      = read.metlin(observation_file)
hmdb        = read.hmdb(observation_file)
cofactors   = read.get_cofactors(data_path + 'cofactors')
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
