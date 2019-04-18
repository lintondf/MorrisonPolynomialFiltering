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
        self.transform = rc.RadarCoordinates()
        self.S = np.zeros([6,1])
        for i in range(0, 6) :
            self.S[i,0] = 10**i  # scale error tolerance 


    def tearDown(self):
        pass

    def compareRoundTrip(self, ENU, tol):
        (a,e,r) = pymap3d.enu2aer(ENU[0,0], ENU[0,1], ENU[0,2], deg=False)
        AER = self.transform.ENU2AER( ENU[:,0], ENU[:,1], ENU[:,2] )
        if ((ENU[0,:] > 1e-3).all()) : # pymap3d.enu2aer sets ENU < 1e-3 to zeros
            self.assertAlmostEqual(a, AER[0,0])
            self.assertAlmostEqual(e, AER[0,1])
            self.assertAlmostEqual(r, AER[0,2])
#         print(AER)
        ENU1 = self.transform.AER2ENU( AER[:, 0], AER[:, 1], AER[:, 2])
#             print(ENU - ENU1)
        for j in range(0, ENU.shape[0]) :
            nptest.assert_allclose(ENU[j,:], ENU1[j,:], rtol=0, atol=self.S[j,0]*tol, verbose=True)

    def testRoundTripRandom(self):
        for tol in [1e-8] :
            for i in range(0, 1000) :
                ENU = np.random.randn(6, 3)
                self.compareRoundTrip(ENU, tol)
        
    def testEdgeCases(self):
        ENU = np.zeros([1,3])
        self.compareRoundTrip(ENU, 1e-8)
#         print( self.transform.ENU2AER(ENU[:,0], ENU[:,1], ENU[:,2]))
        ENU[0,0] = 1
        self.compareRoundTrip(ENU, 1e-8)
        ENU[0,0] = -1
        self.compareRoundTrip(ENU, 1e-8)
        ENU[0,0] = 0
        ENU[0,1] = 1
        self.compareRoundTrip(ENU, 1e-8)
        ENU[0,1] = -1
        self.compareRoundTrip(ENU, 1e-8)
        ENU[0,1] = 0
        ENU[0,2] = 1
        self.compareRoundTrip(ENU, 1e-8)
        ENU[0,2] = -1
        self.compareRoundTrip(ENU, 1e-8)
        ENU[0,2] = 0

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
