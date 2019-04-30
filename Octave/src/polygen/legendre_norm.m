function [cjn2] = legendre_norm (j, n, s)

    if (nargin<1)
        syms n s;
        j=4;
    end
    cjn2 = (n+j+1)/(2*j+1)*M(n+j,j)/M(n,j);
end

function [p] = M(z,v) 
    ii=0;
    p =1;
    for(i=1:v) 
        p=p*(z-ii);
        ii = ii+1;
    end;  
end

