''' PolynomialFiltering.filters.controls.IObservationErrorModel
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

from abc import ABC, abstractmethod

from numpy import array
from numpy import array as vector;

from polynomialfiltering.Main import AbstractFilterWithCovariance

class IObservationErrorModel(ABC):
    """
    Interface for all observation error models.
    
    Observation error models provide filters with (potentially varying)
    covariance matrices characterising the random errors in observation
    elements.  The inverse of the covariance matrix ('precision' matrix)
    is more frequently required during filter processing.  Error models 
    generally can compute this inverse more efficiently than by naive 
    inverse of the covariance matrix.
    """
    def __init__(self):
        """
        Constructor
        
        """
        pass

    @abstractmethod # pragma: no cover
    def getPrecisionMatrix(self, f : AbstractFilterWithCovariance, t : float, y : vector, observationId : int) -> array:
        """
        Get the precision matrix (inverse covariance) for an observation
        
        Arguments:
            f - the filter using this model (models can serve multiple filters)
            t - the time of the observation
            y - the observation vector
            observationId - the element of y being used, -1 for all elements
        
        Returns:
            Inverse of the covariance matrix (1x1 if observationId >= 0)
        """
        pass
    
    @abstractmethod # pragma: no cover
    def getCovarianceMatrix(self, f : AbstractFilterWithCovariance, t : float, y : vector, observationId : int) -> array:
        """
        Get the covariance matrix for an observation
        
        Arguments:
            f - the filter using this model (models can serve multiple filters)
            t - the time of the observation
            y - the observation vector
            observationId - the element of y being used, -1 for all elements
        
        Returns:
            Covariance matrix (1x1 if observationId >= 0)
        """
        pass


