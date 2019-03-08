'''
Created on Mar 7, 2019

@author: NOOK
'''
import unittest

from PolynomialFiltering.Components.ExpandingMemoryPolynomialFilter import *

from netCDF4 import Dataset
from TestUtilities import *
from numpy import arange, array2string, cov, log, var, zeros, trace, mean, std, concatenate, transpose
from numpy.linalg import inv
from numpy.random import randn
from numpy.testing import assert_almost_equal
from math import sqrt, sin
from runstats import Statistics
from numpy.testing.nose_tools.utils import assert_allclose
from numpy.linalg.linalg import norm
from numpy.ma.core import isarray


class Test(unittest.TestCase):


    cdf = None;

    @classmethod
    def setUpClass(cls):
        cls.cdf = Dataset("../../testdata/AbstractRecursiveFilter.nc", "w", format="NETCDF4");

    @classmethod
    def tearDownClass(cls):
        cls.cdf.close();

    def testEffectiveTheta(self):
        setup = array([0.1, 5+1, 50])
        expected = array([0.96,0.936,0.912728,0.889892,0.867358,0.845044])

        f = EMP4(setup[0]);
        actual = zeros(int(setup[1]));
        for order in range(0,int(setup[1])) :
            f.order = order;
            actual[order] = f.effectiveTheta(order, setup[2]);

        assert_allclose( expected, actual, atol=0, rtol=1e-2 )
        
    def testConformState(self):
        N = 5+1;
        M = 7;
        setup = array([0.1, N, M])
        data = randn(int(setup[2]));
        
        f = EMP0(setup[0])
        expected = zeros([0])
        for order in range(0,int(setup[1])) :
            f.order = order;
            Z = f._conformState( data );
            assert(len(Z) == order+1)
            assert_allclose(Z, data[0:order+1], atol=1e-14, rtol=0 )
            expected = concatenate([expected, Z], axis=0 )
#         print(expected)
        
    def testInitialization(self):
        for order in range(0,5+1) :
            tau = 0.1;
            setup = array([order, tau])
            data = zeros([0])
            
            group = createTestGroup(self.cdf, 'testInitialization_%d' % order );
            writeTestVariable(group, 'setup', setup);
            writeTestVariable(group, 'data', data);
            
            f = makeEMP(setup[0], setup[1])
    #        [n, n0, t0, t, tau, Z, D] [1, 1, 1, 1, 1, order+1, order+1] [0, order+1, 0, 0, zeros(order+1), D[tau]`]
            expected = array([f.n]);
            expected = concatenate([expected, array([f.n0])], axis=0);
            expected = concatenate([expected, array([f.t0])], axis=0);
            expected = concatenate([expected, array([f.t])], axis=0);
            expected = concatenate([expected, array([f.tau])], axis=0);
            expected = concatenate([expected, f.Z], axis=0);
            expected = concatenate([expected, f.D], axis=0);
            
            actual = array([0, order+1, 0, 0, tau]);
            actual = concatenate([actual, zeros(order+1)], axis=0);
            D = zeros(order+1);
            for i in range(0,order+1) :
                D[i] = tau**i;
            actual = concatenate([actual, D], axis=0);
            assert_allclose( actual, expected, atol=1e-14 )
            writeTestVariable(group, 'expected', expected);
        
    def testStateManagement(self) :
        for order in range(0,5+1) :
            tau = 0.1;
            t0 = 10.0;
            t1 = 20.0;
            setup = array([order, tau, t0, t1])
            data = zeros([2, order+1]);
            for i in range(0,order+1) :
                data[0,i] = (1.0/tau)**i;
            F = stateTransitionMatrix(order+1, t1-t0);
            data[1,:] = (F @ data[0,:])
            group = createTestGroup(self.cdf, 'testStateManagement_%d' % order );
            writeTestVariable(group, 'setup', setup);
            writeTestVariable(group, 'data', data);
            
            f = makeEMP(setup[0], setup[1])
            f.start(setup[2], data[0,:]);
            t = f.getTime();
            assert(t == setup[2])
            expected = zeros([order+1,2]);
            expected[:,0] = f.getState(setup[2]);
            assert_allclose( f.Z, ones(order+1) )
            assert_allclose( expected[:,0], data[0,:], atol=1e-14)
            
            expected[:,1] = f.getState(setup[3]);
            assert_allclose( expected[:,1], data[1,:], atol=1e-14)
            # print( order, expected.shape )
            writeTestVariable(group, 'expected', expected);
            
    
    def testUpdating(self) :
        for order in range(0,5+1) :
            tau = 0.1;
            setup = array([order, tau])
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testEffectiveTheta']
    unittest.main()