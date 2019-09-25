''' PolynomialFiltering.filters.ManagedScalarRecursiveFilter
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

from abc import abstractmethod
from typing import List;

from numpy import array as vector
from polynomialfiltering.PythonUtilities import virtual;
from polynomialfiltering.Main import AbstractFilter
from polynomialfiltering.filters import ManagedFilterBase;
from polynomialfiltering.filters.controls.judge.BaseScalarJudge import BaseScalarJudge


class ManagedScalarRecursiveFilterSet(ManagedFilterBase):
    
    def __init__(self):
        super().__init__(None);
        
    '''workers : List<AbstractFilter>'''
    '''SSRs    : List<float>'''
    '''judges  : List<IJudge>'''
        
    def setWorkers(self, workers : List[AbstractFilter]) -> None:
        self.workers = workers;
        self.worker = workers[0];
        self.SSRs = [];
        self.judges = []
        for i in range(0,len(workers)) : 
            self.SSRs[i] = self.SSR;
            self.judges[i] = BaseScalarJudge(self);
        
    def getWorkers(self) -> List[AbstractFilter]:
        return self.workers;
    
    @virtual
    def add(self, t:float, y:vector, observationId:int = -1) -> bool:
        self.iR = self.errorModel.getPrecisionMatrix(self, t, y, observationId)
        minSSR = 0;
        for iW in range(0, len(self.workers)) :
            Zstar = self.workers[iW].predict(t)
            e = y[0] - Zstar[0]
            innovation = self.workers[iW].update(t, Zstar, e)
            if (self.judges[iW].scalarUpdate(t, y, e, self.iR)) :
                innovation = self.worker.update(t, Zstar, e)
                self.monitor.accepted(t, y, innovation, observationId );
                return True;
            else : 
                self.monitor.rejected(t, y, observationId );
                return False;
        iBest = BaseScalarJudge.best(self.judges);
        if (iBest < 0) :
            iBest = 0;
        self.SSR = self.SSRs[iBest];
        self.worker = self.workers[iBest];
