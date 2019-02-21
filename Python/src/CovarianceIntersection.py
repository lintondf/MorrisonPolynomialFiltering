'''
Created on Feb 21, 2019

@author: NOOK
'''
import numpy as np
from numpy.random.mtrand import randn
from numpy import cov, concatenate, diag, transpose
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
    I = diag([1,1,1])
    print(Paa)
    print(Pab)
    print(Pbb)
    print(I)
    Pcc = inv( inv(Paa) + (inv(Paa) @ Pab - I) @ inv(Pbb - transpose(Pab)@inv(Paa)@Pab) @ (transpose(Pab)@inv(Paa)-I) )
    print(Pcc)