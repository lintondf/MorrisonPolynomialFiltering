function [pj] = laguerre_polynomial(j, The, s)
    
    C = @(n,m) factorial(n)/factorial(n - m)/...
                            factorial(m);

    b = (1-The)/The;
    pj = 1;

    for (v=1:j)
         pj = pj + ((-1)^v)*C(j,v)*b^v*M(s,v)...
             /factorial(v);
    end
    pj = The^(1*j)*pj;

end

function [p] = M(z,v)
    ii=0;
    p =1;
    for(i=1:v)
        p=p*(z-ii);
        ii = ii+1;
    end;
end
