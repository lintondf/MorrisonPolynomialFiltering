from numpy import array, diag, ones

def test0(n : int, m : int) -> int:
    return n+m;

def test1(A : array, B: array, D:int) -> array:
    '''@N : int'''
    test0(5, 7);
    '''@C : array'''
    C = A + (B + A/D)*B;
#     C = A + B + A*B;
    C[1,1] = 0;
    C[:,1] = 1;
    C[1,:] = 2;
    C[:] = 3;
    return C;

class testClass :
    '''@N : int'''
    
    def __init__(self):
        pass;
    
    def method(self, n : int) -> float:
        return 1.0*n;
    
    
if __name__ == '__main__':
#     N = 5;
#     '''@array'''; A = diag(ones([N]));
#     B = A;
#     A = A @ (B * A - 1) / 1**-0.5;
#     B[1,2] = 4;

    pass
#     start = time.time();
#     A = array([1, 2]);
#     B = array([3,4]);
#     for i in range(0, 10000000) :
#         B = test1(A, B)
#     print( time.time() - start)