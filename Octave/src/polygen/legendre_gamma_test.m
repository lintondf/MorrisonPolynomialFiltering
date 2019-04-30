function legendre_gamma_test()
    clear all;
    clc;
    syms n s;

    pm = [  1/(n+1), 2*(2*n+1)/(n+2)/(n+1), 3*(3*n^2+3*n+2)/(n+3)/(n+2)/(n+1), ...
            8*(2*n^3+3*n^2+7*n+3)/(n+4)/(n+3)/(n+2)/(n+1), 5*(5*n^4+10*n^3+55*n^2+50*n+24)/(n+5)/(n+4)/(n+3)/(n+2)/(n+1); ...
            0, 6/(n+2)/(n+1), 18*(2*n+1)/(n+3)/(n+2)/(n+1), 20*(6*n^2+6*n+5)/(n+4)/(n+3)/(n+2)/(n+1), ...
            25*(12*n^3+18*n^2+46*n+20)/(n+5)/(n+4)/(n+3)/(n+2)/(n+1); ...
            0, 0, 30/(n+3)/(n+2)/(n+1), 120*(2*n+1)/(n+4)/(n+3)/(n+2)/(n+1), 1050*(n^2+n+1)/(n+5)/(n+4)/(n+3)/(n+2)/(n+1);
            0, 0, 0, 140/(n+4)/(n+3)/(n+2)/(n+1), 700*(2*n+1)/(n+5)/(n+4)/(n+3)/(n+2)/(n+1);
            0, 0, 0, 0, 630/(n+5)/(n+4)/(n+3)/(n+2)/(n+1) ];

    for (j=0:4)
        for (i=j:-1:0)
            fm = pm(i+1,j+1);
            fp = gamma_EMP_polynomial(i, j, n, s);
            if(~isa(fp-fm,'double'))
                fs = simple(fp-fm);
            else
                fs = fp-fm;
            end
            display([' ']);
            display(['----------------------------------------']);
            display(['Legendre Gamma test (' num2str(i) ', ' num2str(j) ' )']);
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