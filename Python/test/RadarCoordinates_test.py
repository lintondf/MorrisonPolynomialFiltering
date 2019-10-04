'''
Created on Oct 3, 2019

@author: lintondf
'''
import unittest

from numpy import array, zeros, diag, transpose, sqrt, sum
from numpy import array as vector
from math import sin, cos, atan2, pi

from polynomialfiltering.RadarCoordinates import RadarCoordinates

from TestSuite import TestCaseBase
from TestUtilities import covarianceToCorrelation


class Test(TestCaseBase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def stepName(self):
        '''
/Users/lintondf/config/estimation.cfg:Set_Radar_Variance ("0.14",   0.117, 0.194,  45.0);
/Users/lintondf/config/estimation.cfg:Set_Radar_Variance ("1.16",   0.410, 0.490,  10.0);
/Users/lintondf/config/estimation.cfg:Set_Radar_Variance ("19.14",  0.067, 0.1441,  5.0);
/Users/lintondf/config/estimation.cfg:Set_Radar_Variance ("19.17",  0.540, 0.610,   7.0);
/Users/lintondf/config/estimation.cfg:Set_Radar_Variance ("28.14",  0.228, 0.240,   5.0);
/Users/lintondf/config/estimation.cfg:Set_Radar_Variance ("91.14",  0.067, 0.296,   4.0);
        '''
        A = array([pi/180*67.89, 0.000012,    2e-5, 3e-6, 4e-7, 5e-8])
        E = array([pi/180*11.2345, 0.0000014, 3e-6, 2e-7, 1e-8, 9e-9])
        R = array([1829135, 2345.6789,        10.0,  5.0,  2.0,  1.0])
        rc = RadarCoordinates()
        ENU = rc.AER2ENU(A, E, R)
        print(ENU)
        print( rc.ENU2AER(ENU[:,0], ENU[:,1], ENU[:,2]))
        
        print('dAERdENU')
        print( rc.dAERdENU(ENU[:,0], ENU[:,1], ENU[:,2]))
        print('dENUdAER')
        print( rc.dENUdAER(A, E, R))
#         R[0] = 1e3
        D = rc.dENUdAER(A, E, R)
        mils2radians = 2*pi/6400.0
        sigmas = array([0.410*mils2radians, 0.490*mils2radians, 10.0*0.3048])
        print(R[0] * sigmas)
        R = diag( sigmas ** 2 )
        print(R)
        T = ((D) @ R @ transpose(D))
        print(T)
        print(sqrt(sum(diag(T))))
        print(covarianceToCorrelation(T))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()