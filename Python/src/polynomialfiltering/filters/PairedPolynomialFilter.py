''' PolynomialFiltering.components.Pair
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

from typing import Tuple
from abc import abstractmethod
from overrides import overrides

from math import isnan, exp, log;
from numpy import array, diag, zeros, sqrt, transpose
from numpy import array as vector
from polynomialfiltering.components.ICore import ICore
from polynomialfiltering.filters.RecursivePolynomialFilter import RecursivePolynomialFilter
from polynomialfiltering.components.Emp import makeEmpCore, nSwitch
from polynomialfiltering.components.Fmp import makeFmpCore

class PairedPolynomialFilter( RecursivePolynomialFilter ):
    '''@ empCore : ICore | provider of core expanding functions'''
    '''@ fmpCore : ICore | provider of core fading functions'''
    '''@ switchN : int '''
    '''@theta : float'''
    
    
    def __init__(self, order : int, tau : float, theta : float ) :
        '''@!import!static polynomialfiltering.components.Emp.makeEmpCore'''
        '''@!super!Java!super(order, tau, makeEmpCore(order, tau) );'''
        '''@!super!C++!RecursivePolynomialFilter(order, tau, components::Emp::makeEmpCore(order, tau) )'''
        super().__init__(order, tau, makeEmpCore(order, tau) )
        self.empCore = self.core;
        self.fmpCore = makeFmpCore(order, tau, theta);
        self.theta = theta;
        self.switchN = int(nSwitch( self.order, self.theta ))
        
    def update(self, t : float, Zstar : vector, e : float) -> vector:
        '''@ i : array'''
        i = RecursivePolynomialFilter.update(self, t, Zstar, e);
        if (self.n == self.switchN) :
            self.core = self.fmpCore;
        return i

    def start(self, t : float, Z : vector) -> None:
        RecursivePolynomialFilter.start(self, t, Z)
        self.core = self.empCore
        
    def isFading(self) -> bool:
        '''@isF : bool'''
        isF = self.n == self.switchN
        return isF
        
