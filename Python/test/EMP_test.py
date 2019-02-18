'''
Created on Feb 13, 2019

@author: NOOK
'''
import unittest

from PolynomialFiltering.Components.ExpandingMemoryPolynomialFilter import *

from TestUtilities import *
from numpy import arange, array2string, cov, log, var, zeros, trace, mean, std
from numpy.linalg import inv
from numpy.random import randn
from numpy.testing import assert_almost_equal
from math import sqrt, sin
from runstats import Statistics
from numpy.testing.nose_tools.utils import assert_allclose
from numpy.linalg.linalg import norm

class Test(unittest.TestCase):

    Y0 = array([1e4, 1e3, 1e2, 1e1, 1e0, 1e-1]);

    def setUp(self):
        pass


    def tearDown(self):
        pass

    def empPerfect(self, order, filter, tau=1.0, N=100):
        (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], tau, sigma=0.0)
        filter.start(0.0, self.Y0[0:order+1])
        for i in range(1,N) :
            (Zstar, dt, dtau) = filter.predict(times[i][0])
            e = observations[i] - Zstar[0]
            filter.update(times[i][0], dtau, Zstar, e)
            Yf = filter.getState(times[i][0])
#             print(Yf-truth[i,0:order+1])
            assert_allclose( Yf, truth[i,0:order+1], atol=0, rtol=1e-6 )
            
    def empDriver(self, order, filter, N=100, nK = 1):
        nO = order+2
        K = zeros([nK, N-nO, (order+1)]);
        Ns = zeros([nK, N-nO]);
        for k in range(0,nK) :
            (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], filter.getTau())
            filter.start(times[0,0], array([0]))
            for i in range(0,N) :
                (Zstar, dt, dtau) = filter.predict(times[i][0])
                e = observations[i] - Zstar[0]
                filter.update(times[i][0], dtau, Zstar, e)
                
                Yf = filter.getState(times[i][0])
                if (i > nO) :
                    Ns[k,i-nO] = noise[i];
                    K[k, i-nO,:] = Yf - truth[i,:];
        R = zeros([N-nO, 1+(order+1)**2]);
        for n in range(0, N-nO) :
            filter.n = n + order+1;
            R[n,0] = var(Ns[:,n])
            R[n,1:] = cov(K[:,n,:],rowvar=False).flatten() / filter.VRF().flatten();
        meanR = (mean(R,axis=0))
        stdR = (std(R,axis=0))
        print( A2S(meanR[1:] / meanR[0]) )
        print( A2S(stdR[1:] / stdR[0]) )
#         Ce =  (filter.VRF()*var(noise))
#         # print(trace( C @ Ce ) / (norm(C) * norm(Ce)) )
#         print(norm(C)/norm(Ce))
#         print(log(trace(inv(C) * Ce)))
        
        


#     def test_EMP0(self):
#         emp = EMP0(1.0)
#         self.empDriver(0, emp, N=500)
#         for n in range(0,10) :
#             print(n, emp.gamma(n), emp.VRF(n))
#         for theta in arange(0.1, 1.0, 0.1) :
#             print(theta, emp.nSwitch(theta))
#             
#         emp.start(0, 0);
#         O = 10000.0 + randn(1000, 1)
#         R = zeros(O.shape)
#         t = 0;
#         for o in O :
#             (Zstar, dt, dtau) = emp.predict(t)
#             e = o - Zstar[0]
#             emp.update(t, dtau, Zstar, e)
#             R[t] = emp.getState(t)
#             t += 1;
#         print(R)
#         print(sqrt(emp.VRF(t)), (10000 - R[-1]) )
        
#     def test_makeEMP(self):
#         for order in range(0,5+1) :
#             emp = makeEMP(order, 0.1)
#             self.empPerfect(order, emp, N=500)
#             emp = makeEMP(order, 2.0)
#             self.empPerfect(order, emp, N=500)

            
#     def test_EMP1(self):
#         emp = EMP1(10)
#         self.empDriver(emp.order, emp, N=1000, nK=100)
        
        '''
        Yf - truth
        tau=0.1
            K=100 + noise stats first
                [0.98457225 1.01047578 0.92903188 0.92903188 0.86638912]
                [0.1566378  0.18013081 0.16761266 0.16761266 0.15378694]    
            K=100 divided by noise stats
                [0.93415805 0.83348829 0.83348829 0.77744646]
                [0.83940654 0.82665492 0.82665492 0.75086572]  
            K=1000 divided by noise stats
                [0.93571878 0.91652018 0.91652018 0.89374073]
                [0.68315137 0.72159951 0.72159951 0.71250514]                    
         tau = 2
            K=100
                [0.93999425 0.91518428 0.91518428 0.93104171]
                [0.13060023 0.16446756 0.16446756 0.19803956]
            K=1000
                [0.9265811  0.8835155  0.8835155  0.85533978]
                [0.10378123 0.1034984  0.1034984  0.11668402]
            K=10000          
                [0.95561847 0.92918507 0.92918507 0.90183633]
                [0.10104452 0.11231528 0.11231528 0.12838567]  
            K=100 + noise stats first
                [0.99077459 0.96271042 0.91415027 0.91415027 0.90931497]
                [0.16834897 0.15217879 0.19412622 0.19412622 0.2179416 ]  
            K=1000 divided by noise stats
                [1.03117477 1.01361246 1.01361246 1.02479759]
                [0.89776037 0.83258925 0.83258925 0.69992661]           
        tau=10
            K=1000 divided by noise stats
                [0.98506817 0.93158399 0.93158399 0.93695877]
                [0.54150487 0.53981825 0.53981825 0.57391484]        
        '''
 
    def test_EMP2(self):
        emp = EMP2(0.5)
        self.empDriver(emp.order, emp, N=100, nK=1000)
        '''
        tau=0.5
            N=100, nK=1000
            [      0.99      0.965       1.88      0.965      0.931       1.81       1.88       1.81       3.51]
            [         1        1.1       2.38        1.1       1.17       2.55       2.38       2.55       5.49]
        tau=1.5
            N=1000, nK=100
            [1.0240035  0.9965246  1.95258603 0.9965246  0.96821191 1.89401439 1.95258603 1.89401439 3.69809214]
            [0.88190377 1.05297237 2.36958384 1.05297237 0.99478329 2.02083016 2.36958384 2.02083016 3.90145216]  
            [     0.967      0.983       1.99      0.983      0.999       2.02       1.99       2.02       4.06]
            [      1.14       1.21       2.78       1.21       1.11       2.37       2.78       2.37       4.86] 
            [     0.963      0.958        1.9      0.958      0.949       1.88        1.9       1.88       3.74]
            [      1.04       1.19       2.54       1.19       1.12       2.21       2.54       2.21       4.17]
            
            N=100, nK=1000
            [     0.994      0.961       1.86      0.961      0.925       1.79       1.86       1.79       3.49]
            [      1.02       1.05       2.24       1.05       1.12       2.45       2.24       2.45       5.34]
            
                             
        '''
  
#     def test_EMP3(self):
#         emp = EMP3(1.0)
#         self.empDriver(3, emp, N=1000)
# 
#     def test_EMP4(self):
#         emp = EMP4(1.0)
#         self.empDriver(4, emp, N=2000)
# 
#     def test_EMP5(self):
#         emp = EMP5(1.0)
#         self.empDriver(5, emp, N=4000)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testEMP0']
    unittest.main()