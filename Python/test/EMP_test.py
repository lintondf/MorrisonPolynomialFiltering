'''
Created on Feb 13, 2019

@author: NOOK
'''
import unittest

from PolynomialFiltering.Components.ExpandingMemoryPolynomialFilter import *
from PolynomialFiltering.Components.FixedMemoryPolynomialFilter import FixedMemoryFilter

from copy import deepcopy
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
# from gevent.libev.corecext import stat

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class Test(unittest.TestCase):

    Y0 = array([1e4, -5e3, +1e3, -5e2, +1e2, -5e1]);

    cdf = None;

    @classmethod
    def setUpClass(cls):
        cls.cdf = Dataset("../../testdata/ExpandingMemoryFiltering.nc", "w", format="NETCDF4");

    @classmethod
    def tearDownClass(cls):
        cls.cdf.close()

    def setUp(self):
        pass


    def tearDown(self):
        pass

    def empPerfect(self, order, filter, tau=1.0, N=100):
        (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], tau, sigma=0.0)
        filter.start(0.0, self.Y0[0:order+1])
        residuals = zeros([N, order+1]);
        for i in range(1,N) :
            Zstar = filter.predict(times[i][0])
            e = observations[i] - Zstar[0]
            filter.update(times[i][0], Zstar, e)
            Yf = filter.getState()
            assert_allclose( Yf, truth[i,0:order+1], atol=1e-12 )
            residuals[i,:] - Yf - truth[i,0:order+1];
#         print(cov(residuals, rowvar=True))
        return residuals;

#     def empKronecker(self, order, emp, tau=1.0, N=100, K=50):
#         (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], tau, sigma=0.0)
#         emp.start(0.0, zeros([order+1]))
#         residuals = zeros([N, order+1]);
#         for i in range(1,N) :
#             Zstar = emp.predict(times[i][0])
#             if i == K :
#                 e = 1;
#             else :
#                 e = 0;
#             emp.update(times[i][0], Zstar, e)
#             Y = emp.getState(times[i][0])
#             if (i == K) :
#                 print(i, A2S(Y))
#                 Y = emp.getState(times[i][0])
#                 Y.shape = (order+1, 1)
#                 C = Y @ Y.T
#                 print(K,  i)
#                 print(A2S(C))
#                 F = emp.stateTransitionMatrix(emp.order+1, -emp.tau);
#                 V = emp._VRF();
#                 print(A2S(V))
#                 V = (F @ V @ F.T)
#                 D = (V / C)
#                 print(D)
#                 D = 1*diag(D)
#                 D /= D[0];
#                 print(A2S(D))
# #         Y = emp.getState(emp.getTime())
# #         Y.shape = (order+1, 1)
# #         C = Y @ Y.T
# #         print(K,  emp.getN())
# #         print(A2S(C))
# #         print((emp._VRF() / C))
        
            
#     def empUnscented(self, order, filter, tau=1.0, N=200, M=100):
#         (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], tau, sigma=0.0)
#         filter.start(0.0, self.Y0[0:order+1])
#         residuals = zeros([N+M, order+1]);
#         for i in range(1,M) :
#             Zstar = filter.predict(times[i][0])
#             e = observations[i] - Zstar[0]
#             filter.update(times[i][0], Zstar, e)
#             Yf = filter.getState(times[i][0])
#             assert_allclose( Yf, truth[i,0:order+1], atol=1e-12 )
#             residuals[i,:] - Yf - truth[i,0:order+1];
#         empP1 = deepcopy(filter)
#         empM1 = deepcopy(filter)
#         Zstar = filter.predict(times[M][0])
#         if (True) :
#             N = M + 10
#             for M in range(M, N) :
#                 k = -0.5
#                 n = 1.0
#                 w0 = k/(n+k)
#                 wi = 1.0/(2*(n+k))
#                 s = sqrt(n+k)
#     #         A = wi * array([-s, +s])
#     #         O = array([-s, +s]);
#     #             print(i, wi*(O @ O.T))
#                 e0 = observations[M] - Zstar[0]
#                 em1 = (observations[M] - s) - Zstar[0]
#                 ep1 = (observations[M] + s) - Zstar[0]
#                 filter.update(times[M][0], Zstar, e0)
#                 y0 = filter.getState(times[M][0])
#                 empP1.update(times[M][0], Zstar, em1)
#                 ym1 = empP1.getState(times[M][0])
#                 empM1.update(times[M][0], Zstar, ep1)
#                 yp1 = empM1.getState(times[M][0])
#                 zm1 = wi*(ym1 - y0);
#                 zm1.shape = (4,1)
#                 zp1 = wi*(yp1 - y0);
#                 zp1.shape = (4,1)
#         #         print(A2S(zm1), A2S(zp1))
#                 C = zm1 @ zm1.T
#                 C += zp1 @ zp1.T;
#                 print(M, diag(filter._VRF() / C))
#         else :
#             s = 1e-3;
#             e0 = observations[M] - Zstar[0]
#             em1 = (observations[M] - s) - Zstar[0]
#             ep1 = (observations[M] + s) - Zstar[0]
#             filter.update(times[M][0], Zstar, e0)
#             y0 = filter.getState(times[M][0])
#             empP1.update(times[M][0], Zstar, em1)
#             ym1 = empP1.getState(times[M][0])
#             empM1.update(times[M][0], Zstar, ep1)
#             yp1 = empM1.getState(times[M][0])
#             dy = yp1 - ym1;
#             dy.shape = (4,1)
#             dy /= 2*s
#             C = dy @ dy.T
# #         print(filter.n, filter.tau)
# #         print(C)
# #         print(filter._VRF())
#         print(M, diag(filter._VRF() / C))
#             
            
            
    def empDriver(self, filter : EMPBase, times, truth, observations):
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
            V = filter.getCovariance(1); # _VRF(); # 
            if (V[0,0] != 0) :
                diagV[i,:] = (diag(V));       
        return (actual, diagV, V);
    
    
