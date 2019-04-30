function Ns_E2F( )

    syms The s tau n;

    for (j = 0:5)
        i = 0;
        p_Evrf = simple(vrf_EMP_polynomial(i,j,n,s,tau));
        p_Fvrf = simple(vrf_FMP_polynomial(i,j,The,s,tau));

        % assumption one
        p_Evrf = p_Evrf*n;
        p_Evrf = limit(p_Evrf,n,Inf)/n;

        % assumption two
        p_Fvrf = expand((p_Fvrf)/(1-The));
        p_Fvrf = simple(p_Fvrf);
        p_Fvrf = subs(p_Fvrf,'The',1)*(1-The);

        Ns = eval(solve(p_Evrf-p_Fvrf/(1-The),'n'));

        display( [' Ns(' num2str(j) ') = ' ...
                    num2str(Ns) '/(1-The)'] );
    end
end
