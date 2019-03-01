'''
Created on Feb 13, 2019

@author: NOOK
https://filterpy.readthedocs.io/en/latest/kalman/UnscentedKalmanFilter.html
'''
from abc import ABC, abstractmethod
from enum import Enum, auto
from numpy import array, eye, zeros, isscalar, diag, ones
from scipy.linalg.matfuncs import expm
# from typing import str

class FilterStatus(Enum):
    '''@IDLE : enum'''
    IDLE = 0;        # Filter is awaiting the first observation    
    '''@INITIALIZING : enum'''
    INITIALIZING = 1; # Filter has processed one or more observations, but status estimate is not reliable
    '''@RUNNING : enum'''
    RUNNING = 2;      # Filter status estimate is reliable 
    '''@COASTING : enum'''
    COASTING = 3;     # Filter has not received a recent observation, but the predicted status should be usable
    '''@RESETING : enum'''
    RESETING = 4;     # Filter coast interval has been exceed and it will reinitialize on the next observation
        

class AbstractFilter(ABC):
    '''
    classdocs
    '''


    def __init__(self, name : str = ''):
        '''
        Constructor
        '''
        self.setStatus( FilterStatus.IDLE )
        self.name = name
        
    def conformState(self, state : array) -> array:
        Z = zeros([self.order+1])
        if isscalar(state) :
            Z[0] = state
        else:
            m = min( self.order+1, len(state))
            Z[0:m] = state[0:m]
        return Z
        
    @classmethod            
    def stateTransitionMatrix(self, N : int, dt : float) -> array:
        '''
        Return a Pade' expanded status transition matrix of order m [RMKdR(7)]
            P(d)_i,j = (d^(j-i))/(j-i)! where 0 <= i <= j <= m elsewhere zero
        
        :param N: return matrix is (N,N)
        :param dt: time step
        '''
        B = eye(N)
        for i in range(0,N) :
            for j in range(i+1,N):
                ji = j-i
                fji = ji
                for x in range(2,ji) :
                    fji *= x 
                B[i,j] = pow(dt,ji)/fji
        return B
    
    
    def getName(self):
        return self.name
    
    def setName(self, name : str) -> str:
        self.name = name
        
    def getStatus(self) -> FilterStatus:
        return self.status    
        
    def setStatus(self, status : FilterStatus):
        self.status = status
        
    @abstractmethod   
    def getN(self) -> int:
        raise NotImplementedError()
        
    @abstractmethod   
    def getTime(self) -> array:
        raise NotImplementedError()
    
    @abstractmethod   
    def getState(self, t : float = None) -> array:
        raise NotImplementedError()

class ManagedFilterBase(AbstractFilter):
    def __init__(self):
        pass
    
    @abstractmethod   
    def getGoodnessOfFit(self) -> array:
        raise NotImplementedError()
    
    @abstractmethod   
    def getBiasOfFit(self) -> array:
        raise NotImplementedError()
        
    @abstractmethod   
    def add(self, t : float, y : array, observationId : str = ''):    
        raise NotImplementedError()

    @abstractmethod   
    def addWithVariance(self, t : float, y : array, R : array, observationId : str = ''):    
        self.add(t, y, observationId=observationId);

