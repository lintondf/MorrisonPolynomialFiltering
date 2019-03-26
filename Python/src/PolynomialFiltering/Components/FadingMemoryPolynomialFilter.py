'''
Created on Feb 13, 2019

@author: NOOK
'''

from typing import Tuple
from abc import abstractmethod

from numpy import array, zeros, sqrt, diag
from numpy import array as vector
from PolynomialFiltering.Components.AbstractRecursiveFilter import AbstractRecursiveFilter


class FMPBase(AbstractRecursiveFilter) :

    '''@n0 : int'''
    '''@theta : float'''

    def __init__(self, order : int, theta : float, tau : float) :
        super().__init__(order, tau);
        self.theta = theta;
        self.n0 = 1;
        
    #TODO functions to compute theta from effective L and vice versa [Morrison 1969, Table 13.4]    
    def _gammaParameter(self, t : float, dtau : float) -> float:
        return pow(self.theta, abs(dtau))

    @abstractmethod
    def _VRF(self) -> array:
        pass
        
            
class FMP0(FMPBase):    
    def __init__(self, theta : float, tau : float):
        super().__init__(0, theta, tau)

    def _gamma(self, t : float) -> vector:
        return array([1-t])

    def _VRF(self) -> array:
        '''@t : float'''
        '''@V : array'''
        t = self.theta
        V = zeros([self.order+1, self.order+1]);
        V[0,0] = ((1-t)/(1+t));
        return V;

class FMP1(FMPBase):    
    def __init__(self, theta : float, tau : float) :
        super().__init__(1, theta, tau)

    def _gamma(self, t : float) -> vector:
        '''@t2 : float'''
        '''@mt2 : float'''
        t2 = t*t 
        mt2 = (1-t)*(1-t)
        return array([1-t2, 
                      mt2])

    def _VRF(self) -> array:
        '''@t : float'''
        '''@u : float'''
        '''@K : array'''
        '''@d : vector'''
        '''@D : array'''
        t = self.theta
        u = self.tau;
        """VRF correlations from approximating constants from Morrison 2013, Supplemental Materials, Problem 13.3"""
        K = array([[1, 0.894427191], [0.894427191, 1]]);
        d = zeros([self.order+1]);
        d[0] = (t**2+4*t+5)*(1-t) / (1+t)**3
        d[1] = 2*(1-t)**3 / (u**2 * (1+t)**3 )
        D = diag( sqrt(d) );
        return D @ K @ D;
        
class FMP2(FMPBase):    
    def __init__(self, theta : float, tau : float) :
        super().__init__(2, theta, tau)

    def _gamma(self, t : float) -> vector:
        '''@t2 : float'''
        '''@t3 : float'''
        '''@mt2 : float'''
        '''@mt3 : float'''
        t2 = t*t
        t3 = t2*t
        mt2 = (1-t)*(1-t)
        mt3 = (1-t)*mt2
        return array([1-t3, 
                      3.0/2.0*mt2 * (1+t),
                      (2*1)*1.0/2.0*mt3])  # 2! * 1-T^3 ?

    def _VRF(self) -> array:
        '''@t : float'''
        '''@u : float'''
        '''@K : array'''
        '''@d : vector'''
        '''@D : array'''
        t = self.theta
        u = self.tau;
        """VRF approximating constants from Morrison 2013, Supplemental Materials, Problem 13.3"""
        K = array([[1, 0.888234788196, 0.804030252207], [0.888234788196, 1, 0.981980506062], [0.804030252207, 0.981980506062, 1]]);
        d = zeros([self.order+1]);
        d[0] = (t**4 + 6*t**3 + 16*t**2 + 24*t + 19) *(1-t) / (1+t)**5
        d[1] = (13*t**2 + 50*t + 49)*(1-t)**3 / (2*u**2*(1+t)**5)
        d[2] = 6*(1-t)**5 / (u**4*(1+t)**5)
        D = diag( sqrt(d) );
        return D @ K @ D;

