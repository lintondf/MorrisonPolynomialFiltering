from numpy import array, diag, ones, interp, zeros, concatenate, arange

# def test0(n : int, m : int) -> int:
#     return n+m;
# 
class testClass :
    '''@N : int'''
    '''@r : array - test array'''
    def __init__(self, n : int) -> None:
        self.method(1+2*3);
        self.N = n;
    
    def method(self, n : int) -> float:
        return 1.0*n;

    def test1(self, A : array, B: array, D:int) -> array:
        '''@N : int'''
    #    test0(5, 7);
        '''@C : array'''
        C = A + (B + A/D)*B;
    #     C = A + B + A*B;
        C[1,1] = 0;
        C[D+2,D+3] = 1;
        C[:,1] = 1;
        C[1,:] = 2;
        C[:] = 3;
        return C;
    
    
    
if __name__ == '__main__':
    pass
            
            
