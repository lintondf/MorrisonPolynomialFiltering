function [ Sm ] = vrf_FMP_polynomial( i, j, The, s, tau )

display_pretty = 0;
if (nargin < 1)
    syms The s;
    i = 0; j = 2;
    display_pretty = 1;
end

ss = 1; % for 1step, ss=0; for current estimator 
    % calc row i, start at column j=i and stop at j=j (k)
Sm = 0;
for (k=i:j)
  Am = 0;
  F_1stepik = fmatrix(i,k,The,s,ss);
      % calc columm j, start at row j=i, stop at j=j (o)
  for (o=i:j)
      F_1stepio = fmatrix(i,o,The,s,ss);
      Am = Am + F_1stepik*A(k, o, The, s)*...
           F_1stepio;
  end
  Sm = Sm + Am;
end
Sm = (factorial(i)/tau^i)^2*Sm;

if (display_pretty)
    display(['']);
    display(['------------------------------']);
    display(['FMP VRF ' num2str(i) ...
             ' for degree: ' num2str(j)]);
    display(['------------------------------']);
    if(~isa(Sm,'double'))
        pretty(simple(Sm));
    else
        display(num2str(Sm));
    end
end
end

function [ aij ] = A(i, j, The, s)
    aij = factorial(i+j)/factorial(j)/factorial(i)*(1-The)...
        /(1+The)^(i+j+1);
end