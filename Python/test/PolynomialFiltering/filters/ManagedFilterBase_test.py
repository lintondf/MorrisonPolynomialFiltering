'''
Created on Apr 8, 2019

@author: NOOK
'''
import unittest

from numpy import array, zeros
from numpy import array as vector;

from PolynomialFiltering.Components import AbstractRecursiveFilter
from PolynomialFiltering.Components.EmpFmpPair import EmpFmpPair;
from PolynomialFiltering.filters.ManagedFilterBase import ManagedFilterBase;

class ManagedFilterBaseMock(ManagedFilterBase):
    
    def __init__(self, worker : AbstractRecursiveFilter):
        super().__init__(worker);
    
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
        m = ManagedFilterBaseMock( f );
        assert( m.getN() == 0 )
        assert( m.getWorker().getOrder() == 0)
        assert( m.getWorker().getTau() == 0.1)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()