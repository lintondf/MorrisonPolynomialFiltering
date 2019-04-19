'''
Created on Apr 8, 2019

@author: NOOK
'''
import unittest

from numpy import array, zeros
from numpy import array as vector;

from polynomialfiltering.components import AbstractRecursiveFilter
from polynomialfiltering.components.EmpFmpPair import EmpFmpPair;
from polynomialfiltering.filters.ManagedFilterBase import ManagedFilterBase;

class ManagedFilterBaseMock(ManagedFilterBase):
    
    def __init__(self, order : int, worker : AbstractRecursiveFilter):
        super().__init__(order, worker);
    
    def add(self, t:float, y:vector, observationId:int = 0) -> bool :
        return False;
    
    def getCovariance(self) -> array:
        return zeros([1,1])

    def getGoodnessOfFit(self) -> float:
        return 0.0;
    


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        f = EmpFmpPair(0, 0.95, 0.1);
        m = ManagedFilterBaseMock( f.getOrder(), f );
        assert( m.getN() == 0 )
        assert( m.getWorker().getOrder() == 0)
        assert( m.getWorker().getTau() == 0.1)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()