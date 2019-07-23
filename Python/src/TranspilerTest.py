from numpy import array, diag, ones, interp, zeros, concatenate, arange

# def test0(n : int, m : int) -> int:
#     return n+m;
# 
class testClass :
    '''@N : int'''
    '''@r : array - test array'''
#     def __init__(self, n : int) -> None:
#         self.method(1+2*3);
#         self.N = n;
    
    def m0(self, i : int, j : int, a : float ) -> float:
        return (2+3*4)*i - (1-7*4)*j + (2.0+3.0*4.0)*a;
        
    def method(self, n : int) -> float:
        '''@x : float'''
        '''@i : int'''
        i = 3*n + 5;
        x = 10.0*n + 3.14;
        return x;

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
        C[1:4,:] = 4;
        C[:,1:5] = 5;
        C[1:4,1:5] = 6;
        return C;
    
    
    
if __name__ == '__main__':
    pass
            
            
