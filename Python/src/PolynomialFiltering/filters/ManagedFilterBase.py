''' PolynomialFiltering.filters.ManagedFilterBase
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

from abc import abstractmethod

from numpy import array, eye
from numpy import array as vector
from PolynomialFiltering.Main import AbstractFilterWithCovariance, FilterStatus
from PolynomialFiltering.Components import AbstractRecursiveFilter
from PolynomialFiltering.filters.IManagedFilter import IManagedFilter;
from PolynomialFiltering.filters.controls import IObservationErrorModel, IJudge, IMonitor, ConstantObservationErrorModel;


class ManagedFilterBase(AbstractFilterWithCovariance, IManagedFilter):
    '''
    classdocs
    '''

    '''@INITIAL_SSR : float | start point for smoothed SSR '''
    '''@ worker : AbstractRecursiveFilter | that which is managed'''
    '''@ errorModel : IObservationErrorModel | observation covariance/information matrix source'''
    
    def __init__(self, worker : AbstractRecursiveFilter):
        '''
        Constructor
        '''
        self.worker = worker;
        self.errorModel = ConstantObservationErrorModel(eye(1), eye(1))
        self.judge = None;
        self.monitor = None;

    def getStatus(self) -> FilterStatus:
        return self.worker.getStatus(self)

    def getN(self) -> int:
        return self.worker.getN(self)

    def getTime(self) -> float:
        return self.worker.getTime(self)

    def getState(self) -> vector:
        return self.worker.getState(self)

    def setObservationInverseR(self, inverseR:array) -> None:
        self.errorModel = ConstantObservationErrorModel(inverseR)
        
    def setObservationErrorModel(self, errorModel : IObservationErrorModel) -> None:
        self.errorModel = errorModel;
        
    def setJudge(self, judge : IJudge ) -> None:
        self.judge = judge;
        
    def setMonitor(self, monitor : IMonitor) -> None:
        self.monitor = monitor;

    @abstractmethod # pragma: no cover
    def add(self, t:float, y:vector, observationId:int = 0) -> bool :
        pass
    
    @abstractmethod # pragma: no cover
    def getCovariance(self) -> array:
        pass
