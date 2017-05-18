function sizes = get_parent_sizes(G, i)
%finds the child index of each parent of node I in DAG g
ps = parents(G, i);
sizes = zeros(1,length(ps));
for j=1:length(ps)
    p = ps(j);
    p_children = find(G(p,:));
    sizes(j) = length(p_children);
end