function vrf_diag_fmp()

clear all;
clc;
syms The s tau;
for (j=0:5)
    display([' ']);
    display(['---------------------------------------']);
    display(['Fading Memory VRF for degree : ' num2str(j )]);
    display(['---------------------------------------']);
    for (i=j:-1:0)
        pj = vrf_FMP_polynomial(i,j,The,s,tau);
        if(~isa(pj,'double'))
            pretty(simple(pj));
        else
            display(num2str(pj));
        end
    end
end
end

function [ Sm ] = vrf_FMP_polynomial( i, j, The, s, tau )

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
end

function [ aij ] = A(i, j, The, s)
    aij = factorial(i+j)/factorial(j)/factorial(i)*(1-The)...
        /(1+The)^(i+j+1);
end