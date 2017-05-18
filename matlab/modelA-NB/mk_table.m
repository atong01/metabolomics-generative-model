function CPD = mk_table(ps, M, U, mets)
% generates the cpt table for a metabolite node given pathway parents in p,
% metabolite number m, # unconfirmed U, and #metabolites (size of U)
table = zeros((2 * ps) * (mets * U));
count = 1;
for u=1:U
    for i=1:mets
        for j=1:2
            if (i == M)
                table(count)= 0;
                table(count + 1) = 0;
                count = 2 + count;
            end
        end
    end
end

