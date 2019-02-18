'''
Created on Feb 13, 2019

@author: NOOK
'''

from typing import Tuple
from abc import abstractmethod

from numpy import array, diag, zeros
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
        V = zeros([self.order+1, self.order+1]);
        #{$EMP0CVRF}
        V[0,0] = 1/(1+n);

        return V;

    
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
        u = self.tau;
        V = zeros([self.order+1, self.order+1]);
        #{$EMP1CVRF}
        V[0,0] = (2*(1+2*n))/((1+n)*(2+n));
        V[0,1] = 6/((1+n)*(2+n)*u);
        V[1,0] = V[0,1];
        V[1,1] = 12/(n*(1+n)*(2+n)*((u)*(u)));

        return V;

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
        u = self.tau;
        V = zeros([self.order+1, self.order+1]);
        #{$EMP2CVRF}
        V[0,0] = (3*(2+3*n+3*((n)*(n))))/((1+n)*(2+n)*(3+n));
        V[0,1] = (18*(1+2*n))/((1+n)*(2+n)*(3+n)*u);
        V[1,0] = V[0,1];
        V[0,2] = 30/((1+n)*(2+n)*(3+n)*((u)*(u)));
        V[2,0] = V[0,2];
        V[1,1] = (12*(1+2*n)*(-3+8*n))/((-1+n)*n*(1+n)*(2+n)*(3+n)*((u)*(u)));
        V[1,2] = 180/((-1+n)*(1+n)*(2+n)*(3+n)*((u)*(u)*(u)));
        V[2,1] = V[1,2];
        V[2,2] = 180/((-1+n)*n*(1+n)*(2+n)*(3+n)*((u)*(u)*(u)*(u)));

        return V;
        
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
        u = self.tau;
        V = zeros([self.order+1, self.order+1]);
        #{$EMP3CVRF}
        V[0,0] = (8*(1+2*n)*(3+n+((n)*(n))))/((1+n)*(2+n)*(3+n)*(4+n));
        V[0,1] = (20*(5+6*n+6*((n)*(n))))/((1+n)*(2+n)*(3+n)*(4+n)*u);
        V[1,0] = V[0,1];
        V[0,2] = (120*(1+2*n))/((1+n)*(2+n)*(3+n)*(4+n)*((u)*(u)));
        V[2,0] = V[0,2];
        V[0,3] = 140/((1+n)*(2+n)*(3+n)*(4+n)*((u)*(u)*(u)));
        V[3,0] = V[0,3];
        V[1,1] = (200*(2-3*n-3*((n)*(n))-3*((n)*(n)*(n))+6*((n)*(n)*(n)*(n))))/((-2+n)*(-1+n)*n*(1+n)*(2+n)*(3+n)*(4+n)*((u)*(u)));
        V[1,2] = (300*(-2+3*n)*(1+3*n))/((-2+n)*(-1+n)*(1+n)*(2+n)*(3+n)*(4+n)*((u)*(u)*(u)));
        V[2,1] = V[1,2];
        V[1,3] = (280*(2-3*n+6*((n)*(n))))/((-2+n)*(-1+n)*n*(1+n)*(2+n)*(3+n)*(4+n)*((u)*(u)*(u)*(u)));
        V[3,1] = V[1,3];
        V[2,2] = (360*(1+2*n)*(-4+9*n))/((-2+n)*(-1+n)*n*(1+n)*(2+n)*(3+n)*(4+n)*((u)*(u)*(u)*(u)));
        V[2,3] = 4200/((-2+n)*(-1+n)*(1+n)*(2+n)*(3+n)*(4+n)*((u)*(u)*(u)*(u)*(u)));
        V[3,2] = V[2,3];
        V[3,3] = 2800/((-2+n)*(-1+n)*n*(1+n)*(2+n)*(3+n)*(4+n)*((u)*(u)*(u)*(u)*(u)*(u)));

        return V;

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
        u = self.tau;
        V = zeros([self.order+1, self.order+1]);
        #{$EMP4CVRF}
        V[0,0] = (5*(24+50*n+55*((n)*(n))+10*((n)*(n)*(n))+5*((n)*(n)*(n)*(n))))/((1+n)*(2+n)*(3+n)*(4+n)*(5+n));
        V[0,1] = (50*(1+2*n)*(10+3*n+3*((n)*(n))))/((1+n)*(2+n)*(3+n)*(4+n)*(5+n)*u);
        V[1,0] = V[0,1];
        V[0,2] = (1050*(1+n+((n)*(n))))/((1+n)*(2+n)*(3+n)*(4+n)*(5+n)*((u)*(u)));
        V[2,0] = V[0,2];
        V[0,3] = (700*(1+2*n))/((1+n)*(2+n)*(3+n)*(4+n)*(5+n)*((u)*(u)*(u)));
        V[3,0] = V[0,3];
        V[0,4] = 630/((1+n)*(2+n)*(3+n)*(4+n)*(5+n)*((u)*(u)*(u)*(u)));
        V[4,0] = V[0,4];
        V[1,1] = (100*(1+2*n)*(-60+218*n-129*((n)*(n))+60*((n)*(n)*(n))-57*((n)*(n)*(n)*(n))+24*((n)*(n)*(n)*(n)*(n))))/((-3+n)*(-2+n)*(-1+n)*n*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*((u)*(u)));
        V[1,2] = (2100*(15-7*n+7*((n)*(n))-12*((n)*(n)*(n))+9*((n)*(n)*(n)*(n))))/((-3+n)*(-2+n)*(-1+n)*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*((u)*(u)*(u)));
        V[2,1] = V[1,2];
        V[1,3] = (280*(1+2*n)*(-30+109*n-87*((n)*(n))+48*((n)*(n)*(n))))/((-3+n)*(-2+n)*(-1+n)*n*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*((u)*(u)*(u)*(u)));
        V[3,1] = V[1,3];
        V[1,4] = (6300*(5-3*n+2*((n)*(n))))/((-3+n)*(-2+n)*(-1+n)*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*((u)*(u)*(u)*(u)*(u)));
        V[4,1] = V[1,4];
        V[2,2] = (8820*(5-4*n-((n)*(n))-4*((n)*(n)*(n))+9*((n)*(n)*(n)*(n))))/((-3+n)*(-2+n)*(-1+n)*n*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*((u)*(u)*(u)*(u)));
        V[2,3] = (29400*n*(-1+4*n))/((-3+n)*(-2+n)*(-1+n)*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*((u)*(u)*(u)*(u)*(u)));
        V[3,2] = V[2,3];
        V[2,4] = (6300*(5-3*n+9*((n)*(n))))/((-3+n)*(-2+n)*(-1+n)*n*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*((u)*(u)*(u)*(u)*(u)*(u)));
        V[4,2] = V[2,4];
        V[3,3] = (2800*(1+2*n)*(-15+32*n))/((-3+n)*(-2+n)*(-1+n)*n*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*((u)*(u)*(u)*(u)*(u)*(u)));
        V[3,4] = 88200/((-3+n)*(-2+n)*(-1+n)*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*((u)*(u)*(u)*(u)*(u)*(u)*(u)));
        V[4,3] = V[3,4];
        V[4,4] = 44100/((-3+n)*(-2+n)*(-1+n)*n*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*((u)*(u)*(u)*(u)*(u)*(u)*(u)*(u)));

        return V;

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
        u = self.tau;
        V = zeros([self.order+1, self.order+1]);
        #{$EMP5CVRF}
        V[0,0] = (6*(1+2*n)*(120+74*n+77*((n)*(n))+6*((n)*(n)*(n))+3*((n)*(n)*(n)*(n))))/((1+n)*(2+n)*(3+n)*(4+n)*(5+n)*(6+n));
        V[0,1] = (126*(28+50*n+55*((n)*(n))+10*((n)*(n)*(n))+5*((n)*(n)*(n)*(n))))/((1+n)*(2+n)*(3+n)*(4+n)*(5+n)*(6+n)*u);
        V[1,0] = V[0,1];
        V[0,2] = (420*(1+2*n)*(15+4*n+4*((n)*(n))))/((1+n)*(2+n)*(3+n)*(4+n)*(5+n)*(6+n)*((u)*(u)));
        V[2,0] = V[0,2];
        V[0,3] = (1260*(7+6*n+6*((n)*(n))))/((1+n)*(2+n)*(3+n)*(4+n)*(5+n)*(6+n)*((u)*(u)*(u)));
        V[3,0] = V[0,3];
        V[0,4] = (3780*(1+2*n))/((1+n)*(2+n)*(3+n)*(4+n)*(5+n)*(6+n)*((u)*(u)*(u)*(u)));
        V[4,0] = V[0,4];
        V[0,5] = 2772/((1+n)*(2+n)*(3+n)*(4+n)*(5+n)*(6+n)*((u)*(u)*(u)*(u)*(u)));
        V[5,0] = V[0,5];
        V[1,1] = (588*(288-600*n-540*((n)*(n))-280*((n)*(n)*(n))+1585*((n)*(n)*(n)*(n))-700*((n)*(n)*(n)*(n)*(n))+250*((n)*(n)*(n)*(n)*(n)*(n))-100*((n)*(n)*(n)*(n)*(n)*(n)*(n))+25*((n)*(n)*(n)*(n)*(n)*(n)*(n)*(n))))/((-4+n)*(-3+n)*(-2+n)*(-1+n)*n*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*(6+n)*((u)*(u)));
        V[1,2] = (8820*(-48-44*n+219*((n)*(n))-100*((n)*(n)*(n))+65*((n)*(n)*(n)*(n))-30*((n)*(n)*(n)*(n)*(n))+10*((n)*(n)*(n)*(n)*(n)*(n))))/((-4+n)*(-3+n)*(-2+n)*(-1+n)*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*(6+n)*((u)*(u)*(u)));
        V[2,1] = V[1,2];
        V[1,3] = (17640*(24-50*n+50*((n)*(n))-30*((n)*(n)*(n))+75*((n)*(n)*(n)*(n))-33*((n)*(n)*(n)*(n)*(n))+12*((n)*(n)*(n)*(n)*(n)*(n))))/((-4+n)*(-3+n)*(-2+n)*(-1+n)*n*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*(6+n)*((u)*(u)*(u)*(u)));
        V[3,1] = V[1,3];
        V[1,4] = (8820*(-48-20*n+185*((n)*(n))-70*((n)*(n)*(n))+25*((n)*(n)*(n)*(n))))/((-4+n)*(-3+n)*(-2+n)*(-1+n)*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*(6+n)*((u)*(u)*(u)*(u)*(u)));
        V[4,1] = V[1,4];
        V[1,5] = (5544*(24-50*n+140*((n)*(n))-45*((n)*(n)*(n))+15*((n)*(n)*(n)*(n))))/((-4+n)*(-3+n)*(-2+n)*(-1+n)*n*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*(6+n)*((u)*(u)*(u)*(u)*(u)*(u)));
        V[5,1] = V[1,5];
        V[2,2] = (17640*(1+2*n)*(-60+173*n-88*((n)*(n))+56*((n)*(n)*(n))-32*((n)*(n)*(n)*(n))+16*((n)*(n)*(n)*(n)*(n))))/((-4+n)*(-3+n)*(-2+n)*(-1+n)*n*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*(6+n)*((u)*(u)*(u)*(u)));
        V[2,3] = (88200*(33-14*n+26*((n)*(n))-16*((n)*(n)*(n))+16*((n)*(n)*(n)*(n))))/((-4+n)*(-3+n)*(-2+n)*(-1+n)*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*(6+n)*((u)*(u)*(u)*(u)*(u)));
        V[3,2] = V[2,3];
        V[2,4] = (12600*(1+2*n)*(-60+161*n-84*((n)*(n))+60*((n)*(n)*(n))))/((-4+n)*(-3+n)*(-2+n)*(-1+n)*n*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*(6+n)*((u)*(u)*(u)*(u)*(u)*(u)));
        V[4,2] = V[2,4];
        V[2,5] = (582120*(3-n+((n)*(n))))/((-4+n)*(-3+n)*(-2+n)*(-1+n)*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*(6+n)*((u)*(u)*(u)*(u)*(u)*(u)*(u)));
        V[5,2] = V[2,5];
        V[3,3] = (75600*(39-20*n+14*((n)*(n))-18*((n)*(n)*(n))+48*((n)*(n)*(n)*(n))))/((-4+n)*(-3+n)*(-2+n)*(-1+n)*n*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*(6+n)*((u)*(u)*(u)*(u)*(u)*(u)));
        V[3,4] = (793800*(1-n+5*((n)*(n))))/((-4+n)*(-3+n)*(-2+n)*(-1+n)*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*(6+n)*((u)*(u)*(u)*(u)*(u)*(u)*(u)));
        V[4,3] = V[3,4];
        V[3,5] = (388080*(3-n+4*((n)*(n))))/((-4+n)*(-3+n)*(-2+n)*(-1+n)*n*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*(6+n)*((u)*(u)*(u)*(u)*(u)*(u)*(u)*(u)));
        V[5,3] = V[3,5];
        V[4,4] = (88200*(1+2*n)*(-12+25*n))/((-4+n)*(-3+n)*(-2+n)*(-1+n)*n*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*(6+n)*((u)*(u)*(u)*(u)*(u)*(u)*(u)*(u)));
        V[4,5] = 1746360/((-4+n)*(-3+n)*(-2+n)*(-1+n)*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*(6+n)*((u)*(u)*(u)*(u)*(u)*(u)*(u)*(u)*(u)));
        V[5,4] = V[4,5];
        V[5,5] = 698544/((-4+n)*(-3+n)*(-2+n)*(-1+n)*n*(1+n)*(2+n)*(3+n)*(4+n)*(5+n)*(6+n)*((u)*(u)*(u)*(u)*(u)*(u)*(u)*(u)*(u)*(u)));

        return V;

def makeEMP(order, tau) :
    emps = [EMP0, EMP1, EMP2, EMP3, EMP4, EMP5];
    return emps[order](tau);
        

if __name__ == '__main__':
    for o in range(0,6) :
        emp = makeEMP(o, 0.1);
        for n in range(o, 10) :
            emp.n = n;
            print(o, n, diag(emp.VRF())[0])
        

        