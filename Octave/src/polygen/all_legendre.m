function all_legendre()

    % Run in Matlab to generate EMP filter   
    % weights up to the 5th degree
    clear all;
    clc;
    syms n s;
    for (j=0:5)
        display([' ']);
        display(['---------------------------------------']);
        display(['Expanding Memory filter for degree : ' ...
                        num2str(j )]);
        display(['---------------------------------------']);
        i = j;
        pj = gamma_EMP_polynomial(i,j,n,s);
        if(~isa(pj,'double'))
            pretty(simple(pj));
        else
            display(num2str(pj));
        end
        for (i=j-1:-1:0)
            pj = gamma_EMP_polynomial(i,j,n,s);
            if(~isa(pj,'double'))
                pretty(simple(pj));
            else
                display(num2str(pj));
            end
        end
    end

end

function [ Gamma ] = gamma_EMP_polynomial( i, j, n, s )

    dipj = 0;
    for (jj = j:-1:0)
        pij = ((-1)^jj)*legendre_polynomial(jj, n, s);
        if (i>0)
            if (~isa(pij,'double'))
                dipj = dipj+diff(pij,'s',i)/...
                       legendre_norm(jj, n, s);
            end
        else
            dipj = dipj+pij/legendre_norm(jj, n, s);
        end
    end

    dipj = dipj/factorial(i);
    Gamma = subs(dipj,s,n,0);

end


