'''
Created on Jan 24, 2019

@author: NOOK
'''
import unittest

from numpy import array, transpose, zeros, argmin
from numpy.linalg import norm
from numpy.random import randn
from Filtering import ReynekeMorrisonFilterBase, stateTransitionMatrix, EMP0, EMP1, EMP2, EMP3, EMP4, EMP5, EMP, EMPSet
from runstats import Statistics

def generateTestData(order, N, t0, Y0, dt, bias=0.0, sigma=1.0):
    truth = zeros([N,order+1])
    observations = bias + sigma*randn(N,1)
    times = zeros([N,1])
    S = stateTransitionMatrix(order+1, dt)
    t = t0 + dt
    Y = Y0
    for i in range(0,N) :
        Y = S @ Y
        observations[i] += Y[0]
        times[i] = t
        truth[i,:] = Y[:]
        t = t+dt
    return (times, truth, observations)

class Test(unittest.TestCase):
    


    def setUp(self):
        pass

    def tearDown(self):
        pass


    def testPBase(self):
        for order in range(0,6) :
            base = ReynekeMorrisonFilterBase(order)
            self.assertEqual(base.order, order, "order %d incorrect" % order)
        try :
            base = ReynekeMorrisonFilterBase(-1)
            self.assertTrue(False, "order -1 not detected")
        except ValueError as err :
            pass
        
        order = 2
        base = ReynekeMorrisonFilterBase(order)
        Y0 = array([100.0, 10.0, 1.0]);
        base.initialize(0.0, Y0, 0.1)
        self.assertEqual(len(base.Z), order+1, "state length incorrect; was %d expected %d" % (len(base.Z), order+1))
        self.assertEqual(len(base.D), order+1, "Denormalization vector length incorrect")
        dtau = base.normalizeDeltaTime(0.1)
        Z = base.predict(dtau)
        Y = base.denormalizeState(Z)
        self.assertEqual( Y[0], 100.0+0.1*10.0+0.5*0.1**2*1.0, "Bad prediction element 0")
        self.assertEqual( Y[1], 10.0+0.1*1.0, "Bad prediction element 1")
        self.assertEqual( Y[2], 1.0, "Bad prediction element 2")                  

    def testStateTransitionMatrix(self):
        y0 = 100.0
        y1 = 10.0
        y2 = 1.0
        Y = array([y0, y1, y2]);
        dt = 0.1
        S = stateTransitionMatrix(2+1, dt)
        for i in range(0,100) :
            y0 += y1*dt + y2 * 0.5*dt**2
            y1 += y2*dt
            Y = S @ Y
            self.assertAlmostEqual( Y[0], y0, 6, "bad y0")
            self.assertAlmostEqual( Y[1], y1, 6, "bad y1")
            self.assertAlmostEqual( Y[2], y2, 6, "bad y2")
        
    def testEMP0(self):
        N = 100
        y0 = 100.0
        y1 = 10.0
        y2 = 1.0
        Y0 = array([y0]);
        (times, truth, observations) = generateTestData(0, N, 0.0, Y0, 0.1)

        emp = EMP0()
        emp.initialize(0.0, Y0, 0.1)
        for i in range(0,N) :
            emp.add(times[i][0], truth[i,0])
            Yf = emp.getState(times[i][0])
            #print(i,Yf,Yf-truth[i,:])
            self.assertLess(norm((Yf-truth[i,:])/Yf), 1e-6, 'Noiseless state error')

    def testEMP1(self):
        N = 100
        y0 = 100.0
        y1 = 10.0
        y2 = 1.0
        Y0 = array([y0, y1]);
        (times, truth, observations) = generateTestData(1, N, 0.0, Y0, 0.1)

        emp = EMP1()
        emp.initialize(0.0, Y0, 0.1)
        for i in range(0,N) :
            emp.add(times[i][0], truth[i,0])
            Yf = emp.getState(times[i][0])
            #print(i,Yf,Yf-truth[i,:])
            self.assertLess(norm((Yf-truth[i,:])/Yf), 1e-6, 'Noiseless state error')
        
    
    def testEMP2(self):
        N = 100
        y0 = 100.0
        y1 = 10.0
        y2 = 1.0
        Y0 = array([y0, y1, y2]);
        (times, truth, observations) = generateTestData(2, N, 0.0, Y0, 0.1)

        emp = EMP2()
        emp.initialize(0.0, Y0, 0.1)
        for i in range(0,N) :
            emp.add(times[i][0], truth[i,0])
            Yf = emp.getState(times[i][0])
            #print(i,Yf,Yf-truth[i,:])
            self.assertLess(norm((Yf-truth[i,:])/Yf), 1e-6, 'Noiseless state error')
