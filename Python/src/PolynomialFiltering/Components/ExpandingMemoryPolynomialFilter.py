'''
Created on Feb 13, 2019

@author: NOOK
'''

from typing import Tuple
from abc import abstractmethod

from math import isnan;
from numpy import array, diag, zeros, sqrt, transpose
from numpy import array as vector
from PolynomialFiltering.Components.AbstractRecursiveFilter import AbstractRecursiveFilter

class EMPBase(AbstractRecursiveFilter):
    """
    Base class for expanding memory polynomial filters.
    """
    def __init__(self, order : int, tau : float) :
        super().__init__(order, tau);
        """
        Constructor
        
        Arguments:
            order - integer polynomial orer
            tau - nominal time step
        """
        
    def _gammaParameter(self, t : float, dtau : float) -> float:
        """
        Compute the parameter for the _gamma method
        
        Arguments:
            t - external time
            dtau - internal step
        
        Returns:
            parameter based on filter subclass
        
        """
        return self._normalizeTime(t)
    
    @abstractmethod
    def nSwitch(self, theta : float) -> float:
        """
        Compute the observation count to switch from EMP to FMP
        
        The 0th element of the EMP VRF declines as the number of observations
        increases.  For the FMP the VRF is constant.  This function returns the 
        observation number at which these elements match
        
        Arguments:
            theta - fading factor at which to switch
        
        Returns:
            matching observation count
        
        """
        pass
    

class EMP0(EMPBase) :
    """
    Class for the 0th order expanding memory polynomial filter.
    """

    def __init__(self, tau : float) :
        super().__init__( 0, tau)
        """
        Constructor
        
        Arguments:
            tau - nominal time step
        """
        
    def _gamma(self, n : float) -> vector:
        """@super"""
        return array([1/(1+n)])
    
    def nSwitch(self, theta : float) -> float:
        """@super"""
        return 2.0/(1.0-theta)
    
    def _VRF(self) -> array:
        """@super"""
        '''@n : int'''
        '''@V : array'''
        n = self.n
        V = array([[1.0/(n + 1)]]);
        return V;

    
class EMP1(EMPBase) :
    """
    Class for the 1st order expanding memory polynomial filter.
    """

    def __init__(self, tau : float) :
        super().__init__( 1, tau )
        """
        Constructor
        
        Arguments:
            tau - nominal time step
        """
        
    def _gamma(self, n : float) -> vector: #
        """@super"""
        '''@denom : float'''
        denom = 1.0/((n+2)*(n+1))
        return denom*array([2*(2*n+1), 
                            6])
    
    def nSwitch(self, theta : float) -> float:
        """@super"""
        return 3.2/(1.0-theta)
    '''
K1 = array([[1, 0.866025403784], [0.866025403784, 1]]);
K2 = array([[1, 0.866025403784, 0.7453559925], [0.866025403784, 1, 0.968245836552], [0.7453559925, 0.968245836552, 1]]);
K3 = array([[1, 0.866025403784, 0.7453559925, 0.661437827766], [0.866025403784, 1, 0.968245836552, 0.916515138991], [0.7453559925, 0.968245836552, 1, 0.986013297183], [0.661437827766, 0.916515138991, 0.986013297183, 1]]);
K4 = array([[1, 0.866025403784, 0.7453559925, 0.661437827766, 0.6], [0.866025403784, 1, 0.968245836552, 0.916515138991, 0.866025403784], [0.7453559925, 0.968245836552, 1, 0.986013297183, 0.9583148475], [0.661437827766, 0.916515138991, 0.986013297183, 1, 0.992156741649], [0.6, 0.866025403784, 0.9583148475, 0.992156741649, 1]]);
K5 = array([[1, 0.866025403784, 0.7453559925, 0.661437827766, 0.6, 0.552770798393], [0.866025403784, 1, 0.968245836552, 0.916515138991, 0.866025403784, 0.820651806648], [0.7453559925, 0.968245836552, 1, 0.986013297183, 0.9583148475, 0.927024810887], [0.661437827766, 0.916515138991, 0.986013297183, 1, 0.992156741649, 0.974996043044], [0.6, 0.866025403784, 0.9583148475, 0.992156741649, 1, 0.994987437107], [0.552770798393, 0.820651806648, 0.927024810887, 0.974996043044, 0.994987437107, 1]]);    
    '''
    
    def _VRF(self) -> array:
        """@super"""
        '''@n : int'''
        '''@tau : float'''
        '''@V : array'''
        n = self.n
        if (n < self.order) :
            return zeros([self.order+1, self.order+1]);
        tau = self.tau;
        V = zeros([self.order + 1, self.order + 1]);
        V[0, 0] = 2 * (2 * n + 3) / (n * (n + 1))
        V[0, 1] = 6 / (n * tau * (n + 1))
        V[1, 0] = V[0, 1];
        V[1, 1] = 12 / (n * tau ** 2 * (n + 1) * (n + 2))        
        return V;


