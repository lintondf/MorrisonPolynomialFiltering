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
from numpy.random import randn
from numpy.testing import assert_almost_equal
from numpy.testing.nose_tools.utils import assert_allclose
from math import sqrt, sin
from runstats import Statistics
from scipy.stats._continuous_distns import chi2

from PolynomialFiltering.Components.FixedMemoryPolynomialFilter import FixedMemoryFilter;



class TestFixedMemoryFiltering(unittest.TestCase):
    
    cdf = None;

    def setUp(self):
        self.cdf = Dataset("../../testdata/FixedMemoryFiltering.nc", "w", format="NETCDF4");


    def tearDown(self):
        self.cdf.close()

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

    def executePerfect(self, setup : array, data : array ) -> array:
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
        return fixed.getState(times[iCheck]);
                
    def testPerfect(self):
        setup = array([0, 11, 12, 11]);
        tau = 0.1;
        N = 25;
        for order in range(2,6):
            setup[0] = order; 
            (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], tau, sigma=0.0)
            data = concatenate([times, observations], axis=1);
            group = self.createTestGroup(self.cdf, 'testPerfect_%d' % order );
            self.writeTestVariable(group, 'setup', setup);
            self.writeTestVariable(group, 'data', data);
            
            expected = self.executePerfect(setup, data);
            
            self.writeTestVariable(group, 'expected', expected);
            print(truth[11,:])
            error = expected - truth[11,:];
            print( A2S(error / truth[11,:]) )
            assert_allclose( expected, truth[11,:], atol=0, rtol=1e-4 )

    def testMidpoints(self):
        setup = array([0, 11, 12, 11]);
        tau = 0.1;
        N = 25;
        order = 2;
        fixed = FixedMemoryFilter(order, 11);
        (times, truth, observations, noise) = generateTestData(fixed.order, N, 0.0, self.Y0[0:fixed.order+1], tau, sigma=0.0)
        for i in range(0,12) :
            for j in range(0,12):
                fixed.add(times[i+j], observations[i+j]);
            j = i+11;
            print(i, j, truth[j,:], fixed.getState(times[j])-truth[j,:]);
            


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()