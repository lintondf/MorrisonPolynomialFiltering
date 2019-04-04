'''
Created on Apr 4, 2019

@author: NOOK
'''
from abc import abstractmethod

from numpy import array as vector
from PolynomialFiltering.PythonUtilities import virtual;
from PolynomialFiltering.Components import AbstractRecursiveFilter
from PolynomialFiltering.filters import ManagedFilterBase;



class ManagedScalarRecursiveFilter(ManagedFilterBase):
    
    def __init__(self, worker : AbstractRecursiveFilter):
        super().__init__(worker);
        
    @virtual
    def add(self, t:float, y:vector, observationId:int = -1):
        self.iR = self.errorModel.getInformationMatrix(self, t, y, observationId)
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
        

        