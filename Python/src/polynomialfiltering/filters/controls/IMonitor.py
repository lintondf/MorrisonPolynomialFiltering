''' PolynomialFiltering.filters.controls.IMonitor
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

from abc import ABC, abstractmethod

from numpy import array
from numpy import array as vector;

from polynomialfiltering.Main import AbstractFilterWithCovariance

class IMonitor(ABC):
    def __init__(self):
        pass
    
    @abstractmethod # pragma: no cover
    def accepted(self, f : AbstractFilterWithCovariance, t : float, y : vector, innovation : vector, observationId : int ) -> None:
        pass
    
    @abstractmethod # pragma: no cover
    def rejected(self, f : AbstractFilterWithCovariance, t : float, y : vector, innovation : vector, observationId : int ) -> None:
        pass
