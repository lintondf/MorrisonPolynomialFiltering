function laguerre_gamma_test()
    clear all;
    clc;
    syms The s;

    pm = [  (1-The), (1-The^2), (1-The^3), (1-The^4), (1-The^5); ...
            0, (1-The)^2, 3/2*((1-The)^2)*(1+The), 1/6*((1-The)^2)*(11+14*The+11*The^2), 5/12*((1-The)^2)*(5+7*The+ 7*The^2 + 5*The^3);...
            0, 0, ((1-The)^3)/2, ((1-The)^3)*(1+The), 5/24*((1-The)^3)*(7+10*The+7*The^2);
            0, 0, 0, ((1-The)^4)/6, 5/12*((1-The)^4)*(1+The);
            0, 0, 0, 0, ((1-The)^5)/24 ];

    for (j=0:4)
        for (i=j:-1:0)
            fm = pm(i+1,j+1);
            fp = gamma_FMP_polynomial(i, j, The, s);
            if(~isa(fp-fm,'double'))
                fs = simple(fp-fm);
            else
                fs = fp-fm;
            end
            display([' ']);
            display(['----------------------------------------']);
            display(['Laguerre Gamma test (' num2str(i) ', ' num2str(j) ' )']);
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
