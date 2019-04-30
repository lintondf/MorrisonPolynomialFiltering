syms n s;
tau = 1;

%% All vrf elements
P = [
     pmatrix( 0, 0, n, s, n+1 ) pmatrix( 0, 1, n, s, n+1 )
     pmatrix( 1, 0, n, s, n+1 ) pmatrix( 1, 1, n, s, n+1 )
];

C2 = [
        1/legendre_norm( 0, n, s ) 0
        0 1/legendre_norm( 1, n, s )
];

Svrf = P*C2*transpose(P);
pretty(simple(Svrf));

%% Vrf Diagonals only
S_diag = [ 
    vrf_EMP_polynomial( 0, 1, n, s, tau )
    vrf_EMP_polynomial( 1, 1, n, s, tau )
];

eval(S_diag(1)-Svrf(1,1))
eval(S_diag(2)-Svrf(2,2))