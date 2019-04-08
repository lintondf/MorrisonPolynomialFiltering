''' PolynomialFiltering.filters.ManagedScalarRecursiveFilter
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

from abc import abstractmethod
from numpy import zeros
from numpy import array as vector
from PolynomialFiltering.PythonUtilities import virtual;
from PolynomialFiltering.Components import AbstractRecursiveFilter
from PolynomialFiltering.filters.ManagedFilterBase import ManagedFilterBase;
from PolynomialFiltering.filters.controls.BaseScalarJudge import BaseScalarJudge
from PolynomialFiltering.filters.controls.NullMonitor import NullMonitor


class ManagedScalarRecursiveFilter(ManagedFilterBase):
    
    def __init__(self, worker : AbstractRecursiveFilter):
        super().__init__(worker);
        self.setJudge( BaseScalarJudge(self, 0.0 ) );  # default is base judge with no smoothing
        self.setMonitor( NullMonitor() );              # default is do-nothing monitor
        self.iR = zeros([1,1]);
        
    @virtual
    def add(self, t:float, y:vector, observationId:int = -1) -> bool:
        self.iR = self.errorModel.getPrecisionMatrix(self, t, y, observationId)
        Zstar = self.worker.predict(t)
        e = y[0] - Zstar[0]
        if (self.judge.scalarUpdate(t, y, e, self.iR)) :
            innovation = self.worker.update(t, Zstar, e)
            self.monitor.accepted(t, y, innovation, observationId );
            return True;
        else : 
            self.monitor.rejected(t, y, observationId );
            return False;
        
    @virtual
    def getCovariance(self):
        return self.worker.getVRF(self) * 1/self.iR[0,0]
        

        