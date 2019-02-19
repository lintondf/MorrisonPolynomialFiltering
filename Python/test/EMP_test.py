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
from numpy.ma.core import isarray

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
        K = zeros([nK, N, (order+1)]);
        Ns = zeros([nK, N]);
        for k in range(0,nK) :
            (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], filter.getTau())
            filter.start(times[0,0], array([0]))
            for i in range(0,N) :
                (Zstar, dt, dtau) = filter.predict(times[i][0])
                e = observations[i] - Zstar[0]
                filter.update(times[i][0], dtau, Zstar, e)
                
                Yf = filter.getState(times[i][0])
                Ns[k,i] = noise[i];
                K[k, i,:] = Yf - truth[i,:];
#                 V = filter.VRF();
#                 if (V is None) :
#                     print(k, -i, A2S(K[k,i,:]))
#                 else :
#                     print(k, i, A2S(K[k,i,:]))
        R = zeros([N, 1+(order+1)**2]);
        iFirst = 0;
        for n in range(0, N) :
            filter.n = n;
            V = filter.VRF();
            if (V is None) :
                iFirst += 1;
            else:
#                 print(n, R[n,:])
                R[n,0] = var(Ns[:,n])
                R[n,1:] = cov(K[:,n,:],rowvar=False).flatten() / (V.flatten());
#                 print(n, A2S(R[n,1:] / R[n,0]), A2S(R[n,:]))
        print(iFirst)
        R = R[filter.order:,:]
        S = R[:,iFirst:];
        for i in range(0, S.shape[1]) :
            S[:,i] /= R[:,0];
#             print(i, R[0,i], A2S(S[:,i]))
        meanR = (mean(S,axis=0))
        stdR = (std(S,axis=0))
        minR = np.min(S,axis=0)
        maxR = np.max(S,axis=0)
        print( "means = %s" % A2S(meanR) )
        print( "stds  = %s" % A2S(stdR) )
        print( "mins  = %s" % A2S(minR) )
        print( "maxs  = %s" % A2S(maxR) )
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
#         emp = EMP1(0.1)
#         self.empDriver(emp.order, emp, N=100, nK=5000)
        
        '''
means = [     0.999      0.999      0.999      0.997]
stds  = [    0.0237     0.0255     0.0255      0.025]
mins  = [     0.928      0.921      0.921       0.92]
maxs  = [      1.04       1.05       1.05       1.05]
        '''
 
#     def test_EMP2(self):
#         emp = EMP2(0.5)
#         self.empDriver(emp.order, emp, N=100, nK=20000)
        '''
        tau=0.5
            N=100, nK=2000
means = [      1.01       1.01       1.01       1.02       1.02       1.01       1.02       1.02]
stds  = [    0.0399     0.0422     0.0399     0.0395     0.0398     0.0422     0.0398     0.0399]
mins  = [     0.919      0.917      0.919      0.926      0.933      0.917      0.933       0.94]
maxs  = [      1.09        1.1       1.09        1.1       1.11        1.1       1.11       1.11]
----------------------------------------------------------------------
Ran 1 test in 108.186s
            N=100, nK=20000
means = [     0.997      0.998      0.997      0.995      0.995      0.998      0.995      0.995]
stds  = [     0.014     0.0161      0.014     0.0148     0.0157     0.0161     0.0157      0.016]
mins  = [     0.964      0.958      0.964      0.958      0.955      0.958      0.955      0.953]
maxs  = [      1.03       1.04       1.03       1.03       1.03       1.04       1.03       1.03]
----------------------------------------------------------------------
Ran 1 test in 1080.757s

        '''
  
#     def test_EMP3(self):
#         emp = EMP3(1.5)
#         self.empDriver(emp.order, emp, N=100, nK=2000 )
        '''
        tau=1.5
            N=100, nK=2000
3
means = [         1      0.999          1          1          1          1          1          1          1          1      0.999          1          1      0.999]
stds  = [    0.0451     0.0489     0.0405     0.0412     0.0424     0.0434     0.0451     0.0424     0.0424     0.0426     0.0489     0.0434     0.0426     0.0424]
mins  = [     0.891      0.882      0.907      0.903      0.903      0.903      0.891      0.903      0.907       0.91      0.882      0.903       0.91      0.913]
maxs  = [      1.11       1.12       1.09       1.09       1.09       1.09       1.11       1.09       1.09       1.08       1.12       1.09       1.08       1.08]
----------------------------------------------------------------------
Ran 1 test in 122.530s        
        '''
 
