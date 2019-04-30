function [ dipjs ] = pmatrix( i, j, n, s, ss )
% Generates the i^th degree (col) j^th element (row)
% for the legendre solution matrix. Note, n and s
% passed for uniqueness.

display_pretty = 0;
if (nargin < 5)
    ss = n+1; % for 1step, ss=n; for current estimator 
end

if (nargin < 1)
    syms s n;
    i = 4; 
    j = 4;
    ss = n;
    display_pretty = 1;
end

pij = legendre_polynomial(j, n, s);
if ((i>0) &&(~isa(pij,'double')))
    dipj = 1/factorial(i)*diff(pij,'s',i);
else if (i>0)
        dipj = 0;
    else
        dipj = 1/factorial(i)*pij;
    end
end
dipjs = subs(dipj,s,ss,0);


if (display_pretty)
    display(['']);
    display(['------------------------------']);
    display(['P Matrix (' num2str(i) ', ' ...
                          num2str(j) ' )']);
    display(['------------------------------']);
    if(~isa(dipjs,'double'))
        pretty(simple(dipjs));
    else
        display(num2str(dipjs));
    end
end

end

