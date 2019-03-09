'''
Created on Feb 13, 2019

@author: NOOK
'''

from typing import Tuple
from abc import abstractmethod

from numpy import array, diag, zeros
from numpy import array as vector
from PolynomialFiltering.Components.AbstractRecursiveFilter import AbstractRecursiveFilter, IRecursiveFilter

class EMPBase(AbstractRecursiveFilter):
    def __init__(self, order : int, tau : float) :
        super().__init__(order, tau)
        
    def _gammaParameter(self, t : float, dtau : float) -> float:
        return self._normalizeTime(t)
    
    @classmethod
    def _scaleVRF( self, V : array, t : float, n : float ) -> array:
        '''@S : array'''
        '''@i : int'''
        '''@j : int'''
        S = zeros([V.shape[0], V.shape[1]]);
        S[0,0] = 1.0/n;
        for i in range(1,S.shape[0]) :
            S[i,0] = S[i-1,0] / (t*n);
        for i in range(0,S.shape[0]) :
            for j in range(1,S.shape[1]) :
                S[i,j] = S[i,j-1] / (t*n);
        return S * V;
    
    @abstractmethod
    def nSwitch(self, theta : float) -> float:
        pass
    
    @abstractmethod
    def _VRF(self) -> array:
        pass
        

class EMP0(EMPBase) :
    def __init__(self, tau : float) :
        super().__init__( 0, tau)
        
    def _gamma(self, n : float) -> vector:
        return array([1/(1+n)])
    
    def nSwitch(self, theta : float) -> float:
        return 2.0/(1.0-theta)
    
    def _VRF(self) -> array:
        '''@n : int'''
        '''@V : array'''
        n = self.n
        V = array([1/(n+1)]);
        return V;

    
class EMP1(EMPBase) :
    def __init__(self, tau : float) :
        super().__init__( 1, tau )
        
    def _gamma(self, n : float) -> vector: #
        '''@denom : float'''
        denom = 1.0/((n+2)*(n+1))
        return denom*array([2*(2*n+1), 
                            6])
    
    def nSwitch(self, theta : float) -> float:
        return 3.2/(1.0-theta)
    
    
    def _VRF(self) -> array:
        '''@n : int'''
        '''@u : float'''
        '''@V : array'''
        n = self.n
        if (n < self.order) :
            return zeros([self.order+1, self.order+1]);
        u = self.tau;
        '''@C : array'''
        C = array([[4,6],[6,12]]);
        V =  self._scaleVRF(C, u, n);
        V[0,0] = 2*(2*n+3) / ((n+1)*n);
        V[1,1] = 12 / (u**2*(n+2)*(n+1)*n);
        return V;

class EMP2(EMPBase) :
    def __init__(self, tau : float) :
        super().__init__( 2, tau )
        
    def _gamma(self, n : float) -> vector: #
        '''@n2 : float'''
        '''@denom : float'''
        n2 = n*n 
        denom = 1.0/((n+3)*(n+2)*(n+1))
        return denom*array([3*(3*n2+3*n+2), 
                            18*(2*n+1), 
                            (2*1)*30])
    
    def nSwitch(self, theta : float) -> float:
        return 4.3636/(1.0-theta)
    

    def _VRF(self) -> array:
        '''@n : int'''
        '''@u : float'''
        '''@V : array'''
        n = self.n
        if (n < self.order) :
            return zeros([self.order+1, self.order+1]);
        u = self.tau;
        '''@C : array'''
        C = array([[9,36,60],[36,192,360],[60,360,720]]);
        V = self._scaleVRF(C, u, n);
        V[0,0] = 3*(3*n**2+9*n+8) / ((n+1)*n*(n-1));
        V[1,1] =  12*(16*n**2+62*n+57) / (u**2*(n+3)*(n+2)*(n+1)*n*(n-1))
        V[2,2] = 720 / (u**4*(n+3)*(n+2)*(n+1)*n*(n-1))
        return V;
        
