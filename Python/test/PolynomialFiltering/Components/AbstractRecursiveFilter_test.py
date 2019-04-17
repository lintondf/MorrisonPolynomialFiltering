'''
Created on Mar 7, 2019

@author: NOOK
'''
import unittest

from polynomialfiltering.components.ExpandingMemoryPolynomialFilter import *

from netCDF4 import Dataset
from TestUtilities import *
from numpy import arange, array2string, cov, log, var, zeros, trace, mean, std, concatenate, transpose,\
    polyder
from numpy.linalg import inv
from numpy.random import randn
from numpy.testing import assert_almost_equal
from math import sqrt, sin
from runstats import Statistics
from numpy.testing.nose_tools.utils import assert_allclose
from numpy.linalg.linalg import norm
from numpy.ma.core import isarray

from TestSuite import testDataPath;

class AbstractRecursiveFilterMock(AbstractRecursiveFilter):
    def __init__(self, order : int, tau : float) :
        super().__init__(order, tau)

    def _gammaParameter(self, t : float, dtau : float) -> float:
        return 0.0;
            
    def _gamma(self, nOrT : float) -> vector:
        return ones(self.order+1);
    
    def _VRF(self):
        return zeros([self.order+1, self.order+1])

class Test(unittest.TestCase):


    cdf = None;

    @classmethod
    def setUpClass(cls):
        path = testDataPath('AbstractRecursiveFilter.nc');
        cls.cdf = Dataset(path, "w", format="NETCDF4");

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
            
            actual = array([0, order+2, 0, 0, tau]);
            actual = concatenate([actual, zeros(order+1)], axis=0);
            D = zeros(order+1);
            for i in range(0,order+1) :
                D[i] = tau**i;
            actual = concatenate([actual, D], axis=0);
            assert_allclose( actual, expected, atol=1e-14 )
            writeTestVariable(group, 'expected', expected);
        
#     def testPrediction(self):
#         for order in range(5,5+1) :
#             for tau in [1e-1] :
#                 for i in range(0,5+1) :
#                     print(order, tau)
#                     f = AbstractRecursiveFilterMock(order, tau);
#                     X = zeros([5+1])
#                     X[0] = 1
#                     X[i] = 1
#                     print(A2S(X))
#                     f.start(0, X)
#                     print(A2S(f.Z))
#                     Zs = f.predict(tau);
#                     print(A2S(Zs))
#                     Xs = f._denormalizeState(Zs)
#                     print(A2S(Xs))
        
    def testStateManagement(self) :
        """
        Test the state management methods 
        
        tests these methods:
                start()
                getTime()
                getState()  at current filter time
                getState()  at an extrapolated time
                
        setup: [
            order - filter order
            tau - nominal filter time step
            t0 - initialization time
            t1 - extrapolation time
             }
        data:  (2,order+1) [
            row0 - initialization state vector
            row1 - expected extrapolation state vector (not used by transpiled tests)
            ]
        expected: (order+1,2) [
            col0 - post initialization state vector
            col1 - extrapolated state vector
            ]
        """
        for order in range(0,5+1) :
            tau = 0.1;
            t0 = 10.0;
            t1 = 11.0;
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
            expected[:,0] = f.transitionState(setup[2])
            expected[:,1] = f.transitionState(setup[3])
            assert_allclose( f.Z, ones(order+1) )
#             print('data',A2S(data))
#             print('expected', A2S(expected.T))
            assert_allclose( expected[:,0], data[0,:], atol=1e-14)
            
            assert_allclose( expected[:,1], data[1,:], atol=1e-14)
            # print( order, expected.shape )
            writeTestVariable(group, 'expected', expected);
            
    
    def testUpdating(self) :
        """
        Test the state update methods 
        
        tests these methods:
            predict()
            update()
        
        setup: [
            order - filter order
            tau - nominal filter time step
            t0 - initialization time
            t1 - zero error update time
            t2 - unit error update time
             }
        data:  (2,order+1) [
            row0 - initialization state vector
            row1 - expected zero error state vector (not used by transpiled tests)
            row2 - expected unit error state vector (not used by transpiled tests)
            ]
        expected: (order+1,2) [
            col0 - expected zero error updated state vector
            col1 - expected unit error updated state vector
            ]
        """
        for order in range(0,5+1) :
            tau = 0.1;
            t0 = 100.0;
            t1 = 100.5;
            t2 = 100.75;
            setup = array([order, tau, t0, t1, t2])
            data = zeros([3, order+1]);
            for i in range(0,order+1) :
                data[0,order - i] = (1.0/tau)**i;
            F = stateTransitionMatrix(order+1, t1-t0);
            data[1,:] = (F @ data[0,:])
            F = stateTransitionMatrix(order+1, t2-t1);
            data[2,:] = (F @ data[1,:])
            group = createTestGroup(self.cdf, 'testUpdating_%d' % order );
            writeTestVariable(group, 'setup', setup);
            writeTestVariable(group, 'data', data);
            
            f = AbstractRecursiveFilterMock(int(setup[0]), setup[1])
            f.start(setup[2], data[0,:]);
            
            Zstar = f.predict(setup[3]);
            assert_allclose(f._denormalizeState(Zstar), data[1,:], atol=1e-14);
            
            f.update( setup[3], Zstar, 0 );
            expected = zeros([order+1,2]);
            expected[:,0] = f.getState();
            
            Zstar = f.predict(setup[4]);
            f.update( setup[4], Zstar, 1 );
            expected[:,1] = f.getState();
            
            z = 1 + f._normalizeState(data[2,:]);
            assert_allclose(f.Z, z, atol=1e-14 );
            writeTestVariable(group, 'expected', expected);

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testEffectiveTheta']
    unittest.main()