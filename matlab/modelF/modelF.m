function model = modelF(pm, ev)
% model {P,M,E}
% P  = | {pathways} |
% M  = | {kegg mets of paths} |
% E  = | {hard observed} OR {soft observed} |
% pm = list of KEGG IDs for each pathway
% ev = map: evidence -> probability

if nargin == 0
    pm = mk_pathway_links();
    ev = mk_evidence();
end

[Npath, Nmets] = size(pm);
Nev = length(ev);
N = Npath + Nmets + Nev;
path = 1:Npath;
mets = Npath+1:Npath+Nmets;
virt = Npath+Nmets+1:N;
dag = zeros(N,N);
dag(path,   mets) = pm;
sparse(dag(:,87))
length(find(dag(:,87)))
for i=1:length(ev)
    dag(Npath + ev(i,1), Npath+Nmets+i) = 1;
end

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
for i=virt
    j = i-virt(1)+1;
    %bnet.CPD{i} = tabular_CPD(bnet, i, 'CPT', 'unif');
    %t = A(j);
    t = ev(j,2);
    if t==0
        t=0.01
    end
    bnet.CPD{i} = tabular_CPD(bnet, i, [1-t t 0.5 0.5]);
end

engine = likelihood_weighting_inf_engine(bnet, 'nsamples', 100);
'engine made'
bnet
evidence = cell(1,N);
for i=virt
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