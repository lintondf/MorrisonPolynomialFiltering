''' PolynomialFiltering.filters.controls.ConstantObservationErrorModel
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''
from PolynomialFiltering.PythonUtilities import constructor, ignore

from numpy import array
from numpy import array as vector
from numpy.linalg import inv
from PolynomialFiltering.Main import AbstractFilterWithCovariance
from PolynomialFiltering.filters.controls.IObservationErrorModel import IObservationErrorModel


class ConstantObservationErrorModel(IObservationErrorModel):
    
    '''@ R : array | observation covariance matrix'''
    '''@ iR : array | observation precision (inverse covariance) matrix'''
    
    @ignore
    def __init__(self, *args):
        if (len(args) == 1) :
            self._1_ConstantObservationErrorModel(args[0]);
        elif (len(args) == 2) :
            self._2_ConstantObservationErrorModel(args[0], args[1]);
        
    @constructor
    def _1_ConstantObservationErrorModel(self, R : array):
        self.R = R;
        self.iR = inv(R);

    @constructor
    def _2_ConstantObservationErrorModel(self, R : array, inverseR : array):
        self.R = R;
        self.iR = inverseR;


    def getPrecisionMatrix(self, f: AbstractFilterWithCovariance, t:float, y:vector, observationId:int = -1) -> array:
        if (observationId == -1) :
            return self.iR;
        else :
            return self.iR[observationId,observationId];

    def getCovarianceMatrix(self, f : AbstractFilterWithCovariance, t : float, y : vector, observationId : int = -1) -> array:
        if (observationId == -1) :
            return self.R;
        else :
            return self.R[observationId,observationId];