class EMP2(EMPBase) :
    """
    Class for the 2nd order expanding memory polynomial filter.
    """

    def __init__(self, tau : float) :
        super().__init__( 2, tau )
        """
        Constructor
        
        Arguments:
            tau - nominal time step
        """
        
    def _gamma(self, n : float) -> vector: #
        """@super"""
        '''@n2 : float'''
        '''@denom : float'''
        n2 = n*n 
        denom = 1.0/((n+3)*(n+2)*(n+1))
        return denom*array([3*(3*n2+3*n+2), 
                            18*(2*n+1), 
                            (2*1)*30])
    
    def nSwitch(self, theta : float) -> float:
        """@super"""
        return 4.3636/(1.0-theta)
    

    def _VRF(self) -> array:
        """@super"""
        '''@n : int'''
        '''@tau : float'''
        '''@V : array'''
        n = self.n
        if (n < self.order) :
            return zeros([self.order+1, self.order+1]);
        tau = self.tau;
        V = zeros([self.order+1, self.order+1]);
        V[0, 0] = 3 * (3 * n ** 2 + 9 * n + 8) / (n * (n ** 2 - 1))
        V[0, 1] = 18 * (2 * n + 3) / (n * tau * (n ** 2 - 1))
        V[1, 0] = V[0, 1];
        V[0, 2] = 60 / (n * tau ** 2 * (n ** 2 - 1))
        V[2, 0] = V[0, 2];
        V[1, 1] = 12 * ((n - 1) * (n + 3) + 15 * (n + 2) ** 2) / (n * tau ** 2 * (n - 1) * (n + 1) * (n + 2) * (n + 3))
        V[1, 2] = 360 / (n * tau ** 3 * (n - 1) * (n + 1) * (n + 3))
        V[2, 1] = V[1, 2];
        V[2, 2] = 720 / (n * tau ** 4 * (n - 1) * (n + 1) * (n + 2) * (n + 3))
        return V;
        
