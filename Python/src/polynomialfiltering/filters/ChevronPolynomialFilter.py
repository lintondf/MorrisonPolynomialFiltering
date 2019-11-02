''' PolynomialFiltering.components.ChevronPolynomialFilter
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

from typing import Tuple
from abc import abstractmethod
from overrides import overrides
import csv
import sys

from math import isnan, exp, log;
from numpy import array, diag, zeros, sqrt, transpose, linspace, eye
from numpy import array as vector
from scipy import stats

from polynomialfiltering.Main import FilterStatus
from polynomialfiltering.AbstractComponentFilter import AbstractComponentFilter
from polynomialfiltering.components.Emp import nSwitch, makeEmpCore, nFromFirstVRF
from polynomialfiltering.components.Fmp import makeFmpCore
from polynomialfiltering.filters.RecursivePolynomialFilter import RecursivePolynomialFilter
from polynomialfiltering.filters.PairedPolynomialFilter import PairedPolynomialFilter
from polynomialfiltering.PythonUtilities import List, ignore
from sympy.physics.quantum import innerproduct
from TestUtilities import A2S, covarianceToCorrelation
from numpy.linalg import cholesky, eig

class ChevronPolynomialFilter(AbstractComponentFilter):


    def __init__(self, order : int, tau : float, theta : float, switchV0 : float, trace=None ) :
        super().__init__(order)
        self.Z = zeros([order+1])
        self.pair = PairedPolynomialFilter(order, tau, theta) # create primary filter
        self.iActive = 0 # index into emps and switchNs; -1 if primary filter is active
        self.emps = List() # chevron member EMP filters
        self.switchNs = zeros([order])
        fc = self.pair.getFmpCore()
        for o in range(0,order) : # create EMP filters for all lower orders
            self.switchNs[o] = nFromFirstVRF(o, switchV0)
            core = makeEmpCore(o, tau)
            self.emps.append( RecursivePolynomialFilter(o, tau, core)) 
        core = self.pair.getEmpCore()
        self.V0 = core.getVRF(self.order)
        self.trace = trace;

    @ignore
    def close(self):
        if (self.trace != None) :
            self.trace.close()
            
    @ignore
    def getBest(self) -> int:
        return self.iActive
        
    @overrides
    def update(self, t : float, Zstar : vector, e : float) -> vector:
        '''@ z : vector'''
        '''@ innovation : array'''
        '''@ o : float | the observation'''
        '''@ f : float | by filter observation residual'''

        innovation = self.pair.update(t, Zstar, e)
        if (self.iActive == self.order) :
            return innovation
        o = e + Zstar[0] # recover observation
        for i in range(self.iActive, self.order) :
            z = self.emps[i].predict(t)
            f = o - z[0]
            inn = self.emps[i].update(t, z, f)
        if (self.pair.getN() > self.switchNs[self.iActive]) :
            self.iActive += 1
        return innovation
    
    @overrides
    def getStatus(self) -> FilterStatus:
        """
        Return the filter status
        
        Returns:
            FilterStatus enumeration
        """
        if (self.iActive  == self.order) :
            return self.pair.getStatus()
        return self.emps[self.iActive].getStatus()    
            

    @overrides
    def start(self, t : float, Z : vector) -> None:
        self.iActive = 0
        for i in range(0,len(self.emps)) :
            self.emps[i].start(t, Z)
        self.pair.start(t, Z)
        
    @overrides
    def getN(self)->int:
        if (self.iActive  == self.order) :
            return self.pair.getN()
        return self.emps[self.iActive].getN()
    
    @overrides
    def getState(self) -> vector:
        if (self.iActive  == self.order) :
            return self.pair.getState()
        self.Z[:] = 0
        self.Z[0:self.iActive+1] = self.emps[self.iActive].getState()
        return self.Z
    
    @overrides
    def getTime(self) -> float:
        return self.pair.getTime()
    
    @overrides
    def getTau(self) -> float:
        return self.tau

    @overrides
    def add(self, t : float, y : float) -> None:
        '''@Zstar : vector'''
        '''@e : float'''
        Zstar = self.predict(t)
        e = y - Zstar[0]
        self.update(t, Zstar, e)
            
    @overrides
    def predict(self, t : float) -> vector :
        """
        Predict the filter state (Z*) at time t
        
        Arguments:
            t - target time
            
        Returns:
            predicted NORMALIZED state (INTERNAL UNITS)
            
        """
        '''@ Zstar : vector : order+1'''
        '''@ dt : float'''
        '''@ dtau : float'''
        '''@ F : array : order+1 : order+1 '''
        return self.pair.predict(t)

    @overrides
    def getFirstVRF(self) -> float:
        if (self.iActive == self.order) :
            return self.pair.getFirstVRF()
        return self.emps[self.iActive].getFirstVRF()

    @overrides
    def getLastVRF(self) -> float:
        return self.pair.getLastVRF()
    
    @overrides
    def getVRF(self) -> array:
        V = self.pair.getVRF()
        if (V[0,0] == 0) :
            V = self.V0
        if (self.iActive == self.order) :
            return V
        # update upper corner of full order VRF matrix with active filter VRF preserving positive definiteness
        # (vD, vd) = covarianceToCorrelation(V)
        cV = cholesky(V)
        A = self.emps[self.iActive].getVRF()
        cA = cholesky(A)
        cV[0:self.iActive+1,0:self.iActive+1] = cA
        V = cV @ transpose(cV)
        return V
