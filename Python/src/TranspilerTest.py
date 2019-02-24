# import time;
from numpy import array, diag, ones

def test1(A : array, B: array):
    '''@C : array'''
    C = A + B;
    return C;
    
if __name__ == '__main__':
    N = 5;
    '''@array'''; A = diag(ones([N]));
    B = A;
    A = A @ (B * A - 1) / 1**-0.5;

    pass
#     start = time.time();
#     A = array([1, 2]);
#     B = array([3,4]);
#     for i in range(0, 10000000) :
#         B = test1(A, B)
#     print( time.time() - start)