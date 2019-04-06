''' PolynomialFiltering.filters.controls.ConstantObservationErrorModel
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

from numpy import array
from numpy import array as vector
from PolynomialFiltering.Main import AbstractFilterWithCovariance
from PolynomialFiltering.filters.controls.IObservationErrorModel import IObservationErrorModel


class ConstantObservationErrorModel(IObservationErrorModel):
    def __init__(self, R : array, inverseR : array):
        self.R = R;
        self.iR = inverseR;

    def getPrecisionMatrix(self, f: AbstractFilterWithCovariance, t:float, y:vector, observationId:int = -1):
        if (observationId == -1) :
            return self.iR;
        else :
            return self.iR[observationId,observationId];

    def getCovarianceMatrix(self, f : AbstractFilterWithCovariance, t : float, y : vector, observationId : int = -1) -> array:
        if (observationId == -1) :
            return self.R;
        else :
            return self.R[observationId,observationId];
