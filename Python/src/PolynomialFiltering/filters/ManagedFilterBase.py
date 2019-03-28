'''
Created on Mar 27, 2019

@author: NOOK
'''

from abc import abstractmethod

from math import isnan;
from numpy import array, diag, zeros, sqrt, transpose, eye
from numpy import array as vector
from PolynomialFiltering.Main import virtual, AbstractFilterWithCovariance
from PolynomialFiltering.Components import AbstractRecursiveFilter
from PolynomialFiltering.IManagedFilter import IManagedFilter, IObservationErrorModel


class ConstantObservationErrorModel(IObservationErrorModel):
    def __init__(self, inverseR:array):
        self.iR = inverseR;

    def getInverseCovariance(self, t:float, y:vector, observationId:str):
        return self.iR;

        

class ManagedFilterBase(AbstractFilterWithCovariance, IManagedFilter):
    '''
    classdocs
    '''


    '''@ target : AbstractRecursiveFilter'''
    '''@ errorModel : IObservationErrorModel'''
    '''@ iR : array'''
    '''@ SSR : float'''
    '''@ w : float'''
    
    def __init__(self, target : AbstractRecursiveFilter):
        '''
        Constructor
        '''
        self.target = target;
        self.errorModel = ConstantObservationErrorModel(eye(1))
        self.iR = 1;
        self.SSR = 1.959964**2;
        self.w = 0.9

    def getStatus(self):
        return self.target.getStatus(self)


    def getN(self):
        return self.target.getN(self)


    def getTime(self):
        return self.target.getTime(self)


    def getState(self):
        return self.target.getState(self)


    def getCovariance(self):
        return self.target.getVRF(self, 1/self.iR[0,0])

    def setGoodnessOfFitFading(self, w : float):
        self.w = w;

    def getGoodnessOfFit(self):
        return self.SSR

    def setObservationInverseR(self, inverseR:array):
        self.errorModel = ConstantObservationErrorModel(inverseR)
        
    def setObservationErrorModel(self, errorModel : IObservationErrorModel):
        self.errorModel = errorModel;

    @virtual
    def add(self, t:float, y:vector, observationId:str=''):
        self.iR = self.errorModel.getInverseCovariance(t, y, observationId)
        Zstar = self.target.predict(t)
        e = y[0] - Zstar[0]
        innovation = self.target.update(t, Zstar, e)
        self._updateSSR(t, y, e, innovation)
        
    def _updateSSR(self, t:float, y:vector, e : float, innovation : vector):
        if (self.target.getN() > self.target.order) :
            SSR = e * self.iR * e / (1+self.target.order)
            self.SSR = self.w*self.SSR + (1-self.w)*SSR
        


        