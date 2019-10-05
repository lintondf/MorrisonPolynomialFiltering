''' PolynomialFiltering.filters.ManagedScalarRecursiveFilter
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

from abc import abstractmethod
from numpy import zeros
from numpy import array as vector
from polynomialfiltering.PythonUtilities import virtual;
from polynomialfiltering.AbstractComponentFilter import AbstractComponentFilter
from polynomialfiltering.filters.ManagedFilterBase import ManagedFilterBase;
from polynomialfiltering.filters.controls.judge.BaseScalarJudge import BaseScalarJudge
from polynomialfiltering.filters.controls.monitor.NullMonitor import NullMonitor


class ManagedScalarRecursiveFilter(ManagedFilterBase):
    
    def __init__(self, worker : AbstractComponentFilter):
        super().__init__(worker);
        self.setJudge( BaseScalarJudge(self, 0.0 ) );  # default is base judge with no smoothing
        self.setMonitor( NullMonitor() );              # default is do-nothing monitor
        self.iR = zeros([1,1]);
        
    @virtual
    def addaddObservation(self, t:float, y:vector) -> bool:
        self.iR = self.errorModel.getPrecisionMatrix(self, t, y)
        Zstar = self.worker.predict(t)
        e = y[0] - Zstar[0]
        if (self.judge.scalarUpdate(t, y, e, self.iR)) :
            innovation = self.worker.update(t, Zstar, e)
            self.monitor.accepted(t, y, innovation );
            return True;
        else : 
            self.monitor.rejected(t, y );
            return False;
        
    @virtual
    def getCovariance(self):
        return self.worker.getVRF(self) * 1/self.iR[0,0]
        

        