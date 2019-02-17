'''
Created on Feb 13, 2019

@author: NOOK
'''
import unittest

from PolynomialFiltering.Components.ExpandingMemoryPolynomialFilter import *

from TestUtilities import *
from numpy import arange, array2string, zeros
from numpy.random import randn
from math import sqrt, sin
from runstats import Statistics


class Test(unittest.TestCase):

    Y0 = array([1e4, 1e3, 1e2, 1e1, 1e0, 1e-1]);

    def setUp(self):
        pass


    def tearDown(self):
        pass

    def empDriver(self, order, filter, N=100, M=50):
        (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], 1.0)
        filter.start(0.0, array([0]))
        stats = [];
        for i in range(0, order+1): 
            stats.append(Statistics())
        nstats = Statistics()
        for i in range(0,N) :
            (Zstar, dt, dtau) = filter.predict(times[i][0])
            e = observations[i] - Zstar[0]
            filter.update(times[i][0], dtau, Zstar, e)
            
            Yf = filter.getState(times[i][0])
            r = array2string(Yf, formatter={'float_kind':lambda y: "%10.4g" % y})
            r = ("EMP%d: %5d %10.6g %10.6g %s %10.6g" % \
                 (order, i, times[i][0], truth[i,0], r, Yf[0]-truth[i,0]))
#             print(r)
            if (i > N-M) :
                for o in range(0,len(Yf)) :
                    stats[o].push( Yf[o] - truth[i,o] )
                nstats.push( noise[i] )
#         print(stats.variance(), nstats.variance(), filter.VRF(N)*nstats.variance())
#         print(order, N, M)
#         for o in range(0,len(Yf)) :
#             print("%5d %5d %12.6g %12.6g %12.6g %12.6g" % \
#                   (order,o,stats[o].variance(), nstats.variance(), filter.VRF()[o], stats[o].variance() / (nstats.variance()*filter.VRF()[o])))
        for o in range(0,len(Yf)) :
            msg = "Excess variance %d,%d: %10.6g, %10.6g, %10.6g" % (o, N-M, stats[o].variance(), nstats.variance(), filter.VRF()[o])
            self.assertLess(stats[o].variance(), filter.VRF()[o]*nstats.variance(), msg)
        


    def test_EMP0(self):
        emp = EMP0(1.0)
        self.empDriver(0, emp, N=500)
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
        
    def test_makeEMP(self):
        for order in range(0,5+1) :
            emp = makeEMP(order, 1.0)
            
    def test_EMP1(self):
        emp = EMP1(1.0)
        self.empDriver(1, emp, N=500)

    def test_EMP2(self):
        emp = EMP2(1.0)
        self.empDriver(2, emp, N=500)

    def test_EMP3(self):
        emp = EMP3(1.0)
        self.empDriver(3, emp, N=500)

    def test_EMP4(self):
        emp = EMP4(1.0)
        self.empDriver(4, emp, N=500)

    def test_EMP5(self):
        emp = EMP5(1.0)
        self.empDriver(5, emp, N=1000)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testEMP0']
    unittest.main()