class FMP3(FMPBase):    
    def __init__(self, theta : float, tau : float):
        super().__init__(3, theta, tau)

    def _gamma(self, t : float) -> vector:
        '''@t2 : float'''
        '''@t3 : float'''
        '''@t4 : float'''
        '''@mt2 : float'''
        '''@mt3 : float'''
        '''@mt4 : float'''
        t2 = t*t 
        t3 = t2*t
        t4 = t3*t
        mt2 = (1-t)*(1-t)
        mt3 = (1-t)*mt2
        mt4 = mt2*mt2
        return array([1-t4, 
                      1.0/6.0*mt2 * (11+14*t+11*t2),
                      (2*1)*mt3*(1+t), # ?
                      (3*2*1)*1.0/6.0*mt4]) # ?

    def _VRF(self) -> array:
        '''@t : float'''
        '''@u : float'''
        '''@K : array'''
        '''@d : vector'''
        '''@D : array'''
        t = self.theta
        u = self.tau;
        """VRF approximating constants from Morrison 2013, Supplemental Materials, Problem 13.3"""
        K = array([[1, 0.88436317611, 0.794996299293, 0.741982233216], [0.88436317611, 1, 0.980286162792, 0.953514126371], [0.794996299293, 0.980286162792, 1, 0.99380799], [0.741982233216, 0.953514126371, 0.99380799, 1]]);
        d = zeros([self.order+1]);
        d[0] = (t**6 + 8*t**5 + 29*t**4 + 64*t**3 + 97*t**2 + 104*t + 69)*(1-t) / (1+t)**7
        d[1] = 5/18*(53*t**4 + 298*t**3 + 762*t**2 + 970*t + 581)*(1-t)**3 / (u**2*(1+t)**7)
        d[2] = 2*(23*t**2 + 76*t + 63)*(1-t)**5 / (u**4*(1+t)**7)
        d[3] = 20*(1-t)**7 / (u**6*(1+t)**7)
        D = diag( sqrt(d) );
        return D @ K @ D;

class FMP4(FMPBase):    
    def __init__(self, theta : float, tau : float):
        super().__init__(4, theta, tau)

    def _gamma(self, t : float) -> vector:
        '''@t2 : float'''
        '''@t3 : float'''
        '''@t5 : float'''
        '''@mt2 : float'''
        '''@mt3 : float'''
        '''@mt4 : float'''
        '''@mt5 : float'''
        t2 = t*t 
        t3 = t2*t
        t5 = t2*t3
        mt2 = (1-t)*(1-t)
        mt3 = (1-t)*mt2
        mt4 = mt2*mt2
        mt5 = mt2*mt3
        return array([1-t5, 
                      5.0/12.0*mt2 * (5+7*t+7*t2+5*t3),
                      (2*1)*5.0/24.0*mt3*(7+10*t+7*t2),
                      (3*2*1)*5.0/12.0*mt4*(1+t),
                      (4*3*2*1)*1.0/24.0*mt5])

    def _VRF(self) -> array:
        '''@t : float'''
        '''@u : float'''
        '''@K : array'''
        '''@d : vector'''
        '''@D : array'''
        t = self.theta
        u = self.tau;
        """VRF approximating constants from Morrison 2013, Supplemental Materials, Problem 13.3"""
        K = array([[1, 0.881694998952, 0.788560555275, 0.732485084173, 0.696485834473], [0.881694998952, 1, 0.979001802066, 0.95, 0.925929720202], [0.788560555275, 0.979001802066, 1, 0.993190197131, 0.981794965522], [0.732485084173, 0.95, 0.993190197131, 1, 0.997155044022], [0.696485834473, 0.925929720202, 0.981794965522, 0.997155044022, 1]]);
        d = zeros([self.order+1]);
        d[0] = (t**8+10*t**7+46*t**6+130*t**5+256*t**4+380*t**3+446*t**2+410*t+251)*(1-t) / ((1+t)**9)
        d[1] = 5*(449*t**6+2988*t**5+10013*t**4+21216*t**3+28923*t**2+25588*t+12199)*(1-t)**3 / (72*u**2*(1+t)**9) 
        d[2] = 7*(2021*t**4+10144*t**3+22746*t**2+25144*t+12521)*(1-t)**5 / (72*u**4*(1+t)**9)
        d[3] = 5*(113*t**2 + 338*t + 253)*(1-t)**7 / (2*u**6*(1+t)**9)
        d[4] = 70*(1-t)**9 / (u**8*(1+t)**9)
        D = diag( sqrt(d) );
        return D @ K @ D;

class FMP5(FMPBase):    
    def __init__(self, theta : float, tau : float):
        super().__init__(5, theta, tau)

    def _gamma(self, t : float) -> vector:
        '''@t2 : float'''
        '''@t3 : float'''
        '''@t4 : float'''
        '''@t6 : float'''
        '''@mt2 : float'''
        '''@mt3 : float'''
        '''@mt4 : float'''
        '''@mt5 : float'''
        '''@mt6 : float'''
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
                      5.0/8.0*mt3*(3+5*t+5*t2+3*t3),
                      1.0/24.0*mt4*(17+26*t+17*t2),
                      1.0/8.0*mt5*(1+t),
                      mt6/120.0 ])
