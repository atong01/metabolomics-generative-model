function model = mk_modelC(unconfirmed)
%unconfirmed is a probability matrix with each row summing to 1. With n + 1
%columns representing the n metabolites in the concerned pathway and an
%extra non pathway metabolite.

%This model implements two additional features
%First, a single pathway in which all of the metabolites are connected to
%that pathway. Second, it removes the dependency that all unconfirmed are
%size M, so unconfirmed are dynamically sized, and therefore the
%conditional probability tables linking unconfirmed to virtual nodes are
%much more simplified. 

%ASSUMPTIONS:
%   The length of data size(data)(2) == metabolites + 1

default_data = [ 0.5 0.5 0 ];
if nargin < 1
    unconfirmed = default_data;
end
G = ~~unconfirmed; %bit array of non zero values


Npaths  = 1;
[Nunconf, Nmetas] = size(unconfirmed);


%     path, root, size of unconf, binary virtual/metas
ns = [2, 2, sum(G, 2), 2 * ones(1, Nmetas * 2)];

N = length(ns);
root    = 1;
path    = 2                           :Npaths + 1;
unconf  = Npaths + 2                  :Npaths + Nunconf + 1;
virtual = Npaths + Nunconf + 2        :Npaths + Nunconf + Nmetas + 1;
mets    = Npaths + Nunconf + Nmetas + 2:N;
assert(isequal([root, path, unconf, virtual, mets], 1:N))

%%%% SET INTRA/INTER
intra                            = zeros(N);        
intra(unconf, virtual)           = G;               %link unconf to non-zero v
intra(path, mets)                = 1;               %link path to all m
intra(virtual, virtual + Nmetas) = eye(Nmetas);     %link v_i to m_i
intra(root, unconf)              = 1;               %link root to unconf
inter                            = zeros(size(intra));
inter(mets, path)                = invert(G);


%%% SET ECLASSES
eclass1 = 1:N;
eclass2 = [1, N + 1, 3:N];

%%% MAKE DYNAMIC BAYESIAN NETWORK
%dbnet = mk_dbn(intra, inter, ns, 'discrete', 1:N, 'eclass1', eclass1, 'eclass2', eclass2);

dbnet = mk_dbn(intra, inter, ns, 'discrete', 1:N, 'observed', 1, 'eclass1', eclass1, 'eclass2', eclass2);
dbnet

%%% SET ROOT PRIOR
dbnet.CPD{1} = root_CPD(dbnet, 1);
%%% SET PATHWAY PRIOR
dbnet.CPD{2} = tabular_CPD(dbnet, 2, 'CPT', 'unif');
nps = length(parents(inter, 2));
dbnet.CPD{N+1} = tabular_CPD(dbnet, N + 2, mk_bpercent_table(nps));

%%% SET UNCONFIRMED PRIOR
for i=1:Nunconf
    class = i + Npaths + 1; %add 1 for root
    truth_t = unconfirmed(unconfirmed(i,1:end)~=0);
    dbnet.CPD{class} = tabular_CPD(dbnet, class, [1 - truth_t, truth_t]);
end

%%% SET VIRTUAL CPT
%Virtual node CPT is dependent on the number of parent unconfirmed
%construct table for virtual node i
%[1 0;
% ...
% 0 1; %line i
% 1 0];
for i=1:Nmetas %Nmetas == Nvirtual
    class = 1 + Npaths + Nunconf + i;
    table = mk_virtual_table(i, Nunconf, Nmetas);
    dbnet.CPD{class} = tabular_CPD(dbnet, class, table); % (pathways and unknowns)
end

%%% SET METABOLITE CPT
leak = ones(1, N);
inhibet = zeros(N, N);
for i=mets
    ps = parents(intra, i);
    class = i - mets(1) + 1 + 1 + 1 + Nunconf + Nmetas;
    dbnet.CPD{class} = noisyor_CPD(dbnet, i, 1, inhibet(ps, i - Npaths));
end

model = struct('bnet', dbnet, 'N', N, 'Npaths', Npaths, 'Nmets', Nmetas);
