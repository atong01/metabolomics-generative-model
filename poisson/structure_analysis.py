import networkx as nx
from  analyze import Posterior
import analyze
import read
import matplotlib.pyplot as plt

def get_path_dict():
    data_path = '../data/'
    return read.get_model(data_path + 'model2.csv')

def create_metabolite_graph(pathways):
    """ Plot pathway graph with metabolites that are observed """
    DG = nx.DiGraph()
    path_dict = get_path_dict()
    hard, soft = read.clean_sets()
    observed = hard | set(soft.keys())
    g = {}
    allmets = set()
    for p in pathways:
        g[p] = path_dict[p[2:]] & observed
        allmets |= g[p]
    DG.add_nodes_from(pathways)
    DG.add_nodes_from(allmets)
    for path, mets in g.iteritems():
        for m in mets:
            DG.add_edge(path, m)
    return DG, pathways, allmets
def find_common_mets(DG, allmets):
    degree2mets = set()
    degree2edges = set()
    for m in allmets:
        if DG.degree(m) > 1:
            degree2mets.add(m)
    for path, met in DG.edges():
        if met in degree2mets:
            degree2edges.add((path, met))
    degree2mets = list(degree2mets)
    degree2weights = [DG.degree(m) for m in degree2mets]
    top_mets = zip(degree2mets, degree2weights)
    return degree2mets, degree2edges, top_mets

def plot(DG, nodelist, edgelist):
    nx.draw_networkx(DG, with_labels = True, nodelist = nodelist, edgelist = edgelist)
    plt.show()


def plot_largest():
    p5 = Posterior('results/5.csv') 
    p6 = Posterior('results/6.csv')
    sorted_diffs = p5.compare_pathway_probs(p6)
    print sorted_diffs[:15]
    plot(zip(*sorted_diffs)[0][:15])

if __name__ == '__main__':
    posteriors = [Posterior('results/' + str(i) + '.csv') for i in range(5, 9)]
    analyze.compare_pathway_probs(posteriors)




