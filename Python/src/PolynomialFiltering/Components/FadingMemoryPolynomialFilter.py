'''
Created on Feb 13, 2019

@author: NOOK
'''

from typing import Tuple
from abc import abstractmethod

from numpy import array, zeros
from PolynomialFiltering.Components.AbstractRecursiveFilter import AbstractRecursiveFilter


class FMPBase(AbstractRecursiveFilter) :
    def __init__(self, order : int, theta : float, tau : float) -> None:
        super().__init__(order, tau)
        self.theta = theta
        self.n0 = 1
    
    def gammaParameter(self, t : float, dtau : array) -> array:
        return pow(self.theta, abs(dtau))

    @classmethod
    def _scaleVRF( self, V : array, u : float, theta : float ) -> array:
        t = 1-theta;
        S = zeros(V.shape);
        S[0,0] = t;
        for i in range(1,S.shape[0]) :
            S[i,0] = S[i-1,0] * t / u;
        for i in range(0,S.shape[0]) :
            for j in range(1,S.shape[1]) :
                S[i,j] = S[i,j-1] * t / u;
        return S * V;    
        
    @abstractmethod
    def _VRF(self) -> array:
        pass
        
            
class FMP0(FMPBase):    
    def __init__(self, theta : float, tau : float) -> None:
        super().__init__(0, theta, tau)

    def gamma(self, t : float) -> None:
        return array([1-t])

    def _VRF(self) -> array:
        t = self.theta
        V = zeros([self.order+1, self.order+1]);
        #{$FMP0CVRF}
        V[0,0] = ((1-t)/(1+t));
        return V;

class FMP1(FMPBase):    
    def __init__(self, theta : float, tau : float) -> None:
        super().__init__(1, theta, tau)

    def gamma(self, t : float) -> None:
        t2 = t*t 
        mt2 = (1-t)*(1-t)
        return array([1-t2, 
                      mt2])

    def _VRF(self) -> array:
        t = 1 - self.theta
        u = self.tau;
        """VRF approximating constants from Morrison 2013, Supplemental Materials, Problem 13.3"""
        V = array([[1.25,    0.5],[0.5,    0.25]]);
        return self._scaleVRF(V, u, t);
        
class FMP2(FMPBase):    
    def __init__(self, theta : float, tau : float) -> None:
        super().__init__(2, theta, tau)

    def gamma(self, t : float) -> None:
        t2 = t*t
        t3 = t2*t
        mt2 = (1-t)*(1-t)
        mt3 = (1-t)*mt2
        return array([1-t3, 
                      3.0/2.0*mt2 * (1+t),
                      (2*1)*1.0/2.0*mt3])

    def _VRF(self) -> array:
        t = 1 - self.theta
        u = self.tau;
        """VRF approximating constants from Morrison 2013, Supplemental Materials, Problem 13.3"""
        V = array([[2.0625,1.6875,0.5],[1.6875,    1.75,    0.5625],[0.5,    0.5625,    0.1875]]);
        return self._scaleVRF(V, u, t);

class FMP3(FMPBase):    
    def __init__(self, theta : float, tau : float) -> None:
        super().__init__(3, theta, tau)

    def gamma(self, t : float) -> None:
        t2 = t*t 
        t3 = t2*t
        t4 = t3*t
        mt2 = (1-t)*(1-t)
        mt3 = (1-t)*mt2
        mt4 = mt2*mt2
        return array([1-t4, 
                      1.0/6.0*mt2 * (11+14*t+11*t2),
                      (2*1)*mt3*(1+t),
                      (3*2*1)*1.0/6.0*mt4])

    def _VRF(self) -> array:
        t = 1 - self.theta
        u = self.tau;
        """VRF approximating constants from Morrison 2013, Supplemental Materials, Problem 13.3"""
        V = array([[2.90625,    3.625,    2.15625,    0.5],\
                   [3.625,    5.78125,    3.75,    0.90625],\
                   [2.15625,    3.75,    2.53125,    0.625],\
                   [0.5,    0.90625,    0.625,    0.15625]]);
        return self._scaleVRF(V, u, t);

class FMP4(FMPBase):    
    def __init__(self, theta : float, tau : float) -> None:
        super().__init__(4, theta, tau)

    def gamma(self, t : float) -> None:
        t2 = t*t 
        t3 = t2*t
        t5 = t2*t3
        mt2 = (1-t)*(1-t)
        mt3 = (1-t)*mt2
        mt4 = mt2*mt2
        return array([1-t5, 
                      5.0/12.0*mt2 * (5+7*t+7*t2+5*t3),
                      (2*1)*5.0/24.0*mt3*(7+10*t+7*t2),
                      (3*2*1)*5.0/12.0*mt4*(1+t),
                      (4*3*2*1)*1.0/24.0*mt4])

    def _VRF(self) -> array:
        t = 1 - self.theta
        u = self.tau;
        """VRF approximating constants from Morrison 2013, Supplemental Materials, Problem 13.3"""
        V = array([[3.7695313,   6.3476563,   5.6835938,   2.6367188,   0.5],\
                   [6.3476563,   13.75,   13.476563,   6.53125,   1.2695313],\
                   [5.6835938,   13.476563,   13.78125,   6.8359375,   1.3476563],\
                   [2.6367188,   6.53125,   6.8359375,   3.4375,   0.68359375],\
                   [0.5,   1.2695313,   1.3476563,   0.68359375,   0.13671875]]);
        return self._scaleVRF(V, u, t);

class FMP5(FMPBase):    
    def __init__(self, theta : float, tau : float) -> None:
        super().__init__(5, theta, tau)

    def gamma(self, t : float) -> None:
        t2 = t*t 
        t3 = t2*t
        t4 = t3*t
        t6 = t2*t4
        mt2 = (1-t)*(1-t)
        mt3 = (1-t)*mt2
        mt4 = mt2*mt2
        mt5 = mt3*mt2
        mt6 = mt3*mt3
        return array([1-t6, 
                      1.0/60.0*mt2 * (137+202*t+222*t2+202*t3+137*t4),
                      (2*1)*5.0/8.0*mt3*(1+t)*(3+2*t+3*t2),
                      (3*2*1)*1.0/24.0*mt4*(17+26*t+17*t2),
                      (4*3*2*1)*1.0/8.0*mt5*(1+t),
                      (5*4*3*2*1)*1.0/120.0*mt6 ])
        
    def nSwitch(self):
        return 7.7478/(1.0-self.theta)
 
    def _VRF(self) -> array:
        t = 1 - self.theta
        u = self.tau;
        """VRF approximating constants from Morrison 2013, Supplemental Materials, Problem 13.3"""
        V = array([[4.6464844,   9.8789063,   11.832031,   8.2382813,   3.1230469,   0.5],\
                   [9.8789063,   27.138672,   35.683594,   26.003906,   10.117188,   1.6464844],\
                   [11.832031,   35.683594,   49.054687,   36.640625,   14.472656,   2.3789063],\
                   [8.2382813,   26.003906,   36.640625,   27.773438,   11.074219,   1.8320313],\
                   [3.1230469,   10.117188,   14.472656,   11.074219,   4.4433594,   0.73828125],\
                   [0.5,   1.6464844,   2.3789063,   1.8320313,   0.73828125,   0.12304688]]);

        return self._scaleVRF(V, u, t);

    
def makeFMP(order, theta : float, tau : float ) -> FMPBase :
    Fmps = [FMP0, FMP1, FMP2, FMP3, FMP4, FMP5];
    return Fmps[order](theta, tau);
        
        