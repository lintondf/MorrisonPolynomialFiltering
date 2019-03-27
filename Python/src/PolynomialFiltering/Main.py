'''
Created on Feb 13, 2019

@author: NOOK
https://filterpy.readthedocs.io/en/latest/kalman/UnscentedKalmanFilter.html
'''
''' TODO requirements.txt
pip install numpy_ringbuffer
pip install runstats
pip install statistics
pip install netcdf4
'''
from abc import ABC, abstractmethod
from enum import Enum
from numpy import array, eye, transpose
from numpy import array as vector;

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
    
    '''@name : str'''
    '''@status : FilterStatus'''

    def __init__(self, name : str = '') -> None:
        '''
        Constructor
        '''
        self.setStatus( FilterStatus.IDLE )
        self.name = name
        
    @classmethod            
    def stateTransitionMatrix(self, N : int, dt : float) -> array:
        '''
        Return a Pade' expanded status transition matrix of order N [RMKdR(7)]
            P(d)_i,j = (d^(j-i))/(j-i)! where 0 <= i <= j <= N elsewhere zero
        
        :param N: return matrix is (N,N)
        :param dt: time step
        '''
        '''@B: array'''
        '''@i : int'''
        '''@j : int'''
        '''@x : float'''
        '''@ji : int'''
        '''@fji : float'''
        
        B = eye(N)
        for i in range(0,N) :
            for j in range(i+1,N):
                ji = j-i
                fji = ji
                for x in range(2,ji) :
                    fji *= x 
                B[i,j] = pow(dt,ji)/fji
        return B
    
    
    def getName(self) -> str:
        return self.name
    
    def setName(self, name : str) -> None:
        self.name = name
        
    def getStatus(self) -> FilterStatus:
        return self.status    
        
    def setStatus(self, status : FilterStatus) -> None:
        self.status = status
        
    @abstractmethod   
    def getN(self) -> int:
        pass
        
    @abstractmethod   
    def getTime(self) -> float:
        pass
    
    @abstractmethod   
    def getState(self) -> vector:
        pass
    

