'''
Created on Jan 24, 2019

@author: NOOK
'''
import unittest

from numpy import array, transpose, zeros, argmin, array2string, var, average
from numpy.linalg import norm
from numpy.random import randn
from Filtering import RecursiveFilterBase, stateTransitionMatrix,\
                      EMP0, EMP1, EMP2, EMP3, EMP4, EMP5, EMP, EMPSet,\
                      FMP0, FMP1, FMP2, FMP3, FMP4, FMP5, FMP, FMPSet, \
                      ReynekeMorrison
from runstats import Statistics
from math import sin
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def generateTestData(order, N, t0, Y0, dt, bias=0.0, sigma=1.0):
    if (order >= 0) :
        truth = zeros([N,order+1])
        noise = bias + sigma*randn(N,1)
        observations = zeros([N])
        times = zeros([N,1])
        S = stateTransitionMatrix(order+1, dt)
        t = t0 + dt
        Y = Y0
        for i in range(0,N) :
            Y = S @ Y
            observations[i] = Y[0] + noise[i]
            times[i] = t
            truth[i,:] = Y[:]
            t = t+dt
    else :
        order = -order
        truth = zeros([N,order+1])
        noise = bias + sigma*randn(N,1)
        observations = zeros([N]) + noise
        times = zeros([N,1])
        t = t0 + dt
        Y = Y0
        for i in range(0,N) :
            Y[0] = Y0[0] + Y0[1]*sin(0.01*t)
            observations[i] += Y[0]
            times[i] = t
            truth[i,:] = Y[:]
            t = t+dt
    return (times, truth, observations, noise)

class Test(unittest.TestCase):
    
    Y0 = array([1e4, 1e3, 1e2, 1e1, 1e0, 1e-1]);

    def setUp(self):
        pass

    def tearDown(self):
        pass


#     def testRecursiveFilterBase(self):
#         for order in range(0,6) :
#             base = RecursiveFilterBase(order)
#             self.assertEqual(base.order, order, "order %d incorrect" % order)
#         try :
#             base = RecursiveFilterBase(-1)
#             self.assertTrue(False, "order -1 not detected")
#         except ValueError as err :
#             pass
#         
#         order = 2
#         base = RecursiveFilterBase(order)
#         Y0 = array([100.0, 10.0, 1.0]);
#         base.initialize(0.0, Y0, 0.1)
#         self.assertEqual(len(base.Z), order+1, "state length incorrect; was %d expected %d" % (len(base.Z), order+1))
#         self.assertEqual(len(base.D), order+1, "Denormalization vector length incorrect")
#         dtau = base._normalizeDeltaTime(0.1)
#         Z = base._predict(dtau)
#         Y = base._denormalizeState(Z)
#         self.assertEqual( Y[0], 100.0+0.1*10.0+0.5*0.1**2*1.0, "Bad prediction element 0")
#         self.assertEqual( Y[1], 10.0+0.1*1.0, "Bad prediction element 1")
#         self.assertEqual( Y[2], 1.0, "Bad prediction element 2")                  

    def testStateTransitionMatrix(self):
        y0 = 100.0
        y1 = 10.0
        y2 = 1.0
        y3 = 0.1
        Y = array([y0, y1, y2]);
        dt = 0.1
        S = stateTransitionMatrix(2+1, dt)
#         print(S)
        for i in range(0,100) :
            y0 += y1*dt + y2 * 0.5*dt**2
            y1 += y2*dt
            Y = S @ Y
            self.assertAlmostEqual( Y[0], y0, 6, "bad y0")
            self.assertAlmostEqual( Y[1], y1, 6, "bad y1")
            self.assertAlmostEqual( Y[2], y2, 6, "bad y2")
        Y = array([y0, y1, y2, y3]);
        dt = 0.1
        S = stateTransitionMatrix(3+1, dt)
#         print(S)
        for i in range(0,100) :
            y0 += y1*dt + y2 * 0.5*dt**2 + y3 * (1.0/6.0)*dt**3
            y1 += y2*dt + y3 * 0.5*dt**2;
            y2 += y3*dt;
            Y = S @ Y
            self.assertAlmostEqual( Y[0], y0, 6, "bad y0")
            self.assertAlmostEqual( Y[1], y1, 6, "bad y1")
            self.assertAlmostEqual( Y[2], y2, 6, "bad y2")
            self.assertAlmostEqual( Y[3], y3, 6, "bad y3")
        
