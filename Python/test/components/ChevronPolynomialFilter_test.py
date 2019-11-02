'''
Created on Oct 30, 2019

@author: lintondf
'''
import unittest
from TestSuite import slow, TestCaseBase

import numpy as np
import random


from numpy import arange, array2string, cov, log, var, zeros, trace, mean, std, transpose, \
    concatenate, allclose, min, max, nonzero, cumsum, histogram, where, diag, ones
from numpy import array, array as vector, array_equal
from numpy import sqrt
from TestUtilities import assert_allclose, assert_almost_equal, assert_array_less
from scipy.optimize.zeros import brentq
from typing import List;

from TestData import TestData
from TestSuite import slow, TestCaseBase
from TestUtilities import generateTestPolynomial, generateTestData, createTestGroup, writeTestVariable, A2S, assert_report, assert_clear
from polynomialfiltering.Main import AbstractFilterWithCovariance, FilterStatus
from polynomialfiltering.PythonUtilities import assert_not_empty
from polynomialfiltering.PythonUtilities import ignore, testcase, testclass, testclassmethod
from polynomialfiltering.components.Emp import nSwitch
from polynomialfiltering.components.ICore import ICore
from polynomialfiltering.filters.PairedPolynomialFilter import PairedPolynomialFilter
from polynomialfiltering.filters.RecursivePolynomialFilter import RecursivePolynomialFilter

from polynomialfiltering.filters.ChevronPolynomialFilter import ChevronPolynomialFilter

import matplotlib
import matplotlib.pyplot as plt

class ChevronPolynomialFilter_test(TestCaseBase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def thetaFromN(self, order : int, n : int )-> float :
        def targetTheta(theta : float) -> float:
            return  n - nSwitch(order, theta)
        
        t0 = brentq( targetTheta, 1e-6, 1-1e-8 );
        return t0


    def generateStates(self, testData : TestData) -> None:
        iter = 2
        random.seed(iter)
        np.random.seed(iter)
        print()
        """
    0.5
0.725480190570896 0.5356909159335558
0.6882733072035283 0.6785007714946476
1.761486453025724 0.5107522556593901
1.38403500991246 0.5782497929112056        
    0.4
0.5141276855136485 0.5850719094903344
0.6843619058801106 0.6317006487620059
0.4329093260551004 0.5697405367798848
2.4606737598087243 0.6339824343218847
    0.25
1.2171964190023308 0.5297074207464119
0.5423237027086846 0.38693586556830833
0.5526032329122892 0.39536547197967575
1.7675207661802363 0.5064018902646222
        """
        
        R = 100.0
        N = array([64, 128, 512, 512, 1024, 2048])
        setup = array([
            [1, 0.01],[1, 0.1], [1, 1.0], [1, 10.0],  
            [2, 0.01], [2, 0.1], [2, 1.0], [2, 10.0],  
            [3, 0.01], [3, 0.1], [3, 1.0], [3, 10.0],  
            [4, 0.01],[4, 0.1], [4, 1.0], [4, 10.0],  
            [5, 0.01],[5, 0.1], [5, 1.0], [5, 10.0]
            ])
        group = testData.createTestGroup('States')
        for i in range(16,setup.shape[0]) :
            case = testData.createTestGroup( 'States_Case_%d' % i)
            order = int(setup[i,0])
            tau = setup[i,1]
            theta = self.thetaFromN( order, N[order]//2)  # switch half-way thru data
            testData.putInteger(case, 'order', order)
            testData.putScalar(case, 'tau', tau)
            testData.putScalar(case, 'theta', theta)
            testData.putInteger(case, 'N', N[order])
            t0 = 0.0
            nS =  N[order] # 100 # 
            Y = generateTestPolynomial( order, nS, t0, tau )
            R = 0.15 * abs(Y[0])
            f = ChevronPolynomialFilter(order, tau, theta)
            p = PairedPolynomialFilter(order, tau, theta)
            (times, truth, observations, noise) = generateTestData(order, nS, 0.0, Y[0:order+1], tau, sigma=R)
            testData.putArray(case, 'times', times)
            testData.putArray(case, 'observations', observations)
            paired = zeros([nS, p.order+1]) 
            expected = zeros([nS, f.order+1]) 
            for j in range(0,nS) :
#                 print('%6.3f' % times[j][0],'O', A2S(observations[j,0]))
                Zstar = f.predict(times[j][0])
                e = observations[j,0] - Zstar[0]
                f.update(times[j][0], Zstar, e)
                expected[j,:] = f.getState();
#                 print('%6.3f' % times[j][0],'T', A2S(truth[j,:]))
#                 print('%6.3f' % times[j][0],'>', A2S(expected[j,:]))
                Zstar = p.predict(times[j][0])
                e = observations[j,0] - Zstar[0]
                p.update(times[j][0], Zstar, e)
                paired[j,:] = p.getState();
                if (f.getBest() == order) :
                    break;
                
            print(mean(expected[0:j,0]-truth[0:j,0])/mean(paired[0:j,0]-truth[0:j,0]), 
                  var(expected[0:j,0]-truth[0:j,0])/var(paired[0:j,0]-truth[0:j,0]))
            testData.putArray(case, 'expected', expected)
            ax = plt.subplot(1,1,1)
            ax.plot(times[0:j,0], truth[0:j,0]-truth[0:j,0], 'b-')
            ax.plot(times[0:j,0], observations[0:j,0]-truth[0:j,0], 'b.')
            ax.plot(times[0:j,0], paired[0:j,0]-truth[0:j,0], 'r-')
            ax.plot(times[0:j,0], expected[0:j,0]-truth[0:j,0], 'k-')
            plt.show()
       
    def step0Generate(self):
        testData = TestData('testChevron.nc', 'w');
        self.generateStates(testData)
        testData.close()
       


    def step9Basic(self):
        f = ChevronPolynomialFilter(5, 0.1, 0.95)
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()