#     def empResidualsDriver(self, filter : EMPBase, N : int):
#         (actual, truth, diagV, V) = self.empDriver(filter, N, filter.order)
#         r = actual - truth;
#         r = r[5:,:] / diagV[5:,:];
#         return concatenate([mean(r,axis=0), std(r,axis=0)], axis=0);

#     def xtest_EMP0(self):
#         emp = EMP0(0.1)
#         self.empDriver(emp, N=101, dataOrder=emp.order )
#             
#     def xtest_EMP1(self):
#         emp = EMP1(0.1)
#         self.empDriver(emp, N=101, dataOrder=emp.order )
#         
#     def xtest_EMP2(self):
#         emp = EMP2(0.5)
#         self.empDriver(emp, N=101, dataOrder=emp.order )

    def test_EMPPerfect(self):
        iCase = 0;
        N = 10;
        tau = 1.0;
        R = 0;
        for order in range(0,5+1) :
            emp = makeEMP(order, tau);
            group = createTestGroup(self.cdf, 'testEMPPerfect_%d' % (order) );
            setup = array([order, tau, N, R])
            (times, truth, observations, noise) = \
                generateTestData(emp.order, N, 0.0, self.Y0[0:emp.order+1], emp.tau, sigma=sqrt(R))

            data = concatenate([times, observations, truth], axis=1);
            
            writeTestVariable(group, 'setup', setup);
            writeTestVariable(group, 'data', data);
        
            (actual, diagV, V) = self.empDriver(emp, data[:,0], data[:,2:], data[:,1] )

            writeTestVariable(group, 'expected', actual);
            assert_allclose( actual, truth, atol=1e-8, rtol=0 );
            
    def test_EMP(self):
        iCase = 0;
        for order in range(0,5+1) :
            for tau in [1e-3, 1e-2, 1e-1, 1, 1e1, 1e2] :
                N = (1+order) * 4000
                emp = makeEMP(order, tau);
                R = 1e4;
                print(order, tau, N)
                
                iCase += 1;
                group = createTestGroup(self.cdf, 'EMPFullSuite_%d' % (iCase) );
                setup = array([order, tau, N, R])
                (times, truth, observations, noise) = \
                    generateTestData(emp.order, N, 0.0, self.Y0[0:emp.order+1], emp.tau, sigma=sqrt(R))
                
                data = concatenate([times, observations, truth], axis=1);
                
                writeTestVariable(group, 'setup', setup);
                writeTestVariable(group, 'data', data);
                    
                (actual, diagV, V) = self.empDriver(emp, data[:,0], data[:,2:], data[:,1] )

                writeTestVariable(group, 'expected', actual);
            
                fixed = FixedMemoryFilter(emp.order, N);
                for i in range(0,N) :
                    fixed.add(times[i], observations[i]);
                X = V / fixed.getCovariance();  # EMP VRF vs Fixed MP VRF
                Y = fixed.getState();