class EMP3(EMPBase) :
    def __init__(self, tau : float) :
        super().__init__( 3, tau )
        
    def _gamma(self, n : float) -> vector: #
        '''@n2 : float'''
        '''@n3 : float'''
        '''@denom : float'''
        n2 = n*n 
        n3 = n2*n 
        denom = 1.0/((n+4)*(n+3)*(n+2)*(n+1))
        return denom*array([8*(2*n3+3*n2+7*n+3), 
                            20*(6*n2+6*n+5), 
                            (2*1)*120*(2*n+1), # 
                            (3*2*1)*140])   # 
    
    def nSwitch(self, theta : float) -> float:
        return 5.50546/(1.0-theta)
    

    def _VRF(self) -> array:
        '''@n : int'''
        '''@u : float'''
        '''@V : array'''
        n = self.n
        if (n < self.order) :
            return zeros([self.order+1, self.order+1]);
        u = self.tau;
        '''@C : array'''
        C = array([[16, 120, 480, 840],[120, 1200,5400, 10080],[480, 5400, 25920, 50400],[840, 10080, 50400, 100800]]);
        V = self._scaleVRF(C, u, n);
        V[0,0] = 4*(4*n**3+18*n**2+38*n+30) / ((n+1)*n*(n-1)*(n-2));
        V[1,1] = 200*(6*n**4+51*n**3+159*n**2+219*n+116) / (u**2*(n+4)*(n+3)*(n+2)*(n+1)*n*(n-1)*(n-2));
        V[2,2] = 80*(324*n**2+1278*n+1188) / (u**4*(n+4)*(n+3)*(n+2)*(n+1)*n*(n-1)*(n-2));
        V[3,3] = 100800 / (u**6*(n+4)*(n+3)*(n+2)*(n+1)*n*(n-1)*(n-2));
        return V;

class EMP4(EMPBase) :
    def __init__(self, tau : float) :
        super().__init__( 4, tau )
        
    def _gamma(self, n : float) -> vector: # 
        '''@n2 : float'''
        '''@n3 : float'''
        '''@n4 : float'''
        '''@denom : float'''
        n2 = n*n 
        n3 = n2*n 
        n4 = n2*n2
        denom = 1.0/((n+5)*(n+4)*(n+3)*(n+2)*(n+1))
        return denom*array([5*(5*n4+10*n3+55*n2+50*n+24), 
                            25*(12*n3+18*n2+46*n+20), 
                            (2*1)*1050*(n2+n+1), # 
                            (3*2*1)*700*(2*n+1),  # 
                            (4*3*2*1)*630]) #
    
    def nSwitch(self, theta : float) -> float:
        return 6.6321/(1.0-theta)
    

    def _VRF(self) -> array:
        '''@n : int'''
        '''@u : float'''
        '''@V : array'''
        n = self.n
        if (n < self.order) :
            return zeros([self.order+1, self.order+1]);
        u = self.tau;
        '''@C : array'''
        C = array([[25, 300, 2100, 8400, 15120],[300, 4800, 37800, 161280, 302400],[2100, 37800, 317520, 1411200, 2721600],[8400, 161280, 1411200, 6451200, 12700800],[15120, 302400, 2721600, 12700800, 25401600]]);
        V = self._scaleVRF(C, u, n);
        V[0,0] = 5*(5*n**4+30*n**3+115*n**2+210*n+144) / ((n+1)*n*(n-1)*(n-2)*(n-3));
        V[1,1] = 100*(48*n**6 +666*n**5 +3843*n**4 +11982*n**3 +21727*n**2 +21938*n +9516) / \
                 (u**2*(n+5)*(n+4)*(n+3)*(n+2)*(n+1)*n*(n-1)*(n-2)*(n-3));
        V[2,2] = 720*(441*n**4+3724*n**3+11711*n**2+21938*n+9516)/ \
                 (u**4*(n+5)*(n+4)*(n+3)*(n+2)*(n+1)*n*(n-1)*(n-2)*(n-3));
        V[3,3] = 100800*(64*n**2+254*n+237) /\
                 (u**6*(n+5)*(n+4)*(n+3)*(n+2)*(n+1)*n*(n-1)*(n-2)*(n-3));
        V[4,4] = 25401600 / (u**8 * (n+5)*(n+4)*(n+3)*(n+2)*(n+1)*n*(n-1)*(n-2)*(n-3));
        return V;

