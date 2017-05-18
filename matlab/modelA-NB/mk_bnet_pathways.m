function modelA = mk_bnet_pathways(G, Nunconfirmed)
% MK_QMR_BNET Make a QMR model
% bnet = mk_qmr_bnet(G, inhibit, leak, prior)
%
% G(i,j) = 1 iff there is an arc from disease i to finding j G must be
% pathways by metabolites
% inhibit(i,j) = inhibition probability on i->j arc
% leak(j) = inhibition prob. on leak->j arc
% prior(i) = prob. disease i is on
% tabular_findings = 1 means multinomial leaves (ignores leak/inhibit params)
%   = 0 means noisy-OR leaves (default = 0)
[Npathways, Nmetabolites] = size(G);
N = Npathways + 2 * Nmetabolites + Nunconfirmed;
path = 1:Npathways;
unconf =  Npathways + 1:Npathways + Nunconfirmed;
virtual = Npathways + Nunconfirmed + 1:Npathways + Nunconfirmed + Nmetabolites;
mets = Npathways + Nunconfirmed + Nmetabolites + 1:N;

dag = zeros(N,N);
dag(path,   mets) = G;
dag(unconf, virtual) = 1;
for i=virtual
    dag(i, i + Nmetabolites) = 1;
end

ns = 2*ones(1,N);
ns(unconf) = Nmetabolites;

for i=path
    names{i} = ['p' num2str(i)];
end
for i=unconf
    names{i} = ['u' num2str(i)];
end
for i=virtual
    names{i} = ['v' num2str(i)];
end
for i=mets
    names{i} = ['m' num2str(i)];
end

bnet = mk_bnet(dag, ns, 'names', names, 'observed', unconf);

%set pathway probs and generate names
for i=path
    bnet.CPD{i} = tabular_CPD(bnet, i, [0.5 0.5]);
end

%set unconfirmed initial probs
for i=unconf
    bnet.CPD{i} = tabular_CPD(bnet, i, ones(1, Nmetabolites) / Nmetabolites);
end

dims = Nmetabolites * ones(1,Nunconfirmed);
%NOTE ONLY WORKS FOR SINGLE UNCONFIRMED
if (Nunconfirmed ~= 1)
    'ERROR ERROR ERROR unconfirmed not 1'
end
for i=virtual
    m = i - virtual(1) + 1;
    %construct table for virtual node i
    %[1 0;
    % ...
    % 0 1; %line i
    % 1 0];
    
    for j=1:Nmetabolites
        for k=1:2
            if (m == j)
                table(j,k) = mod(k + 1,2);
            else
                table(j,k) = mod(k,2);
            end
        end
    end
    bnet.CPD{i} = tabular_CPD(bnet, i, table);
end
leak = ones(1, N);
inhibet = zeros(N, N);
for i=mets
    ps = parents(dag, i);
    bnet.CPD{i} = noisyor_CPD(bnet, i, leak(i), inhibet(ps, i - Npathways));
end

modelA = struct('bnet', bnet,                     ...
                'N'   , N,                        ...
                'Npaths',      Npathways,         ...
                'Nmets',       Nmetabolites,      ... 
                'Unconfirmed', unconf,            ...
                'Metabolites', mets,              ...
                'Pathways'   , path);
