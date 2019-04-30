function vrf_diag_emp()

clear all; close all
clc;
syms n s tau;

for (j=0:5)
    display([' ']);
    display(['---------------------------------------']);
    display(['Expanding Memory VRF for degree : ' num2str(j)]);
    display(['---------------------------------------']);
    pjnumi0 = pseries(n+1,j+1,n);
    pjnumij = pseries(n+j+1,j*2+1,n);
    for (i=j:-1:0)
        pj = vrf_EMP_polynomial(i,j,n,s,tau);
        
        if(~isa(pj,'double'))
            if (i>0)
                pretty(simple(pj*pjnumij)/pjnumij);
            else
                pretty(simple(pj*pjnumi0)/pjnumi0);
            end
        else
            display(num2str(pj));
        end
    end
end

end

function [p] = pseries(in,pn,n)
    pi = in; p = pi; pn = pn-1;
    while (pn>0)
       p = p*(pi-1);
       pi = pi-1;
       pn = pn-1;
    end
end

function [ Sm ] = vrf_EMP_polynomial( i, j, n, s, tau )

    ss = n+1; % for 1step, ss=n; for current estimator 
    Sm = pmatrix(i, 0, n, s, ss)^2/legendre_norm(0, n, s);
    for (k=1:j)
       Sm = Sm + pmatrix(i, k, n, s, ss)^2/...
            legendre_norm(k, n, s);
    end
    Sm = (factorial(i)/tau^i)^2*Sm;

end

