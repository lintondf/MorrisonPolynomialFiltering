''' PolynomialFiltering.filters.controls.ConstantObservationErrorModel
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''
from PolynomialFiltering.PythonUtilities import constructor, ignore

from numpy import array, isscalar
from numpy import array as vector
from numpy.linalg import inv
from PolynomialFiltering.Main import AbstractFilterWithCovariance
from PolynomialFiltering.filters.controls.IObservationErrorModel import IObservationErrorModel


class ConstantObservationErrorModel(IObservationErrorModel):
    """
    This model is used when the random errors in observations are constant.
    """
    
    '''@ R : array | observation covariance matrix'''
    '''@ iR : array | observation precision (inverse covariance) matrix'''
    
    @ignore
    def __init__(self, *args):
        '''Python version of constructor overloading'''
        if (len(args) == 1) :
            if (isscalar(args[0])) :
                self.ConstantObservationErrorModel_0(args[0]);
            else:
                self.ConstantObservationErrorModel_1(args[0]);
        elif (len(args) == 2) :
            self.ConstantObservationErrorModel_2(args[0], args[1]);
        
    @constructor
    def ConstantObservationErrorModel_0(self, r : float ):
        """
        Constructor
        
        Arguments:
            r - constant covariance of a scalar observation
        """
        self.R = array([[r]]);
        self.iR = array([[1.0/r]]);
        
    @constructor
    def ConstantObservationErrorModel_1(self, R : array):
        """
        Constructor
        
        Arguments:
            R - constant covariance matrix of a vector observation
        """
        self.R = R;
        self.iR = inv(R);

    @constructor
    def ConstantObservationErrorModel_2(self, R : array, inverseR : array):
        """
        Constructor
        
        Arguments:
            R - constant covariance matrix of a vector observation
            inverseR - inverse of the R matrix; used when inverseR is easily computed.
        """
        self.R = R;
        self.iR = inverseR;


    def getPrecisionMatrix(self, f: AbstractFilterWithCovariance, t:float, y:vector, observationId:int = -1) -> array:
        """@super"""
        if (observationId == -1) :
            return self.iR;
        else :
            return self.iR[observationId:observationId+1,observationId:observationId+1]; # TODO not translated properly

    def getCovarianceMatrix(self, f : AbstractFilterWithCovariance, t : float, y : vector, observationId : int = -1) -> array:
        """@super"""
        if (observationId == -1) :
            return self.R;
        else :
            return self.R[observationId:observationId+1,observationId:observationId+1]; # TODO not translated properly
