''' PolynomialFiltering.components.Pair
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

from typing import Tuple
from abc import abstractmethod

from math import isnan, exp, log;
from numpy import array, diag, zeros, sqrt, transpose
from numpy import array as vector
from polynomialfiltering.components.ICore import ICore
from polynomialfiltering.components.RecursivePolynomialFilter import RecursivePolynomialFilter
from polynomialfiltering.components.Emp import makeEmpCore, nSwitch
from polynomialfiltering.components.Fmp import makeFmpCore

class PairedPolynomialFilter( RecursivePolynomialFilter ):
    '''@ empCore : ICore | provider of core expanding functions'''
    '''@ fmpCore : ICore | provider of core fading functions'''
    '''@ threshold : int '''
    '''@theta : float'''
    
    
    def __init__(self, order : int, tau : float, theta : float ) :
        '''@!super!Java!super(order, tau, Emp.makeEmpCore(order, tau) );'''
        '''@!super!C++!RecursivePolynomialFilter(order, tau, Emp::makeEmpCore(order, tau) )'''
        super().__init__(order, tau, makeEmpCore(order, tau) )
        self.empCore = self.core;
        self.fmpCore = makeFmpCore(order, tau, theta);
        self.theta = theta;
        self.threshold = int(nSwitch( self.order, self.theta ))
        
    def update(self, t : float, Zstar : vector, e : float) -> vector:
        '''@ i : array'''
        i = RecursivePolynomialFilter.update(t, Zstar, e);
        if (self.n == self.threshold) :
            self.core = self.fmpCore;
        return i

    def start(self, t : float, Z : vector) -> None:
        RecursivePolynomialFilter.start(t, Z)
        self.core = self.empCore
        
    def isFading(self) -> bool:
        '''@isF : bool'''
        isF = self.n == self.threshold
        return isF
        
