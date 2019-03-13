'''
Created on Feb 15, 2019

@author: NOOK
'''
import unittest

from PolynomialFiltering.Components.FadingMemoryPolynomialFilter import *

from TestUtilities import *
from numpy import arange, array2string, cov, zeros, mean, std, var, diag,\
    transpose, concatenate, isscalar
from numpy.random import randn
from numpy.testing import assert_almost_equal
from numpy.testing.nose_tools.utils import assert_allclose
from math import sqrt, sin
from runstats import Statistics
from scipy.stats._continuous_distns import chi2
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class Test(unittest.TestCase):

    Y0 = array([1e4, -5e3, +1e2, -5e1, +1e1, -5e0]);


    cdf = None;

    @classmethod
    def setUpClass(cls):
        cls.cdf = Dataset("../../testdata/FadingMemoryFiltering.nc", "w", format="NETCDF4");

    @classmethod
    def tearDownClass(cls):
        cls.cdf.close()
        
    def setUp(self):
        pass


    def tearDown(self):
        pass

    def fmpPerfect(self, order, filter, tau=1.0, N=100):
        (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], tau, sigma=0.0)
        filter.start(0.0, self.Y0[0:order+1])
        residuals = zeros([N, order+1]);
        for i in range(1,N) :
            Zstar = filter.predict(times[i][0])
            e = observations[i] - Zstar[0]
            filter.update(times[i][0], Zstar, e)
            Yf = filter.getState(times[i][0])
            assert_almost_equal( Yf, truth[i,0:order+1] )
            residuals[i,:] - Yf - truth[i,0:order+1];
        return residuals;
            
#     def fmpNoisy(self, order, filter, tau=1.0, N=100):
#         (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], tau, sigma=1.0)
#         filter.start(0.0, self.Y0[0:order+1])
#         E = zeros([N,order+1]);
#         for i in range(1,N) :
#             Zstar = filter.predict(times[i][0])
#             e = observations[i] - Zstar[0]
#             filter.update(times[i][0], Zstar, e)
#             Yf = filter.getState(times[i][0])
# #             assert_almost_equal( Yf, truth[i,0:order+1] )
#             E[i,:] = Yf - truth[i,:]
# #             print(i, A2S(Yf), A2S(truth[i,:]), A2S(E[i,:]) )
#         C = cov(E,rowvar=False); #  / filter.VRF()
#         print('C', A2S(C.flatten()))
         
    def fmpDriver(self, filter : FMPBase, times, truth, observations):
        N = len(times)
        actual = zeros([N, filter.order+1]);
        actual[0,:] = truth[0,:];
        
        filter.start(times[0], actual[0,:]);
        for i in range(1,N) :
            Zstar = filter.predict(times[i])
            e = observations[i] - Zstar[0]
            filter.update(times[i], Zstar, e)
            actual[i,:] = filter.getState(times[i])
        V = filter.getCovariance(times[i]+filter.getTau(), 1); # _VRF(); # 
        return (actual, V);
    
    def test_FMPPerfect(self):
        iCase = 0;
        N = 10;
        tau = 1.0;
        R = 0;
        iCase = 0;
        for theta in [0.5, 0.75, 0.80, 0.95, 0.975, 0.99, 0.999] : 
            for order in range(0,5+1) :
                fmp = makeFMP(order, theta, tau);
                iCase += 1;
                group = createTestGroup(self.cdf, 'testFMPPerfect_%d' % (iCase) );
                setup = array([order, theta, tau, N, R])
                (times, truth, observations, noise) = \
                    generateTestData(fmp.order, N, 0.0, self.Y0[0:fmp.order+1], fmp.tau, sigma=sqrt(R))
    
                data = concatenate([times, observations, truth], axis=1);
                
                writeTestVariable(group, 'setup', setup);
                writeTestVariable(group, 'data', data);
            
                (actual, V) = self.fmpDriver(fmp, data[:,0], data[:,2:], data[:,1] )
    
                writeTestVariable(group, 'expected', actual);
                assert_allclose( actual, truth, atol=1e-8, rtol=0 );
    
    def testFMP(self):
        M = 1000;
        iCase = 0;
        for order in range(0,5+1): 
            results = zeros([M, (order+1)]);
            N = 1000;
            tau = 1.0;
            R = 1;
            theta = 0.9;
            setup = array([order, theta, tau, N, R])
            iCase += 1;
            group = createTestGroup(self.cdf, 'testFMPRandom_%d' % (iCase) );
            fmp = makeFMP(order, theta, tau);
            (times, truth, observations, noise) = \
                generateTestData(fmp.order, N, 0.0, self.Y0[0:fmp.order+1], fmp.tau, sigma=sqrt(R))
    #         print(A2S(truth))
            data = concatenate([times, observations, truth], axis=1);
            
            writeTestVariable(group, 'setup', setup);
            writeTestVariable(group, 'data', data);
            
            (actual, V) = self.fmpDriver(fmp, data[:,0], data[:,2:], data[:,1] )
            
            writeTestVariable(group, 'expected', actual);
            
            residuals = actual - truth;
