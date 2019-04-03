'''
Created on Mar 27, 2019

@author: NOOK
'''

from abc import abstractmethod
from typing import List;

from math import isnan;
from numpy import array, diag, zeros, sqrt, transpose, eye
from numpy import array as vector
from PolynomialFiltering.Main import virtual, AbstractFilterWithCovariance
from PolynomialFiltering.Components import AbstractRecursiveFilter
from PolynomialFiltering.IManagedFilter import IManagedFilter, IObservationErrorModel


class ConstantObservationErrorModel(IObservationErrorModel):
    def __init__(self, inverseR:array):
        self.iR = inverseR;

    def getInverseCovariance(self, f: AbstractFilterWithCovariance, t:float, y:vector, observationId:int = 0):
        return self.iR;

        

class ManagedFilterBase(AbstractFilterWithCovariance, IManagedFilter):
    '''
    classdocs
    '''

    '''@INITIAL_SSR : float'''
    '''@ worker : AbstractRecursiveFilter'''
    '''@ errorModel : IObservationErrorModel'''
    '''@ iR : array'''
    '''@ SSR : float'''
    '''@ w : float'''
    
    def __init__(self, worker : AbstractRecursiveFilter):
        '''
        Constructor
        '''
        self.worker = worker;
        self.errorModel = ConstantObservationErrorModel(eye(1))
        self.iR = 1;
        self.INITIAL_SSR = 1.959964**2;
        self.SSR = self.INITIAL_SSR;
        self.w = 0.9

    def getStatus(self):
        return self.worker.getStatus(self)


    def getN(self):
        return self.worker.getN(self)


    def getTime(self):
        return self.worker.getTime(self)


    def getState(self):
        return self.worker.getState(self)


    def setGoodnessOfFitFading(self, w : float):
        self.w = w;

    def getGoodnessOfFit(self):
        return self.SSR

    def setObservationInverseR(self, inverseR:array):
        self.errorModel = ConstantObservationErrorModel(inverseR)
        
    def setObservationErrorModel(self, errorModel : IObservationErrorModel):
        self.errorModel = errorModel;

    @abstractmethod # pragma: no cover
    def add(self, t:float, y:vector, observationId:int = 0):
        pass
    
    @abstractmethod # pragma: no cover
    def getCovariance(self):
        pass

    @abstractmethod # pragma: no cover
    def _updateSSR(self, t:float, y:vector, e : float, innovation : vector):
        pass

        
class Managed1CRecursiveFilter(ManagedFilterBase):
    
    def __init__(self, worker : AbstractRecursiveFilter):
        super().__init__(worker);
        
    @virtual
    def add(self, t:float, y:vector, observationId:int = 0):
        self.iR = self.errorModel.getInverseCovariance(self, t, y, observationId)
        Zstar = self.worker.predict(t)
        e = y[0] - Zstar[0]
        innovation = self.worker.update(t, Zstar, e)
        self._updateSSR(t, y, e, innovation)
        
    @virtual
    def getCovariance(self):
        return self.worker.getVRF(self) * 1/self.iR[0,0]

    @virtual
    def _updateSSR(self, t:float, y:vector, e : float, innovation : vector):
        if (self.worker.getN() > self.worker.getOrder()) :
            SSR = e * self.iR * e / (1+self.worker.getOrder())
            self.SSR = self.w*self.SSR + (1-self.w)*SSR
        

class Managed1CRecursiveFilterSet(ManagedFilterBase):
    
    def __init__(self, worker : AbstractRecursiveFilter):
        super().__init__(None);
        
    '''workers : List<AbstractRecursiveFilter>'''
    '''SSRs    : List<float>'''
        
    def setWorkers(self, workers : List[AbstractRecursiveFilter]) -> None:
        self.workers = workers;
        self.worker = workers[0];
        self.SSRs = len(workers)*[self.SSR];
        
    def getWorkers(self) -> List[AbstractRecursiveFilter]:
        return self.workers;
    
    @virtual
    def add(self, t:float, y:vector, observationId:int = 0):
        self.iR = self.errorModel.getInverseCovariance(self, t, y, observationId)
        minSSR = 1e100;
        iBest = -1;
        for iW in range(0, len(self.workers)) :
            Zstar = self.workers[iW].predict(t)
            e = y[0] - Zstar[0]
            innovation = self.workers[iW].update(t, Zstar, e)
            self._updateSSR(t, y, e, innovation)
            self.SSRs[iW] = self.SSR;
            if (self.SSR < minSSR) :
                minSSR = self.SSR;
                iBest = iW;
        self.SSR = self.SSRs[iBest];
        self.worker = self.workers[iBest];
    