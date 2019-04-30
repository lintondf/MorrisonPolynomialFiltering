function [pj] = legendre_polynomial(j, n, s)

    C = @(n,m) factorial(n)/factorial(n - m)/...
               factorial(m);

    pj = C(j,0)*C(j,0)*M(s,0)/M(n,0);
    for (v=1:j)
        pj = pj + ((-1)^v)*C(j,v)*C(j+v,v)*M(s,v)/...
                                           M(n,v);
    end

end

function [p] = M(z,v)
    ii=0;
    p =1;
    for(i=1:v)
        p=p*(z-ii);
        ii = ii+1;
    end;
end
