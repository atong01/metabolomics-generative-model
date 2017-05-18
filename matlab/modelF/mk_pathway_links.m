function G = mk_pathway_links(pathway_data, all_mets)
if nargin == 0
    pathway_data = import_pathways('pathways.csv');
    all_mets     = import_all_mets('all_mets.csv');
end
data = pathway_data(:,2);

P = length(data);
M = length(all_mets);
parsed = cell(1,length(data));
for i=1:length(data)
    parsed{i}=strread(data{i},'%s','delimiter',' ');
end
parsed;
ind = cell(1, length(data));
for i=1:length(data)
  for j=1:length(parsed{i})
      ind{i}(j) = find(strcmp(all_mets, parsed{i}{j}));
      
  end
end
G = zeros(P, M);
for i=1:P
    for j=1:length(parsed{i})
        G(i,ind{i}(j)) = 1;
    end
end
