'''
Created on Feb 15, 2019

@author: NOOK 
'''
import unittest

from PolynomialFiltering.Components.FadingMemoryPolynomialFilter import *

from TestUtilities import *
from numpy import arange, array2string, cov, zeros, mean, std, var, diag,\
    transpose, concatenate, isscalar, sqrt
from numpy.linalg import eig
from numpy.random import randn
from numpy.testing import assert_almost_equal
from numpy.testing import assert_allclose
from math import sin
# from runstats import Statistics
from scipy.stats import jarque_bera, chi2
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#from CovarianceIntersection import *
from FadingStatistics import RingStatistics

class Test(unittest.TestCase):

    Y0 = array([1, -5, 5, 5, -6*2, -1*4]); #1e4, -5e3, +1e2, -5e1, 1e1, -5e0]);


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
            Yf = filter.getState()
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
#             Yf = filter.getState()
# #             assert_almost_equal( Yf, truth[i,0:order+1] )
#             E[i,:] = Yf - truth[i,:]
# #             print(i, A2S(Yf), A2S(truth[i,:]), A2S(E[i,:]) )
#         C = cov(E,rowvar=False); #  / filter.VRF()
#         print('C', A2S(C.flatten()))
         
    def fmpDriver(self, filter : FMPBase, times, truth, observations):
        N = len(times)
        actual = zeros([N, filter.order+1]);
        residuals = zeros([N, 1]);
        actual[0,:] = truth[0,:];
        
        filter.start(times[0], actual[0,:]);
        for i in range(1,N) :
            Zstar = filter.predict(times[i])
            e = observations[i] - Zstar[0]
            residuals[i,:] = e;
            filter.update(times[i], Zstar, e)
            actual[i,:] = filter.getState()
        return (actual, residuals);
    
    def xtest_FMPPerfect(self):
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
            
                (actual, __) = self.fmpDriver(fmp, data[:,0], data[:,2:], data[:,1] )
    
                writeTestVariable(group, 'expected', actual);
                assert_allclose( actual, truth, atol=1e-8, rtol=0 );
    
    '''
    [     0.915      0.949      0.964      0.974]
    [     0.161      0.163      0.165      0.166]
    [     0.899      0.934      0.952      0.963      0.971]
    [     0.141      0.146       0.15      0.152      0.153]
    [     0.843      0.749      0.747       0.75      0.755       0.76]
    [      0.11     0.0914     0.0912     0.0915     0.0922     0.0929]    
[      0.85      0.752       0.75      0.753      0.758      0.764]
[     0.115     0.0967     0.0964     0.0968     0.0974     0.0982]
[      0.85      0.753      0.751      0.754      0.759      0.765]
[     0.117     0.0969     0.0965     0.0969     0.0975     0.0983]
    '''
    def testFMP(self):
        verbose = False; # True;
        M = 10;
        iCase = 0;
        for order in range(0, 5+1): 
            results = zeros([M, (order+1)]);
#             N = 2000;
            for m in range(0,M) :
#             for N in [1000, 2500, 5000, 10000, 50000] :
                N = 1000;
                tau = 5/N;
                R = eye(1);
                theta = thetaFromVrf(order, tau, 0.1 )
                setup = array([order, theta, tau, N, R])
                iCase += 1;
                print(order, theta, tau)
                group = createTestGroup(self.cdf, 'FMPFullSuite_%d' % (iCase) );
                fmp = makeFMP(order, theta, tau);
                if (verbose) :
                    print( A2S( diag(fmp._VRF())))
            
#                 Y = self.Y0[0:fmp.order+1];
                Y = 1000*sqrt(R[0,0])*randn(fmp.order+1)
                (times, truth, observations, noise) = \
                    generateTestData(fmp.order, N, -1.0, Y, fmp.tau, bias=0.0, sigma=sqrt(R))
                R = var(noise)
                V = fmp.getCovariance(R)
                data = concatenate([times, observations, truth], axis=1);
                
                writeTestVariable(group, 'setup', setup);
                writeTestVariable(group, 'data', data);
                
                (actual, residuals) = self.fmpDriver(fmp, data[:,0], data[:,2:], data[:,1] )
                if (verbose) :
                    print(A2S(truth[0:10,:]))
                    print(A2S(observations[0:10,:]))
                    print(A2S(actual[0:10,:]))
                    print(A2S(actual[0:10,:]-truth[0:10,:]))
                    print('final = ', A2S(actual[-1,:]))
                    print('final errors = ', A2S(actual[-1,:]-truth[-1,:]))

                k = fmp.order + 1 - 1;  # Ny - Nx
                stats = RingStatistics(10);
                nOver5 = 0;
                for i in range(0, residuals.shape[0]) :
                    SSR = residuals[i] * (1/(R+V[0,0])) * residuals[i]
                    if (k == 0) :
                        if (SSR > 4.0) :
                            nOver5 += 1;
                            print(i, residuals[i], SSR)
                    else :
                        NSSR = SSR/k
                        p = chi2.cdf(NSSR, k)
                        stats.update(NSSR);
                        pL = chi2.cdf(stats.getLength()*stats.getMean(),k+stats.getLength());
                        if (pL > 0.05) :
                            print('%3d, %10.3f, %8.6f, %8.6f' % \
                                  (i, NSSR, p, pL) )
                print(iCase, nOver5, 0.05*N)
                assert(nOver5 <= 0.06*N)
