Npaths = 1;
Nmets  = 5;
N = Npaths + Nmets;
findings = Npaths+1:N;
G = ones(Npaths, Nmets);
G = [1 1 1;
     0 1 0;
     0 0 1];
G = ones(Npaths, Nmets);
leak = 0.9 * ones(1, N);
inhibit = 0.5 * ones(Npaths, Nmets); %%%% WHY DOES 0 NOT WORK

prior = 0.25 * ones(1, Npaths);
tabular_leaves = 0;
obs_nodes = findings;

bnet = mk_qmr_bnet(G, inhibit, leak, prior, tabular_leaves, obs_nodes);

evidence = cell(1,N);
%evidence{4} = 2
soft_evidence = cell(1,N);
observations  = [0.5 0.5 0.5, 1, 1];
observations  = rand(1, Nmets);
for i=1:Nmets
    j = findings(i);
    r = observations(i);
    soft_evidence{j} = [1 - r, r];
end
stages = cell(1,N);
for i=1:N
    stages{i} = N + 1 - i;
end
soft_evidence;
engine = jtree_inf_engine(bnet, 'stages', stages, 'maximize', 4);
[engine, loglik] = enter_evidence(engine, evidence, 'soft', soft_evidence);
post = zeros(1, N);
[mpe, ll] = calc_mpe(engine, evidence); 
mpe
for i=1:N
  m = marginal_nodes(engine, i);
  m.T;
  if (numel(m.T) == 2)
    post(i) = m.T(2);
  else
    post(i) = -1;
  end
end
path = post(1:Npaths)
mets = post(Npaths+1:end)