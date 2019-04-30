function gamma_FMP_coefficients()
    clear all;
    clc;
    syms The s;

    for (j=0:8)
        for (i=j:-1:0)
            fp = gamma_FMP_polynomial(i, j, The, s);
            if(~isa(fp,'double'))
                fs = simple(fp);
            else
                fs = fp;
            end
            display([' ']);
            display(['----------------------------------------']);
            display(['Laguerre FMP Gamma (' num2str(i) ', ' num2str(j) ' )']);
            display(['----------------------------------------']);
            if(~isa(fs,'double'))
                pretty(simple(fs));
            else
                display(['                                       ' num2str(fs)]);
            end
        end
    end
end

function [ Gamma ] = gamma_FMP_polynomial( i, j, ...
                                           The, s )
    dipj = 0;
    for (jj = j:-1:0)
        pij = ((-1)^i)*(laguerre_polynomial(jj, The, s))*The^(1*jj);
        if (i>0)
            if (~isa(pij,'double'))
                dipj = dipj+diff(pij,'s',i)/...
                            laguerre_norm(jj, The, s);
            end
        else
            dipj = dipj+pij/laguerre_norm(jj, The, s);
        end
    end
    dipj = dipj/factorial(i);
    Gamma = subs(dipj,s,0);

end
