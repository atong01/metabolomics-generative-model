README
=====

analyze.py
    Used for more closely examining portions of the dataset. For example, I want
    to know the # of compounds with evidence for pathway PXXXXX that are observed
    vs. not observed and how many pathways they are members of.
main.py
    Runs sampling on the model

meta.py
    Creates venn diagrams on the metadata showing the structure of the data.

model.py
    Bayesian model specification using pymc.

gen.py
    Creates sample / test data to use in the model.

read.py
    Provides helper functions to read in data.

