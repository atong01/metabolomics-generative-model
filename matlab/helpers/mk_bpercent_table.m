function table = mk_bpercent_table(Nparents, base)

% series [0 1 1 2 1 2 2 3 1 2 2 3 2 3 3 4 ...
%         1 2 3 4 5 6 7 8

if nargin < 2
    base = 2;
end
series = zeros(1, base ^ Nparents);
for i=1:base^Nparents
    series(i) = sum_digits_base(i - 1, base); 
end
table = [1 - (series / Nparents), series / Nparents];