#     def test_EMP4(self):
#         emp = EMP4(1.0)
#         self.empDriver(emp.order, emp, N=100, nK=2000 )
        '''
        tau=1
            N=100, nK=2000
4
means = [      1.01       1.01          1      0.998      0.998      0.998      0.998       1.01      0.998      0.998      0.999      0.999       1.01      0.998      0.999          1          1       1.01      0.998      0.999          1          1]
stds  = [    0.0572      0.067     0.0356     0.0339     0.0355      0.037     0.0384     0.0462     0.0355     0.0367     0.0379      0.039     0.0572      0.037     0.0379     0.0389     0.0398      0.067     0.0384      0.039     0.0398     0.0404]
mins  = [     0.903      0.879      0.906      0.913       0.92      0.924      0.927      0.906       0.92      0.925      0.915      0.909      0.903      0.924      0.915      0.906      0.901      0.879      0.927      0.909      0.901      0.896]
maxs  = [      1.36       1.45       1.13       1.08       1.09        1.1        1.1       1.25       1.09        1.1       1.11       1.11       1.36        1.1       1.11       1.11       1.11       1.45        1.1       1.11       1.11       1.12]
----------------------------------------------------------------------
Ran 1 test in 192.830s
            
        '''
        
    def test_EMP5(self):
        emp = EMP5(0.1)
        self.empDriver(emp.order, emp, N=100, nK=100 )
        '''
        tau=0.1
            N=100, nK=100
5
means = [      1.04       1.05       1.02       1.03       1.04       1.04       1.05       1.05       1.02       1.04       1.05       1.06       1.06       1.07       1.03       1.04       1.06       1.07       1.07       1.08       1.04       1.05       1.06
               1.07       1.08       1.08       1.05       1.05       1.07       1.08       1.08       1.09]
stds  = [      0.27      0.302      0.163      0.181      0.194      0.201      0.205      0.209      0.198      0.194      0.203      0.207      0.209      0.211      0.234      0.201      0.207       0.21      0.211      0.212       0.27      0.205      0.209
               0.211      0.212      0.212      0.302      0.209      0.211      0.212      0.212      0.213]
mins  = [     0.337      0.199      0.663      0.659      0.661       0.66      0.656      0.649       0.58      0.661      0.672      0.676      0.675      0.672      0.448       0.66      0.676      0.684      0.687      0.687      0.337      0.656      0.675
              0.687      0.693      0.698      0.199      0.649      0.672      0.687      0.698      0.705]
maxs  = [      1.84       1.89       1.64       1.67       1.73       1.77        1.8       1.82       1.72       1.73       1.78       1.82       1.84       1.87       1.79       1.77       1.82       1.85       1.88        1.9       1.84        1.8       1.84
               1.88        1.9       1.92       1.89       1.82       1.87        1.9       1.92       1.94]
----------------------------------------------------------------------
Ran 1 test in 6.374s
        
            N=100, nK=2000
5
means = [     0.994      0.991          1          1      0.999      0.997      0.996      0.995          1      0.999      0.996      0.994      0.993      0.992      0.997      0.997      0.994      0.992      0.991       0.99      0.994      0.996      0.993
              0.991      0.989      0.988      0.991      0.995      0.992       0.99      0.988      0.987]
stds  = [    0.0535     0.0608     0.0315     0.0335     0.0351     0.0363     0.0373     0.0381     0.0387     0.0351     0.0356      0.036     0.0363     0.0367     0.0461     0.0363      0.036      0.036     0.0361     0.0362     0.0535     0.0373     0.0363
             0.0361      0.036     0.0361     0.0608     0.0381     0.0367     0.0362     0.0361      0.036]
mins  = [     0.856      0.844      0.928      0.923      0.919      0.915       0.91      0.906      0.898      0.919      0.912      0.906      0.903        0.9      0.873      0.915      0.906      0.902      0.899      0.897      0.856       0.91      0.903
              0.899      0.897      0.896      0.844      0.906        0.9      0.897      0.896      0.895]
maxs  = [      1.19       1.24       1.07       1.08       1.08       1.08       1.08       1.08       1.09       1.08       1.07       1.07       1.07       1.08       1.13       1.08       1.07       1.07       1.08       1.08       1.19       1.08       1.07
               1.08       1.08       1.08       1.24       1.08       1.08       1.08       1.08       1.09]
----------------------------------------------------------------------
Ran 1 test in 153.871s 
            N=100, nK=10000
5
means = [     0.997      0.997      0.998      0.999      0.999      0.999      0.999      0.999      0.998      0.999      0.999      0.999      0.999      0.999      0.997      0.999      0.999      0.999      0.999      0.999      0.997      0.999      0.999
             0.999      0.999      0.999      0.997      0.999      0.999      0.999      0.999      0.999]
stds  = [    0.0285     0.0313     0.0173     0.0179      0.019       0.02     0.0209     0.0218     0.0216      0.019     0.0198     0.0205     0.0212     0.0219     0.0254       0.02     0.0205     0.0211     0.0216     0.0221     0.0285     0.0209     0.0212
             0.0216      0.022     0.0224     0.0313     0.0218     0.0219     0.0221     0.0224     0.0227]
mins  = [     0.876      0.857      0.953      0.954      0.949      0.946      0.942      0.939      0.932      0.949      0.948      0.946      0.944      0.942      0.901      0.946      0.946      0.945      0.943      0.942      0.876      0.942      0.944
              0.943      0.943      0.942      0.857      0.939      0.942      0.942      0.942      0.942]
maxs  = [      1.06       1.07       1.04       1.04       1.04       1.05       1.05       1.05       1.04       1.04       1.05       1.05       1.05       1.05       1.05       1.05       1.05       1.05       1.05       1.05       1.06       1.05       1.05
               1.05       1.05       1.05       1.07       1.05       1.05       1.05       1.05       1.05]
----------------------------------------------------------------------
Ran 1 test in 647.189s           
        '''

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testEMP0']
    unittest.main()