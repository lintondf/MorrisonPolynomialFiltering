'''
Created on Feb 23, 2019

@author: NOOK

 netCDF4 Visual Studio https://www.unidata.ucar.edu/software/netcdf/docs/winbin.html
 C:\Program Files\netCDF 4.6.3
'''
import unittest
from netCDF4 import Dataset
from TestUtilities import *
from numpy import arange, array2string, cov, zeros, mean, std, var, diag,\
    transpose, concatenate
from numpy.linalg import inv
from numpy.random import randn
from numpy.testing import assert_almost_equal
from numpy.testing.nose_tools.utils import assert_allclose
from math import sqrt, sin
from runstats import Statistics
from scipy.stats._continuous_distns import chi2

from PolynomialFiltering.Components.FixedMemoryPolynomialFilter import FixedMemoryFilter;

from TestSuite import testDataPath;

class TestFixedMemoryFiltering(unittest.TestCase):
    
    cdf = None;

    @classmethod
    def setUpClass(cls):
        path = testDataPath('FixedMemoryFiltering.nc');
        cls.cdf = Dataset(path, "w", format="NETCDF4");

    @classmethod
    def tearDownClass(cls):
        cls.cdf.close()

    Y0 = array([1e4, 1e3, 1e2, 1e1, 1e0, 1e-1]);
    
    def createTestGroup(self, cdf : Dataset, name : str ) -> Dataset:
        return cdf.createGroup(name);
    
    def writeTestVariable(self, group : Dataset, name : str, data : array) -> None:
        dims = data.shape;
        if (len(dims) == 1) :
            dims = (dims[0], 1);
        nDim = '%s_N' % name;
        mDim = '%s_M' % name;
        group.createDimension(nDim, dims[0]);
        group.createDimension(mDim, dims[1]);
        v = group.createVariable(name, 'd', (nDim, mDim))
        v[:] = data;

    def executeEstimatedState(self, setup : array, data : array ) -> array:
        order = int(setup[0]);
        window = int(setup[1]);
        M = int(setup[2]);
        iCheck = int(setup[3]);
        times = data[:,0:1];
        data = data[:,1:];
        observations = data[:,0:1];
        data = data[:,1:];
        fixed = FixedMemoryFilter(order, window);
        for i in range(0,M) :
            fixed.add(times[i], observations[i]);
        return fixed.transitionState(times[iCheck]);
                
                
    def testPerfect(self):
        setup = array([None, 11, 12, 11]);
        tau = 0.1;
        N = 25;
        for order in range(2,6):
            setup[0] = order; 
            (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], tau, sigma=0.0)
            data = concatenate([times, observations], axis=1);
            group = self.createTestGroup(self.cdf, 'testPerfect_%d' % order );
            self.writeTestVariable(group, 'setup', setup);
            self.writeTestVariable(group, 'data', data);
            
            expected = self.executeEstimatedState(setup, data);
            
            self.writeTestVariable(group, 'expected', expected);
            assert_allclose( expected, truth[11,:], atol=0, rtol=1e-3 )

    def testNoisy(self):
        setup = array([None, 11, 12, 11]);
        tau = 0.1;
        N = 25;
        for order in range(2,6):
            setup[0] = order; 
            (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], tau, sigma=1.0)
            data = concatenate([times, observations], axis=1);
            group = self.createTestGroup(self.cdf, 'testNoisy_%d' % order );
            self.writeTestVariable(group, 'setup', setup);
            self.writeTestVariable(group, 'data', data);
            
            expected = self.executeEstimatedState(setup, data);
            
            self.writeTestVariable(group, 'expected', expected);
            #assert_allclose( expected, truth[11,:], atol=0, rtol=1e-2 )

    
    def testMidpoints(self):
        tau = 0.1;
        N = 25;
        order = 2;
        window = 11;
        M = 12; # number of points to input
        offset = M - window;
        for iCheck in range(offset, M) :
            setup = array([order, window, M, iCheck]);
            fixed = FixedMemoryFilter(order, window);
            (times, truth, observations, noise) = generateTestData(fixed.order, N, 0.0, self.Y0[0:fixed.order+1], tau, sigma=0.0)
            
            data = concatenate([times, observations], axis=1);
            group = self.createTestGroup(self.cdf, 'testMidpoints_%d' % iCheck );
            self.writeTestVariable(group, 'setup', setup);
            self.writeTestVariable(group, 'data', data);
            
            expected = self.executeEstimatedState(setup, data);
            
            self.writeTestVariable(group, 'expected', expected);
            assert_allclose( truth[iCheck,:], expected );
            
    def executeVRF(self, setup : array, data : array ) -> array:
        order = int(setup[0]);
        window = int(setup[1]);
        M = int(setup[2]);
        iCheck = int(setup[3]);
        times = data[:,0:1];
        data = data[:,1:];
        observations = data[:,0:1];
        data = data[:,1:];
        fixed = FixedMemoryFilter(order, window);
        for i in range(0,M) :
            fixed.add(times[i], observations[i]);
        return fixed.getCovariance();
                
    def testVRF(self) :
        tau = 0.1;
        N = 25;
        window = 11;
        M = 12; # number of points to input
        iCheck = M-1;
        for order in range(2,6) :
            setup = array([order, window, M, iCheck]);
            fixed = FixedMemoryFilter(order, window);
            (times, truth, observations, noise) = generateTestData(fixed.order, N, 0.0, self.Y0[0:fixed.order+1], tau, sigma=0.0)
            
            data = concatenate([times, observations], axis=1);
            group = self.createTestGroup(self.cdf, 'testVRF%d' % order );
            self.writeTestVariable(group, 'setup', setup);
            self.writeTestVariable(group, 'data', data);
            
            expected = self.executeVRF(setup, data);
            
            self.writeTestVariable(group, 'expected', expected);
        
        
    def xtestVRFStatistics(self):
        '''
         This extended numeric test validates the computed VRF matrix
         against the actual residuals for a large sample of filter runs.
         N=1000, K=5000, 492.609 seconds
        [     0.998          1          1          1          1          1          1          1          1]        
        '''
        tau = 0.1;
        N = 1000;
        order = 2;
        window = 51;
        M = window; # number of points for initial input
        setup = array([order, window, M]);
        K = 5000;
        C = zeros([K,(order+1)**2])
        for k in range(0,K) :
            fixed = FixedMemoryFilter(order, window);
            (times, truth, observations, noise) = generateTestData(fixed.order, N, 0.0, self.Y0[0:fixed.order+1], tau, sigma=1.0)
            for i in range(0,window) :
                fixed.add(times[i], observations[i]);
            results = zeros([N-window, order+1]);
            for i in range(window, N) :
                fixed.add(times[i], observations[i]);
                results[i-window,:] = fixed.getState() - truth[i,:];
            c = cov(results,rowvar=False);
            C[k,:] = c.flatten();
            V = fixed.getCovariance();
            
        E = mean(C,axis=0) / V.flatten()
        print( A2S( E ) );
        assert_allclose( E, ones([(order+1)**2]), atol=1e-2 )
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()