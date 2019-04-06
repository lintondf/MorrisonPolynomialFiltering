''' PolynomialFiltering.filters.controls.IJudge
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

from sys import float_info;
from abc import ABC, abstractmethod

from numpy import array, zeros, eye, exp, transpose
from numpy import array as vector;

from scipy.stats import chi2;

from PolynomialFiltering.Main import AbstractFilterWithCovariance
from PolynomialFiltering.Components.FadingMemoryPolynomialFilter import makeFMP


class IJudge(ABC):
    """
    Judges the goodness of fit of a filter
    
    Called to determine whether to accept or reject the current observation and
    to estimate th
    """
    
    def __init__(self):
        pass

    @abstractmethod # pragma: no cover
    def scalarUpdate(self, e : float, iR : array ) -> bool:
        pass;

    @abstractmethod # pragma: no cover
    def vectorUpdate(self, e : vector, iR : array ) -> bool:
        pass;

    @abstractmethod # pragma: no cover
    def getChi2(self) -> float:
        pass;
    
    @abstractmethod # pragma: no cover
    def getGOF(self) -> float:
        pass;

