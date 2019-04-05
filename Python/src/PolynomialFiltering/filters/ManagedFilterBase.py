'''
Created on Mar 27, 2019

@author: NOOK
'''

from abc import abstractmethod

from numpy import array, eye
from numpy import array as vector
from PolynomialFiltering.Main import AbstractFilterWithCovariance, FilterStatus
from PolynomialFiltering.Components import AbstractRecursiveFilter
from PolynomialFiltering.IManagedFilter import IManagedFilter, IObservationErrorModel


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

        

class ManagedFilterBase(AbstractFilterWithCovariance, IManagedFilter):
    '''
    classdocs
    '''

    '''@INITIAL_SSR : float | start point for smoothed SSR '''
    '''@ worker : AbstractRecursiveFilter | that which is managed'''
    '''@ errorModel : IObservationErrorModel | observation covariance/information matrix source'''
    '''@ iR : array | last observation information matrix'''
    '''@ SSR : float | smooth, scaled sigma ratio of observation mis-predict'''
    '''@ w : float | SSR smoothing factor'''
    
    def __init__(self, worker : AbstractRecursiveFilter):
        '''
        Constructor
        '''
        self.worker = worker;
        self.errorModel = ConstantObservationErrorModel(eye(1), eye(1))
        self.iR = 1;
        self.INITIAL_SSR = 3**2;
        self.SSR = self.INITIAL_SSR;
        self.w = 0.9

    def getStatus(self) -> FilterStatus:
        return self.worker.getStatus(self)


    def getN(self) -> int:
        return self.worker.getN(self)


    def getTime(self) -> float:
        return self.worker.getTime(self)


    def getState(self) -> vector:
        return self.worker.getState(self)


    def setGoodnessOfFitFading(self, w : float) -> None:
        self.w = w;

    def getGoodnessOfFit(self) -> float:
        return self.SSR

    def setObservationInverseR(self, inverseR:array) -> None:
        self.errorModel = ConstantObservationErrorModel(inverseR)
        
    def setObservationErrorModel(self, errorModel : IObservationErrorModel) -> None:
        self.errorModel = errorModel;

    @abstractmethod # pragma: no cover
    def add(self, t:float, y:vector, observationId:int = 0) ->bool :
        pass
    
    @abstractmethod # pragma: no cover
    def getCovariance(self) -> array:
        pass

    @abstractmethod # pragma: no cover
    def _updateSSR(self, t:float, y:vector, e : float, innovation : vector) -> None:
        pass
