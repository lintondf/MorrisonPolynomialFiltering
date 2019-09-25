'''
Created on Apr 8, 2019

@author: NOOK
'''
import unittest

from numpy import array, zeros
from numpy import array as vector;

from polynomialfiltering.PythonUtilities import ignore, testcase, testclass, testclassmethod

from polynomialfiltering.Main import AbstractFilter, AbstractFilterWithCovariance
from polynomialfiltering.components.Emp import makeEmp
from polynomialfiltering.filters.ManagedFilterBase import ManagedFilterBase;
from polynomialfiltering.Main import FilterStatus

class ManagedFilterBase_test(unittest.TestCase):

    @testclass
    class ManagedFilterBaseMock(ManagedFilterBase):
        
        @testclassmethod
        def __init__(self, order : int, worker : AbstractFilter):
            super().__init__(order, worker);
        
        @testclassmethod
        def add(self, t:float, y:vector, observationId:int = 0) -> bool :
            return False;
        
        @testclassmethod
        def getCovariance(self) -> array:
            return zeros([1,1])
    
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
            '''V : array'''
            V = zeros(self.order+1, self.order+1)
            return V;
        
        
    
    

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        f = makeEmp(0, 0.1)
        m = self.ManagedFilterBaseMock( f.getOrder(), f );
        assert( m.getN() == 0 )
        assert( m.getWorker().getOrder() == 0)
        assert( m.getWorker().getTau() == 0.1)
        
    def testWorkerPassthru(self):
        f = makeEmp(1, 0.2)
        m = self.ManagedFilterBaseMock( f.getOrder(), f )
        assert( m.getWorker() == f)
        f.setStatus(FilterStatus.RESETING);
        assert( m.getStatus() == f.getStatus() )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()