class EMP3(EMPBase) :
    """
    Class for the 3rd order expanding memory polynomial filter.
    """

    def __init__(self, tau : float) :
        super().__init__( 3, tau )
        """
        Constructor
        
        Arguments:
            tau - nominal time step
        """
        
    def _gamma(self, n : float) -> vector: #
        """@super"""
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
        """@super"""
        return 5.50546/(1.0-theta)
    

    def _VRF(self) -> array:
        """@super"""
        '''@n : int'''
        '''@tau : float'''
        '''@V : array'''
        n = self.n
        if (n < self.order) :
            return zeros([self.order+1, self.order+1]);
        tau = self.tau;
        V = zeros([self.order+1, self.order+1]);
        V[0, 0] = 8 * (2 * n ** 3 + 9 * n ** 2 + 19 * n + 15) / (n * (n ** 3 - 2 * n ** 2 - n + 2))
        V[0, 1] = 20 * (6 * n ** 2 + 18 * n + 17) / (n * tau * (n ** 3 - 2 * n ** 2 - n + 2))
        V[1, 0] = V[0, 1];
        V[0, 2] = 240 * (2 * n + 3) / (n * tau ** 2 * (n ** 3 - 2 * n ** 2 - n + 2))
        V[2, 0] = V[0, 2];
        V[0, 3] = 840 / (n * tau ** 3 * (n ** 3 - 2 * n ** 2 - n + 2))
        V[3, 0] = V[0, 3];
        V[1, 1] = 200 * (6 * n ** 4 + 51 * n ** 3 + 159 * n ** 2 + 219 * n + 116) / (n * tau ** 2 * (n ** 6 + 7 * n ** 5 + 7 * n ** 4 - 35 * n ** 3 - 56 * n ** 2 + 28 * n + 48))
        V[1, 2] = 600 * (9 * n ** 2 + 39 * n + 40) / (n * tau ** 3 * (n ** 5 + 5 * n ** 4 - 3 * n ** 3 - 29 * n ** 2 + 2 * n + 24))
        V[2, 1] = V[1, 2];
        V[1, 3] = 1680 * (6 * n ** 2 + 27 * n + 32) / (n * tau ** 4 * (n ** 6 + 7 * n ** 5 + 7 * n ** 4 - 35 * n ** 3 - 56 * n ** 2 + 28 * n + 48))
        V[3, 1] = V[1, 3];
        V[2, 2] = 720 * ((n - 2) * (n + 4) + 35 * (n + 2) ** 2) / (n * tau ** 4 * (n - 2) * (n - 1) * (n + 1) * (n + 2) * (n + 3) * (n + 4))
        V[2, 3] = 50400 / (n * tau ** 5 * (n - 2) * (n - 1) * (n + 1) * (n + 3) * (n + 4))
        V[3, 2] = V[2, 3];
        V[3, 3] = 100800 / (n * tau ** 6 * (n - 2) * (n - 1) * (n + 1) * (n + 2) * (n + 3) * (n + 4))
        return V

