'''
Created on Apr 5, 2019

@author: NOOK
'''

from numpy import array
from numpy import array as vector
from PolynomialFiltering.Main import AbstractFilterWithCovariance
from PolynomialFiltering.filters.controls import IObservationErrorModel


class ConstantObservationErrorModel(IObservationErrorModel):
    def __init__(self, R : array, inverseR : array):
        self.R = R;
        self.iR = inverseR;

    def getInformationMatrix(self, f: AbstractFilterWithCovariance, t:float, y:vector, observationId:int = -1):
        if (observationId == -1) :
            return self.iR;
        else :
            return self.iR[observationId,observationId];

    def getCovarianceMatrix(self, f : AbstractFilterWithCovariance, t : float, y : vector, observationId : int = -1) -> array:
        if (observationId == -1) :
            return self.R;
        else :
            return self.R[observationId,observationId];
