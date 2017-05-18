function modelB = mk_modelB(G, Nunconfirmed)
[Npathways, Nmetabolites] = size(G);
modelA = mk_modelA(G, Nunconfirmed);
[Npathways, Nmetabolites] = size(G);
N = Npathways + 2 * Nmetabolites + Nunconfirmed;
path = 1:Npathways;
unconf =  Npathways + 1:Npathways + Nunconfirmed;
virtual = Npathways + Nunconfirmed + 1:Npathways + Nunconfirmed + Nmetabolites;
mets = Npathways + Nunconfirmed + Nmetabolites + 1:N;

ns = 2*ones(1,N);
ns(unconf) = Nmetabolites;
intra = modelA.bnet.dag; % connections within a time slice i.e. modelA

%connections between time slices, i.e. mets(t) -> parent_pathways(t+1)
inter = zeros(size(intra));
for i=modelA.Metabolites
    for j=modelA.Pathways
        inter(i,j) = 1;
    end
end
%flip all connections from P(t) --> M(t) to M(t) --> P(t + 1)
Gp = invert(G);
inter(modelA.Metabolites, modelA.Pathways) = Gp;


Op_class = ones(1, Npathways);
O_class  = 2:N - Npathways + 1;
initial_p_class = O_class(end) + 1;
p_class = initial_p_class: initial_p_class + Npathways - 1;
%TODO hardcoded need to change
%Do equivalence classes need to have the same parents?
%eclass1 = [1 1 1 2 3 4 5 6 7 8]; %class of node(i) in slice 1
%eclass2 = [9 10 11 2 3 4 5 6 7 8]; %class of node(i) in slice 2:N
eclass1 = [Op_class, O_class];
eclass2 = [p_class, O_class];
%dbnet = mk_dbn(intra, inter, ns, 'discrete', 1:modelA.N);
dbnet = mk_dbn(intra, inter, ns, 'discrete', 1:modelA.N, 'observed', unconf, 'eclass1', eclass1, 'eclass2', eclass2);
dbnet.CPD{1} = tabular_CPD(dbnet, 1, 'CPT', 'unif');
dbnet.CPD{2} = tabular_CPD(dbnet, 4, 'CPT', 'unif');

virtual = Npathways + Nunconfirmed + 1:Npathways + Nunconfirmed + Nmetabolites;

for i=virtual
    m = i - virtual(1) + 1;
    %construct table for virtual node i
    %[1 0;
    % ...
    % 0 1; %line i
    % 1 0];
    table = mk_virtual_table(m, Nunconfirmed, Nmetabolites);
    dbnet.CPD{m + 1 + Nunconfirmed} = tabular_CPD(dbnet, i, table); % (pathways and unknowns)
end
inhibet = zeros(N, N);

for i=mets
    ps = parents(modelA.bnet.dag, i);
    class = i - mets(1) + 1 + 1 + Nunconfirmed + Nmetabolites;
    dbnet.CPD{class} = noisyor_CPD(dbnet, i, 1, inhibet(ps, i - Npathways));
end

for i=1:Npathways
    nps = length(parents(inter, i));
    class = i - Npathways + N + 1;
    % do a little math awkward but should do. percentage of metabolites is
    % percentage likelyhood that pathway is on.
    dbnet.CPD{class} = tabular_CPD(dbnet, N + i, mk_bpercent_table(nps));
end
modelB = struct('bnet', dbnet,                                ...
                'N'   , modelA.N,                             ...
                'Npaths',      modelA.Npaths,                 ...
                'Nmets',       modelA.Nmets,                  ... 
                'Unconfirmed', modelA.Unconfirmed,            ...
                'Metabolites', modelA.Metabolites,            ...
                'Pathways'   , modelA.Pathways);
