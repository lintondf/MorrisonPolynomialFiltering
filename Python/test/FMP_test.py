    '''
Created on Feb 15, 2019

@author: NOOK
'''
import unittest

from PolynomialFiltering.Components.FadingMemoryPolynomialFilter import *

from TestUtilities import *
from numpy import arange, array2string, zeros
from numpy.random import randn
from numpy.testing import assert_almost_equal
from math import sqrt, sin
from runstats import Statistics
from scipy.stats._continuous_distns import chi2

class Test(unittest.TestCase):

    Y0 = array([1e4, 1e3, 1e2, 1e1, 1e0, 1e-1]);


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def fmpPerfect(self, order, filter, tau=1.0, N=100):
        (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], tau, sigma=0.0)
        filter.start(0.0, self.Y0[0:order+1])
        for i in range(1,N) :
            (Zstar, dt, dtau) = filter.predict(times[i][0])
            e = observations[i] - Zstar[0]
            filter.update(times[i][0], dtau, Zstar, e)
            Yf = filter.getState(times[i][0])
            assert_almost_equal( Yf, truth[i,0:order+1] )
            
            
    def fmpDriver(self, order, filter, tau=1.0, N=100, M=50):
        status = 0;
        (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], tau)
        filter.start(0.0, self.Y0[0:order+1])
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
            r = ("FMP%d: %5d %10.6g %10.6g %s %10.6g" % \
                 (order, i, times[i][0], truth[i,0], r, Yf[0]-truth[i,0]))
#             print(r)
            if (i > N-M) :
                for o in range(0,len(Yf)) :
                    stats[o].push( Yf[o] - truth[i,o] )
                nstats.push( noise[i] )
#             r = array2string(Yf - truth[i,:], formatter={'float_kind':lambda y: "%10.4g" % y}).replace("[","").replace("]","")
#             print("%10.3f %10.4g %s" % (times[i][0], noise[i], r))
                
#         print(stats.variance(), nstats.variance(), filter.VRF()*nstats.variance())
#         print(order, N, M)
#         for o in range(0,len(Yf)) :
#             print("%5d %5d %12.6g %12.6g %12.6g %12.6g" % \
#                   (order,o,stats[o].variance(), nstats.variance(), filter.VRF()[o], stats[o].variance() / (nstats.variance()*filter.VRF()[o])))
        for o in range(0,len(Yf)) :
#             print(o, stats[o].variance(), nstats.variance(), stats[o].variance()/nstats.variance())
            msg = "Excess variance %d %10.3f: sample: %10.6g, noise: %10.6g, VRF: %10.6g, ratio: %10.4g" % \
              (o, times[i][0], stats[o].variance(), nstats.variance(), filter.VRF()[o], stats[o].variance()/(filter.VRF()[o]*nstats.variance()))
            print( o, N, M, (M-1) * stats[o].variance() / (filter.VRF()[o]*nstats.variance()), 
                   isChi2Valid(stats[o].variance(), filter.VRF()[o]*nstats.variance(), M, 0.05) )
#             self.assertLess(stats[o].variance(), filter.VRF()[o]*nstats.variance(), msg)
#             if (stats[o].variance() > 1.1*filter.VRF()[o]*nstats.variance()) :
#                 print(msg)
#                 status = 1;
#                 exit(0)
#         return status
        


#     def test_FMP0(self):
#         fmp = FMP0(0.95, 0.1)
#         self.fmpPerfect(0, fmp, tau=fmp.getTau(), N=500)
#         self.fmpDriver(0, fmp, tau=fmp.getTau(), N=500)
 
    def test_FMP1(self):
        fmp = FMP1(0.95, 0.1)
        print(fmp.VRF())
        self.fmpPerfect(1, fmp, tau=fmp.getTau(), N=500)
        failures = 0
        for i in range(0,10) :
            self.fmpDriver(1, fmp, tau=fmp.getTau(), N=50000, M=40000)
#         print(failures)
  
#     def test_FMP2(self):
#         fmp = FMP2(0.95, 1.0)
#         print(fmp.VRF())
#         self.fmpDriver(2, fmp, tau=fmp.getTau(), N=500)
#  
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