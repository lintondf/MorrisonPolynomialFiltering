'''
Created on Apr 4, 2019

@author: NOOK
'''

from abc import abstractmethod
from typing import List;

from numpy import array as vector
from PolynomialFiltering.PythonUtilities import virtual;
from PolynomialFiltering.Components import AbstractRecursiveFilter
from PolynomialFiltering.filters import ManagedFilterBase;


class ManagedScalarRecursiveFilterSet(ManagedFilterBase):
    
    def __init__(self):
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
    def add(self, t:float, y:vector, observationId:int = -1):
        self.iR = self.errorModel.getInformationMatrix(self, t, y, observationId)
        minSSR = 0;
        iBest = -1;
        for iW in range(0, len(self.workers)) :
            Zstar = self.workers[iW].predict(t)
            e = y[0] - Zstar[0]
            innovation = self.workers[iW].update(t, Zstar, e)
            self._updateSSR(t, y, e, innovation)
            self.SSRs[iW] = self.SSR;
            if (iBest < 0) :
                iBest = iW;
                minSSR = self.SSR;
            elif (self.SSR < minSSR) :
                minSSR = self.SSR;
                iBest = iW;
        self.SSR = self.SSRs[iBest];
        self.worker = self.workers[iBest];
            