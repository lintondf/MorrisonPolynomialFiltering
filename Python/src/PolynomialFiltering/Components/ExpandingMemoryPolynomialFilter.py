'''
Created on Feb 13, 2019

@author: NOOK
'''

from typing import Tuple
from abc import abstractmethod

from numpy import array
from PolynomialFiltering.Components.AbstractRecursiveFilter import AbstractRecursiveFilter, IRecursiveFilter

class EMPBase(AbstractRecursiveFilter):
    def __init__(self, order : int, tau : float) -> None :
        super().__init__(order, tau)
        
    def gammaParameter(self, t : array, dtau : array) -> array:
        return self._normalizeTime(t)
    
    @abstractmethod
    def nSwitch(self, theta : float) -> float:
        raise NotImplementedError()
    
    @abstractmethod
    def VRF(self) -> array:
        raise NotImplementedError()
        

class EMP0(EMPBase) :
    def __init__(self, tau : float) :
        super().__init__( 0, tau)
        
    def gamma(self, n : array) -> array:
        return array([1/(1+n)])
    
    def nSwitch(self, theta : float) -> float:
        return 2.0/(1.0-theta)
    
    def VRF(self) -> array:
        n = self.n
        if (n < self.order) :
            return None;
        denom = 1.0/((n+1))
        return array([denom])

    
class EMP1(EMPBase) :
    def __init__(self, tau : float) :
        super().__init__( 1, tau )
        
    def gamma(self, n : array) -> array: #
        denom = 1.0/((n+2)*(n+1))
        return denom*array([2*(2*n+1), 
                            6])
    
    def nSwitch(self, theta : float) -> float:
        return 3.2/(1.0-theta)
    
    def VRF(self) -> array:
        n = self.n
        if (n < self.order) :
            return None;
        tau = self.tau;
        return array([
            (((2)*((((2)*(n))+(3)))))/(((((n)+(1)))*((n)))),
            ((12))/(((((((tau)*(tau)))*(((n)+(2))))*(((n)+(1))))*((n))))
            ])

class EMP2(EMPBase) :
    def __init__(self, tau : float) :
        super().__init__( 2, tau )
        
    def gamma(self, n : array) -> array: #
        n2 = n*n 
        denom = 1.0/((n+3)*(n+2)*(n+1))
        return denom*array([3*(3*n2+3*n+2), 
                            18*(2*n+1), 
                            (2*1)*30])
    
    def nSwitch(self, theta : float) -> float:
        return 4.3636/(1.0-theta)
    
    def VRF(self) -> array:
        n = self.n
        if (n < self.order) :
            return None;
        tau = self.tau;
        return array([
            (((3)*(((((3)*(((n)*(n))))+((9)*(n)))+(8)))))/((((((n)+(1)))*((n)))*(((n)-(1))))),
            (((12)*(((((16)*(((n)*(n))))+((62)*(n)))+(57)))))/(((((((((tau)*(tau)))*(((n)+(3))))*(((n)+(2))))*(((n)+(1))))*((n)))*(((n)-(1))))),
            ((720))/(((((((((((tau)*(tau))*(tau))*(tau)))*(((n)+(3))))*(((n)+(2))))*(((n)+(1))))*((n)))*(((n)-(1)))))
            ])
        
class EMP3(EMPBase) :
    def __init__(self, tau : float) :
        super().__init__( 3, tau )
        
    def gamma(self, n : array) -> array: #
        n2 = n*n 
        n3 = n2*n 
        denom = 1.0/((n+4)*(n+3)*(n+2)*(n+1))
        return denom*array([8*(2*n3+3*n2+7*n+3), 
                            20*(6*n2+6*n+5), 
                            (2*1)*120*(2*n+1), # 
                            (3*2*1)*140])   # 
    
    def nSwitch(self, theta : float) -> float:
        return 5.50546/(1.0-theta)
    
    def VRF(self) -> array:
        n = self.n
        if (n < self.order) :
            return None;
        tau = self.tau;
        return array([
            (((4)*((((((4)*((((n)*(n))*(n))))+((18)*(((n)*(n)))))+((38)*(n)))+(30)))))/(((((((n)+(1)))*((n)))*(((n)-(1))))*(((n)-(2))))),
            (((200)*(((((((6)*(((((n)*(n))*(n))*(n))))+((51)*((((n)*(n))*(n)))))+((159)*(((n)*(n)))))+((219)*(n)))+(116)))))/(((((((((((tau)*(tau)))*(((n)+(4))))*(((n)+(3))))*(((n)+(2))))*(((n)+(1))))*((n)))*(((n)-(1))))*(((n)-(2))))),
            ((((1440)*((((2)*(n))+(3))))*((((9)*(n))+(22)))))/(((((((((((((tau)*(tau))*(tau))*(tau)))*(((n)+(4))))*(((n)+(3))))*(((n)+(2))))*(((n)+(1))))*((n)))*(((n)-(1))))*(((n)-(2))))),
            ((100800))/(((((((((((((((tau)*(tau))*(tau))*(tau))*(tau))*(tau)))*(((n)+(4))))*(((n)+(3))))*(((n)+(2))))*(((n)+(1))))*((n)))*(((n)-(1))))*(((n)-(2)))))
            ])

