N = 2;
G = [0 1;
     0 0];
 
ns = 2 * ones(1,N);
bnet = mk_bnet(G, ns);
bnet.CPD{1} = tabular_CPD(bnet, 1, 'CPT', 'unif');
bnet.CPD{2} = tabular_CPD(bnet, 2, [0.1 0.9 0.5 0.5]);


engine = jtree_inf_engine(bnet);

evidence = cell(1,N);
evidence{2} = 1;
evidence
[engine, ll] = enter_evidence(engine, evidence);
post = zeros(1, N);
for i=1:N
  m = marginal_nodes(engine, i);
  m.T
  if (numel(m.T) == 2)
    post(i) = m.T(2);
  else
    post(i) = -1;
  end
end
marginal = post;