class EMP5(EMPBase) :
    def __init__(self, tau : float) :
        super().__init__( 5, tau )
        
    def _gamma(self, n : float) -> vector:
        '''@n2 : float'''
        '''@n3 : float'''
        '''@n4 : float'''
        '''@denom : float'''
        n2 = n*n 
        n3 = n2*n 
        n4 = n2*n2
        denom = 1.0/((n+6)*(n+5)*(n+4)*(n+3)*(n+2)*(n+1))
        return denom*array([6*(2*n+1)*(3*n4+6*n3+77*n2+74*n+120), 
                            126*(5*n4+10*n3+55*n2+50*n+28), 
                            (2*1)*420*(2*n+1)*(4*n2+4*n+15), #
                            (3*2*1)*1260*(6*n2+6*n+7), #  
                            (4*3*2*1)*3780*(2*n+1),  # 
                            (5*4*3*2*1)*2772]) #
        
    def nSwitch(self, theta : float) -> float:
        return 7.7478/(1.0-theta)
    
   
    def _VRF(self) -> array:
        '''@n : int'''
        '''@u : float'''
        '''@V : array'''
        n = self.n
        if (n < self.order) :
            return zeros([self.order+1, self.order+1]);
        u = self.tau;
        '''@C : array'''
        C = array([[36, 630, 6720, 45360, 181440, 332640],[630, 14700, 176400, 1270080, 5292000, 9979200],[6720, 176400, 2257920, 16934400, 72576000, 139708800],[45360, 1270080, 16934400, 130636800, 571536000, 1117670400],[181440, 5292000, 72576000, 571536000, 2540160000, 5029516800],[332640, 9979200, 139708800, 1117670400, 5029516800, 10059033600]]);
        V = self._scaleVRF(C, u, n);
        V[0,0] = 6*(2*n+3)*(3*n**4+18*n**3+113*n**2+258*n+280) /\
                ((n+1)*n*(n-1)*(n-2)*(n-3)*(n-4));
        V[1,1] = 588*(25*n**8 +500*n**7 +4450*n**6 +23300*n**5 +79585*n**4 +181760*n**3 +267180*n**2 +226920*n +84528) / \
                (u**2*(n+6)*(n+5)*(n+4)*(n+3)*(n+2)*(n+1)*n*(n-1)*(n-2)*(n-3)*(n-4));
        V[2,2] = 70560*(2*n+3)*(16*n**5+192*n**4+952*n**3+2472*n**2+3501*n+2230) / \
                (u**4*(n+6)*(n+5)*(n+4)*(n+3)*(n+2)*(n+1)*n*(n-1)*(n-2)*(n-3)*(n-4));
        V[3,3] = 2721600*(48*n**4+402*n**3+1274*n**2+1828*n+1047) / \
                (u**6*(n+6)*(n+5)*(n+4)*(n+3)*(n+2)*(n+1)*n*(n-1)*(n-2)*(n-3)*(n-4));
        V[4,4] = 50803200*(2*n+3)*(25*n+62) / \
                (u**8*(n+6)*(n+5)*(n+4)*(n+3)*(n+2)*(n+1)*n*(n-1)*(n-2)*(n-3)*(n-4));
        V[5,5] = 10059033600 / \
                (u**10*(n+6)*(n+5)*(n+4)*(n+3)*(n+2)*(n+1)*n*(n-1)*(n-2)*(n-3)*(n-4));
        return V;

def makeEMP(order : int, tau : float) -> EMPBase:
    if (order == 0) :
        return EMP0(tau);
    elif (order == 1) :
        return EMP1(tau);
    elif (order == 2) :
        return EMP2(tau);
    elif (order == 3) :
        return EMP3(tau);
    elif (order == 4) :
        return EMP4(tau);
    else : # (order == 5) :
        return EMP5(tau);


# if __name__ == "__main__":
#     from TestUtilities import A2S
#     order = 2;
#     for tau in [1e-3, 1e-2, 1e-1, 1, 1e1, 1e2] :
# #         emp = makeEMP(order, tau);
# #         emp.start(0.0, [1, 1, 1])
# #         emp.n = 50;
# #         V = (emp.getCovariance(emp.tau, 1))
# #         print(tau,order, (diag(V)))
# 
#         order = 1;
#         n = 1;
#         emp= EMP0(tau);
#         emp.start(0.0, [1, 1, 1])
#         emp.n = 1;
#         P = emp.getCovariance(emp.tau, 1)
#         P.shape = (1,1);
#         while (order < 5+1) :
#             emp = makeEMP(order, tau);
#             emp.start(0.0, [1, 1, 1])
#             while (True) :
#                 emp.n = n;
#                 V = emp.getCovariance(0.0+emp.tau, 1)
#                 if (V[0,0] > 0) :
#                     if (V[order-1,order-1] <= P[order-1,order-1] and V[order,order] <= 1) :
#                         print(tau, order, n, A2S(diag(V)))
#                         P = V;
#                         break;
#                 n += 1;
#             order += 1;
#     """
#     """
#     
