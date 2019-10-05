''' PolynomialFiltering.filters.ManagedFilterBase
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

from abc import abstractmethod 

from numpy import array, eye
from numpy import array as vector
from polynomialfiltering.Main import AbstractFilterWithCovariance, FilterStatus
from polynomialfiltering.AbstractComponentFilter import AbstractComponentFilter
from polynomialfiltering.filters.AbstractManagedFilter import AbstractManagedFilter;
from polynomialfiltering.filters.controls.IObservationErrorModel import IObservationErrorModel
from polynomialfiltering.filters.controls.IJudge import IJudge
from polynomialfiltering.filters.controls.IMonitor import IMonitor
from polynomialfiltering.filters.controls.errormodel.ConstantObservationErrorModel import ConstantObservationErrorModel


class ManagedFilterBase(AbstractManagedFilter):
    """
    Base class for all managed filters
    
    Managed filters support analytic or empirical error models, observation editing and goodness-of-fit
    evaluators, and running status monitors that can stop and restart filters. 
    """

    '''@INITIAL_SSR : float | start point for smoothed SSR '''
    '''@ worker : AbstractComponentFilter | that which is managed'''
    '''@ errorModel : IObservationErrorModel | observation covariance/precision matrix source'''
    '''@ judge : IJudge | residuals-based observation editing and goodness-of-fit evaluator'''
    '''@ monitor : IMonitor | filter state monitoring and control'''
    
    def __init__(self, order : int, worker : AbstractComponentFilter):
        super().__init__(order);
        '''
        Constructor
        '''
        self.worker = worker;
        self.errorModel = ConstantObservationErrorModel(1.0)
        self.judge = None;
        self.monitor = None;

    def getStatus(self) -> FilterStatus:
        return self.worker.getStatus()

    def getN(self) -> int:
        return self.worker.getN()

    def getTime(self) -> float:
        return self.worker.getTime()

    def getState(self) -> vector:
        return self.worker.getState()
    
    def getWorker(self) -> AbstractComponentFilter:
        return self.worker;

    def setObservationInverseR(self, inverseR:array) -> None:
        self.errorModel = ConstantObservationErrorModel(inverseR)
        
    def setObservationErrorModel(self, errorModel : IObservationErrorModel) -> None:
        self.errorModel = errorModel;
        
    def setJudge(self, judge : IJudge ) -> None:
        self.judge = judge;
        
    def setMonitor(self, monitor : IMonitor) -> None:
        self.monitor = monitor;

    @abstractmethod # pragma: no cover
    def addObservation(self, t:float, y:vector) -> bool :
        pass
    
    @abstractmethod # pragma: no cover
    def getCovariance(self) -> array:
        pass

    @abstractmethod # pragma: no cover 
    def getGoodnessOfFit(self) -> float:
        pass
    
