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
    """
    FMPBase
    
    Base class for the fading memory polynomial filters.
            
    Attributes:
        theta - fading factor
    """

    '''@theta : float'''

    def __init__(self, order : int, theta : float, tau : float) :
        super().__init__(order, tau);
        """
        Constructor
        
        Arguments:
            order - integer polynomial orer
            theta - fading factor
            tau - nominal time step
        """
        self.theta = theta;
        self.n0 = 1;
        
    def getTheta(self) -> float:
        """
        Return the fading factor for the filter
        
        Arguments:
            None
        
        Returns:
            fading factor
        """
        return self.theta;
        
    def _gammaParameter(self, t : float, dtau : float) -> float:
        """@super"""
        return pow(self.theta, abs(dtau))

        
            
class FMP0(FMPBase):    
    """
    FMP0
    
    Class for the 0th order fading memory polynomial filter.
    """

    def __init__(self, theta : float, tau : float):
        super().__init__(0, theta, tau)
        """
        Constructor
        
        Arguments:
            theta - fading factor
            tau - nominal time step
        """

    def _gamma(self, t : float) -> vector:
        """@super"""
        return array([1-t])

    def _VRF(self) -> array:
        """@super"""
        '''@t : float'''
        '''@V : array'''
        t = self.theta
        V = zeros([self.order+1, self.order+1]);
        V[0,0] = ((1-t)/(1+t));
        return V;

class FMP1(FMPBase):    
    """
    FMP1
    
    Class for the 1st order fading memory polynomial filter.
    """

    def __init__(self, theta : float, tau : float) :
        super().__init__(1, theta, tau)
        """
        Constructor
        
        Arguments:
            theta - fading factor
            tau - nominal time step
        """

    def _gamma(self, t : float) -> vector:
        """@super"""
        '''@t2 : float'''
        '''@mt2 : float'''
        t2 = t*t 
        mt2 = (1-t)*(1-t)
        return array([1-t2, 
                      mt2])

    def _VRF(self) -> array:
        """@super"""
        '''@t : float'''
        '''@u : float'''
        '''@V : array'''
        t = self.theta
        u = self.tau;
        V = zeros(self.order+1, self.order+1)
        return V;
        
class FMP2(FMPBase):    
    """
    FMP2
    
    Class for the 2nd order fading memory polynomial filter.
    """

    def __init__(self, theta : float, tau : float) :
        super().__init__(2, theta, tau)
        """
        Constructor
        
        Arguments:
            theta - fading factor
            tau - nominal time step
        """

    def _gamma(self, t : float) -> vector:
        """@super"""
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
        """@super"""
        '''@t : float'''
        '''@u : float'''
        '''@V : array'''
        t = self.theta
        u = self.tau;
        V = zeros(self.order+1, self.order+1)
        return V;

class FMP3(FMPBase):    
    """
    FMP3
    
    Class for the 3rd order fading memory polynomial filter.
    """

    def __init__(self, theta : float, tau : float):
        super().__init__(3, theta, tau)
        """
        Constructor
        
        Arguments:
            theta - fading factor
            tau - nominal time step
        """

    def _gamma(self, t : float) -> vector:
        """@super"""
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
        """@super"""
        '''@t : float'''
        '''@u : float'''
        '''@V : array'''
        t = self.theta
        u = self.tau;
        V = zeros(self.order+1, self.order+1)
        return V;

class FMP4(FMPBase):    
    """
    FMP4
    
    Class for the 4th order fading memory polynomial filter.
    """

    def __init__(self, theta : float, tau : float):
        super().__init__(4, theta, tau)
        """
        Constructor
        
        Arguments:
            theta - fading factor
            tau - nominal time step
        """

    def _gamma(self, t : float) -> vector:
        """@super"""
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
        """@super"""
        '''@t : float'''
        '''@u : float'''
        '''@V : array'''
        t = self.theta
        u = self.tau;
        V = zeros(self.order+1, self.order+1)
        return V;

class FMP5(FMPBase):    
    """
    FMP5
    
    Class for the 5th order fading memory polynomial filter.
    """

    def __init__(self, theta : float, tau : float):
        super().__init__(5, theta, tau)
        """
        Constructor
        
        Arguments:
            theta - fading factor
            tau - nominal time step
        """

    def _gamma(self, t : float) -> vector:
        """@super"""
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
        
    def _VRF(self) -> array:
        """@super"""
        '''@t : float'''
        '''@u : float'''
        '''@V : array'''
        t = self.theta
        u = self.tau;
        V = zeros(self.order+1, self.order+1)
        return V;

    
def makeFMP(order : int, theta : float, tau : float) -> FMPBase:
    """
    Factory for fading memory polynomial filters
    
    Arguments:
        order - integer polynomial orer
        theta - fading factor
        tau - nominal time step
        
    Returns:
        fading memory filter object
    """
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
    """
    Compute the fading factor which give the target value
    
    Determines the theta values which yields a VRF[0,0] element with
    the value vrf at the specified order and nominal time step.
    At some orders and tau values the target may not be achievable
    in these cases the theta value yielding the nearest V[0,0] is
    returned.
    
    Arguments:
        order - integer polynomial orer
        tau - nominal time step
        vrf - target VRF[0,0] value
        
    Returns:
        fading factor
    """
    '''@x : float'''
    if (order == 0) :
        x = max(1e-14, min(1-1e-6, vrf))
        return 2/(1+x) - 1;
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
