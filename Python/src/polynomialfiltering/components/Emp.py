''' PolynomialFiltering.components.Emp
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

from typing import Tuple
from abc import abstractmethod
from polynomialfiltering.PythonUtilities import forcestatic

from math import isnan, exp, log;
from numpy import array, diag, zeros, sqrt, transpose
from numpy import array as vector
from polynomialfiltering.components.ICore import ICore
from polynomialfiltering.filters.RecursivePolynomialFilter import RecursivePolynomialFilter

class CoreEmp0(ICore) :
    """
    Class for the 0th order expanding memory polynomial filter.
    """

    '''@ order : int'''
    '''@ tau : float '''
    
    def __init__(self, tau : float) :
        super().__init__()
        """
        Constructor
        
        Arguments:
            tau - nominal time step
        """
        self.order = 0;
        self.tau = tau;
        
    def getSamplesToStart(self) -> int:
        return self.order + 2
        
    def getGamma(self, n : float, dtau : float) -> vector:
        """@super"""
        
        '''@g : vector : 1'''       
        g = array([1.0/(1.0+n)])
        return g;
    
    def getFirstVRF(self, n : int) -> float:
        return self._getFirstVRF(n, self.tau)

    def getLastVRF(self, n : int) -> float:
        return self._getLastVRF(n, self.tau)
    
    def getDiagonalVRF(self, n : int) -> array:
        return self._getDiagonalVRF(n, self.tau)

    def getVRF(self, n : int) -> array:
        return self._getVRF(n, self.tau)
    
    def _getFirstVRF(self, n : float, tau : float ) -> float:
        return 1.0/(n+1.0)

    def _getLastVRF(self, n : float, tau : float ) -> float:
        return 1.0/(n+1.0)

    def _getDiagonalVRF(self, n : float, tau : float ) -> array:
        '''@ V : array : order + 1 : order + 1'''
        V = zeros([self.order + 1, self.order + 1]);
        V[0,0]=self._getFirstVRF(n, tau);
        return V;

    def _getVRF(self, n : float, tau : float ) -> array:
        '''@ V : array : order + 1 : order + 1'''
        V = self._getDiagonalVRF(n, tau)
        return V;


    
class CoreEmp1(ICore) :
    """
    Class for the 1st order expanding memory polynomial filter.
    """

    '''@ order : int'''
    '''@ tau : float '''

    def __init__(self, tau : float) :
        super().__init__()
        """
        Constructor
        
        Arguments:
            tau - nominal time step
        """
        self.order = 1;
        self.tau = tau;
        
    def getSamplesToStart(self) -> int:
        return self.order + 2
        
    def getGamma(self, n : float, dtau : float) -> vector: #
        """@super"""
        '''@denom : float'''
        '''@g : vector : 2'''       
        denom = 1.0/((n+2)*(n+1))
        g = array([2.0*(2.0*n+1.0), 
                            6.0])
        g = denom*g;
        return g;
        
    def getFirstVRF(self, n : int) -> float:
        return self._getFirstVRF(n, self.tau)

    def getLastVRF(self, n : int) -> float:
        return self._getLastVRF(n, self.tau)
    
    def getDiagonalVRF(self, n : int) -> array:
        return self._getDiagonalVRF(n, self.tau)

    def getVRF(self, n : int) -> array:
        return self._getVRF(n, self.tau)
    
    def _getFirstVRF(self, n : float, tau : float ) -> float:
        return 2.0*(2.0*n+3.0)/(n*(n+1.0));

    def _getLastVRF(self, n : float, tau : float ) -> float:
        return 12.0/(n*tau**2*(n+1.0)*(n+2.0));

    def _getDiagonalVRF(self, n : float, tau : float ) -> array:
        '''@ V : array : 2 : 2'''
        V = zeros([self.order+1, self.order+1]);
        V[0,0]=self._getFirstVRF(n, tau);
        V[1,1]=self._getLastVRF(n, tau);
        return V;

    def _getVRF(self, n : float, tau : float ) -> array:
        '''@ V : array : 2 : 2'''
        V = self._getDiagonalVRF(n, tau)
        V[0,1]=6.0/(n*tau*(n+1.0))
        V[1,0]=V[0,1];
        return V;




class CoreEmp2(ICore) :
    """
    Class for the 2nd order expanding memory polynomial filter.
    """

    '''@ order : int'''
    '''@ tau : float '''

    def __init__(self, tau : float) :
        super().__init__()
        """
        Constructor
        
        Arguments:
            tau - nominal time step
        """
        self.order = 2;
        self.tau = tau;
        
    def getSamplesToStart(self) -> int:
        return self.order + 2
        
    def getGamma(self, n : float, dtau : float) -> vector: #
        """@super"""
        '''@n2 : float'''
        '''@denom : float'''
        '''@g : vector : 3'''       
        n2 = n*n 
        denom = 1.0/((n+3)*(n+2)*(n+1))
        g = array([3.0*(3.0*n2+3.0*n+2.0), 
                            18.0*(2.0*n+1.0), 
                            (2.0*1.0)*30.0])
        g = denom*g;
        return g;        
    
    def getFirstVRF(self, n : int) -> float:
        return self._getFirstVRF(n, self.tau)

    def getLastVRF(self, n : int) -> float:
        return self._getLastVRF(n, self.tau)
    
    def getDiagonalVRF(self, n : int) -> array:
        return self._getDiagonalVRF(n, self.tau)

    def getVRF(self, n : int) -> array:
        return self._getVRF(n, self.tau)
    
    def _getFirstVRF(self, n : float, tau : float ) -> float:
        return 3.0*(3.0*n**2+9.0*n+8.0)/(n*(n**2-1.0));

    def _getLastVRF(self, n : float, tau : float ) -> float:
        return 720.0/(n*tau**4*(n-1.0)*(n+1.0)*(n+2.0)*(n+3.0));

    def _getDiagonalVRF(self, n : float, tau : float ) -> array:
        '''@ V : array : order + 1 : order + 1'''
        V = zeros([self.order+1, self.order+1]);
        V[0,0]=self._getFirstVRF(n, tau);
        V[1,1]=12.0*((n-1.0)*(n+3.0)+15.0*(n+2.0)**2)/(n*tau**2*(n-1.0)*(n+1.0)*(n+2.0)*(n+3.0))
        V[2,2]=self._getLastVRF(n, tau);
        return V;

    def _getVRF(self, n : float, tau : float ) -> array:
        '''@ V : array : order + 1 : order + 1'''
        V = self._getDiagonalVRF(n, tau)
        V[0,1]=18.0*(2.0*n+3.0)/(n*tau*(n**2-1.0))
        V[1,0]=V[0,1];
        V[0,2]=60.0/(n*tau**2*(n**2-1.0))
        V[2,0]=V[0,2];
        V[1,2]=360.0/(n*tau**3*(n-1.0)*(n+1.0)*(n+3.0))
        V[2,1]=V[1,2];
        return V;
    
        
        
class CoreEmp3(ICore) :
    """
    Class for the 3rd order expanding memory polynomial filter.
    """

    '''@ order : int'''
    '''@ tau : float '''

    def __init__(self, tau : float) :
        super().__init__()
        """
        Constructor
        
        Arguments:
            tau - nominal time step
        """
        self.order = 3;
        self.tau = tau;
        
    def getSamplesToStart(self) -> int:
        return self.order + 2
        
    def getGamma(self, n : float, dtau : float) -> vector: #
        """@super"""
        '''@n2 : float'''
        '''@n3 : float'''
        '''@denom : float'''
        '''@g : vector : 4'''       
        n2 = n*n 
        n3 = n2*n 
        denom = 1.0/((n+4)*(n+3)*(n+2)*(n+1))
        g = array([8.0*(2.0*n3+3.0*n2+7.0*n+3.0), 
                            20.0*(6.0*n2+6.0*n+5.0), 
                            (2.0*1.0)*120.0*(2.0*n+1.0), # 
                            (3.0*2.0*1.0)*140.0])   # 
        g = denom*g;
        return g;
    
    def getFirstVRF(self, n : int) -> float:
        return self._getFirstVRF(n, self.tau)

    def getLastVRF(self, n : int) -> float:
        return self._getLastVRF(n, self.tau)
    
    def getDiagonalVRF(self, n : int) -> array:
        return self._getDiagonalVRF(n, self.tau)

    def getVRF(self, n : int) -> array:
        return self._getVRF(n, self.tau)

    def _getFirstVRF(self, n : float, tau : float ) -> float:
        return 8.0*(2.0*n**3+9.0*n**2+19.0*n+15.0)/(n*(n**3-2.0*n**2-n+2.0));

    def _getLastVRF(self, n : float, tau : float ) -> float:
        return 100800.0/(n*tau**6*(n-2.0)*(n-1.0)*(n+1.0)*(n+2.0)*(n+3.0)*(n+4.0));

    def _getDiagonalVRF(self, n : float, tau : float ) -> array:
        '''@ V : array : order + 1 : order + 1'''
        V = zeros([self.order+1, self.order+1]);
        V[0,0]=self._getFirstVRF(n, tau);
        V[1,1]=200.0*(6.0*n**4+51.0*n**3+159.0*n**2+219.0*n+116.0)/(n*tau**2*(n**6+7.0*n**5+7.0*n**4-35.0*n**3-56.0*n**2+28.0*n+48.0))
        V[2,2]=720.0*((n-2.0)*(n+4.0)+35.0*(n+2.0)**2)/(n*tau**4*(n-2.0)*(n-1.0)*(n+1.0)*(n+2.0)*(n+3.0)*(n+4.0))
        V[3,3]=self._getLastVRF(n, tau);
        return V;

    def _getVRF(self, n : float, tau : float ) -> array:
        '''@ V : array : order + 1 : order + 1'''
        V = self._getDiagonalVRF(n, tau)
        V[0,1]=20.0*(6.0*n**2+18.0*n+17.0)/(n*tau*(n**3-2.0*n**2-n+2.0))
        V[1,0]=V[0,1];
        V[0,2]=240.0*(2.0*n+3.0)/(n*tau**2*(n**3-2.0*n**2-n+2.0))
        V[2,0]=V[0,2];
        V[0,3]=840.0/(n*tau**3*(n**3-2.0*n**2-n+2.0))
        V[3,0]=V[0,3];
        V[1,2]=600.0*(9.0*n**2+39.0*n+40.0)/(n*tau**3*(n**5+5.0*n**4-3.0*n**3-29.0*n**2+2.0*n+24.0))
        V[2,1]=V[1,2];
        V[1,3]=1680.0*(6.0*n**2+27.0*n+32.0)/(n*tau**4*(n**6+7.0*n**5+7.0*n**4-35.0*n**3-56.0*n**2+28.0*n+48.0))
        V[3,1]=V[1,3];
        V[2,3]=50400.0/(n*tau**5*(n-2.0)*(n-1.0)*(n+1.0)*(n+3.0)*(n+4.0))
        V[3,2]=V[2,3];
        return V;


class CoreEmp4(ICore) :
    """
    Class for the 4th order expanding memory polynomial filter.
    """

    '''@ order : int'''
    '''@ tau : float '''

    def __init__(self, tau : float) :
        super().__init__()
        """
        Constructor
        
        Arguments:
            tau - nominal time step
        """
        self.order = 4;
        self.tau = tau;
        
    def getSamplesToStart(self) -> int:
        return self.order + 2
        
    def getGamma(self, n : float, dtau : float) -> vector: # 
        """@super"""
        '''@n2 : float'''
        '''@n3 : float'''
        '''@n4 : float'''
        '''@denom : float'''
        '''@g : vector : 5'''       
        n2 = n*n 
        n3 = n2*n 
        n4 = n2*n2
        denom = 1.0/((n+5)*(n+4)*(n+3)*(n+2)*(n+1))
        g = array([5.0*(5.0*n4+10.0*n3+55.0*n2+50.0*n+24.0), 
                            25.0*(12.0*n3+18.0*n2+46.0*n+20.0), 
                            (2.0*1.0)*1050.0*(n2+n+1.0), # 
                            (3.0*2.0*1.0)*700.0*(2.0*n+1.0),  # 
                            (4.0*3.0*2.0*1.0)*630.0]) #
        g = denom*g;
        return g;
    
    def getFirstVRF(self, n : int) -> float:
        return self._getFirstVRF(n, self.tau)

    def getLastVRF(self, n : int) -> float:
        return self._getLastVRF(n, self.tau)
    
    def getDiagonalVRF(self, n : int) -> array:
        return self._getDiagonalVRF(n, self.tau)

    def getVRF(self, n : int) -> array:
        return self._getVRF(n, self.tau)
    
    def _getFirstVRF(self, n : float, tau : float ) -> float:
        return 5.0*(5.0*n**4+30.0*n**3+115.0*n**2+210.0*n+144.0)/(n*(n**4-5.0*n**3+5.0*n**2+5.0*n-6.0));

    def _getLastVRF(self, n : float, tau : float ) -> float:
        return 25401600.0/(n*tau**8*(n-3.0)*(n-2.0)*(n-1.0)*(n+1.0)*(n+2.0)*(n+3.0)*(n+4.0)*(n+5.0));

    def _getDiagonalVRF(self, n : float, tau : float ) -> array:
        '''@ V : array : order + 1 : order + 1'''
        V = zeros([self.order+1, self.order+1]);
        V[0,0]=self._getFirstVRF(n, tau);
        V[1,1]=100.0*(48.0*n**6+666.0*n**5+3843.0*n**4+11982.0*n**3+21727.0*n**2+21938.0*n+9516.0)/(n*tau**2*(n**8+9.0*n**7+6.0*n**6-126.0*n**5-231.0*n**4+441.0*n**3+944.0*n**2-324.0*n-720.0))
        V[2,2]=35280.0*(9.0*n**4+76.0*n**3+239.0*n**2+336.0*n+185.0)/(n*tau**4*(n**8+9.0*n**7+6.0*n**6-126.0*n**5-231.0*n**4+441.0*n**3+944.0*n**2-324.0*n-720.0))
        V[3,3]=100800.0*((n-3.0)*(n+5.0)+63.0*(n+2.0)**2)/(n*tau**6*(n-3.0)*(n-2.0)*(n-1.0)*(n+1.0)*(n+2.0)*(n+3.0)*(n+4.0)*(n+5.0))
        V[4,4]=self._getLastVRF(n, tau);
        return V;

    def _getVRF(self, n : float, tau : float ) -> array:
        '''@ V : array : order + 1 : order + 1'''
        V = self._getDiagonalVRF(n, tau)
        V[0,1]=50.0*(6.0*n**3+27.0*n**2+59.0*n+48.0)/(n*tau*(n**4-5.0*n**3+5.0*n**2+5.0*n-6.0))
        V[1,0]=V[0,1];
        V[0,2]=2100.0*(n**2+3.0*n+3.0)/(n*tau**2*(n**4-5.0*n**3+5.0*n**2+5.0*n-6.0))
        V[2,0]=V[0,2];
        V[0,3]=4200.0*(2.0*n+3.0)/(n*tau**3*(n**4-5.0*n**3+5.0*n**2+5.0*n-6.0))
        V[3,0]=V[0,3];
        V[0,4]=15120.0/(n*tau**4*(n**4-5.0*n**3+5.0*n**2+5.0*n-6.0))
        V[4,0]=V[0,4];
        V[1,2]=4200.0*(9.0*n**4+84.0*n**3+295.0*n**2+467.0*n+297.0)/(n*tau**3*(n**7+7.0*n**6-8.0*n**5-110.0*n**4-11.0*n**3+463.0*n**2+18.0*n-360.0))
        V[2,1]=V[1,2];
        V[1,3]=1680.0*(96.0*n**4+894.0*n**3+3191.0*n**2+5059.0*n+2940.0)/(n*tau**4*(n**8+9.0*n**7+6.0*n**6-126.0*n**5-231.0*n**4+441.0*n**3+944.0*n**2-324.0*n-720.0))
        V[3,1]=V[1,3];
        V[1,4]=151200.0*(2.0*n**2+11.0*n+19.0)/(n*tau**5*(n**7+7.0*n**6-8.0*n**5-110.0*n**4-11.0*n**3+463.0*n**2+18.0*n-360.0))
        V[4,1]=V[1,4];
        V[2,3]=352800.0*(4.0*n**2+17.0*n+18.0)/(n*tau**5*(n**7+7.0*n**6-8.0*n**5-110.0*n**4-11.0*n**3+463.0*n**2+18.0*n-360.0))
        V[3,2]=V[2,3];
        V[2,4]=302400.0*(9.0*n**2+39.0*n+47.0)/(n*tau**6*(n**8+9.0*n**7+6.0*n**6-126.0*n**5-231.0*n**4+441.0*n**3+944.0*n**2-324.0*n-720.0))
        V[4,2]=V[2,4];
        V[3,4]=12700800.0/(n*tau**7*(n-3.0)*(n-2.0)*(n-1.0)*(n+1.0)*(n+3.0)*(n+4.0)*(n+5.0))
        V[4,3]=V[3,4];
        return V;


class CoreEmp5(ICore) :
    """
    Class for the 5th order expanding memory polynomial filter.
    """

    '''@ order : int'''
    '''@ tau : float '''

    def __init__(self, tau : float) :
        super().__init__()
        """
        Constructor
        
        Arguments:
            tau - nominal time step
        """
        self.order = 5;
        self.tau = tau;
        
    def getSamplesToStart(self) -> int:
        return self.order + 2
        
    def getGamma(self, n : float, dtau : float) -> vector:
        """@super"""
        '''@n2 : float'''
        '''@n3 : float'''
        '''@n4 : float'''
        '''@denom : float'''
        '''@g : vector : 6'''       
        n2 = n*n 
        n3 = n2*n 
        n4 = n2*n2
        denom = 1.0/((n+6)*(n+5)*(n+4)*(n+3)*(n+2)*(n+1))
        g = array([6.0*(2.0*n+1.0)*(3.0*n4+6.0*n3+77.0*n2+74.0*n+120.0), 
                            126.0*(5.0*n4+10.0*n3+55.0*n2+50.0*n+28.0), 
                            (2.0*1.0)*420.0*(2.0*n+1.0)*(4.0*n2+4.0*n+15.0), #
                            (3.0*2.0*1.0)*1260.0*(6.0*n2+6.0*n+7.0), #  
                            (4.0*3.0*2.0*1.0)*3780.0*(2.0*n+1.0),  # 
                            (5.0*4.0*3.0*2.0*1.0)*2772.0]) #
        g = denom*g;
        return g;
           
    def getFirstVRF(self, n : int) -> float:
        return self._getFirstVRF(n, self.tau)

    def getLastVRF(self, n : int) -> float:
        return self._getLastVRF(n, self.tau)
    
    def getDiagonalVRF(self, n : int) -> array:
        return self._getDiagonalVRF(n, self.tau)

    def getVRF(self, n : int) -> array:
        return self._getVRF(n, self.tau)
    
    def _getFirstVRF(self, n : float, tau : float ) -> float:
        return 6.0*(6.0*n**5+45.0*n**4+280.0*n**3+855.0*n**2+1334.0*n+840.0)/(n*(n**5-9.0*n**4+25.0*n**3-15.0*n**2-26.0*n+24.0));

    def _getLastVRF(self, n : float, tau : float ) -> float:
        return 10059033600.0/(n*tau**10.0*(n-4.0)*(n-3.0)*(n-2.0)*(n-1.0)*(n+1.0)*(n+2.0)*(n+3.0)*(n+4.0)*(n+5.0)*(n+6.0));

    def _getDiagonalVRF(self, n : float, tau : float ) -> array:
        '''@ V : array : order + 1 : order + 1'''
        V = zeros([self.order+1, self.order+1]);
        V[0,0]=self._getFirstVRF(n, tau);
        V[1,1]=588.0*(25.0*n**8+500.0*n**7+4450.0*n**6+23300.0*n**5+79585.0*n**4+181760.0*n**3+267180.0*n**2+226920.0*n+84528.0)/(n*tau**2*(n**10.0+11.0*n**9-330.0*n**7-627.0*n**6+3003.0*n**5+7370.0*n**4-9020.0*n**3-24024.0*n**2+6336.0*n+17280.0))
        V[2,2]=70560.0*(32.0*n**6+432.0*n**5+2480.0*n**4+7800.0*n**3+14418.0*n**2+14963.0*n+6690.0)/(n*tau**4*(n**10.0+11.0*n**9-330.0*n**7-627.0*n**6+3003.0*n**5+7370.0*n**4-9020.0*n**3-24024.0*n**2+6336.0*n+17280.0))
        V[3,3]=2721600.0*(48.0*n**4+402.0*n**3+1274.0*n**2+1828.0*n+1047.0)/(n*tau**6*(n**10.0+11.0*n**9-330.0*n**7-627.0*n**6+3003.0*n**5+7370.0*n**4-9020.0*n**3-24024.0*n**2+6336.0*n+17280.0))
        V[4,4]=25401600.0*((n-4.0)*(n+6.0)+99.0*(n+2.0)**2)/(n*tau**8*(n-4.0)*(n-3.0)*(n-2.0)*(n-1.0)*(n+1.0)*(n+2.0)*(n+3.0)*(n+4.0)*(n+5.0)*(n+6.0))
        V[5,5]=self._getLastVRF(n, tau);
        return V;

    def _getVRF(self, n : float, tau : float ) -> array:
        '''@ V : array : order + 1 : order + 1'''
        V = self._getDiagonalVRF(n, tau)
        V[0,1]=126.0*(5.0*n**4+30.0*n**3+115.0*n**2+210.0*n+148.0)/(n*tau*(n**5-9.0*n**4+25.0*n**3-15.0*n**2-26.0*n+24.0))
        V[1,0]=V[0,1];
        V[0,2]=840.0*(8.0*n**3+36.0*n**2+82.0*n+69.0)/(n*tau**2*(n**5-9.0*n**4+25.0*n**3-15.0*n**2-26.0*n+24.0))
        V[2,0]=V[0,2];
        V[0,3]=7560.0*(6.0*n**2+18.0*n+19.0)/(n*tau**3*(n**5-9.0*n**4+25.0*n**3-15.0*n**2-26.0*n+24.0))
        V[3,0]=V[0,3];
        V[0,4]=90720.0*(2.0*n+3.0)/(n*tau**4*(n**5-9.0*n**4+25.0*n**3-15.0*n**2-26.0*n+24.0))
        V[4,0]=V[0,4];
        V[0,5]=332640.0/(n*tau**5*(n**5-9.0*n**4+25.0*n**3-15.0*n**2-26.0*n+24.0))
        V[5,0]=V[0,5];
        V[1,2]=17640.0*(10.0*n**6+150.0*n**5+965.0*n**4+3420.0*n**3+7179.0*n**2+8520.0*n+4356.0)/(n*tau**3*(n**9+9.0*n**8-18.0*n**7-294.0*n**6-39.0*n**5+3081.0*n**4+1208.0*n**3-11436.0*n**2-1152.0*n+8640.0))
        V[2,1]=V[1,2];
        V[1,3]=105840.0*(12.0*n**6+177.0*n**5+1125.0*n**4+3870.0*n**3+7550.0*n**2+7954.0*n+3588.0)/(n*tau**4*(n**10.0+11.0*n**9-330.0*n**7-627.0*n**6+3003.0*n**5+7370.0*n**4-9020.0*n**3-24024.0*n**2+6336.0*n+17280.0))
        V[3,1]=V[1,3];
        V[1,4]=211680.0*(25.0*n**4+270.0*n**3+1205.0*n**2+2400.0*n+1692.0)/(n*tau**5*(n**9+9.0*n**8-18.0*n**7-294.0*n**6-39.0*n**5+3081.0*n**4+1208.0*n**3-11436.0*n**2-1152.0*n+8640.0))
        V[4,1]=V[1,4];
        V[1,5]=665280.0*(15.0*n**4+165.0*n**3+770.0*n**2+1630.0*n+1284.0)/(n*tau**6*(n**10.0+11.0*n**9-330.0*n**7-627.0*n**6+3003.0*n**5+7370.0*n**4-9020.0*n**3-24024.0*n**2+6336.0*n+17280.0))
        V[5,1]=V[1,5];
        V[2,3]=1058400.0*(16.0*n**4+144.0*n**3+506.0*n**2+822.0*n+549.0)/(n*tau**5*(n**9+9.0*n**8-18.0*n**7-294.0*n**6-39.0*n**5+3081.0*n**4+1208.0*n**3-11436.0*n**2-1152.0*n+8640.0))
        V[3,2]=V[2,3];
        V[2,4]=604800.0*(120.0*n**4+1068.0*n**3+3766.0*n**2+6047.0*n+3594.0)/(n*tau**6*(n**10.0+11.0*n**9-330.0*n**7-627.0*n**6+3003.0*n**5+7370.0*n**4-9020.0*n**3-24024.0*n**2+6336.0*n+17280.0))
        V[4,2]=V[2,4];
        V[2,5]=139708800.0*(n**2+5.0*n+9.0)/(n*tau**7*(n**9+9.0*n**8-18.0*n**7-294.0*n**6-39.0*n**5+3081.0*n**4+1208.0*n**3-11436.0*n**2-1152.0*n+8640.0))
        V[5,2]=V[2,5];
        V[3,4]=114307200.0*(5.0*n**2+21.0*n+23.0)/(n*tau**7*(n**9+9.0*n**8-18.0*n**7-294.0*n**6-39.0*n**5+3081.0*n**4+1208.0*n**3-11436.0*n**2-1152.0*n+8640.0))
        V[4,3]=V[3,4];
        V[3,5]=279417600.0*(4.0*n**2+17.0*n+21.0)/(n*tau**8*(n**10.0+11.0*n**9-330.0*n**7-627.0*n**6+3003.0*n**5+7370.0*n**4-9020.0*n**3-24024.0*n**2+6336.0*n+17280.0))
        V[5,3]=V[3,5];
        V[4,5]=5029516800.0/(n*tau**9*(n-4.0)*(n-3.0)*(n-2.0)*(n-1.0)*(n+1.0)*(n+3.0)*(n+4.0)*(n+5.0)*(n+6.0))
        V[5,4]=V[4,5];
        return V;

@forcestatic
def nSwitch(order : int, theta : float) -> float:
    """
    Estimate the sample number when the first VRF diagonal elements of an EMP/FMP pair will match
    
    Uses approximate relationships to estimate the switchover point for an EMP/FMP pair when the
    0th element of the VRF diagonals will match, e.g. approximately equal noise reduction.  The 
    approximations are more accurate as theta approaches one.
    
    Arguments:
         order - polynomial filter order
         theta - FMP fading factor
         
    Returns:
        n - estimated crossover sample number
       
    """
    
    if (1.0 - theta <= 0.0) :
        return 0.0;
    if (order == 0) :
        return 2.0/(1.0-theta)
    elif (order == 1.0) :
        return 3.2/(1.0-theta)
    elif (order == 2.0) :
        return 4.3636/(1.0-theta)
    elif (order == 3.0) :
        return 5.50546/(1.0-theta)
    elif (order == 4.0) :
        return 6.6321/(1.0-theta)
    elif (order == 5.0) :
        return 7.7478/(1.0-theta)
    else :
        raise ValueError("Polynomial orders < 0.0 or > 5.0 are not supported")

@forcestatic
def nUnitLastVRF( order : int, tau : float ) -> int:
    """
    Estimate the sample number when the final VRF diagonal value is one or less
    
    Uses curve fits to estimate the sample number when the final VRF diagonal element
    first approaches zero.  For larger tau values, will return the first value value
    for this element.
    
    Arguments:
        order - polynomial filter order
        tau - default time step 
        
    Returns:
        n - estimated sample number
    """
    if (order == 0) :
        return 1+0;
    elif (order == 1.0) :
        return 1+int(max(order, exp(-0.7469*log(tau) + 0.3752)));
    elif (order == 2.0) :
        return 1+int(max(order, exp(-0.8363*log(tau) + 1.1127)));
    elif (order == 3.0) :
        return 1+int(max(order, exp(-0.8753*log(tau) + 1.5427)));
    elif (order == 4.0) :
        return 1+int(max(order, exp(-0.897*log(tau) + 1.8462))); 
    else :
        return 1+int(max(order, exp(-0.9108*log(tau) + 2.0805))); 
        
@forcestatic
def makeEmpCore(order : int, tau : float) -> ICore:
    """
    Factory for expanding memory polynomial filters
    
    Arguments:
        order - integer polynomial orer
        tau - nominal time step
        
    Returns:
        expanding memory filter object
    """
    if (order == 0) :
        return CoreEmp0(tau);
    elif (order == 1.0) :
        return CoreEmp1(tau);
    elif (order == 2.0) :
        return CoreEmp2(tau);
    elif (order == 3.0) :
        return CoreEmp3(tau);
    elif (order == 4.0) :
        return CoreEmp4(tau);
    else : # (order == 5.0) :
        return CoreEmp5(tau);
    
@forcestatic
def makeEmp(order : int, tau : float) -> RecursivePolynomialFilter:
    '''@core : ICore'''
    core = makeEmpCore(order, tau);
    return RecursivePolynomialFilter(order, tau, core)


