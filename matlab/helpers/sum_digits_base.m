function sum = sum_digits_base(n, base, digit)
switch nargin 
    case 1
        base = 2;
        digit = 1;
    case 2
        digit = 1;
end

if (n == 0)
    if digit == 0
        sum = 1;
    else
        sum = 0;
    end
else
    sum = sum_digits_base(floor(n / base), base, digit);
    last = mod(n,base);
    if last == digit
        sum = sum + 1;
    end
end