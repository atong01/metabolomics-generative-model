Repositiory for metabolomics generative model


v1
==

First small test case 
* P = 3
* M = 3

Utilized pymc graphing features to graph marginal posterior for each RV.

v2
==

Test on real data HilNeg. Uses Metlin and HMDB data as hard evidence. If CXXXXX
appears as a match in the metlin or hmdb databases this is treated as a hard
match for this test.

This is a baseline test for the real data so that we can compare with using the 
additional information with metfrag data.

lambda  = 0.5 prior over all pathways
pi      = 0.1 prior probability on observing a metabolite

v3
==

Incorporates soft evidence