#         return array([1-t6, 
#                       1.0/60.0*mt2 * (137+202*t+222*t2+202*t3+137*t4),
#                       (2*1)*5.0/8.0*mt3*(1+t)*(3+2*t+3*t2),
#                       (3*2*1)*1.0/24.0*mt4*(17+26*t+17*t2),
#                       (4*3*2*1)*1.0/8.0*mt5*(1+t),
#                       (5*4*3*2*1)*1.0/120.0*mt6 ])
        
#     def nSwitch(self) -> float:
#         return 7.7478/(1.0-self.theta)
 
    def _VRF(self) -> array:
        '''@t : float'''
        '''@u : float'''
        '''@K : array'''
        '''@d : vector'''
        '''@D : array'''
        t = self.theta
        u = self.tau;
        """correlation matrix from VRF approximating constants from Morrison 2013, Supplemental Materials, Problem 13.3"""
        K = array([[1, 0.87973592749, 0.783712552247, 0.725202936114, 0.687322471879, 0.661260314876], [0.87973592749, 1, 0.977989154933, 0.947173349319, 0.921318523517, 0.901006701352], [0.783712552247, 0.977989154933, 1, 0.992676628391, 0.980284789003, 0.96828182239], [0.725202936114, 0.947173349319, 0.992676628391, 1, 0.996879269744, 0.991020788184], [0.687322471879, 0.921318523517, 0.980284789003, 0.996879269744, 1, 0.99846033011], [0.661260314876, 0.901006701352, 0.96828182239, 0.991020788184, 0.99846033011, 1]]);
        d = zeros([self.order+1]);
        d[0] = (t**10+12*t**9+67*t**8+232*t**7+562*t**6+1024*t**5+1484*t**4+1792*t**3+1847*t**2+1572*t+923)*(1-t) / (1+t)**11 
        d[1] = 7*(17467*t**8+124874*t**7+478036*t**6+1239958*t**5+2345510*t**4+3250918*t**3+3352636*t**2+2454074*t+1028527)*(1-t)**3 / \
                     (1800*u**2*(1+t)**11)
        d[2] = 7*(7121*t**6+43016*t**5+129715*t**4+244880*t**3+295855*t**2+225176*t+87581)*(1-t)**5 / \
                     (72*(2*1)**2 * u**4*(1+t)**11)
        d[3] = 3*(2549*t**4+12072*t**3+24926*t**2+25176*t+11117)*(1-t)**7 / ((3*2*1)**2 * 4*u**6*(1+t)**11)
        d[4] = 14*(113*t**2+316*t+221)*(1-t)**9 / ((4*3*2*1)**2 * u**8*(1+t)**11)
        d[5] = (252*(1-t)**11) / ((5*4*3*2*1)**2 * u**10*(1+t)**11)   
        D = diag( sqrt(d) );
        return D @ K @ D;

    
def makeFMP(order : int, theta : float, tau : float) -> FMPBase:
    if (order == 0) :
        return FMP0(theta, tau);
    elif (order == 1) :
        return FMP1(theta, tau);
    elif (order == 2) :
        return FMP2(theta, tau);
    elif (order == 3) :
        return FMP3(theta, tau);
    elif (order == 4) :
        return FMP4(theta, tau);
    else : # (order == 5) :
        return FMP5(theta, tau);

def thetaFromVrf( order : int, tau : float, vrf : float) -> float:
    '''@x : float'''
    if (order == 0) :
        vrf = max(1e-14, min(1-1e-6, vrf))
        return 2/(1+vrf) - 1;
    elif (order == 1) :
        x = tau**(2./3.)*(vrf * 1./2.)**(1./3.); 
        x = max(1e-14, min(1-1e-6, x))
        return -1. + 2./(1.0+x) 
    elif (order == 2) :
        x = tau**(4./5.)*(vrf * 1./6.)**(1./5.); 
        x = max(1e-14, min(1-1e-6, x))
        return -1. + 2./(1.0+x) 
    elif (order == 3) :
        x = tau**(6./7.)*(vrf * 1./20.)**(1./7.); 
        x = max(1e-14, min(1-1e-6, x))
        return -1. + 2./(1.0+x) 
    elif (order == 4) :
        x = tau**(8./9.)*(vrf * 1./70.)**(1./9.); 
        x = max(1e-14, min(1-1e-6, x))
        return -1. + 2./(1.0+x) 
    else : # (order == 5) :
        x = tau**(10./11.)*(vrf * 14400./252.)**(1./11.); 
        x = max(1e-14, min(1-1e-6, x))
        return -1. + 2./(1.0+x) 