class EMP4(EMPBase) :
    """
    Class for the 4th order expanding memory polynomial filter.
    """

    def __init__(self, tau : float) :
        super().__init__( 4, tau )
        """
        Constructor
        
        Arguments:
            tau - nominal time step
        """
        
    def _gamma(self, n : float) -> vector: # 
        """@super"""
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
        """@super"""
        return 6.6321/(1.0-theta)
    

    def _VRF(self) -> array:
        """@super"""
        '''@n : int'''
        '''@tau : float'''
        '''@V : array'''
        n = self.n
        if (n < self.order) :
            return zeros([self.order+1, self.order+1]);
        tau = self.tau;
        V = zeros([self.order+1, self.order+1]);
        V[0, 0] = 5 * (5 * n ** 4 + 30 * n ** 3 + 115 * n ** 2 + 210 * n + 144) / (n * (n ** 4 - 5 * n ** 3 + 5 * n ** 2 + 5 * n - 6))
        V[0, 1] = 50 * (6 * n ** 3 + 27 * n ** 2 + 59 * n + 48) / (n * tau * (n ** 4 - 5 * n ** 3 + 5 * n ** 2 + 5 * n - 6))
        V[1, 0] = V[0, 1];
        V[0, 2] = 2100 * (n ** 2 + 3 * n + 3) / (n * tau ** 2 * (n ** 4 - 5 * n ** 3 + 5 * n ** 2 + 5 * n - 6))
        V[2, 0] = V[0, 2];
        V[0, 3] = 4200 * (2 * n + 3) / (n * tau ** 3 * (n ** 4 - 5 * n ** 3 + 5 * n ** 2 + 5 * n - 6))
        V[3, 0] = V[0, 3];
        V[0, 4] = 15120 / (n * tau ** 4 * (n ** 4 - 5 * n ** 3 + 5 * n ** 2 + 5 * n - 6))
        V[4, 0] = V[0, 4];
        V[1, 1] = 100 * (48 * n ** 6 + 666 * n ** 5 + 3843 * n ** 4 + 11982 * n ** 3 + 21727 * n ** 2 + 21938 * n + 9516) / (n * tau ** 2 * (n ** 8 + 9 * n ** 7 + 6 * n ** 6 - 126 * n ** 5 - 231 * n ** 4 + 441 * n ** 3 + 944 * n ** 2 - 324 * n - 720))
        V[1, 2] = 4200 * (9 * n ** 4 + 84 * n ** 3 + 295 * n ** 2 + 467 * n + 297) / (n * tau ** 3 * (n ** 7 + 7 * n ** 6 - 8 * n ** 5 - 110 * n ** 4 - 11 * n ** 3 + 463 * n ** 2 + 18 * n - 360))
        V[2, 1] = V[1, 2];
        V[1, 3] = 1680 * (96 * n ** 4 + 894 * n ** 3 + 3191 * n ** 2 + 5059 * n + 2940) / (n * tau ** 4 * (n ** 8 + 9 * n ** 7 + 6 * n ** 6 - 126 * n ** 5 - 231 * n ** 4 + 441 * n ** 3 + 944 * n ** 2 - 324 * n - 720))
        V[3, 1] = V[1, 3];
        V[1, 4] = 151200 * (2 * n ** 2 + 11 * n + 19) / (n * tau ** 5 * (n ** 7 + 7 * n ** 6 - 8 * n ** 5 - 110 * n ** 4 - 11 * n ** 3 + 463 * n ** 2 + 18 * n - 360))
        V[4, 1] = V[1, 4];
        V[2, 2] = 35280 * (9 * n ** 4 + 76 * n ** 3 + 239 * n ** 2 + 336 * n + 185) / (n * tau ** 4 * (n ** 8 + 9 * n ** 7 + 6 * n ** 6 - 126 * n ** 5 - 231 * n ** 4 + 441 * n ** 3 + 944 * n ** 2 - 324 * n - 720))
        V[2, 3] = 352800 * (4 * n ** 2 + 17 * n + 18) / (n * tau ** 5 * (n ** 7 + 7 * n ** 6 - 8 * n ** 5 - 110 * n ** 4 - 11 * n ** 3 + 463 * n ** 2 + 18 * n - 360))
        V[3, 2] = V[2, 3];
        V[2, 4] = 302400 * (9 * n ** 2 + 39 * n + 47) / (n * tau ** 6 * (n ** 8 + 9 * n ** 7 + 6 * n ** 6 - 126 * n ** 5 - 231 * n ** 4 + 441 * n ** 3 + 944 * n ** 2 - 324 * n - 720))
        V[4, 2] = V[2, 4];
        V[3, 3] = 100800 * ((n - 3) * (n + 5) + 63 * (n + 2) ** 2) / (n * tau ** 6 * (n - 3) * (n - 2) * (n - 1) * (n + 1) * (n + 2) * (n + 3) * (n + 4) * (n + 5))
        V[3, 4] = 12700800 / (n * tau ** 7 * (n - 3) * (n - 2) * (n - 1) * (n + 1) * (n + 3) * (n + 4) * (n + 5))
        V[4, 3] = V[3, 4];
        V[4, 4] = 25401600 / (n * tau ** 8 * (n - 3) * (n - 2) * (n - 1) * (n + 1) * (n + 2) * (n + 3) * (n + 4) * (n + 5))        
        return V;
    