#                     if (stats.getMean() > 0.05) :
#                         print(i, stats.getMean(), stats.getVariance(), stats.getSerialCorrelation())
#                 L = 10;
#                 stats = RingStatistics(10);
#                 for i in range(L, residuals.shape[0]) :
# #                     SSR = transpose(residuals[i-L:i]) @ ((1/R)*eye(L)) @ residuals[i-L:i]
#                     SSR = residuals[i] * (1/R) * residuals[i]
#                     NSSR = SSR/k
#                     stats.update(NSSR)
#                     p = chi2.cdf(stats.getMean(), k)
#                     print(i,NSSR,stats.getMean(), chi2.cdf(NSSR, k), p )
#                     if (p > 0.05) :
#                         print(i, NSSR, stats.getMean(), p )
                writeTestVariable(group, 'expected', actual);
                
#                 errors = actual - truth;
#     #             print(A2S( mean(errors,axis=0)))
# #                 F = fmp.stateTransitionMatrix(order+1, -1)
# #                 V = F @ V @ transpose(F);
#                 dV = diag(V)
#                 uR = zeros([order+1, 1])
#                 P = cov(errors,rowvar=False);
#                 uP= mean(errors, axis=0);
# #                 print('uP = ', A2S(uP))
#                 print('P/V = ', A2S(P/V))
#                 print('P = ', A2S(P))
#                 (cP, dP) = covarianceToCorrelation(P);
#                 print(A2S(cP))
#                 print(A2S(dP))
#                 (cR, dR) = covarianceToCorrelation(R*V);
#                 print(A2S(cR))
#                 print(A2S(dR))
                

#                 E = P/(R*V);
# #                 print(A2S(E))
#                 results[iCase,:] = sqrt(diag(E));
#                 if (len(P.shape) == 0) :
#                     dP = array([P]);
#                 else :
#                     dP = diag(P)
#                 uP.shape = uR.shape;
#                 print('%2d, %5d, %10.8f, %6d, %10.6f, %8.4f, %10.3f' % \
#                       (order, iCase, theta, N, tau, \
#                        hellingerDistance(uP, P, uR, R*V), mean(E)))
        
#         print(A2S(results))
#         print(A2S(mean(results,axis=0)))
#         print(A2S(std(results,axis=0)))
        if (False) :
            M = 0;
            f0 = plt.figure(figsize=(10, 6))
            ax = plt.subplot(1, 1, 1)
            ax.plot(times[M:], truth[M:,0], 'r-', times[M:], observations[M:], 'b.', times[M:], actual[M:,0], 'k-')
            f1 = plt.figure(figsize=(10, 6))
            A = (f1.add_subplot(2, 2, 1), f1.add_subplot(2, 2, 2), f1.add_subplot(2, 2, 3), f1.add_subplot(2, 2, 4));
            for i in range(0,min([4, truth.shape[1]-1, actual.shape[1]-1])) :
                A[i].plot(times[M:], truth[M:,1+i], 'r-', times[M:], actual[M:,1+i], 'k-')
            plt.show()
    
#             E = P/(R*V)
#             (cE, dE) = covarianceToCorrelation(E)
#             print('dE', A2S(dE))
#             print('cE', A2S(cE))
#             w, v = eig(E)
#             print('wE', A2S(w))
#             print('vE', A2S(v))
#             print(order, max(E.flatten()), min(E.flatten())) 
#             print('P',A2S(P))
#             print('R', A2S(R*V))
#             Q = covarianceIntersection( P, R*V );
#             print('iPiR',A2S(Q))
#              
#             (cP, dP) = covarianceToCorrelation(P);
# #             print(A2S(cP))
# #             print(A2S(dP))
#             w, v = eig(cP);
#             print('wP', A2S(w))
#             print('vP', A2S(v))
#             (cR, dR) = covarianceToCorrelation(R*V);
# #             print(A2S(cR))
# #             print(A2S(dR))
#             w, v = eig(cR);
#             print('wR', A2S(w))
#             print('vR', A2S(v))
#             cQ = covarianceIntersection(cP, cR)
#             (cQ, _) = covarianceToCorrelation(cQ)
#             print('A2S(cQ))
#             assert_allclose( P/(R*V), ones(P.shape), rtol=0, atol=0.25 )
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
#                 Yf = filter.getState()
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

    def test_VRF(self):
        R = eye(1);
        iCase = 0;
        for order in range(1,1+1) :
            for tau in [1e-4, 1e-3, 1e-2, 1e-1, 1, 1e1, 1e2, 1e3] :
                theta = thetaFromVrf(order, tau, 0.1)
                iCase += 1
                group = createTestGroup(self.cdf, 'testVRF_%d' % (iCase) );
                setup = array([order, theta, tau])
                data = self.Y0;
                
                writeTestVariable(group, 'setup', setup);
                writeTestVariable(group, 'data', data);
                
                fmp = makeFMP(order, theta, tau)
                fmp.start(0.0, self.Y0);
                print(order,theta,tau)
                V0 = fmp.getCovariance(R)
                V1 = fmp.transitionCovariance(fmp.getTime() - tau, R)
                V2 = fmp.transitionCovariance(fmp.getTime() + 2*tau, R)
                expected = concatenate([V0, V1, V2],axis=0);
                print(A2S((expected)))
                writeTestVariable(group, 'expected', expected);
                

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()