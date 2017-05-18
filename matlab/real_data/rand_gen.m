[A, O, N] = import_observation_data('data.csv');
G = ones(1, length(A));
G = rand(100) > 0.9;
[Npath, Nmets] = size(G);
N = Npath + Nmets + Nmets;
path = 1:Npath;
mets = Npath+1:Npath+Nmets;
virt = Npath+Nmets+1:N;

dag = zeros(N,N);
dag(path,   mets) = G;
dag(mets,virt) = eye(Nmets);

ns = 2 * ones(1,N);
bnet = mk_bnet(dag, ns);

for i=path
    bnet.CPD{i} = tabular_CPD(bnet, i, [0.5 0.5]);
end
leak = ones(1, N);
inhibet = zeros(N, N);
for i=mets
    ps = parents(dag, i);
    bnet.CPD{i} = noisyor_CPD(bnet, i, leak(i), inhibet(ps, i - Npath));
end
'hello'
for i=virt
    j = i-virt(1)+1;
    %bnet.CPD{i} = tabular_CPD(bnet, i, 'CPT', 'unif');
    %t = A(j);
    t = rand();
    if t==0  % TERRRIBLE SMOOTHING
        t=0.001
    end
    bnet.CPD{i} = tabular_CPD(bnet, i, [1-t t 0.5 0.5]);
end

%engine = jtree_inf_engine(bnet);
%engine = pearl_inf_engine(bnet, 'max_iter', 30);
%engine = belprop_inf_engine(bnet);
engine = likelihood_weighting_inf_engine(bnet, 'nsamples', 100);
'engine made'

evidence = cell(1,N);
for i=virt(1:10)
    evidence{i} = 1;
end
[engine, ll] = enter_evidence(engine, evidence);
'evidence entered'
post = zeros(1, N);
for i=1:N
  m = marginal_nodes(engine, i);
  if (numel(m.T) == 2)
    post(i) = m.T(2);
  else
    post(i) = -1;
  end
end
post(path)

