function [ Sm ] = vrf_EMP_polynomial( i, j, n, s, tau )

display_pretty = 0;
if (nargin < 1)
    syms n s tau;
    i = 0;  j = 2; 
    display_pretty = 1;
end

ss = n+1; % for 1step, ss=n; for current estimator 
Sm = pmatrix(i, 0, n, s, ss)^2/legendre_norm(0, n, s);
for (k=1:j)
   Sm = Sm + pmatrix(i, k, n, s, ss)^2/legendre_norm(k, n, s);
end
Sm = (factorial(i)/tau^i)^2*Sm;
   
if (display_pretty)
    display(['']);
    display(['------------------------------']);
    display(['EMP VRF ' num2str(i) ...
             ' for degree: ' num2str(j)]);
    display(['------------------------------']);
    if(~isa(Sm,'double'))
        pretty(simple(Sm));
    else
        display(num2str(Sm));
    end
end

end
