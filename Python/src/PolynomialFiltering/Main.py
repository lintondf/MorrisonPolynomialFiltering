''' PolynomialFiltering.Main
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

''' TODO
0. https://filterpy.readthedocs.io/en/latest/kalman/UnscentedKalmanFilter.html
1. cache state transition matrices
2. cache FMP VRF
'''

from abc import ABC, abstractmethod
from enum import Enum
from numpy import array, eye, transpose, zeros
from numpy import array as vector;
from PolynomialFiltering.PythonUtilities import virtual;

class FilterStatus(Enum):
    """
    The FilterStats enumeration defines the possible states of a filter.
    
    IDLE - Filter is awaiting the first observation
    INITIALIZING - Filter has processed one or more observations, but status estimate is not reliable
    RUNNING - Filter status estimate is reliable
    COASTING - Filter has not received a recent observation, but the predicted status should be usable
    RESETING - Filter coast interval has been exceed and it will reinitialize on the next observation
    """
    '''@IDLE : enum'''
    IDLE = 0;        #    
    '''@INITIALIZING : enum'''
    INITIALIZING = 1; # 
    '''@RUNNING : enum'''
    RUNNING = 2;      # 
    '''@COASTING : enum'''
    COASTING = 3;     # 
    '''@RESETING : enum'''
    RESETING = 4;     # 
        

class AbstractFilter(ABC):
    """
    The base class for all of the filters and components in this package.    
    """
    
    '''@order : int | polynomial order''' 
    '''@name : str | name of this filter'''
    '''@status : FilterStatus | current status'''

    def __init__(self, order : int, name : str = '') :
        """
        Base Constructor
        
        Arguments:
            order - polynomial order of the filter (state contains order+1 elements)
            name - optional identifying string
        """
        self.setStatus( FilterStatus.IDLE )
        self.order = order
        self.name = name
        
    @classmethod
    def conformState(self, order : int, state : vector) -> vector:
        """
        Matches an input state vector to the filter order
        
        Longer state vectors are truncated and short ones are zero filled
        
        Arguments:
            order - target state vector order
            state(vector) - arbitrary length input state vector
        
        Returns:
            conformed state vector with order+1 elements
        
        """
        '''@Z : vector'''
        '''@m : int'''
        Z = zeros([order+1])
        m = min( order+1, state.shape[0] )
        Z[0:m] = state[0:m]
        return Z
        
    
        
    @classmethod            
    def stateTransitionMatrix(self, N : int, dt : float) -> array: # TODO remove
        """
        Return a state transition matrix of size N for time step dt
        
        Returns a Pade' expanded status transition matrix of order N [RMKdR(7)]
            P(d)_i,j = (d^(j-i))/(j-i)! where 0 <= i <= j <= N elsewhere zero
        
        Arguments:
            N - return matrix is (N,N)
            dt - time step
        
        Returns:
            N by N state transition matrix
        """
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
        """
        Return the filter name
        
        Returns:
            Name string, empty if none
            
        """
        return self.name
    
    def setName(self, name : str) -> None:
        """
        Set the filter name
        
        Arguments:
            name - string name
        """
        self.name = name
        
    def getOrder(self) -> int:
        """
        Return the filter order
        
        Returns:
            integer filter order
        """
        return self.order;
    
    def getStatus(self) -> FilterStatus:
        """
        Return the filter status
        
        Returns:
            FilterStatus enumeration
        """
        return self.status    
        
    def setStatus(self, status : FilterStatus) -> None:
        """
        Set the filter status
        
        Arguments:
            status - enumeration value to set
        """
        self.status = status
        
    @virtual
    def transitionState(self, t : float) -> vector :
        """
        Transition the current state to the target time t
        
        Arguments:
            t - target time
            
        Returns: 
            predicted-state (not normalized)
        """        
        '''@ dt : float'''
        '''@ F : array'''
        dt = t - self.getTime()
        F = self.stateTransitionMatrix(self.order+1, dt );
        return F @ self.getState();
        
    @abstractmethod   # pragma: no cover
    def getN(self) -> int:
        """
        Return the number of observation the filter has processed
        
        Returns:
            Count of observations used
        """
        pass
        
    @abstractmethod   # pragma: no cover
    def getTime(self) -> float:
        """
        Return the current filter time
        
        Returns:
            Filter time
        """
        pass
    
    @abstractmethod   # pragma: no cover
    def getState(self) -> vector:
        """
        Returns the current filter state vector
        
        Returns:
            State vector (order+1 elements)
        """
        pass
    
    
class AbstractFilterWithCovariance(AbstractFilter) :
    """
    Extends AbstractFilter to support state vector covariance methods.
    """
    
    def __init__(self, order : int, name : str = '') :
        super().__init__(order, name)
        """
        Constructor
        
        Arguments:
            order - polynomial order of the filter (state contains order+1 elements)
            name - optional identifying string
        """

    @classmethod
    def transitionCovarianceMatrix(self, dt : float, V : array ) -> array:
        """
        Transition the specified covariance by the specified time step
        
        Arguments:
            dt - time step
            V - N x N covariance matrix
            
        Returns:
            N x N covariance matrix
        """
        '''@ F : array'''
        F = AbstractFilter.stateTransitionMatrix(int(V.shape[0]), dt );
        return (F) @ V @ transpose(F);

    @virtual
    def transitionCovariance(self, t : float ) -> array:
        """
        Transition the current filter covariance matrix to the specified time
        
        Arguments:
            t - target time
            
        Returns:
            N x N covariance matrix
        """
        '''@ dt : float'''
        '''@ V : array | covariance matrix of the filter'''
        V = self.getCovariance()
        dt = t - self.getTime()
        return self.transitionCovarianceMatrix(dt, V);
        
    @abstractmethod # pragma: no cover
    def getCovariance(self) -> array:
        """
        Get the current filter covariance matrix
        
        Returns:
            Covariance matrix
        """
        pass



