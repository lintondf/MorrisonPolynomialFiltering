function all_laguerre()

    % Run in Matlab to generate FMP filter   
    % weights up to the 5th degree
    clear all;
    clc;
    syms The s;
    for (j=0:5)
        display([' ']);
        display(['---------------------------------------']);
        display(['Fading Memory filter for degree : '... 
                        num2str(j )]);
        display(['---------------------------------------']);
        i = j;
        pj = gamma_FMP_polynomial(i,j,The,s);
        if(~isa(pj,'double'))
            pretty(simple(pj));
        else
            display(num2str(pj));
        end
        for (i=j-1:-1:0)
            pj = gamma_FMP_polynomial(i,j,The,s);
            if(~isa(pj,'double'))
                pretty(simple(pj));
            else
                display(num2str(pj));
            end
        end
    end

end

function [ Gamma ] = gamma_FMP_polynomial( i, j, ...
                                           The, s )
    dipj = 0;
    for (jj = j:-1:0)
        pij = ((-1)^i)*(laguerre_polynomial(jj, The, s))...
            *The^(1*jj);
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
