function indices = get_child_indicies(G, i)
%finds the child index of each parent of node I in DAG g
ps = parents(G, i);
indices = zeros(1,length(ps));
for j=1:length(ps)
    p = ps(j);
    p_children = find(G(p,:));
    indices(j) = find(p_children == i);
end