#             print(A2S( mean(residuals,axis=0)))
            F = fmp.stateTransitionMatrix(order+1, -1)
            V = F @ V @ transpose(F);
            dRV = diag(R*V)
            P = cov(residuals,rowvar=False);
            if (len(P.shape) == 0) :
                dP = array([P]);
            else :
                dP = diag(P)
            E = P/(R*V)
            print(order, max(E.flatten()), min(E.flatten())) 
            print(A2S(E))
            assert_allclose( P/(R*V), ones(P.shape), rtol=0, atol=0.25 )
#             results[iCase,:] = concatenate([dP/dRV]);
#             print(A2S(results[iCase,:]))
#         m = mean(results, axis=0)
#         s = var(results, axis=0)
#         print(order, A2S(m))
        '''
            1000,1000
1 [     0.991      0.996]
2 [     0.982      0.996      0.995]
3 [     0.993          1      0.999      0.999]
4 [     0.986      0.996      0.995      0.995      0.995]
5 [      0.98      0.995      0.995      0.994      0.994      0.994]
----------------------------------------------------------------------
Ran 2 tests in 388.745s
            10000,1000
1 [     0.989      0.995]
2 [     0.991      0.995      0.995]
3 [     0.991      0.997      0.997      0.996]
4 [     0.987      0.997      0.996      0.996      0.996]
5 [     0.981      0.996      0.996      0.996      0.995      0.995]
----------------------------------------------------------------------
Ran 2 tests in 3745.461s            
        '''            
#             print(A2S(dRV))
#         print(A2S(s))
#         assert_allclose( m[2*(order+1):], ones([order+1]), atol=0.0025, rtol=0) 
#         print(A2S( P ))
#         print(A2S( P / (R*V) ))
        
#         print(var(noise))
#         print(var(observations[:,0] - truth[:,0]))
#         Q = ((observations[:,0] - truth[:,0]) - noise[:,0])
#         print(A2S(Q))
#         print(observations.shape, noise.shape, truth[:,0].shape, Q.shape)
        
        if (False) :
            M = 0;
            f0 = plt.figure(figsize=(10, 6))
            ax = plt.subplot(1, 1, 1)
            ax.plot(times[M:], truth[M:,0], 'r-', times[M:], observations[M:], 'b.', times[M:], actual[M:,0], 'k-')
            f1 = plt.figure(figsize=(10, 6))
            A = (f1.add_subplot(2, 2, 1), f1.add_subplot(2, 2, 2), f1.add_subplot(2, 2, 3), f1.add_subplot(2, 2, 4));
            for i in range(0,min([4, truth.shape[1]-1, actual.shape[1]-1])) :
                A[i].plot(times[M:], truth[M:,1+i], 'ro', times[M:], actual[M:,1+i], 'k-')
            plt.show()
    
#     def oldfmpDriver(self, order, filter, tau=1.0, N=100, nK=10):
#         K = zeros([nK,(order+1)**2])
#         F = stateTransitionMatrix(order+1, -tau)
# #         V = F @ filter.VRF() @ transpose(F);
#         V = filter._VRF();
#         print('V', A2S(V.flatten()))
#         dV = np.sqrt(diag(V))
# #         print(A2S(V))
#         for k in range(0,nK) :
#             (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], tau)
#             varN = var(noise); 
#             filter.start(0.0, self.Y0[0:order+1])
#             E = zeros([N,order+1]);
#             for i in range(0,N) :
#                 Zstar = filter.predict(times[i][0])
#                 e = observations[i] - Zstar[0]
#                 filter.update(times[i][0], Zstar, e)
#                 Yf = filter.getState(times[i][0])
#                 r = ("FMP%d: %5d %10.6g %10.6g %s %s" % \
#                      (order, i, times[i][0], truth[i,0], A2S(Yf), A2S((Yf-truth[i,:])/dV)))
#     #             print(r)
#                 E[i,:] = Yf - truth[i,:]
# #             print(k, np.min(E,axis=0), np.max(E,axis=0) )
#             K[k,:] = (cov(E,rowvar=False) ).flatten();  # 
#         meanR = (mean(K,axis=0))
#         stdR = (std(K,axis=0))
#         minR = np.min(K,axis=0)
#         maxR = np.max(K,axis=0)
#         print( "means = %s" % A2S(meanR) )
#         print( "stds  = %s" % A2S(stdR) )
#         print( "mins  = %s" % A2S(minR) )
#         print( "maxs  = %s" % A2S(maxR) )
#         print( A2S(V.flatten() / meanR))