class EMP4(EMPBase) :
    def __init__(self, tau : float) :
        super().__init__( 4, tau )
        
    def gamma(self, n : array) -> array: # 
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
    
    def VRF(self) -> array:
        n = self.n
        if (n < self.order) :
            return None;
        tau = self.tau;
        return array([
            (((5)*(((((((5)*(((((n)*(n))*(n))*(n))))+((30)*((((n)*(n))*(n)))))+((115)*(((n)*(n)))))+((210)*(n)))+(144)))))/((((((((n)+(1)))*((n)))*(((n)-(1))))*(((n)-(2))))*(((n)-(3))))),
            ((((100)*((((2)*(n))+(3))))*((((((((24)*((((((n)*(n))*(n))*(n))*(n))))+((297)*(((((n)*(n))*(n))*(n)))))+((1476)*((((n)*(n))*(n)))))+((3777)*(((n)*(n)))))+((5198)*(n)))+(3172)))))/(((((((((((((tau)*(tau)))*(((n)+(5))))*(((n)+(4))))*(((n)+(3))))*(((n)+(2))))*(((n)+(1))))*((n)))*(((n)-(1))))*(((n)-(2))))*(((n)-(3))))),
            (((35280)*(((((((9)*(((((n)*(n))*(n))*(n))))+((76)*((((n)*(n))*(n)))))+((239)*(((n)*(n)))))+((336)*(n)))+(185)))))/(((((((((((((((tau)*(tau))*(tau))*(tau)))*(((n)+(5))))*(((n)+(4))))*(((n)+(3))))*(((n)+(2))))*(((n)+(1))))*((n)))*(((n)-(1))))*(((n)-(2))))*(((n)-(3))))),
            ((((100800)*((((2)*(n))+(3))))*((((32)*(n))+(79)))))/(((((((((((((((((tau)*(tau))*(tau))*(tau))*(tau))*(tau)))*(((n)+(5))))*(((n)+(4))))*(((n)+(3))))*(((n)+(2))))*(((n)+(1))))*((n)))*(((n)-(1))))*(((n)-(2))))*(((n)-(3))))),
            ((25401600))/(((((((((((((((((((tau)*(tau))*(tau))*(tau))*(tau))*(tau))*(tau))*(tau)))*(((n)+(5))))*(((n)+(4))))*(((n)+(3))))*(((n)+(2))))*(((n)+(1))))*((n)))*(((n)-(1))))*(((n)-(2))))*(((n)-(3)))))
            ])