#     def testEMP0(self):
#         N = 100
#         (times, truth, observations, noise) = generateTestData(0, N, 0.0, self.Y0[0:1], 0.1)
# 
#         emp = EMP0()
#         emp.initialize(0.0, array([self.Y0[0]]), 0.1)
#         for i in range(0,N) :
#             emp.add(times[i][0], truth[i,0])
#             Yf = emp.getState(times[i][0])
#             #print(i,Yf,Yf-truth[i,:])
#             self.assertLess(norm((Yf-truth[i,:])/Yf), 1e-6, 'Noiseless state error')
# 
#         emp.restart(0.0, array([self.Y0[0]]))
#         stats = Statistics()
#         nstats = Statistics()
#         for i in range(0,N) :
#             emp.add(times[i][0], observations[i])
#             Yf = emp.getState(times[i][0])
#             if (i > N-30) :
#                 stats.push( Yf[0] - truth[i,0] )
#                 nstats.push( noise[i] )
# #             print(i,Yf,Yf[0]-truth[i,0])
#         self.assertLess( stats.variance(), emp.VRF(N-15)*nstats.variance(), 'Excess noise in state vectors')
# 
#     def testEMP1(self):
#         N = 100
#         (times, truth, observations, noise) = generateTestData(1, N, 0.0, self.Y0[0:1+1], 0.1)
# 
#         emp = EMP1()
#         emp.initialize(0.0, array([self.Y0[0]]), 0.1)
#         for i in range(0,N) :
#             emp.add(times[i][0], truth[i,0])
#             Yf = emp.getState(times[i][0])
#             self.assertLess(norm((Yf-truth[i,:])/Yf), 1e-6, 'Noiseless state error')
# 
#         emp.restart(0.0, array([self.Y0[0]]))
#         stats = Statistics()
#         nstats = Statistics()
#         for i in range(0,N) :
#             emp.add(times[i][0], observations[i])
#             Yf = emp.getState(times[i][0])
#             if (i > N-30) :
#                 stats.push( Yf[0] - truth[i,0] )
#                 nstats.push( noise[i] )
# #             print(i,Yf,Yf[0]-truth[i,0])
#         self.assertLess( stats.variance(), emp.VRF(N-15)*nstats.variance(), 'Excess noise in state vectors')
#         
#     
#     def testEMP2(self):
#         N = 100
#         (times, truth, observations, noise) = generateTestData(2, N, 0.0, self.Y0[0:2+1], 0.1)
# 
#         emp = EMP2()
#         emp.initialize(0.0, array([self.Y0[0]]), 0.1)
#         for i in range(0,N) :
#             emp.add(times[i][0], truth[i,0])
#             Yf = emp.getState(times[i][0])
#             if (emp.getN() > emp.getN0()) :
#                 self.assertLess(norm((Yf-truth[i,:])/Yf), 1e-6, 'Noiseless state error')
# 
#         emp.restart(0.0, array([self.Y0[0]]))
#         stats = Statistics()
#         nstats = Statistics()
#         for i in range(0,N) :
#             emp.add(times[i][0], observations[i])
#             Yf = emp.getState(times[i][0])
#             if (i > N-30) :
#                 stats.push( Yf[0] - truth[i,0] )
#                 nstats.push( noise[i] )
# #             print(i,Yf,Yf[0]-truth[i,0])
#         self.assertLess( stats.variance(), 1.5*emp.VRF(N-15)*nstats.variance(), 'Excess noise in state vectors')
#             
#     def testEMP3(self):
#         N = 100
#         (times, truth, observations, noise) = generateTestData(3, N, 0.0, self.Y0[0:3+1], 0.1)
# 
#         emp = EMP3()
#         emp.initialize(0.0, array([self.Y0[0]]), 0.1)
#         for i in range(0,N) :
#             emp.add(times[i][0], truth[i,0])
#             Yf = emp.getState(times[i][0])
#             if (emp.getN() > emp.getN0()) :
#                 self.assertLess(norm((Yf-truth[i,:])/Yf), 1e-6, 'Noiseless state error')
# 
#         emp.restart(0.0, array([self.Y0[0]]))
#         stats = Statistics()
#         nstats = Statistics()
#         for i in range(0,N) :
#             emp.add(times[i][0], observations[i])
#             Yf = emp.getState(times[i][0])
#             if (i > N-30) :
#                 stats.push( Yf[0] - truth[i,0] )
#                 nstats.push( noise[i] )
# #             print(i,Yf,Yf[0]-truth[i,0])
#         self.assertLess( stats.variance(), emp.VRF(N-15)*nstats.variance(), 'Excess noise in state vectors')
#             
#     def testEMP4(self):
#         N = 100
#         (times, truth, observations, noise) = generateTestData(4, N, 0.0, self.Y0[0:4+1], 0.1)
# 
#         emp = EMP4()
#         emp.initialize(0.0, array([self.Y0[0]]), 0.1)
#         for i in range(0,N) :
#             emp.add(times[i][0], truth[i,0])
#             Yf = emp.getState(times[i][0])
#             if (emp.getN() > emp.getN0()) :
#                 self.assertLess(norm((Yf-truth[i,:])/Yf), 1e-6, 'Noiseless state error')
# 
#         emp.restart(0.0, array([self.Y0[0]]))
#         stats = Statistics()
#         nstats = Statistics()
#         for i in range(0,N) :
#             emp.add(times[i][0], observations[i])
#             Yf = emp.getState(times[i][0])
#             if (i > N-30) :
#                 stats.push( Yf[0] - truth[i,0] )
#                 nstats.push( noise[i] )
# #             print(i,Yf,Yf[0]-truth[i,0])
#         self.assertLess( stats.variance(), emp.VRF(N-15)*nstats.variance(), 'Excess noise in state vectors')
#         
#     def testEMP5(self):
# #         Y0 = array([8, -1, -2*2, -0.02, 0.004, 1e-12])
#         N = 100
#         (times, truth, observations, noise) = generateTestData(5, N, 0.0, self.Y0[0:5+1], 0.1)
# 
#         emp = EMP5()
#         emp.initialize(0.0, array([self.Y0[0]]), 0.1)
#         for i in range(0,N) :
#             emp.add(times[i][0], truth[i,0])
#             Yf = emp.getState(times[i][0])
#             if (emp.getN() > emp.getN0()) :
#                 self.assertLess(norm((Yf-truth[i,:])/Yf), 1e-5, 'Noiseless state error')
# 
#         emp.restart(0.0, array([self.Y0[0]]))
#         stats = Statistics()
#         nstats = Statistics()
#         for i in range(0,N) :
#             emp.add(times[i][0], observations[i])
#             Yf = emp.getState(times[i][0])
#             if (i > N-30) :
#                 stats.push( Yf[0] - truth[i,0] )
#                 nstats.push( noise[i] )
# #             print(i,Yf,Yf[0]-truth[i,0])
#         self.assertLess( stats.variance(), emp.VRF(N-15)*nstats.variance(), 'Excess noise in state vectors')
# 
#     def testEMP(self):
#         N = 100
#         
#         for order in range(0, 5+1) :
#             (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], 0.1)
#             emp = EMP(order)
#             emp.initialize(0.0, array([self.Y0[0]]), 0.1)
#             stats = Statistics()
#             nstats = Statistics()
#             for i in range(0,N) :
#                 emp.add(times[i][0], observations[i])
#                 Yf = emp.getState(times[i][0])
#                 if (i > N-30) :
#                     stats.push( Yf[0] - truth[i,0] )
#                     nstats.push( noise[i] )
#             self.assertLess( stats.variance(), 2*emp.VRF(N-15)*nstats.variance(), 'Excess noise in state vectors')
# 
#     def _testFading(self, order, filter, N=100):
#         (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], 0.1)
#         filter.initialize(0.0, array([self.Y0[0]]), 0.1)
#         stats = Statistics()
#         nstats = Statistics()
#         for i in range(0,N) :
#             filter.add(times[i][0], observations[i])
#             Yf = filter.getState(times[i][0])
#             r = array2string(Yf, formatter={'float_kind':lambda y: "%10.4g" % y})
#             r = ("FM%d: %5d %10.6g %10.6g %s %10.6g %10.6g" % \
#                  (order, i, times[i][0], truth[i,0], r, Yf[0]-truth[i,0], filter.getGoodnessOfFit()))
#             print(r)
#             if (i > N-30) :
#                 stats.push( Yf[0] - truth[i,0] )
#                 nstats.push( noise[i] )
#         print(stats.variance(), nstats.variance(),filter.VRF(filter.theta))
#         
#     def testFMP0(self):
#         self._testFading( 0, FMP0(0.90), 100)
#         
#     def testFMP1(self):
#         self._testFading( 1, FMP0(0.90), 100)
#         
#     def testFMP2(self):
#         self._testFading( 2, FMP0(0.90), 100)
#         
#     def testFMP3(self):
#         self._testFading( 3, FMP0(0.90), 100)
#         
#     def testFMP4(self):
#         self._testFading( 4, FMP0(0.90), 100)
#         
#     def testFMP5(self):
#         self._testFading( 5, FMP0(0.90), 100)
#         
#     def testEMPSet(self):        
#         N = 100
#         order = 5
#         (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], 0.1)
# 
#         emp = EMPSet(order)
#         emp.initialize(0.0, array([self.Y0[0]]), 0.1)
#         for i in range(0,N) :
#             emp.add(times[i][0], truth[i,0])
#             Yf = emp.getState(times[i][0])
# #             print("*EMPSet %d %10.4g %10.4g %10.4g" % (i, Yf[0], truth[i,0], norm((Yf-truth[i,0:len(Yf)])/Yf)))
# #             print( emp.report() )
#             if (emp.current == order) :
#                 self.assertLess(norm((Yf-truth[i,0:len(Yf)])/Yf), 1e-5, 'Noiseless state error')
#             else:
#                 self.assertLess(norm((Yf-truth[i,0:len(Yf)])/Yf), 1, 'Noiseless state error')
# 
#         emp.restart(0.0, array([self.Y0[0]]))
#         stats = Statistics()
#         nstats = Statistics()
#         for i in range(0,N) :
#             emp.add(times[i][0], observations[i])
#             Yf = emp.getState(times[i][0])
#             if (i > N-30) :
#                 stats.push( Yf[0] - truth[i,0] )
#                 nstats.push( noise[i] )
#         r = array2string(Yf, formatter={'float_kind':lambda y: "%10.4g" % y})
#         r = ("%5d %10.4g %10.4g %s %10.4g" % (i, times[i][0], truth[i,0], r, Yf[0]-truth[i,0]))
#         self.assertLess( stats.variance(), emp.VRF(N-15)*nstats.variance(), 'Excess noise in state vectors; ' + r)
# 
#     def testReynekeMorrison(self):
#         N = 200
#         order = 5
#         (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], 0.1)
#         rm = ReynekeMorrison(order, 0.90)
#         
#         rm.initialize(0.0, array([self.Y0[0]]), 0.1)
#         stats = Statistics()
#         nstats = Statistics()
#         for i in range(0,N) :
#             rm.add(times[i][0], observations[i])
#             Yf = rm.getState(times[i][0])
#             r = array2string(Yf, formatter={'float_kind':lambda y: "%10.4g" % y})
#             print("RM %5d %10.4g %10.4g %s %10.4g %10.4g %10.4g" % \
#                   (i, times[i][0], truth[i,0], r, Yf[0]-truth[i,0], rm.getGoodnessOfFit(), noise[i]))
#             if (i > N-30) :
#                 stats.push( Yf[0] - truth[i,0] )
#                 nstats.push( noise[i] )
#         print(stats.variance(), nstats.variance())
# #         self.assertLess( stats.variance(), 1.5*filter.VRF(filter.theta)*nstats.variance(), 'Excess noise in state vectors')
       

