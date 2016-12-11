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

"""
PLOTTING
"""
figure, axes = plt.subplots(2, 2)
venn3([features, metlin, hmdb], ('features', 'metlin', 'hmdb'), ax = axes[0][0])
venn3([features, cofactors, metlin | hmdb], ('features', 'cofactors', 'observed'), ax = axes[0][1])
venn3([cofactors, metlin, hmdb], ('cofactors', 'metlin', 'hmdb'), ax = axes[1][0])
plt.show()