class EMP5(EMPBase) :
    def __init__(self, tau : float) :
        super().__init__( 5, tau )
        
    def gamma(self, n : array) -> array:
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
    
    def VRF(self) -> array:
        n = self.n
        if (n < self.order) :
            return None;
        '''
        {(6*(3 + 2*n)*(280 + 258*n + 113*n^2 + 18*n^3 + 3*n^4))/
          ((-4 + n)*(-3 + n)*(-2 + n)*(-1 + n)*n*(1 + n)), 
          
         (588*(84528 + 226920*n + 267180*n^2 + 181760*n^3 + 79585*n^4 + 23300*n^5 + 4450*n^6 + 500*n^7 + 25*n^8))/
            ((-4 + n)*(-3 + n)*(-2 + n)*(-1 + n)*n*(1 + n)*(2 + n)*(3 + n)*(4 + n)*(5 + n)*(6 + n)*tau^2),
            
         (70560*(3 + 2*n)*(2230 + 3501*n + 2472*n^2 + 952*n^3 + 192*n^4 + 16*n^5))/
          ((-4 + n)*(-3 + n)*(-2 + n)*(-1 + n)*n*(1 + n)*(2 + n)*(3 + n)*(4 + n)*(5 + n)*(6 + n)*tau^4),
           
         (2721600*(1047 + 1828*n + 1274*n^2 + 402*n^3 + 48*n^4))/
          ((-4 + n)*(-3 + n)*(-2 + n)*(-1 + n)*n*(1 + n)*(2 + n)*(3 + n)*(4 + n)*(5 + n)*(6 + n)*tau^6),
          
         (50803200*(3 + 2*n)*(62 + 25*n))/
          ((-4 + n)*(-3 + n)*(-2 + n)*(-1 + n)*n*(1 + n)*(2 + n)*(3 + n)*(4 + n)*(5 + n)*(6 + n)*tau^8),
           
         10059033600/
             ((-4 + n)*(-3 + n)*(-2 + n)*(-1 + n)*n*(1 + n)*(2 + n)*(3 + n)*(4 + n)*(5 + n)*(6 + n)*tau^10)}        
        '''
        tau = self.tau;
        return array([
            ((((6)*((((2)*(n))+(3))))*(((((((3)*(((((n)*(n))*(n))*(n))))+((18)*((((n)*(n))*(n)))))+((113)*(((n)*(n)))))+((258)*(n)))+(280)))))/(((((((((n)+(1)))*((n)))*(((n)-(1))))*(((n)-(2))))*(((n)-(3))))*(((n)-(4))))),
            (((588)*(((((((((((25)*(((((((((n)*(n))*(n))*(n))*(n))*(n))*(n))*(n))))+((500)*((((((((n)*(n))*(n))*(n))*(n))*(n))*(n)))))+((4450)*(((((((n)*(n))*(n))*(n))*(n))*(n)))))+((23300)*((((((n)*(n))*(n))*(n))*(n)))))+((79585)*(((((n)*(n))*(n))*(n)))))+((181760)*((((n)*(n))*(n)))))+((267180)*(((n)*(n)))))+((226920)*(n)))+(84528)))))/(((((((((((((((tau)*(tau)))*(((n)+(6))))*(((n)+(5))))*(((n)+(4))))*(((n)+(3))))*(((n)+(2))))*(((n)+(1))))*((n)))*(((n)-(1))))*(((n)-(2))))*(((n)-(3))))*(((n)-(4))))),
            ((((70560)*((((2)*(n))+(3))))*((((((((16)*((((((n)*(n))*(n))*(n))*(n))))+((192)*(((((n)*(n))*(n))*(n)))))+((952)*((((n)*(n))*(n)))))+((2472)*(((n)*(n)))))+((3501)*(n)))+(2230)))))/(((((((((((((((((tau)*(tau))*(tau))*(tau)))*(((n)+(6))))*(((n)+(5))))*(((n)+(4))))*(((n)+(3))))*(((n)+(2))))*(((n)+(1))))*((n)))*(((n)-(1))))*(((n)-(2))))*(((n)-(3))))*(((n)-(4))))),
            (((2721600)*(((((((48)*(((((n)*(n))*(n))*(n))))+((402)*((((n)*(n))*(n)))))+((1274)*(((n)*(n)))))+((1828)*(n)))+(1047)))))/(((((((((((((((((((tau)*(tau))*(tau))*(tau))*(tau))*(tau)))*(((n)+(6))))*(((n)+(5))))*(((n)+(4))))*(((n)+(3))))*(((n)+(2))))*(((n)+(1))))*((n)))*(((n)-(1))))*(((n)-(2))))*(((n)-(3))))*(((n)-(4))))),
            ((((50803200)*((((2)*(n))+(3))))*((((25)*(n))+(62)))))/(((((((((((((((((((((tau)*(tau))*(tau))*(tau))*(tau))*(tau))*(tau))*(tau)))*(((n)+(6))))*(((n)+(5))))*(((n)+(4))))*(((n)+(3))))*(((n)+(2))))*(((n)+(1))))*((n)))*(((n)-(1))))*(((n)-(2))))*(((n)-(3))))*(((n)-(4))))),
            ((10059033600))/(((((((((((((((((((((((tau)*(tau))*(tau))*(tau))*(tau))*(tau))*(tau))*(tau))*(tau))*(tau)))*(((n)+(6))))*(((n)+(5))))*(((n)+(4))))*(((n)+(3))))*(((n)+(2))))*(((n)+(1))))*((n)))*(((n)-(1))))*(((n)-(2))))*(((n)-(3))))*(((n)-(4)))))
            ])

def makeEMP(order, tau) :
    emps = [EMP0, EMP1, EMP2, EMP3, EMP4, EMP5];
    return emps[order](tau);
        

        

        