#                 print( (actual[-1,:] - Y) / Y )
#                 print( A2S((V / fixed.getCovariance())-1))
                assert_allclose( actual[-1,:], Y, rtol=1e-5, atol=0, verbose=True)
                assert_allclose( X, ones([emp.order+1, emp.order+1]), rtol=2e-3, atol=0, verbose=True )
            
 
    def xtest_EMP3(self):
        for tau in [1e-3, 1e-2, 1e-1, 1, 1e1, 1e2] :
            emp = EMP3(tau)
            for N in [5000] : # [100, 500, 1000, 2000, 5000] :
                print(tau, N)
                R = 1e4;
                (times, truth, observations, noise) = \
                    generateTestData(emp.order, N, 0.0, self.Y0[0:emp.order+1], emp.tau, sigma=sqrt(R))
                (actual, truth, diagV, V) = self.empDriver(emp, times, truth, observations, noise )
                last = (actual[-1,:] - truth[-1,:]) / (noise[-1]**2);
                last.shape = (emp.order+1,1)
        #         print( A2S(last @ last.T))
        #         print(A2S(actual[-1,:]))
        #         print(A2S(V))
                fixed = FixedMemoryFilter(emp.order, N);
                for i in range(0,N) :
                    fixed.add(times[i], observations[i]);
        #         print(A2S(fixed.getState(fixed.getTime())))
        #         print(A2S(fixed.getVRF()))
        #         
        #         print( actual[-1,:] - fixed.getState(fixed.getTime()) )
                X = V / fixed.getCovariance();  # EMP VRF vs Fixed MP VRF
                assert_allclose( X, ones([emp.order+1, emp.order+1]), atol=1e-2 )


#     def xtest_EMP4(self):
#         emp = EMP4(1.5)
#         self.empDriver(emp, N=101, dataOrder=emp.order )
#  
#     def xtest_EMP5(self):
#         N = 1000;
#         M = 1000;
#         K = 500;
#         stats = zeros([M,3+1]);
#         actual = zeros([K*M, 3+1]);
#         for m in range(0,M) :
#             emp = EMP3(1e0)
#             dataOrder = 3;
#             for sigma in [10] :
#                 (times, truth, observations, noise) = generateTestData(dataOrder, N, 0.0, self.Y0[0:emp.order+1], emp.tau, sigma=sigma)
#                 R = var(noise)
#                 data = zeros([N, 2]);
#                 data[:,0] = times[:,0];
#                 data[:,1] = observations[:,0];
#         #         print('noise std', std( data[-500:,1] - truth[-500:,0]))
#                 
#                 emp.start(times[0,0], self.Y0[0:emp.order+1])
#                 V = 0;
#                 for i in range(1,N) :
#                     Zstar = emp.predict(times[i,0])
#                     e = observations[i] - Zstar[0]
#                     emp.update(times[i,0], Zstar, e)
#                     if (i >= N-K) :
#                         V = emp.getCovariance(data[i,0], R)
#                         actual[m*K + i-(N-K),:] = (emp.getState(times[i,0]) - truth[i,:]) # / sqrt(diag(V))
#                     
#         print(emp.tau, N, sigma, A2S(mean(actual,axis=0)), A2S(std(actual,axis=0)))

#         plt.close('all')
#         f0 = plt.figure(figsize=(10, 6))
#         ax = plt.subplot(1, 1, 1)
#         ax.plot(times[M:], truth[M:,0], 'r-', times[M:], observations[M:], 'b.', times[M:], actual[M:,0], 'k-')
#         f1 = plt.figure(figsize=(10, 6))
#         A = (f1.add_subplot(2, 2, 1), f1.add_subplot(2, 2, 2), f1.add_subplot(2, 2, 3), f1.add_subplot(2, 2, 4));
#         for i in range(0,min([4, truth.shape[1]-1, actual.shape[1]-1])) :
#             A[i].plot(times[M:], truth[M:,1+i], 'r-', times[M:], actual[M:,1+i], 'k-')
#         plt.show()
        
#     def xtest_EMP5A(self):
#         K = 40;
#         for tau in [1e-3, 1e-2, 1e-1, 1, 1e1, 1e2] :
#             print('tau', tau)
#             emp = EMP5(tau)
#             (actual, truth, diagV, V) = self.empDriver(emp, N=1001, dataOrder=emp.order )
#             residuals = actual[K:,:] - truth[K:,0:emp.order+1];
#             print( 'mean', A2S( mean(residuals, axis=0) ) )
# #             print('actual covariance diag')
# #             C = cov(residuals, rowvar=False);
# #             print( A2S( diag(C) ) )
# #             print('predicted covariance diag')
# #             print( A2S( diag(V) ) )
 
