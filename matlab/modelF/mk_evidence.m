function ev = mk_evidence()
[comp, prob] = import_evidence('ev.csv');
all_mets     = import_all_mets('all_mets.csv');
ev = zeros(length(comp),2);
for i=1:length(comp)
    ev(i,1) = find(strcmp(all_mets,comp(i)));
    ev(i,2) = prob(i);
end