class EMP5(EMPBase) :
    """
    Class for the 5th order expanding memory polynomial filter.
    """

    def __init__(self, tau : float) :
        super().__init__( 5, tau )
        """
        Constructor
        
        Arguments:
            tau - nominal time step
        """
        
    def _gamma(self, n : float) -> vector:
        """@super"""
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
        """@super"""
        return 7.7478/(1.0-theta)
    
   
    def _VRF(self) -> array:
        """@super"""
        '''@n : int'''
        '''@tau : float'''
        '''@V : array'''
        n = self.n
        if (n < self.order) :
            return zeros([self.order+1, self.order+1]);
        tau = self.tau;
        V = zeros([self.order+1, self.order+1]);
        V[0, 0] = 6 * (6 * n ** 5 + 45 * n ** 4 + 280 * n ** 3 + 855 * n ** 2 + 1334 * n + 840) / (n * (n ** 5 - 9 * n ** 4 + 25 * n ** 3 - 15 * n ** 2 - 26 * n + 24))
        V[0, 1] = 126 * (5 * n ** 4 + 30 * n ** 3 + 115 * n ** 2 + 210 * n + 148) / (n * tau * (n ** 5 - 9 * n ** 4 + 25 * n ** 3 - 15 * n ** 2 - 26 * n + 24))
        V[1, 0] = V[0, 1];
        V[0, 2] = 840 * (8 * n ** 3 + 36 * n ** 2 + 82 * n + 69) / (n * tau ** 2 * (n ** 5 - 9 * n ** 4 + 25 * n ** 3 - 15 * n ** 2 - 26 * n + 24))
        V[2, 0] = V[0, 2];
        V[0, 3] = 7560 * (6 * n ** 2 + 18 * n + 19) / (n * tau ** 3 * (n ** 5 - 9 * n ** 4 + 25 * n ** 3 - 15 * n ** 2 - 26 * n + 24))
        V[3, 0] = V[0, 3];
        V[0, 4] = 90720 * (2 * n + 3) / (n * tau ** 4 * (n ** 5 - 9 * n ** 4 + 25 * n ** 3 - 15 * n ** 2 - 26 * n + 24))
        V[4, 0] = V[0, 4];
        V[0, 5] = 332640 / (n * tau ** 5 * (n ** 5 - 9 * n ** 4 + 25 * n ** 3 - 15 * n ** 2 - 26 * n + 24))
        V[5, 0] = V[0, 5];
        V[1, 1] = 588 * (25 * n ** 8 + 500 * n ** 7 + 4450 * n ** 6 + 23300 * n ** 5 + 79585 * n ** 4 + 181760 * n ** 3 + 267180 * n ** 2 + 226920 * n + 84528) / (n * tau ** 2 * (n ** 10 + 11 * n ** 9 - 330 * n ** 7 - 627 * n ** 6 + 3003 * n ** 5 + 7370 * n ** 4 - 9020 * n ** 3 - 24024 * n ** 2 + 6336 * n + 17280))
        V[1, 2] = 17640 * (10 * n ** 6 + 150 * n ** 5 + 965 * n ** 4 + 3420 * n ** 3 + 7179 * n ** 2 + 8520 * n + 4356) / (n * tau ** 3 * (n ** 9 + 9 * n ** 8 - 18 * n ** 7 - 294 * n ** 6 - 39 * n ** 5 + 3081 * n ** 4 + 1208 * n ** 3 - 11436 * n ** 2 - 1152 * n + 8640))
        V[2, 1] = V[1, 2];
        V[1, 3] = 105840 * (12 * n ** 6 + 177 * n ** 5 + 1125 * n ** 4 + 3870 * n ** 3 + 7550 * n ** 2 + 7954 * n + 3588) / (n * tau ** 4 * (n ** 10 + 11 * n ** 9 - 330 * n ** 7 - 627 * n ** 6 + 3003 * n ** 5 + 7370 * n ** 4 - 9020 * n ** 3 - 24024 * n ** 2 + 6336 * n + 17280))
        V[3, 1] = V[1, 3];
        V[1, 4] = 211680 * (25 * n ** 4 + 270 * n ** 3 + 1205 * n ** 2 + 2400 * n + 1692) / (n * tau ** 5 * (n ** 9 + 9 * n ** 8 - 18 * n ** 7 - 294 * n ** 6 - 39 * n ** 5 + 3081 * n ** 4 + 1208 * n ** 3 - 11436 * n ** 2 - 1152 * n + 8640))
        V[4, 1] = V[1, 4];
        V[1, 5] = 665280 * (15 * n ** 4 + 165 * n ** 3 + 770 * n ** 2 + 1630 * n + 1284) / (n * tau ** 6 * (n ** 10 + 11 * n ** 9 - 330 * n ** 7 - 627 * n ** 6 + 3003 * n ** 5 + 7370 * n ** 4 - 9020 * n ** 3 - 24024 * n ** 2 + 6336 * n + 17280))
        V[5, 1] = V[1, 5];
        V[2, 2] = 70560 * (32 * n ** 6 + 432 * n ** 5 + 2480 * n ** 4 + 7800 * n ** 3 + 14418 * n ** 2 + 14963 * n + 6690) / (n * tau ** 4 * (n ** 10 + 11 * n ** 9 - 330 * n ** 7 - 627 * n ** 6 + 3003 * n ** 5 + 7370 * n ** 4 - 9020 * n ** 3 - 24024 * n ** 2 + 6336 * n + 17280))
        V[2, 3] = 1058400 * (16 * n ** 4 + 144 * n ** 3 + 506 * n ** 2 + 822 * n + 549) / (n * tau ** 5 * (n ** 9 + 9 * n ** 8 - 18 * n ** 7 - 294 * n ** 6 - 39 * n ** 5 + 3081 * n ** 4 + 1208 * n ** 3 - 11436 * n ** 2 - 1152 * n + 8640))
        V[3, 2] = V[2, 3];
        V[2, 4] = 604800 * (120 * n ** 4 + 1068 * n ** 3 + 3766 * n ** 2 + 6047 * n + 3594) / (n * tau ** 6 * (n ** 10 + 11 * n ** 9 - 330 * n ** 7 - 627 * n ** 6 + 3003 * n ** 5 + 7370 * n ** 4 - 9020 * n ** 3 - 24024 * n ** 2 + 6336 * n + 17280))
        V[4, 2] = V[2, 4];
        V[2, 5] = 139708800 * (n ** 2 + 5 * n + 9) / (n * tau ** 7 * (n ** 9 + 9 * n ** 8 - 18 * n ** 7 - 294 * n ** 6 - 39 * n ** 5 + 3081 * n ** 4 + 1208 * n ** 3 - 11436 * n ** 2 - 1152 * n + 8640))
        V[5, 2] = V[2, 5];
        V[3, 3] = 2721600 * (48 * n ** 4 + 402 * n ** 3 + 1274 * n ** 2 + 1828 * n + 1047) / (n * tau ** 6 * (n ** 10 + 11 * n ** 9 - 330 * n ** 7 - 627 * n ** 6 + 3003 * n ** 5 + 7370 * n ** 4 - 9020 * n ** 3 - 24024 * n ** 2 + 6336 * n + 17280))
        V[3, 4] = 114307200 * (5 * n ** 2 + 21 * n + 23) / (n * tau ** 7 * (n ** 9 + 9 * n ** 8 - 18 * n ** 7 - 294 * n ** 6 - 39 * n ** 5 + 3081 * n ** 4 + 1208 * n ** 3 - 11436 * n ** 2 - 1152 * n + 8640))
        V[4, 3] = V[3, 4];
        V[3, 5] = 279417600 * (4 * n ** 2 + 17 * n + 21) / (n * tau ** 8 * (n ** 10 + 11 * n ** 9 - 330 * n ** 7 - 627 * n ** 6 + 3003 * n ** 5 + 7370 * n ** 4 - 9020 * n ** 3 - 24024 * n ** 2 + 6336 * n + 17280))
        V[5, 3] = V[3, 5];
        V[4, 4] = 25401600 * ((n - 4) * (n + 6) + 99 * (n + 2) ** 2) / (n * tau ** 8 * (n - 4) * (n - 3) * (n - 2) * (n - 1) * (n + 1) * (n + 2) * (n + 3) * (n + 4) * (n + 5) * (n + 6))
        V[4, 5] = 5029516800 / (n * tau ** 9 * (n - 4) * (n - 3) * (n - 2) * (n - 1) * (n + 1) * (n + 3) * (n + 4) * (n + 5) * (n + 6))
        V[5, 4] = V[4, 5];
        V[5, 5] = 10059033600 / (n * tau ** 10 * (n - 4) * (n - 3) * (n - 2) * (n - 1) * (n + 1) * (n + 2) * (n + 3) * (n + 4) * (n + 5) * (n + 6))        
        return V;
    
def makeEMP(order : int, tau : float) -> EMPBase:
    """
    Factory for expanding memory polynomial filters
    
    Arguments:
        order - integer polynomial orer
        tau - nominal time step
        
    Returns:
        expanding memory filter object
    """
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
