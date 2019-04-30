function [cjn2] = laguerre_norm(j, The, s)

    if (nargin<1)
        syms The s;
        j=4;
    end
    
    cjn2 = The^j/(1-The);
end
