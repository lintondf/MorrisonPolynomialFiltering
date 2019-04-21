''' PolynomialFiltering.components.Emp (C) Copyright 2019 - Blue Lightning Development, LLC. D. F. Linton. support@BlueLightningDevelopment.com SPDX-License-Identifier: MIT See separate LICENSE file for full text'''from typing import Tuplefrom abc import abstractmethodfrom math import isnan;from numpy import array, diag, zeros, sqrt, transposefrom numpy import array as vectorfrom polynomialfiltering.components.RecursivePolynomialFilter import ICore, RecursivePolynomialFilterclass CoreEmp0(ICore) :    """    Class for the 0th order expanding memory polynomial filter.    """    def __init__(self, tau : float) :        super().__init__()        """        Constructor                Arguments:            tau - nominal time step        """        self.order = 0;        self.tau = tau;            def getGamma(self, n : float, dtau : float) -> vector:        """@super"""        return array([1/(1+n)])        def getFirstVariance(self)->float:        return self.getVRF()[0,0];    def getLastVariance(self)->float:        return self.getVRF()[self.order,self.order];    def getVRF(self, n : int) -> array:        """@super"""        '''@n : int'''        '''@V : array'''        V = zeros([self.order + 1, self.order + 1]);        V[0,0]=1.0/(n+1)
        return V;        def _getFirstVRF(self, n : int, tau : float ) -> float:        return 2*(2*n+1)/(n**2+3*n+2);    def _getLastVRF(self, n : int, tau : float ) -> float:        return 12/(n*tau**2*(n+1)*(n+2));    def _getDiagonalVRF(self, n : int, tau : float ) -> array:        V = zeros([self.order + 1, self.order + 1]);        V[0,0]=self._getFirstVRF(n, tau);        V[1,1]=self._getLastVRF(n, tau);        return V;    def _getVRF(self, n : int, tau : float ) -> array:        V = self._getDiagonalVRF(n, tau)        V[0,1]=6/(tau*(n+1)*(n+2))        V[1,0]=V[0,1];        return V;    class CoreEmp1(ICore) :    """    Class for the 1st order expanding memory polynomial filter.    """    def __init__(self, tau : float) :        super().__init__()        """        Constructor                Arguments:            tau - nominal time step        """        self.order = 1;        self.tau = tau;            def getGamma(self, n : float, dtau : float) -> vector: #        """@super"""        '''@denom : float'''        denom = 1.0/((n+2)*(n+1))        return denom*array([2*(2*n+1),                             6])            def getFirstVariance(self)->float:        return self.getVRF()[0,0];    def getLastVariance(self)->float:        return self.getVRF()[self.order,self.order];    def getVRF(self, n : int) -> array:        """@super"""        '''@n : int'''        '''@tau : float'''        '''@V : array'''        if (n < self.order) :            return zeros([self.order+1, self.order+1]);        tau = self.tau;        V = zeros([self.order + 1, self.order + 1]);        V[0,0]=2*(2*n+1)/(n**2+3*n+2)
        V[0,1]=6/(tau*(n+1)*(n+2))
        V[1,0]=V[0,1];
        V[1,1]=12/(n*tau**2*(n+1)*(n+2))
        return V;        def _getFirstVRF(self, n : int, tau : float ) -> float:        return 3*(3*n**2+3*n+2)/(n**3+6*n**2+11*n+6);    def _getLastVRF(self, n : int, tau : float ) -> float:        return 720/(n*tau**4*(n-1)*(n+1)*(n+2)*(n+3));    def _getDiagonalVRF(self, n : int, tau : float ) -> array:        V = zeros([self.order+1, self.order+1]);        V[0,0]=self._getFirstVRF(n, tau);        V[1,1]=12*(15*n**2+(n-1)*(n+3))/(n*tau**2*(n-1)*(n+1)*(n+2)*(n+3))        V[2,2]=self._getLastVRF(n, tau);        return V;    def _getVRF(self, n : int, tau : float ) -> array:        V = self._getDiagonalVRF(n, tau)        V[0,1]=18*(2*n+1)/(tau*(n+1)*(n+2)*(n+3))        V[1,0]=V[0,1];        V[0,2]=60/(tau**2*(n+1)*(n+2)*(n+3))        V[2,0]=V[0,2];        V[1,2]=360/(tau**3*(n-1)*(n+1)*(n+2)*(n+3))        V[2,1]=V[1,2];        return V;class CoreEmp2(ICore) :    """    Class for the 2nd order expanding memory polynomial filter.    """    def __init__(self, tau : float) :        super().__init__()        """        Constructor                Arguments:            tau - nominal time step        """        self.order = 2;        self.tau = tau;            def getGamma(self, n : float, dtau : float) -> vector: #        """@super"""        '''@n2 : float'''        '''@denom : float'''        n2 = n*n         denom = 1.0/((n+3)*(n+2)*(n+1))        return denom*array([3*(3*n2+3*n+2),                             18*(2*n+1),                             (2*1)*30])        def getFirstVariance(self)->float:        return self.getVRF()[0,0];    def getLastVariance(self)->float:        return self.getVRF()[self.order,self.order];    def getVRF(self, n : int) -> array:        """@super"""        '''@n : int'''        '''@tau : float'''        '''@V : array'''        if (n < self.order) :            return zeros([self.order+1, self.order+1]);        tau = self.tau;        V = zeros([self.order+1, self.order+1]);        V[0,0]=3*(3*n**2+3*n+2)/(n**3+6*n**2+11*n+6)
        V[0,1]=18*(2*n+1)/(tau*(n+1)*(n+2)*(n+3))
        V[1,0]=V[0,1];
        V[0,2]=60/(tau**2*(n+1)*(n+2)*(n+3))
        V[2,0]=V[0,2];
        V[1,1]=12*(15*n**2+(n-1)*(n+3))/(n*tau**2*(n-1)*(n+1)*(n+2)*(n+3))
        V[1,2]=360/(tau**3*(n-1)*(n+1)*(n+2)*(n+3))
        V[2,1]=V[1,2];
        V[2,2]=720/(n*tau**4*(n-1)*(n+1)*(n+2)*(n+3))
        return V;        def _getFirstVRF(self, n : int, tau : float ) -> float:        return 3*(3*n**2+3*n+2)/(n**3+6*n**2+11*n+6);            def _getLastVRF(self, n : int, tau : float ) -> float:        return 720/(n*tau**4*(n-1)*(n+1)*(n+2)*(n+3));        def _getDiagonalVRF(self, n : int, tau : float ) -> array:        V = zeros([self.order+1, self.order+1]);        V[0,0]=self._getFirstVRF(n, tau)        V[1,1]=12*(15*n**2+(n-1)*(n+3))/(n*tau**2*(n-1)*(n+1)*(n+2)*(n+3))        V[2,2]=self._getLastVRF(n, tau)        return V;        def _getVRF(self, n : int, tau : float ) -> array:        V = self._getDiagonalVRF(n, tau)        V[0,1]=18*(2*n+1)/(tau*(n+1)*(n+2)*(n+3))        V[1,0]=V[0,1];        V[0,2]=60/(tau**2*(n+1)*(n+2)*(n+3))        V[2,0]=V[0,2];        V[1,2]=360/(tau**3*(n-1)*(n+1)*(n+2)*(n+3))        V[2,1]=V[1,2];        return V;                class CoreEmp3(ICore) :    """    Class for the 3rd order expanding memory polynomial filter.    """    def __init__(self, tau : float) :        super().__init__()        """        Constructor                Arguments:            tau - nominal time step        """        self.order = 3;        self.tau = tau;            def getGamma(self, n : float, dtau : float) -> vector: #        """@super"""        '''@n2 : float'''        '''@n3 : float'''        '''@denom : float'''        n2 = n*n         n3 = n2*n         denom = 1.0/((n+4)*(n+3)*(n+2)*(n+1))        return denom*array([8*(2*n3+3*n2+7*n+3),                             20*(6*n2+6*n+5),                             (2*1)*120*(2*n+1), #                             (3*2*1)*140])   #         def getFirstVariance(self)->float:        return self.getVRF()[0,0];    def getLastVariance(self)->float:        return self.getVRF()[self.order,self.order];    def getVRF(self, n : int) -> array:        """@super"""        '''@n : int'''        '''@tau : float'''        '''@V : array'''        if (n < self.order) :            return zeros([self.order+1, self.order+1]);        tau = self.tau;        V = zeros([self.order+1, self.order+1]);        V[0,0]=8*(2*n**3+3*n**2+7*n+3)/(n**4+10*n**3+35*n**2+50*n+24)
        V[0,1]=20*(6*n**2+6*n+5)/(tau*(n**4+10*n**3+35*n**2+50*n+24))
        V[1,0]=V[0,1];
        V[0,2]=240*(2*n+1)/(tau**2*(n+1)*(n+2)*(n+3)*(n+4))
        V[2,0]=V[0,2];
        V[0,3]=840/(tau**3*(n+1)*(n+2)*(n+3)*(n+4))
        V[3,0]=V[0,3];
        V[1,1]=200*(6*n**4-3*n**3-3*n**2-3*n+2)/(n*tau**2*(n**6+7*n**5+7*n**4-35*n**3-56*n**2+28*n+48))
        V[1,2]=600*(9*n**2-3*n-2)/(tau**3*(n**6+7*n**5+7*n**4-35*n**3-56*n**2+28*n+48))
        V[2,1]=V[1,2];
        V[1,3]=1680*(6*n**2-3*n+2)/(n*tau**4*(n**6+7*n**5+7*n**4-35*n**3-56*n**2+28*n+48))
        V[3,1]=V[1,3];
        V[2,2]=720*(35*n**2+(n-2)*(n+4))/(n*tau**4*(n-2)*(n-1)*(n+1)*(n+2)*(n+3)*(n+4))
        V[2,3]=50400/(tau**5*(n-2)*(n-1)*(n+1)*(n+2)*(n+3)*(n+4))
        V[3,2]=V[2,3];
        V[3,3]=100800/(n*tau**6*(n-2)*(n-1)*(n+1)*(n+2)*(n+3)*(n+4))
        return V;    def _getFirstVRF(self, n : int, tau : float ) -> float:        return 8*(2*n**3+3*n**2+7*n+3)/(n**4+10*n**3+35*n**2+50*n+24);    def _getLastVRF(self, n : int, tau : float ) -> float:        return 100800/(n*tau**6*(n-2)*(n-1)*(n+1)*(n+2)*(n+3)*(n+4));    def _getDiagonalVRF(self, n : int, tau : float ) -> array:        V = zeros([self.order+1, self.order+1]);        V[0,0]=self._getFirstVRF(n, tau);        V[1,1]=200*(6*n**4-3*n**3-3*n**2-3*n+2)/(n*tau**2*(n**6+7*n**5+7*n**4-35*n**3-56*n**2+28*n+48))        V[2,2]=720*(35*n**2+(n-2)*(n+4))/(n*tau**4*(n-2)*(n-1)*(n+1)*(n+2)*(n+3)*(n+4))        V[3,3]=self._getLastVRF(n, tau);        return V;    def _getVRF(self, n : int, tau : float ) -> array:        V = self._getDiagonalVRF(n, tau)        V[0,1]=20*(6*n**2+6*n+5)/(tau*(n**4+10*n**3+35*n**2+50*n+24))        V[1,0]=V[0,1];        V[0,2]=240*(2*n+1)/(tau**2*(n+1)*(n+2)*(n+3)*(n+4))        V[2,0]=V[0,2];        V[0,3]=840/(tau**3*(n+1)*(n+2)*(n+3)*(n+4))        V[3,0]=V[0,3];        V[1,2]=600*(9*n**2-3*n-2)/(tau**3*(n**6+7*n**5+7*n**4-35*n**3-56*n**2+28*n+48))        V[2,1]=V[1,2];        V[1,3]=1680*(6*n**2-3*n+2)/(n*tau**4*(n**6+7*n**5+7*n**4-35*n**3-56*n**2+28*n+48))        V[3,1]=V[1,3];        V[2,3]=50400/(tau**5*(n-2)*(n-1)*(n+1)*(n+2)*(n+3)*(n+4))        V[3,2]=V[2,3];        return V;class CoreEmp4(ICore) :    """    Class for the 4th order expanding memory polynomial filter.    """    def __init__(self, tau : float) :        super().__init__()        """        Constructor                Arguments:            tau - nominal time step        """        self.order = 4;        self.tau = tau;            def getGamma(self, n : float, dtau : float) -> vector: #         """@super"""        '''@n2 : float'''        '''@n3 : float'''        '''@n4 : float'''        '''@denom : float'''        n2 = n*n         n3 = n2*n         n4 = n2*n2        denom = 1.0/((n+5)*(n+4)*(n+3)*(n+2)*(n+1))        return denom*array([5*(5*n4+10*n3+55*n2+50*n+24),                             25*(12*n3+18*n2+46*n+20),                             (2*1)*1050*(n2+n+1), #                             (3*2*1)*700*(2*n+1),  #                             (4*3*2*1)*630]) #        def getFirstVariance(self)->float:        return self.getVRF()[0,0];    def getLastVariance(self)->float:        return self.getVRF()[self.order,self.order];    def getVRF(self, n : int) -> array:        """@super"""        '''@n : int'''        '''@tau : float'''        '''@V : array'''        if (n < self.order) :            return zeros([self.order+1, self.order+1]);        tau = self.tau;        V = zeros([self.order+1, self.order+1]);        V[0,0]=5*(5*n**4+10*n**3+55*n**2+50*n+24)/(n**5+15*n**4+85*n**3+225*n**2+274*n+120)
        V[0,1]=50*(6*n**3+9*n**2+23*n+10)/(tau*(n**5+15*n**4+85*n**3+225*n**2+274*n+120))
        V[1,0]=V[0,1];
        V[0,2]=2100*(n**2+n+1)/(tau**2*(n**5+15*n**4+85*n**3+225*n**2+274*n+120))
        V[2,0]=V[0,2];
        V[0,3]=4200*(2*n+1)/(tau**3*(n+1)*(n+2)*(n+3)*(n+4)*(n+5))
        V[3,0]=V[0,3];
        V[0,4]=15120/(tau**4*(n+1)*(n+2)*(n+3)*(n+4)*(n+5))
        V[4,0]=V[0,4];
        V[1,1]=100*(48*n**6-90*n**5+63*n**4-198*n**3+307*n**2+98*n-60)/(n*tau**2*(n**8+9*n**7+6*n**6-126*n**5-231*n**4+441*n**3+944*n**2-324*n-720))
        V[1,2]=4200*(9*n**4-12*n**3+7*n**2-7*n+15)/(tau**3*(n**8+9*n**7+6*n**6-126*n**5-231*n**4+441*n**3+944*n**2-324*n-720))
        V[2,1]=V[1,2];
        V[1,3]=1680*(96*n**4-126*n**3+131*n**2+49*n-30)/(n*tau**4*(n**8+9*n**7+6*n**6-126*n**5-231*n**4+441*n**3+944*n**2-324*n-720))
        V[3,1]=V[1,3];
        V[1,4]=151200*(2*n**2-3*n+5)/(tau**5*(n**8+9*n**7+6*n**6-126*n**5-231*n**4+441*n**3+944*n**2-324*n-720))
        V[4,1]=V[1,4];
        V[2,2]=35280*(9*n**4-4*n**3-n**2-4*n+5)/(n*tau**4*(n**8+9*n**7+6*n**6-126*n**5-231*n**4+441*n**3+944*n**2-324*n-720))
        V[2,3]=352800*n*(4*n-1)/(tau**5*(n**8+9*n**7+6*n**6-126*n**5-231*n**4+441*n**3+944*n**2-324*n-720))
        V[3,2]=V[2,3];
        V[2,4]=302400*(9*n**2-3*n+5)/(n*tau**6*(n**8+9*n**7+6*n**6-126*n**5-231*n**4+441*n**3+944*n**2-324*n-720))
        V[4,2]=V[2,4];
        V[3,3]=100800*(63*n**2+(n-3)*(n+5))/(n*tau**6*(n-3)*(n-2)*(n-1)*(n+1)*(n+2)*(n+3)*(n+4)*(n+5))
        V[3,4]=12700800/(tau**7*(n-3)*(n-2)*(n-1)*(n+1)*(n+2)*(n+3)*(n+4)*(n+5))
        V[4,3]=V[3,4];
        V[4,4]=25401600/(n*tau**8*(n-3)*(n-2)*(n-1)*(n+1)*(n+2)*(n+3)*(n+4)*(n+5))
        return V;        def _getFirstVRF(self, n : int, tau : float ) -> float:        return 5*(5*n**4+10*n**3+55*n**2+50*n+24)/(n**5+15*n**4+85*n**3+225*n**2+274*n+120);    def _getLastVRF(self, n : int, tau : float ) -> float:        return 25401600/(n*tau**8*(n-3)*(n-2)*(n-1)*(n+1)*(n+2)*(n+3)*(n+4)*(n+5));    def _getDiagonalVRF(self, n : int, tau : float ) -> array:        V = zeros([self.order+1, self.order+1]);        V[0,0]=self._getFirstVRF(n, tau);        V[1,1]=100*(48*n**6-90*n**5+63*n**4-198*n**3+307*n**2+98*n-60)/(n*tau**2*(n**8+9*n**7+6*n**6-126*n**5-231*n**4+441*n**3+944*n**2-324*n-720))        V[2,2]=35280*(9*n**4-4*n**3-n**2-4*n+5)/(n*tau**4*(n**8+9*n**7+6*n**6-126*n**5-231*n**4+441*n**3+944*n**2-324*n-720))        V[3,3]=100800*(63*n**2+(n-3)*(n+5))/(n*tau**6*(n-3)*(n-2)*(n-1)*(n+1)*(n+2)*(n+3)*(n+4)*(n+5))        V[4,4]=self._getLastVRF(n, tau);        return V;    def _getVRF(self, n : int, tau : float ) -> array:        V = self._getDiagonalVRF(n, tau)        V[0,1]=50*(6*n**3+9*n**2+23*n+10)/(tau*(n**5+15*n**4+85*n**3+225*n**2+274*n+120))        V[1,0]=V[0,1];        V[0,2]=2100*(n**2+n+1)/(tau**2*(n**5+15*n**4+85*n**3+225*n**2+274*n+120))        V[2,0]=V[0,2];        V[0,3]=4200*(2*n+1)/(tau**3*(n+1)*(n+2)*(n+3)*(n+4)*(n+5))        V[3,0]=V[0,3];        V[0,4]=15120/(tau**4*(n+1)*(n+2)*(n+3)*(n+4)*(n+5))        V[4,0]=V[0,4];        V[1,2]=4200*(9*n**4-12*n**3+7*n**2-7*n+15)/(tau**3*(n**8+9*n**7+6*n**6-126*n**5-231*n**4+441*n**3+944*n**2-324*n-720))        V[2,1]=V[1,2];        V[1,3]=1680*(96*n**4-126*n**3+131*n**2+49*n-30)/(n*tau**4*(n**8+9*n**7+6*n**6-126*n**5-231*n**4+441*n**3+944*n**2-324*n-720))        V[3,1]=V[1,3];        V[1,4]=151200*(2*n**2-3*n+5)/(tau**5*(n**8+9*n**7+6*n**6-126*n**5-231*n**4+441*n**3+944*n**2-324*n-720))        V[4,1]=V[1,4];        V[2,3]=352800*n*(4*n-1)/(tau**5*(n**8+9*n**7+6*n**6-126*n**5-231*n**4+441*n**3+944*n**2-324*n-720))        V[3,2]=V[2,3];        V[2,4]=302400*(9*n**2-3*n+5)/(n*tau**6*(n**8+9*n**7+6*n**6-126*n**5-231*n**4+441*n**3+944*n**2-324*n-720))        V[4,2]=V[2,4];        V[3,4]=12700800/(tau**7*(n-3)*(n-2)*(n-1)*(n+1)*(n+2)*(n+3)*(n+4)*(n+5))        V[4,3]=V[3,4];        return V;class CoreEmp5(ICore) :    """    Class for the 5th order expanding memory polynomial filter.    """    def __init__(self, tau : float) :        super().__init__()        """        Constructor                Arguments:            tau - nominal time step        """        self.order = 5;        self.tau = tau;            def getGamma(self, n : float, dtau : float) -> vector:        """@super"""        '''@n2 : float'''        '''@n3 : float'''        '''@n4 : float'''        '''@denom : float'''        n2 = n*n         n3 = n2*n         n4 = n2*n2        denom = 1.0/((n+6)*(n+5)*(n+4)*(n+3)*(n+2)*(n+1))        return denom*array([6*(2*n+1)*(3*n4+6*n3+77*n2+74*n+120),                             126*(5*n4+10*n3+55*n2+50*n+28),                             (2*1)*420*(2*n+1)*(4*n2+4*n+15), #                            (3*2*1)*1260*(6*n2+6*n+7), #                              (4*3*2*1)*3780*(2*n+1),  #                             (5*4*3*2*1)*2772]) #               def getFirstVariance(self)->float:        return self.getVRF()[0,0];    def getLastVariance(self)->float:        return self.getVRF()[self.order,self.order];    def getVRF(self, n : int) -> array:        """@super"""        '''@n : int'''        '''@tau : float'''        '''@V : array'''        if (n < self.order) :            return zeros([self.order+1, self.order+1]);        tau = self.tau;        V = zeros([self.order+1, self.order+1]);        V[0,0]=6*(6*n**5+15*n**4+160*n**3+225*n**2+314*n+120)/(n**6+21*n**5+175*n**4+735*n**3+1624*n**2+1764*n+720)
        V[0,1]=126*(5*n**4+10*n**3+55*n**2+50*n+28)/(tau*(n**6+21*n**5+175*n**4+735*n**3+1624*n**2+1764*n+720))
        V[1,0]=V[0,1];
        V[0,2]=840*(8*n**3+12*n**2+34*n+15)/(tau**2*(n**6+21*n**5+175*n**4+735*n**3+1624*n**2+1764*n+720))
        V[2,0]=V[0,2];
        V[0,3]=7560*(6*n**2+6*n+7)/(tau**3*(n**6+21*n**5+175*n**4+735*n**3+1624*n**2+1764*n+720))
        V[3,0]=V[0,3];
        V[0,4]=90720*(2*n+1)/(tau**4*(n+1)*(n+2)*(n+3)*(n+4)*(n+5)*(n+6))
        V[4,0]=V[0,4];
        V[0,5]=332640/(tau**5*(n+1)*(n+2)*(n+3)*(n+4)*(n+5)*(n+6))
        V[5,0]=V[0,5];
        V[1,1]=588*(25*n**8-100*n**7+250*n**6-700*n**5+1585*n**4-280*n**3-540*n**2-600*n+288)/(n*tau**2*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))
        V[1,2]=17640*(10*n**6-30*n**5+65*n**4-100*n**3+219*n**2-44*n-48)/(tau**3*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))
        V[2,1]=V[1,2];
        V[1,3]=105840*(12*n**6-33*n**5+75*n**4-30*n**3+50*n**2-50*n+24)/(n*tau**4*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))
        V[3,1]=V[1,3];
        V[1,4]=211680*(25*n**4-70*n**3+185*n**2-20*n-48)/(tau**5*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))
        V[4,1]=V[1,4];
        V[1,5]=665280*(15*n**4-45*n**3+140*n**2-50*n+24)/(n*tau**6*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))
        V[5,1]=V[1,5];
        V[2,2]=70560*(32*n**6-48*n**5+80*n**4-120*n**3+258*n**2+53*n-60)/(n*tau**4*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))
        V[2,3]=1058400*(16*n**4-16*n**3+26*n**2-14*n+33)/(tau**5*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))
        V[3,2]=V[2,3];
        V[2,4]=604800*(120*n**4-108*n**3+238*n**2+41*n-60)/(n*tau**6*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))
        V[4,2]=V[2,4];
        V[2,5]=139708800*(n**2-n+3)/(tau**7*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))
        V[5,2]=V[2,5];
        V[3,3]=2721600*(48*n**4-18*n**3+14*n**2-20*n+39)/(n*tau**6*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))
        V[3,4]=114307200*(5*n**2-n+1)/(tau**7*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))
        V[4,3]=V[3,4];
        V[3,5]=279417600*(4*n**2-n+3)/(n*tau**8*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))
        V[5,3]=V[3,5];
        V[4,4]=25401600*(99*n**2+(n-4)*(n+6))/(n*tau**8*(n-4)*(n-3)*(n-2)*(n-1)*(n+1)*(n+2)*(n+3)*(n+4)*(n+5)*(n+6))
        V[4,5]=5029516800/(tau**9*(n-4)*(n-3)*(n-2)*(n-1)*(n+1)*(n+2)*(n+3)*(n+4)*(n+5)*(n+6))
        V[5,4]=V[4,5];
        V[5,5]=10059033600/(n*tau**10*(n-4)*(n-3)*(n-2)*(n-1)*(n+1)*(n+2)*(n+3)*(n+4)*(n+5)*(n+6))
        return V;        def _getFirstVRF(self, n : int, tau : float ) -> float:        return 6*(6*n**5+15*n**4+160*n**3+225*n**2+314*n+120)/(n**6+21*n**5+175*n**4+735*n**3+1624*n**2+1764*n+720);    def _getLastVRF(self, n : int, tau : float ) -> float:        return 10059033600/(n*tau**10*(n-4)*(n-3)*(n-2)*(n-1)*(n+1)*(n+2)*(n+3)*(n+4)*(n+5)*(n+6));    def _getDiagonalVRF(self, n : int, tau : float ) -> array:        V = zeros([self.order+1, self.order+1]);        V[0,0]=self._getFirstVRF(n, tau);        V[1,1]=588*(25*n**8-100*n**7+250*n**6-700*n**5+1585*n**4-280*n**3-540*n**2-600*n+288)/(n*tau**2*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))        V[2,2]=70560*(32*n**6-48*n**5+80*n**4-120*n**3+258*n**2+53*n-60)/(n*tau**4*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))        V[3,3]=2721600*(48*n**4-18*n**3+14*n**2-20*n+39)/(n*tau**6*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))        V[4,4]=25401600*(99*n**2+(n-4)*(n+6))/(n*tau**8*(n-4)*(n-3)*(n-2)*(n-1)*(n+1)*(n+2)*(n+3)*(n+4)*(n+5)*(n+6))        V[5,5]=self._getLastVRF(n, tau);        return V;    def _getVRF(self, n : int, tau : float ) -> array:        V = self._getDiagonalVRF(n, tau)        V[0,1]=126*(5*n**4+10*n**3+55*n**2+50*n+28)/(tau*(n**6+21*n**5+175*n**4+735*n**3+1624*n**2+1764*n+720))        V[1,0]=V[0,1];        V[0,2]=840*(8*n**3+12*n**2+34*n+15)/(tau**2*(n**6+21*n**5+175*n**4+735*n**3+1624*n**2+1764*n+720))        V[2,0]=V[0,2];        V[0,3]=7560*(6*n**2+6*n+7)/(tau**3*(n**6+21*n**5+175*n**4+735*n**3+1624*n**2+1764*n+720))        V[3,0]=V[0,3];        V[0,4]=90720*(2*n+1)/(tau**4*(n+1)*(n+2)*(n+3)*(n+4)*(n+5)*(n+6))        V[4,0]=V[0,4];        V[0,5]=332640/(tau**5*(n+1)*(n+2)*(n+3)*(n+4)*(n+5)*(n+6))        V[5,0]=V[0,5];        V[1,2]=17640*(10*n**6-30*n**5+65*n**4-100*n**3+219*n**2-44*n-48)/(tau**3*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))        V[2,1]=V[1,2];        V[1,3]=105840*(12*n**6-33*n**5+75*n**4-30*n**3+50*n**2-50*n+24)/(n*tau**4*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))        V[3,1]=V[1,3];        V[1,4]=211680*(25*n**4-70*n**3+185*n**2-20*n-48)/(tau**5*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))        V[4,1]=V[1,4];        V[1,5]=665280*(15*n**4-45*n**3+140*n**2-50*n+24)/(n*tau**6*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))        V[5,1]=V[1,5];        V[2,3]=1058400*(16*n**4-16*n**3+26*n**2-14*n+33)/(tau**5*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))        V[3,2]=V[2,3];        V[2,4]=604800*(120*n**4-108*n**3+238*n**2+41*n-60)/(n*tau**6*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))        V[4,2]=V[2,4];        V[2,5]=139708800*(n**2-n+3)/(tau**7*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))        V[5,2]=V[2,5];        V[3,4]=114307200*(5*n**2-n+1)/(tau**7*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))        V[4,3]=V[3,4];        V[3,5]=279417600*(4*n**2-n+3)/(n*tau**8*(n**10+11*n**9-330*n**7-627*n**6+3003*n**5+7370*n**4-9020*n**3-24024*n**2+6336*n+17280))        V[5,3]=V[3,5];        V[4,5]=5029516800/(tau**9*(n-4)*(n-3)*(n-2)*(n-1)*(n+1)*(n+2)*(n+3)*(n+4)*(n+5)*(n+6))        V[5,4]=V[4,5];        return V;def nSwitch(order : int, theta : float) -> float:        if (order == 0) :        return 2.0/(1.0-theta)    elif (order == 1) :        return 3.2/(1.0-theta)    elif (order == 2) :        return 4.3636/(1.0-theta)    elif (order == 3) :        return 5.50546/(1.0-theta)    elif (order == 4) :        return 6.6321/(1.0-theta)    elif (order == 5) :        return 7.7478/(1.0-theta)    else :        raise ValueError("Polynomial orders < 0 or > 5 are not supported")    def makeEmpCore(order : int, tau : float) -> ICore:    """    Factory for expanding memory polynomial filters        Arguments:        order - integer polynomial orer        tau - nominal time step            Returns:        expanding memory filter object    """    if (order == 0) :        return CoreEmp0(tau);    elif (order == 1) :        return CoreEmp1(tau);    elif (order == 2) :        return CoreEmp2(tau);    elif (order == 3) :        return CoreEmp3(tau);    elif (order == 4) :        return CoreEmp4(tau);    else : # (order == 5) :        return CoreEmp5(tau);    def makeEmp(order : int, tau : float) -> RecursivePolynomialFilter:    core = makeEmpCore(order, tau);    return RecursivePolynomialFilter(order, tau, core)##################################################################################