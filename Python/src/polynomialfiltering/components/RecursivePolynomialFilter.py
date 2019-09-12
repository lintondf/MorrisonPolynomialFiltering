''' PolynomialFiltering.components.RecursivePolynomialFilter
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

# from __future__ import annotations;

from abc import ABC, abstractmethod
from polynomialfiltering.PythonUtilities import virtual, inline;

from numpy import array, zeros;
from numpy import array as vector;

from polynomialfiltering.Main import AbstractFilter, FilterStatus
from polynomialfiltering.components.ICore import ICore

class RecursivePolynomialFilter(AbstractFilter):
    """
    Base class for both expanding and fading polynomial filter and their combinations.            
    """
    
    '''@ n : int | number of samples'''
    '''@ dtau : float | delta nominal scaled time step'''
    '''@ t0 : float | filter start time'''
    '''@ tau : float | nominal scaled time step'''
    '''@ t : float |  time of the last input'''
    '''@ Z : vector | NORMALIZED state vector at time of last input'''
    '''@ D : vector | noralization/denormalization scaling vector; D(tau) = [tau^-0, tau^-1,...tau^-order]'''
    '''@ core : ICore | provider of core expanding / fading functions'''
            
    def __init__(self, order : int, tau : float, core : ICore ) :
        super().__init__(order)
        """
        Constructor
        
        Arguments:
            order - integer polynomial orer
            tau - nominal time step
        """
        '''@ td : float | tau^d '''
        if (order < 0 or order > 5) :
            raise ValueError("Polynomial orders < 0 or > 5 are not supported")
        self.n = 0
        self.core = core;
        self.dtau = 0
        self.t0 = 0;
        self.t = 0;
        self.Z = zeros([self.order+1]);
        self.tau = tau
        # diagonal matrix D implemented as vector using element-wise operations
        # status denormalization vector D(tau) = [tau^-0, tau^-1,...tau^-order]
        self.D = zeros([self.order+1])
        '''@ d : int'''
        for d in range(0,self.order+1):
            td = pow(self.tau, d)
            self.D[d] = td
      
    @staticmethod            
    def effectiveTheta(order : int, n : float) -> float:
        """
        Estimate of the FMP fading factor theta to match 0th variance of an EMP
        
        Arguments:
            order - integer polynomial order
            n - float sample number
        """
        '''@factor : float'''
        if (n < 1):
            return 0.0
        factor = 1.148*order + 2.0367;
        return 1.0 - factor/n
    
    
    #TODO @virtual      
    def copyState(self, that : 'RecursivePolynomialFilter') -> None:
        """
        Copy the state of another filter into this filter.
        """
        self.n = that.n;
        self.t0 = that.t0;
        self.t = that.t;
        self.tau = that.tau;
        self.D = that.D;
        self.Z = that.Z;
            
    def start(self, t : float, Z : vector) -> None:
        """
        Start or restart the filter
        
        Arguments:
            t - external start time
            Z - state vector in external units
        
        Returns:
            None
        
        """
        self.n = 0;
        self.t0 = t;
        self.t = t;
        self.Z = self._normalizeState(self._conformState(Z));
    
    def predict(self, t : float) -> vector :
        """
        Predict the filter state (Z*) at time t
        
        Arguments:
            t - target time
            
        Returns:
            predicted state INTERNAL UNITS
            
        """
        '''@ Zstar : vector'''
        '''@ dt : float'''
        '''@ dtau : float'''
        '''@ F : array'''
        dt = t - self.t
        dtau = self._normalizeDeltaTime(dt)
        F = self.stateTransitionMatrix(self.order+1, dtau)
        Zstar = F @ self.Z;
        return Zstar;
    
    def update(self, t : float, Zstar : vector, e : float) -> vector:
        """
        Update the filter state from using the prediction error e
        
        Arguments:
            t - update time
            Zstar - predicted NORMALIZED state at update time
            e - prediction error (observation - predicted state)
            
        Returns:
            innovation vector
            
        Examples:
            Zstar = self.predict(t)
            e = observation[0] - Zstar[0]
            self.update(t, Zstar, e )
        """
        '''@ dt : float'''
        '''@ dtau : float'''
        '''@ gamma : vector'''
        '''@ innovation : vector'''
        dt = t - self.t
        dtau = self._normalizeDeltaTime(dt)
        gamma = self.core.getGamma(self._normalizeTime(t), dtau)
        innovation = gamma * e;
        self.Z = (Zstar + innovation)
        self.t = t
        self.n += 1;
        if (self.n < self.core.getSamplesToStart()) :
            self.setStatus( FilterStatus.INITIALIZING )
        else :
            self.setStatus( FilterStatus.RUNNING )
        return innovation;
    
    @inline
    def getCore(self) -> ICore:
        return self.core
    
    @inline    
    def getN(self)->int:
        """
        Return the number of processed observations since start
        
        Arguments:
            None
        
        Returns:
            Count of processed observations
        
        """
        return self.n
    
    @inline
    def getTau(self) -> float:
        """
        Return the nominal time step for the filter
        
        Arguments:
            None
        
        Returns:
            Nominal time step (tau) in external units
        
        """
        return self.tau
    
    @inline
    def getTime(self) -> float:
        """
        Return the time of the last processed observation or filter start
        
        Arguments:
            None
        
        Returns:
            Time in external units
        
        """
        return self.t
    
    @inline
    def getState(self) -> vector:
        """
        Get the current filter state vector
        
        Arguments:
            None
        
        Returns:
            State vector in external units
        
        """
        return self._denormalizeState(self.Z)
    
    @inline
    def getFirstVRF(self) -> float:
        if (self.n < self.core.getSamplesToStart()) :
            return 0.0;
        return self.core.getFirstVRF(self.n)

    @inline
    def getLastVRF(self) -> float:
        if (self.n < self.core.getSamplesToStart()) :
            return 0.0;
        return self.core.getLastVRF(self.n)
    
    @inline
    def getDiagonalVRF(self) -> array:
        if (self.n < self.core.getSamplesToStart()) :
            return zeros([self.order + 1, self.order + 1]);
        return self.core.getDiagonalVRF(self.n)

    @inline
    def getVRF(self) -> array:
        """
        Get the variance reduction factor matrix
        
        Arguments:
            None
        
        Returns:
            Square matrix (order+1) of input to output variance ratios
        
        """
        '''@ V : array'''
        if (self.n < self.order+1) :
            return zeros([self.order + 1, self.order + 1]);
        V = self.core.getVRF(self.n)
        return V;

    def _conformState(self, state : vector) -> vector:
        """
        Matches an input state vector to the filter order
        
        Longer state vectors are truncated and short ones are zero filled
        
        Arguments:
            state(vector) - arbitrary length input state vector
        
        Returns:
            conformed state vector with order+1 elements
        
        """
        '''@Z : vector'''
        
        return RecursivePolynomialFilter.conformState(self.order, state)
        
    @inline
    def _normalizeTime(self, t : float) -> float:
        """
        Convert an external time to internal (tau) units
        
        Arguments:
            t - external time (e.g. seconds)
        
        Returns:
            time in internal units (tau steps since t0)
        
        """
        return (t - self.t0)/self.tau
    
    @inline
    def _normalizeDeltaTime(self, dt : float) -> float:
        """
        Converts external delta time to internal (tau) step units
        
        Arguments:
            dt - external time step (e.g. seconds)
        
        Returns:
            time step in internal units
        
        """
        return dt / self.tau
    
    @inline
    def _normalizeState(self, Z : vector) -> vector:
        """
        Normalize a state vector
        
        Multiplies the input state vector by the normalization vector D
        
        Arguments:
            Z(vector) - state vector in external units
        
        Returns:
            state vector in internal units
        
        """
        return Z * self.D
    
    @inline
    def _denormalizeState(self, Z : vector) -> vector:
        """
        Denormalize a state vector
        
        Divides the input state vector by the normalization vector D
        
        Arguments:
            Z(vector) - state vector in internal units
        
        Returns:
            state vector in external units
        
        """
        return Z / self.D
