'''
Created on Oct 30, 2019

@author: lintondf
'''
import unittest
from TestSuite import slow, TestCaseBase

import numpy as np
import random
import csv

from numpy import arange, array2string, cov, log, var, zeros, trace, mean, std, transpose, \
    concatenate, allclose, min, max, nonzero, cumsum, histogram, where, diag, ones
from numpy import array, array as vector, array_equal
from numpy import sqrt
from TestUtilities import assert_allclose, assert_almost_equal, assert_array_less,\
    covarianceToCorrelation
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
from scipy.optimize.optimize import fminbound
from numpy.linalg.linalg import cholesky

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
        for i in range(0,setup.shape[0]) :
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
            (times, truth, observations, noise) = generateTestData(order, nS, 0.0, Y[0:order+1], tau, sigma=R)
            testData.putArray(case, 'times', times)
            testData.putArray(case, 'observations', observations)
            
            def runOne( v0 : float ):
                f = ChevronPolynomialFilter(order, tau, theta, v0)
#                 print(v0,f.switchNs)
                p = PairedPolynomialFilter(order, tau, theta)
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
                return (expected, paired, j)
            
            def targetV0(v0 : float):
                (expected, paired, j) = runOne(v0)
                return var(expected[0:j,0]-truth[0:j,0]) / var(paired[0:j,0]-truth[0:j,0])
            
            for v0 in arange(0.1, 1.0, 0.1) :
                (expected, paired, j) = runOne(v0)
                print(v0, mean(expected[0:j,0]-truth[0:j,0])/mean(paired[0:j,0]-truth[0:j,0]), 
                      var(expected[0:j,0]-truth[0:j,0])/var(paired[0:j,0]-truth[0:j,0]))
#             v0 = fminbound( targetV0, 0.1, 1.0 )
#             (expected, paired, j) = runOne(v0)
#             print(v0, mean(expected[0:j,0]-truth[0:j,0])/mean(paired[0:j,0]-truth[0:j,0]), 
#                   var(expected[0:j,0]-truth[0:j,0])/var(paired[0:j,0]-truth[0:j,0]))
            testData.putArray(case, 'expected', expected)
#             ax = plt.subplot(1,1,1)
#             ax.plot(times[0:j,0], truth[0:j,0]-truth[0:j,0], 'b-')
#             ax.plot(times[0:j,0], observations[0:j,0]-truth[0:j,0], 'b.')
#             ax.plot(times[0:j,0], paired[0:j,0]-truth[0:j,0], 'r-')
#             ax.plot(times[0:j,0], expected[0:j,0]-truth[0:j,0], 'k-')
#             plt.show()
       
    def xstep9TestLaunchRanges(self):
        print()
        testData = TestData()
        nS = 3000
        times = zeros([nS,1])
        truth = zeros([nS,5+1])
        observations = zeros([nS,1])
        i = 0
        t = 0
        with open(testData.testDataPath('launch_radar_1.csv'), newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader :
                times[i,0] = t # float(row[0])
                t += 0.1
                truth[i,0] = float(row[3])
                observations[i,0] = float(row[6])
                i += 1
                if (i >= times.shape[0]) :
                    break
        tau = 0.1
        R = 10.0
        
        def runOne( order : int, theta : float, v0 : float ):
            f = ChevronPolynomialFilter(order, tau, theta, v0)
            p = PairedPolynomialFilter(order, tau, theta)
            paired = zeros([nS, p.order+1]) 
            expected = zeros([nS, f.order+1]) 
            for j in range(0,nS) :
                Zstar = f.predict(times[j][0])
                e = observations[j,0] - Zstar[0]
                f.update(times[j][0], Zstar, e)
                expected[j,:] = f.getState();
                Zstar = p.predict(times[j][0])
                e = observations[j,0] - Zstar[0]
                p.update(times[j][0], Zstar, e)
                paired[j,:] = p.getState();
            return (expected, paired, j)
        
        v0 = 0.1
#         for order in range(1, 5+1) :
#             for theta in (0.9, 0.95, 0.99) :
#                 (expected, paired, j) = runOne(order, theta, v0)
#                 print('%d %6.3f %8.5f %10.3f %10.4f' % (order, v0, theta, var(expected[0:j,0]-truth[0:j,0]), 
#                       var(expected[0:j,0]-truth[0:j,0])/var(paired[0:j,0]-truth[0:j,0])))
        order = 2
        theta = 0.95
        (expected, paired, j) = runOne(order, theta, v0)
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
        order = 5
        tau = 0.1
        theta = 0.95
        f = ChevronPolynomialFilter(order, tau, theta, 0.1)
        print(f.switchNs)
        t0 = 0.0
        nS = 1+int(nSwitch(order, theta))
        Y = generateTestPolynomial( order, nS, t0, tau )
        R = 0.15 * abs(Y[0])
        (times, truth, observations, noise) = generateTestData(order, nS, 0.0, Y[0:order+1], tau, sigma=R)
        for j in range(0,nS) :
            Zstar = f.predict(times[j][0])
            e = observations[j,0] - Zstar[0]
            f.update(times[j][0], Zstar, e)
            V = f.getVRF()
            print('%6.3f' % times[j][0], f.getStatus(), f.getBest(), A2S(diag(V)))
            (cholesky(V)) # will throw exception if not positive definite
            print(A2S(V))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()