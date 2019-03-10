'''
Created on Feb 13, 2019

@author: NOOK
'''
import unittest

from PolynomialFiltering.Components.ExpandingMemoryPolynomialFilter import *

from TestUtilities import *
from numpy import arange, array2string, cov, log, var, zeros, trace, mean, std, transpose,\
    concatenate, allclose
from numpy import sqrt
from numpy.linalg import inv
from numpy.random import randn
from numpy.testing import assert_almost_equal
from numpy.testing.nose_tools.utils import assert_allclose
from numpy.linalg.linalg import norm
from numpy.ma.core import isarray
from scipy.stats import norm as normalDistribution
from math import sin
from runstats import Statistics
from gevent.libev.corecext import stat

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class Test(unittest.TestCase):

    Y0 = array([1e4, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10]);

    def setUp(self):
        pass


    def tearDown(self):
        pass

    def empPerfect(self, order, filter, tau=1.0, N=100):
        (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], tau, sigma=0.0)
        filter.start(0.0, self.Y0[0:order+1])
        for i in range(1,N) :
            Zstar = filter.predict(times[i][0])
            e = observations[i] - Zstar[0]
            filter.update(times[i][0], Zstar, e)
            Yf = filter.getState(times[i][0])
            assert_allclose( Yf, truth[i,0:order+1], atol=0, rtol=1e-6 )
            
    def empDriver(self, filter : EMPBase, N : int, dataOrder : int ):
        (times, truth, observations, noise) = generateTestData(dataOrder, N, 0.0, self.Y0[0:filter.order+1], filter.tau, sigma=1.0)
        
        data = zeros([N, 2]);
        data[:,0] = times[:,0];
        data[:,1] = observations[:,0];
        
        actual = zeros([N, filter.order+1]);
        diagV = zeros([N, filter.order+1]);
        actual[0,:] = truth[0,:];
        
        filter.start(data[0,0], actual[0,:]);
        for i in range(1,N) :
            Zstar = filter.predict(data[i,0])
            e = data[i,1] - Zstar[0]
            filter.update(data[i,0], Zstar, e)
            actual[i,:] = filter.getState(data[i,0])
            V = filter.getCovariance(1);
            if (V[0,0] != 0) :
                diagV[i,:] = (diag(V));       
        return (actual, truth, diagV, V);
    
    
    def empResidualsDriver(self, filter : EMPBase, N : int):
        (actual, truth, diagV, V) = self.empDriver(filter, N, filter.order)
        r = actual - truth;
        r = r[5:,:] / diagV[5:,:];
        return concatenate([mean(r,axis=0), std(r,axis=0)], axis=0);
        
            



    def xtest_EMP0(self):
        emp = EMP0(0.1)
        self.empDriver(emp, N=101, dataOrder=emp.order )
            
    def xtest_EMP1(self):
        emp = EMP1(0.1)
        self.empDriver(emp, N=101, dataOrder=emp.order )
        
    def xtest_EMP2(self):
        emp = EMP2(0.5)
        self.empDriver(emp, N=101, dataOrder=emp.order )
 
    def xtest_EMP3(self):
        emp = EMP3(1.5)
        self.empDriver(emp, N=101, dataOrder=emp.order )

    def xtest_EMP4(self):
        emp = EMP4(1.5)
        self.empDriver(emp, N=101, dataOrder=emp.order )
 
    def test_EMP5(self):
        N = 150;
        emp = EMP5(1e2)
        dataOrder = 2;
        (times, truth, observations, noise) = generateTestData(dataOrder, N, 0.0, self.Y0[0:emp.order+1], emp.tau, sigma=10)
        
        data = zeros([N, 2]);
        data[:,0] = times[:,0];
        data[:,1] = observations[:,0];
        
        actual = zeros([N, emp.order+1]);
        emp.start(0.0, array([0,0,0,0,0,0]))
        for i in range(0,N) :
            Zstar = emp.predict(data[i,0])
            e = data[i,1] - Zstar[0]
            emp.update(data[i,0], Zstar, e)
            actual[i,:] = emp.getState(data[i,0])

        f0 = plt.figure(figsize=(10, 6))
        ax = plt.subplot(1, 1, 1)
        ax.plot(times, truth[:,0], 'r-', times, observations, 'b.', times, actual[:,0], 'k-')
        f1 = plt.figure(figsize=(10, 6))
        A = (f1.add_subplot(2, 2, 1), f1.add_subplot(2, 2, 2), f1.add_subplot(2, 2, 3), f1.add_subplot(2, 2, 4));
        for i in range(0,4) :
            A[i].plot(times[15:], truth[15:,1+i], 'r-', times[15:], actual[15:,1+i], 'k-')
        plt.show()
        
    def xtest_EMP5(self):
        K = 40;
        for tau in [1e-3, 1e-2, 1e-1, 1, 1e1, 1e2] :
            print('tau', tau)
            emp = EMP5(tau)
            (actual, truth, diagV, V) = self.empDriver(emp, N=1001, dataOrder=emp.order )
            residuals = actual[K:,:] - truth[K:,0:emp.order+1];
            print( 'mean', A2S( mean(residuals, axis=0) ) )
