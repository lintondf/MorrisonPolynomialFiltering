function gamma_EMP_coefficients()
    clear all;
    clc;
    syms n s;

    for (j=0:8)
        for (i=j:-1:0)
            fp = gamma_EMP_polynomial(i, j, n, s);
            if(~isa(fp,'double'))
                fs = simple(fp);
            else
                fs = fp;
            end
            display([' ']);
            display(['----------------------------------------']);
            display(['Legendre EMP Gamma (' num2str(i) ', ' num2str(j) ' )']);
            display(['----------------------------------------']);
            if(~isa(fs,'double'))
                %pretty(fm);
                pretty(simple(fs));
            else
                display(['                                       ' num2str(fs)]);
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