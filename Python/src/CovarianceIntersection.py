'''
Created on Feb 21, 2019

@author: NOOK
'''
import numpy as np
from numpy.random.mtrand import randn
from numpy import cov, concatenate, diag, transpose, arange, trace, array, zeros, \
     polyfit, polyder, polyval, roots
from numpy.linalg import det
from TestUtilities import A2S
from numpy.linalg.linalg import inv

if __name__ == '__main__':
    Z = randn(1000,6);
    P = cov(Z,rowvar=False);
    print(A2S(P))
    Y = Z[:,0:3];
    Y = concatenate([Y, Z[:,3:6]], axis=0);
    S = cov(Y,rowvar=False);
    print(A2S(S))
    Paa = P[0:3,0:3]
    Pbb = P[3:6,3:6]
    Pab = P[0:3,3:6]
#     I = diag([1,1,1])
    Paa = 2*array([[1, 0.8],[0.8, 1]]);
    Pbb = 3*array([[1,-0.5],[-0.5,1]]);
    print(A2S(Paa))
    print(A2S(Pab))
#     print(Pbb)
#     print(I)
#     Pcc = inv( inv(Paa) + (inv(Paa) @ Pab - I) @ inv(Pbb - transpose(Pab)@inv(Paa)@Pab) @ (transpose(Pab)@inv(Paa)-I) )
#     print(Pcc)

    print(trace(S), trace(Paa), trace(Pbb))
    W = [0.0, 0.25, 0.5, 0.75, 1.0];
    T = zeros([len(W),1]);
    for i in range(0,len(W))  :
        T[i] = trace( inv(W[i]*inv(Paa) + (1-W[i])*inv(Pbb)))
    print(A2S(T))
    p = polyfit( W, T, deg=2 );
    d = polyder(p[:,0]);
    print(polyval( p, W ) )
    print('p', p[:,0], d)
    w = roots(d)
    print(w, trace( inv(w*inv(Paa) + (1-w)*inv(Pbb))))
    