#     def xtest_EMPVRF(self):
#         for tau in [1e-3] : #[1e-3, 1e-2, 1e-1, 1, 1e1, 1e2] :
#             M = 10000;  # number of runs
#             N = 50;    # number of observations
#             for order in range(2,2+1) :
#                 residuals = zeros([0, (order+1)]) # final sample residuals for all runs
#                 for i in range(0,M) :
#                     emp = makeEMP(order, tau)
#                     (actual, truth, diagV, V) = self.empDriver(emp, N=N, dataOrder=filter.order );
#                     r = actual - truth;
#                     residuals = concatenate([residuals, r[N-1:N,:]], axis=0 );
#             print('residuals %d' % order, residuals.shape, tau);
#             # print( A2S( residuals) )
#             print( 'mean', A2S( mean(residuals, axis=0) ) )
#             print('actual covariance diag')
#             C = cov(residuals, rowvar=False);
#             print( A2S( diag(C) ) )
#             print('expected covariance diag')
#             print( A2S(diag(V)))   
#             print('actual/expected covariance diag')
#             print( A2S(diag(C / V)) )
# #         if (not allclose(V, V.T, atol=1e-14)) :
# #             print(A2S(V-V.T))
#             '''
# M = 10000
# residuals 2 (10000, 3) 0.001
# mean [   0.00458      0.348       14.2]
# actual covariance diag
# [     0.164   1.39e+03   2.08e+06]
# expected covariance diag
# [     0.195   1.57e+03   2.19e+06]
# actual/expected covariance diag
# [     0.839       0.89      0.954]
#             
# M=1000
# residuals 2 (1000, 3) 0.001
# mean [   9.5e-05      0.159      -1.12]
# actual covariance diag
# [     0.151   1.33e+03   2.03e+06]
# expected covariance diag
# [     0.195   1.57e+03   2.19e+06]
# actual/expected covariance diag
# [     0.772      0.846      0.927]
# 
#         '''
#         '''
#         (self.t+self.tau)-t
# residuals 2 (10, 3) 0.001
# mean [    0.0582       7.76        304]
# actual covariance diag
# [     0.251   2.25e+03   3.17e+06]
# expected covariance diag
# [     0.195   1.63e+03   2.44e+06]
# actual/expected covariance diag
# [      1.29       1.38        1.3]
#         
#         0.0
# residuals 2 (10, 3) 0.001
# mean [      0.13       16.6        582]
# actual covariance diag
# [    0.0966    1.1e+03   1.68e+06]
# expected covariance diag
# [     0.195    1.6e+03   2.31e+06]
# actual/expected covariance diag
# [     0.495      0.691      0.729]
# 
#         t-(self.t+self.tau)
# residuals 2 (10, 3) 0.001
# mean [     0.198       20.8        847]
# actual covariance diag
# [     0.195   2.08e+03   3.72e+06]
# expected covariance diag
# [     0.195   1.57e+03   2.19e+06]
# actual/expected covariance diag
# [     0.997       1.33        1.7]        
#         ''' 
#         '''
#     1st order, M = 1000 @ N=50
#     0: [      0.97       1.01]
#     2nd order, M = 1000 @ N=50
#     0: [     0.868      0.901      0.931]
#     3rd order, M = 1000 @ N=50
#     0: [     0.662      0.707      0.776      0.826]
#     4th order, M = 1000 @ N=50
#     0: [     0.601      0.717      0.812      0.878      0.926]    
#     5th order, M = 1000 @ N=50
#    -1: [      0.49      0.586      0.658      0.705      0.742      0.773]
#     0: [      0.47      0.599      0.702      0.772      0.825      0.866]
#    +1: [     0.515      0.627      0.714      0.771      0.812      0.843]
#         '''

#     def xtest_VerifyStatistics(self):
#         """
#         This OVERNIGHT test verifies the output statistics of the EMP filters
#         
#         """
#         for order in range(1,5+1) :
#             results = zeros([1000, 2*(5+1)])
#             for i in range(0,results.shape[0]) :
#                 emp = makeEMP(order, 0.1)
#                 results[i,0:2*(order+1)] = self.empResidualsDriver(emp, N=1000 )
#             print(order, A2S(mean(results,axis=0)));

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testEMP0']
    unittest.main()
    