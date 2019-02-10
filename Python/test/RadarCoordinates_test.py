'''
Created on Feb 9, 2019

@author: NOOK
'''
import unittest
import pymap3d
import numpy as np
import numpy.testing as nptest
from math import sqrt, atan2
import RadarCoordinates as rc

class RadarCoordinates_test(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testGradient(self):
        S = np.zeros([6,1])
        for i in range(0, 6) :
            S[i,0] = 10**i  # scale error tolerance 
        for tol in [1e-8] :
            print(tol)
            for i in range(0, 10000) :
                ENU = np.random.randn(6, 3) # np.array([[1.0, 0.0, 15.0], [0.5,-0.5,2.0]])
        #         print(ENU)
        #         ENU0 pymap3d.enu2aer(ENU[0,0], ENU[0,1], ENU[0,2], deg=False) )
                transform = rc.RadarCoordinates()
                AER = transform.ENU2AER( ENU[:,0], ENU[:,1], ENU[:,2] )
        #         print(AER)
                ENU1 = transform.AER2ENU( AER[:, 0], AER[:, 1], AER[:, 2])
    #             print(ENU - ENU1)
                for j in range(0, 6) :
                    nptest.assert_allclose(ENU[j,:], ENU1[j,:], rtol=0, atol=S[j,0]*tol, verbose=True)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
