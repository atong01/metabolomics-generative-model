function table = mk_virtual_table(connection_i, sizes)
%connection_i is a vector of length p where p is the number of parents of
%node i. Each value corrosponds to the child number of the virtual node in
%question
%sizes is an array of the sizes of each parent unconfirmed node.

assert(length(connection_i) == length(sizes));

dims = length(connection_i);
trues = cell(dims);
for i=1:dims
    for j=1:dims
        if i == j
            trues{i,j} = connection_i(i);
        else
            trues{i,j} = 1:sizes(j);
        end
    end
end
if length(sizes) == 1
    table = zeros(1, sizes);
else
    table = zeros(sizes);
end

for i=1:dims
    table(trues{i,:}) = 1;
end
