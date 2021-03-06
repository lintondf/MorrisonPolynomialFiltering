'''
Created on Apr 8, 2019

@author: NOOK
'''
import unittest

from numpy import array, zeros
from numpy import array as vector;

from TestSuite import TestCaseBase
from TestUtilities import assert_allclose, assert_almost_equal, assert_array_less

from polynomialfiltering.PythonUtilities import ignore, testcase, testclass, testclassmethod

from polynomialfiltering.AbstractComponentFilter import AbstractComponentFilter
from polynomialfiltering.components.Emp import makeEmp
from polynomialfiltering.filters.ManagedFilterBase import ManagedFilterBase;
from polynomialfiltering.Main import FilterStatus

class ManagedFilterBase_test(TestCaseBase):

    @testclass
    class ManagedFilterBaseMock(ManagedFilterBase):
        
        @testclassmethod
        def __init__(self, order : int, worker : AbstractComponentFilter):
            super().__init__(order, worker);
        
        @testclassmethod
        def addObservation(self, t:float, y:vector) -> bool :
            return False;
        
        @testclassmethod
        def getCovariance(self) -> array:
            '''@ C : array'''
            C = zeros([1,1])
            return C
    
        @testclassmethod
        def getGoodnessOfFit(self) -> float:
            return 0.0;
        
        @testclassmethod
        def getFirstVRF(self) -> float:
            return 0.0;
        
        @testclassmethod
        def getLastVRF(self) -> float:
            return 0.0;
        
        @testclassmethod
        def getVRF(self) -> array:
            '''@V : array'''
            V = zeros(self.order+1, self.order+1)
            return V;
        
    def setUp(self):
        pass


    def tearDown(self):
        pass


    def step9Basic(self):
        f = makeEmp(0, 0.1)
        m = self.ManagedFilterBaseMock( f.getOrder(), f );
        assert( m.getN() == 0 )
        assert( m.getWorker().getOrder() == 0)
        assert( m.getWorker().getTau() == 0.1)
        
    def step9WorkerPassthru(self):
        f = makeEmp(1, 0.2)
        m = self.ManagedFilterBaseMock( f.getOrder(), f )
        assert( m.getWorker() == f)
        f.setStatus(FilterStatus.RESETING);
        assert( m.getStatus() == f.getStatus() )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()