#     def testGoodnessOfFit(self):
#         N = 300
#         y0 = 100.0
#         y1 = 10.0
#         y2 = 1.0
#         Y0 = array([y0, y1, y2, 0.5, 0.25, -0.125]);
#         tau = 0.1
#         (times, truth, observations, __) = generateTestData(5, N, 0.0, Y0, tau)
#         print(times[0], truth[0,:] )
#         print(times[-1], truth[-1,:] )
#          
#         empSet = [EMP0(), EMP1(),EMP2(), EMP3(), EMP4(), EMP5()]
#         for i in range(0, len(empSet)):
#             Y0 = zeros([i+1])
#             Y0[0] = y0
#             empSet[i].initialize(0.0, Y0, 0.1)
#             
#         currentEMP = 0
#         gofs = zeros([len(empSet)])
#         for i in range(0,N) :
#             report = "%5d: " % (i)
#             for e in empSet :
#                 e.add(times[i][0], observations[i])
#                 gof = e.getGOF()
#                 report += " %10.3g" % (gof)
#                 gofs[e.order] = gof
#             j = argmin(gofs)
#             if (gofs[j] < 0.90*gofs[currentEMP]) :
#                 print("%5d Switch from %d (%10.3g) to %d (%10.3g)" % (i, currentEMP, gofs[currentEMP], j, gofs[j]))
#                 currentEMP = j
# #             print(report)
#         print(report)
#         print( empSet[currentEMP].getState(times[-1][0]) )
                
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()