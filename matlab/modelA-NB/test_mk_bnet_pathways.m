G = [1 1 0;
     0 1 0;
     0 1 1];
unconfirmed = 1;
pathways = 3;
metabolites = 3;

bnet = mk_bnet_pathways(G, unconfirmed)
N = unconfirmed + pathways + 2 * metabolites;

evidence = cell(1,N);
soft_evidence = cell(1,N);
soft_evidence{4} = [0.3 0.7 0];
engine = jtree_inf_engine(bnet);
[engine, loglik] = enter_evidence(engine, evidence, 'soft', soft_evidence);
%displays likelyhood vector for each evaluation [1 -- false, 2 -- true]
%for i=1:N
%    marg = marginal_nodes(engine, i);
%    marg.T
%end
post = zeros(1, N);
for i=1:N
  m = marginal_nodes(engine, i);
  post(i) = m.T(2);
end
post;
pathways = post(1:pathways)
metabolites = post(end-metabolites + 1:end)