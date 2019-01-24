'''
Created on Jan 24, 2019

@author: NOOK
'''
import unittest

from numpy import array, transpose, zeros
from numpy.random import randn
from Filtering import PBase, stateTransitionMatrix, EMP0, EMP1, EMP2, EMP3


class Test(unittest.TestCase):


    def setUp(self):
        y0 = 100.0
        y1 = 10.0
        y2 = 1.0
        Y = array([y0, y1, y2]);
        dt = 0.1
        self.truth = zeros([101,3])
        self.observations = randn(100,1)
        self.times = zeros([100,1])
        t = dt
        for i in range(0,100) :
            self.truth[i,:] = Y[:]
            y0 += y1*dt + y2 * 0.5*dt**2
            y1 += y2*dt
            Y = array([y0, y1, y2]);
            self.observations[i] += y0
            self.times[i] = t
            t = t+dt
        self.truth[-1,:] = Y[:]

    def tearDown(self):
        pass


    def testPBase(self):
        for order in range(0,6) :
            base = PBase(order)
            self.assertEqual(base.order, order, "order %d incorrect" % order)
            self.assertEqual(len(base.Z), order+1, "state length incorrect; was %d expected %d" % (len(base.Z), order+1))
        try :
            base = PBase(-1)
            self.assertTrue(False, "order -1 not detected")
        except ValueError as err :
            pass
        
        order = 2
        base = PBase(order)
        Y0 = array([100.0, 10.0, 1.0]);
        base.initialize(0.0, Y0, 0.1)
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
        S = stateTransitionMatrix(2, dt)
        for i in range(0,100) :
            y0 += y1*dt + y2 * 0.5*dt**2
            y1 += y2*dt
            Y = S @ Y
            self.assertAlmostEqual( Y[0], y0, 6, "bad y0")
            self.assertAlmostEqual( Y[1], y1, 6, "bad y1")
            self.assertAlmostEqual( Y[2], y2, 6, "bad y2")
        
    
    def testEMP0(self):
        print(self.truth[0:5,:])
        Y = self.truth[0,0:3]
        print(Y)
        emp = EMP2()
        emp.initialize(0.0, Y, 0.1)
        for i in range(1,100) :
            Yf = emp.add(self.times[i][0],self.truth[i,0])
            print(i,Yf,Yf-self.truth[i,:])
        emp.initialize(0.0, Y, 0.1)
        for i in range(1,100) :
            Yf = emp.add(self.times[i][0],self.observations[i])
            print(i,Yf,Yf-self.truth[i,:])
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()