#     def test_FMP0(self):
#         fmp = FMP0(0.95, 0.1)
#         self.fmpPerfect(0, fmp, tau=fmp.getTau(), N=500)
#         self.fmpDriver(0, fmp, tau=fmp.getTau(), N=500)
 
#     def test_FMP1(self):
#         fmp = FMP1(0.95, 0.1)
#         self.fmpPerfect(fmp.order, fmp, tau=fmp.getTau(), N=500)
#         
#         self.fmpDriver(fmp.order, fmp, tau=fmp.getTau(), N=100, nK=1500)
        '''
        N=100, nK=500
means = [     0.752      0.865      0.865      0.873]
stds  = [     0.384       0.41       0.41        0.4]
mins  = [     0.229      0.286      0.286      0.299]
maxs  = [      3.19       3.13       3.13       2.97]
----------------------------------------------------------------------
Ran 1 test in 32.635s        
        '''
#         failures = 0
#         for i in range(0,10) :
#             self.fmpDriver(1, fmp, tau=fmp.getTau(), N=5000, M=4000)
#         print(failures)
  
#     def xtest_FMP2(self):
#         fmp = FMP2(0.95, 0.1)
#         print('V=',A2S(fmp._VRF().flatten()))
#         residuals = self.fmpPerfect(fmp.order, fmp, tau=fmp.getTau(), N=50)
# #         self.fmpNoisy(fmp.order, fmp, tau=fmp.getTau(), N=10000)
# #         self.fmpDriver(fmp.order, fmp, tau=fmp.getTau(), N=10000, nK=100)
        '''
        tau=0.1
            N=100, nK=50
means = [     0.901      0.998       1.04      0.998          1       1.02       1.04       1.02       1.03]
stds  = [     0.306      0.312      0.308      0.312      0.315      0.315      0.308      0.315      0.317]
mins  = [     0.246      0.284      0.315      0.284      0.282      0.296      0.315      0.296      0.301]
maxs  = [      1.97       2.03        2.1       2.03       2.12       2.17        2.1       2.17       2.21]
----------------------------------------------------------------------
Ran 1 test in 33.035s    
            N=100, nK=1000
means = [    0.0866     0.0398    0.00626     0.0398     0.0208    0.00346    0.00626    0.00346   0.000589]
stds  = [    0.0347     0.0149    0.00224     0.0149    0.00783    0.00128    0.00224    0.00128   0.000218]
mins  = [    0.0224     0.0114    0.00194     0.0114    0.00597    0.00103    0.00194    0.00103   0.000177]
maxs  = [     0.286      0.127     0.0195      0.127     0.0672     0.0112     0.0195     0.0112    0.00193]
means = [    0.0806     0.0372    0.00586     0.0372     0.0195    0.00325    0.00586    0.00325   0.000554]
stds  = [    0.0364     0.0157    0.00236     0.0157    0.00828    0.00136    0.00236    0.00136   0.000231]
mins  = [    0.0224     0.0115    0.00194     0.0115    0.00603    0.00103    0.00194    0.00103   0.000177]
maxs  = [     0.282      0.126     0.0189      0.126     0.0648     0.0105     0.0189     0.0105    0.00176]
----------------------------------------------------------------------
Ran 1 test in 66.056s
            N=100, nK=1500
means = [     0.789      0.874       0.91      0.874      0.876       0.89       0.91       0.89      0.895]
stds  = [     0.318      0.327      0.322      0.327      0.328      0.327      0.322      0.327      0.328]
mins  = [      0.23      0.229      0.242      0.229      0.259      0.273      0.242      0.273      0.282]
maxs  = [      2.31       2.57       2.67       2.57       2.55       2.58       2.67       2.58       2.58]
----------------------------------------------------------------------
Ran 1 test in 100.764s    
        '''
  
#     def test_FMP3(self):
#         fmp = FMP3(0.95, 1.0)
#         print(fmp.VRF())
#         self.fmpDriver(3, fmp, tau=fmp.getTau(), N=500)
#  
#     def test_FMP4(self):
#         fmp = FMP4(0.95, 1.0)
#         print(fmp.VRF())
#         self.fmpDriver(4, fmp, tau=fmp.getTau(), N=500)
#  
#     def test_FMP5(self):
#         fmp = FMP5(0.95, 1.0)
#         print(fmp.VRF())
#         self.fmpDriver(5, fmp, tau=fmp.getTau(), N=1000)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()