#         emp.initialize(0.0, Y0, 0.1)
#         for i in range(0,N) :
#             emp.add(times[i][0], observations[i])
#             Yf = emp.getState()
#             print(i,Yf,Yf-truth[i,:])
            
    def testEMP3(self):
        N = 100
        y0 = 100.0
        y1 = 10.0
        y2 = 1.0
        Y0 = array([1e4, 1e3, 1e2, 1e1]);
        (times, truth, observations) = generateTestData(3, N, 0.0, Y0, 0.1)

        emp = EMP3()
        emp.initialize(0.0, Y0, 0.1)
        for i in range(0,N) :
            emp.add(times[i][0], truth[i,0])
            Yf = emp.getState(times[i][0])
            self.assertLess(norm((Yf-truth[i,:])/Yf), 1e-6, 'Noiseless state error')
#         emp.initialize(0.0, Y0, 0.1)
#         for i in range(0,N) :
#             emp.add(times[i][0], observations[i])
#             Yf = emp.getState()
#             print(i,Yf,Yf-truth[i,:])
            
    def testEMP4(self):
        N = 100
        y0 = 100.0
        y1 = 10.0
        y2 = 1.0
        Y0 = array([1e4, 1e3, 1e2, 1e1, 1e0]);
        (times, truth, observations) = generateTestData(4, N, 0.0, Y0, 0.1)

        emp = EMP4()
        emp.initialize(0.0, Y0, 0.1)
        for i in range(0,N) :
            emp.add(times[i][0], truth[i,0])
            Yf = emp.getState(times[i][0])
            self.assertLess(norm((Yf-truth[i,:])/Yf), 1e-6, 'Noiseless state error')
#         emp.initialize(0.0, Y0, 0.1)
#         for i in range(0,N) :
#             emp.add(times[i][0], observations[i])
#             Yf = emp.getState()
#             print(i,Yf,Yf-truth[i,:])
        
    def testEMP5(self):
        N = 100
        y0 = 100.0
        y1 = 10.0
        y2 = 1.0
        Y0 = array([1e4, 1e3, 1e2, 1e1, 1e0, 1e-1]);
        (times, truth, observations) = generateTestData(5, N, 0.0, Y0, 0.1)

        emp = EMP5()
        emp.initialize(0.0, Y0, 0.1)
        for i in range(0,N) :
            emp.add(times[i][0], truth[i,0])
            Yf = emp.getState(times[i][0])
            self.assertLess(norm((Yf-truth[i,:])/Yf), 1e-6, 'Noiseless state error')
#         emp.initialize(0.0, Y0, 0.1)
#         stats = Statistics()
#         for i in range(0,N) :
#             emp.add(times[i][0], observations[i])
#             Yf = emp.getState()
# #             print(i,Yf,norm((Yf-truth[i,:])/Yf))
#             if (i > N-30) :
#                 stats.push( Yf[0] - truth[i,0] )
# #             print(i,Yf[0],Yf[0]-truth[i,0])
# #             self.assertLess(norm((Yf-truth[i,:])/Yf), 2.5, 'Excess noise state error')
#         print(stats.mean(), stats.variance(), emp.VRF(N-15) )

    def testEMP(self):
        N = 100
        y0 = 100.0
        y1 = 10.0
        y2 = 1.0
        Y0 = array([1e4, 1e3, 1e2, 1e1, 1e0, 1e-1]);
        
        for order in range(0, 5+1) :
            print(order, Y0[0:order+1])
            (times, truth, observations) = generateTestData(order, N, 0.0, Y0[0:order+1], 0.1)
            emp = EMPSet(5)
            emp.initialize(0.0, Y0, 0.1)
            for i in range(0,N) :
                emp.add(times[i][0], truth[i,0])
                Yf = emp.getState(times[i][0])
#                 print(i, Yf, Yf[0]-truth[i,0])
                if (i > 5) :
                    self.assertLess(norm(Yf[0]-truth[i,0]), 1e-6, 
                                'Noiseless state error (%d, %d)' % (order, i))

        

    def testGoodnessOfFit(self):
        N = 300
        y0 = 100.0
        y1 = 10.0
        y2 = 1.0
        Y0 = array([y0, y1, y2, 0.5, 0.25, -0.125]);
        tau = 0.1
        (times, truth, observations) = generateTestData(5, N, 0.0, Y0, tau)
        print(times[0], truth[0,:] )
        print(times[-1], truth[-1,:] )
         
        empSet = [EMP0(), EMP1(),EMP2(), EMP3(), EMP4(), EMP5()]
        for i in range(0, len(empSet)):
            Y0 = zeros([i+1])
            Y0[0] = y0
            empSet[i].initialize(0.0, Y0, 0.1)
            
        currentEMP = 0
        gofs = zeros([len(empSet)])
        for i in range(0,N) :
            report = "%5d: " % (i)
            for e in empSet :
                e.add(times[i][0], observations[i])
                gof = e.getGOF()
                report += " %10.3g" % (gof)
                gofs[e.order] = gof
            j = argmin(gofs)
            if (gofs[j] < 0.90*gofs[currentEMP]) :
                print("%5d Switch from %d (%10.3g) to %d (%10.3g)" % (i, currentEMP, gofs[currentEMP], j, gofs[j]))
                currentEMP = j
#             print(report)
        print(report)
        print( empSet[currentEMP].getState(times[-1][0]) )
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()