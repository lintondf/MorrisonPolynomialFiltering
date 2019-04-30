function [ dipjs ] = fmatrix( i, j, The, s , ss )
% Generates the i^th degree (col) j^th element (row)
% for the leguerre solution matrix. Note, The and s
% passed for uniqueness.

display_pretty = 0;
if (nargin < 5)
    ss = -1; % for 1step, ss=0; for current estimator 
end

if (nargin < 1)
    syms The s;
    i = 4; 
    j = 4;
    display_pretty = 1;
end

pij = ((-1)^i)*laguerre_polynomial(j, The, s);
if ((i>0) &&(~isa(pij,'double')))
    dipj = diff(pij,'s',i);
else if (i>0)
        dipj = 0;
    else
        dipj = pij;
    end
end
dipjs = dipj/factorial(i);
dipjs = subs(dipjs,{s},{ss},0);


if (display_pretty)
    display(['']);
    display(['------------------------------']);
    display(['F Matrix (' num2str(i) ', ' ...
                          num2str(j) ' )']);
    display(['------------------------------']);
    if(~isa(dipjs,'double'))
        pretty(simple(dipjs));
    else
        display(num2str(dipjs));
    end
end

end


