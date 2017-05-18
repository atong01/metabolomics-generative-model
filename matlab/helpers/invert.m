function Gp = invert(G)
%Given an adjacency matrix G, flips all the connections
[I, J] = size(G);
Gp = zeros(J, I);
for i=1:I
    for j=1:J
        Gp(j,i) = G(i,j);
    end
end

        