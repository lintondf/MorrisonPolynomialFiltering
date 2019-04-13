'''
Created on Mar 27, 2019

@author: NOOK
'''
import os
import unittest

from PolynomialFiltering.Components.EmpFmpPair import *

from TestUtilities import *
from numpy import arange, array2string, cov, log, var, zeros, trace, mean, std, transpose,\
    concatenate, allclose

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from TestSuite import testDataPath;

class Test(unittest.TestCase):

    Y0 = array([1e4, -5e3, +1e3, -5e2, +1e2, -5e1]);

    cdf = None;

    @classmethod
    def setUpClass(cls):
        path = testDataPath('EmpFmpPair.nc');
        cls.cdf = Dataset(path, "w", format="NETCDF4");

    @classmethod
    def tearDownClass(cls):
        cls.cdf.close()


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def driver(self, filter : EmpFmpPair, times, truth, observations):
        N = len(times)
        actual = zeros([N, filter.order+1]);
        diagV = zeros([N, filter.order+1]);
        actual[0,:] = truth[0,:];
        
        filter.start(times[0], actual[0,:]);
        for i in range(1,N) :
            Zstar = filter.predict(times[i])
            e = observations[i] - Zstar[0]
            filter.update(times[i], Zstar, e)
            actual[i,:] = filter.getState()
            V = filter.getVRF(); # _VRF(); # 
            if (V[0,0] != 0) :
                diagV[i,:] = (diag(V));   
            assert(filter.getN() == i );    
        return (actual, diagV, V);
    
    

    def testEmpFmpPair(self):
        nSwitch = [21,33,44,56,67,78]
        iCase = 0;
        for order in range(0, 5+1) :
            for tau in [1e-3, 1e-2, 1e-1, 1, 1e1, 1e2] :
                N = 100
                emp = EmpFmpPair(order, 0.9, tau);
                R = 1e4;
                print(order, tau, N)
                
                iCase += 1;
                group = createTestGroup(self.cdf, 'EmpFmpPair_%d' % (iCase) );
                setup = array([order, tau, N, R])
                (times, truth, observations, noise) = \
                    generateTestData(emp.order, N, 0.0, self.Y0[0:emp.order+1], emp.tau, sigma=sqrt(R))
                
                data = concatenate([times, observations, truth], axis=1);
                
                writeTestVariable(group, 'setup', setup);
                writeTestVariable(group, 'data', data);
                    
                (actual, diagV, V) = self.driver(emp, data[:,0], data[:,2:], data[:,1] )

                writeTestVariable(group, 'expected', diagV);
                n = nSwitch[order]
                assert( not allclose(diagV[n-1,:], diagV[n,:], rtol=0, atol=1e-14))
                assert( allclose(diagV[n,:], diagV[n+1,:], rtol=0, atol=1e-14))
            
#                 print( (actual[-1,:] - Y) / Y )
#                 print( A2S((V / fixed.getVRF())-1))
#                 assert_allclose( actual[-1,:], Y, rtol=1e-5, atol=0, verbose=True)
#                 assert_allclose( X, ones([emp.order+1, emp.order+1]), rtol=2e-3, atol=0, verbose=True )
#             M = 0
#             f0 = plt.figure(figsize=(10, 6))
#             ax = plt.subplot(1, 1, 1)
#             ax.plot(times[M:], truth[M:,0], 'r-', times[M:], observations[M:], 'b.', times[M:], actual[M:,0], 'k-')
#             f1 = plt.figure(figsize=(10, 6))
#             A = (f1.add_subplot(2, 2, 1), f1.add_subplot(2, 2, 2), f1.add_subplot(2, 2, 3), f1.add_subplot(2, 2, 4));
#             for i in range(0,min([4, truth.shape[1]-1, actual.shape[1]-1])) :
#                 A[i].plot(times[M:], truth[M:,1+i], 'r-', times[M:], actual[M:,1+i], 'k-')
#             plt.show()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()