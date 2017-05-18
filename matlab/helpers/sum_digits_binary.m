function sum = sum_digits_binary(n)

if (n == 0)
    sum = 0;
else
    sum = sum_digits_binary(floor(n / 2)) + mod(n,2);
end