#             print('actual covariance diag')
#             C = cov(residuals, rowvar=False);
#             print( A2S( diag(C) ) )
#             print('predicted covariance diag')
#             print( A2S( diag(V) ) )
 
    def xtest_EMPVRF(self):
        for tau in [1e-3] : #[1e-3, 1e-2, 1e-1, 1, 1e1, 1e2] :
            M = 10000;  # number of runs
            N = 50;    # number of observations
            for order in range(2,2+1) :
                residuals = zeros([0, (order+1)]) # final sample residuals for all runs
                for i in range(0,M) :
                    emp = makeEMP(order, tau)
                    (actual, truth, diagV, V) = self.empDriver(emp, N=N, dataOrder=filter.order );
                    r = actual - truth;
                    residuals = concatenate([residuals, r[N-1:N,:]], axis=0 );
            print('residuals %d' % order, residuals.shape, tau);
            # print( A2S( residuals) )
            print( 'mean', A2S( mean(residuals, axis=0) ) )
            print('actual covariance diag')
            C = cov(residuals, rowvar=False);
            print( A2S( diag(C) ) )
            print('expected covariance diag')
            print( A2S(diag(V)))   
            print('actual/expected covariance diag')
            print( A2S(diag(C / V)) )
#         if (not allclose(V, V.T, atol=1e-14)) :
#             print(A2S(V-V.T))
            '''
M = 10000
residuals 2 (10000, 3) 0.001
mean [   0.00458      0.348       14.2]
actual covariance diag
[     0.164   1.39e+03   2.08e+06]
expected covariance diag
[     0.195   1.57e+03   2.19e+06]
actual/expected covariance diag
[     0.839       0.89      0.954]
            
M=1000
residuals 2 (1000, 3) 0.001
mean [   9.5e-05      0.159      -1.12]
actual covariance diag
[     0.151   1.33e+03   2.03e+06]
expected covariance diag
[     0.195   1.57e+03   2.19e+06]
actual/expected covariance diag
[     0.772      0.846      0.927]

        '''
        '''
        (self.t+self.tau)-t
residuals 2 (10, 3) 0.001
mean [    0.0582       7.76        304]
actual covariance diag
[     0.251   2.25e+03   3.17e+06]
expected covariance diag
[     0.195   1.63e+03   2.44e+06]
actual/expected covariance diag
[      1.29       1.38        1.3]
        
        0.0
residuals 2 (10, 3) 0.001
mean [      0.13       16.6        582]
actual covariance diag
[    0.0966    1.1e+03   1.68e+06]
expected covariance diag
[     0.195    1.6e+03   2.31e+06]
actual/expected covariance diag
[     0.495      0.691      0.729]

        t-(self.t+self.tau)
residuals 2 (10, 3) 0.001
mean [     0.198       20.8        847]
actual covariance diag
[     0.195   2.08e+03   3.72e+06]
expected covariance diag
[     0.195   1.57e+03   2.19e+06]
actual/expected covariance diag
[     0.997       1.33        1.7]        
        ''' 
        '''
    1st order, M = 1000 @ N=50
    0: [      0.97       1.01]
    2nd order, M = 1000 @ N=50
    0: [     0.868      0.901      0.931]
    3rd order, M = 1000 @ N=50
    0: [     0.662      0.707      0.776      0.826]
    4th order, M = 1000 @ N=50
    0: [     0.601      0.717      0.812      0.878      0.926]    
    5th order, M = 1000 @ N=50
   -1: [      0.49      0.586      0.658      0.705      0.742      0.773]
    0: [      0.47      0.599      0.702      0.772      0.825      0.866]
   +1: [     0.515      0.627      0.714      0.771      0.812      0.843]
        '''

    def xtest_VerifyStatistics(self):
        """
        This OVERNIGHT test verifies the output statistics of the EMP filters
        
        """
        for order in range(1,5+1) :
            results = zeros([1000, 2*(5+1)])
            for i in range(0,results.shape[0]) :
                emp = makeEMP(order, 0.1)
                results[i,0:2*(order+1)] = self.empResidualsDriver(emp, N=1000 )
            print(order, A2S(mean(results,axis=0)));
        '''    
1,000 samples
1 [   -0.0114    -0.0199      0.833      0.748          0          0          0          0          0          0          0          0]
2 [    0.0283     0.0402     0.0464      0.903      0.857      0.798          0          0          0          0          0          0]
3 [  -0.00146    0.00337    0.00658      0.007      0.939      0.919      0.881      0.843          0          0          0          0]
4 [  -0.00836    -0.0062    -0.0066   -0.00848    -0.0105      0.944      0.934      0.912      0.889      0.866          0          0]
5 [   0.00138    0.00554    0.00683     0.0081    0.00903    0.00964      0.942       0.94      0.929      0.914      0.898      0.881]
----------------------------------------------------------------------
Ran 1 test in 779.125s
10,000 samples 
1 [  -0.00214   -0.00339      0.824      0.739          0          0          0          0          0          0          0          0]
2 [  0.000479    0.00219    0.00389      0.914      0.868      0.807          0          0          0          0          0          0]
3 [   0.00214   0.000481  -0.000163   -0.00101      0.934      0.914      0.878      0.841          0          0          0          0]
4 [ -3.45e-05   -0.00202    -0.0021   -0.00236   -0.00261       0.94      0.931       0.91      0.886      0.863          0          0]
5 [ -1.08e-05   0.000114   0.000696    0.00138    0.00207    0.00272       0.94      0.938      0.927      0.913      0.897       0.88]
----------------------------------------------------------------------
Ran 1 test in 7827.419s                  
        '''
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testEMP0']
    unittest.main()
    