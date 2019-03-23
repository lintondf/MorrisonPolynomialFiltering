'''
Created on Mar 21, 2019

@author: linto
'''
from numpy import eye
from numpy.linalg.linalg import det, inv

def covarianceIntersection( P1, P2 ):
    I1 = inv(P1)
    I2 = inv(P2)
    dI1 = det(I1)
    dI2 = det(I2)
    dI12 = det(I1+I2)
    w1 = (dI12 - dI2 + dI1) / (2*dI12);
    w2 = 1 - w1;
    P = inv( w1 * I1 + w2 * I2);
    return P

if __name__ == '__main__':
    print(covarianceIntersection(eye(3), 2*eye(3)))