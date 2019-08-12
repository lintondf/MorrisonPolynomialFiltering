'''
Created on Apr 25, 2019

@author: NOOK
'''
import unittest
from typing import List;

from TestSuite import slow

from numpy import array, array as vector
from numpy import arange, array2string, cov, log, var, zeros, trace, mean, std, transpose,\
    concatenate, allclose, min, max, nonzero, cumsum, histogram, where, diag, ones
from numpy import sqrt
from numpy.linalg import inv
from numpy.random import randn, seed, get_state
from numpy.testing import assert_allclose, assert_array_less
from scipy.stats import kstest, chi2, lognorm, norm, anderson

from runstats import Statistics

from netCDF4 import Dataset
from TestSuite import testDataPath;
from TestUtilities import generateTestPolynomial, generateTestData, createTestGroup, writeTestVariable, A2S
from TestData import TestData

from polynomialfiltering.Main import AbstractFilter, FilterStatus
from polynomialfiltering.components.RecursivePolynomialFilter import RecursivePolynomialFilter
from polynomialfiltering.components.ICore import ICore
from polynomialfiltering.components.Fmp import makeFmp, _makeFmpCore

from polynomialfiltering.PythonUtilities import ignore, testcase, testclass, testclassmethod
from polynomialfiltering.PythonUtilities import assert_not_empty

from polynomialfiltering.components.Emp import makeEmp, _makeEmpCore, nSwitch, nUnitLastVRF


class Fmp_test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def generateStates(self, cdf : Dataset) -> None:
        print("generateStates", chi2.ppf(0.95,df=1))
#         N = array([64, 128, 5120, 512, 1024, 2048])
        setup = array([
#             [0, 0.01],[0, 0.1], [0, 1.0], [0, 10.0],  
#             [1, 0.01],[1, 0.1], [1, 1.0], [1, 10.0],  
            [2, 0.01],# [2, 0.1], [2, 1.0], [2, 10.0],  
#             [3, 0.01], [3, 0.1], [3, 1.0], [3, 10.0],  
#             [4, 0.01],[4, 0.1], [4, 1.0], [4, 10.0],  
#             [5, 0.01],[5, 0.1], [5, 1.0], [5, 10.0]
            ])
        thetas = vector([0.90, 0.95, 0.99, 0.999])

        group = createTestGroup(cdf, 'States')
        writeTestVariable(group, 'thetas', thetas)
        writeTestVariable(group, 'setup', setup)
        iCase = 0;
        for k in range(0,thetas.shape[0]) :
            theta = thetas[k]
            for i in range(0,setup.shape[0]) :
                order = int(setup[i,0])
                tau = setup[i,1]
                case = createTestGroup(cdf, 'Case_%d' % iCase)
                iCase += 1
                t0 = 0.0
                n = int(nSwitch(order, theta))
                for it in range(0,10) :
                    Y = generateTestPolynomial( order, n, t0, tau )
                    R = 10.0
                    (times, truth, observations, noise) = generateTestData(order, n, 0.0, Y[0:order+1], tau, sigma=R)
                    R = std(noise)
                    expected = zeros([n, order+1])            
                    residuals = zeros([n, order+1])            
                    f = makeFmp(order, tau, theta);
                    f.start(0.0, Y)
                    tchi2 = chi2.ppf(0.95, df=order+1)
                    for j in range(0,times.shape[0]) :
                        Zstar = f.predict(times[j][0])
                        e = observations[j] - Zstar[0]
                        f.update(times[j][0], Zstar, e)
                        expected[j,:] = f.getState();
                        residuals[j,:] = f.getState() - truth[j,:]
                    C = cov(residuals, rowvar=False)
                    V = R**2 * f.getVRF()
                    CV = sqrt(C/V);
                    print('%8.6f, %d, %6.3f, %6.2f,  %6.3f, %6.3f' % 
                        (theta, order, tau, R, min(CV.flatten())-1, max(CV.flatten())-1))
#                 print(A2S(C/V))


    def test0Generate(self):
        print("test0Generate")
        path = testDataPath('testFMP.nc');
        cdf = Dataset(path, "w", format="NETCDF4");
        self.generateStates(cdf)
        cdf.close()

    @testcase 
    def test9CoreBasic(self) -> None:
        '''@core90 : ICore'''
        '''@core95 : ICore'''
        '''@core95half : ICore'''
        '''@core95double : ICore'''
        core90 = _makeFmpCore(3, 1.0, 0.90)
        core95 = _makeFmpCore(3, 1.0, 0.95)
        core95half = _makeFmpCore(3, 2.0, 0.95)
        core95double = _makeFmpCore(3, 0.5, 0.95)
        
        assert_allclose( core90.getVRF(1), core90.getVRF(10) )  # should be time invariate
        assert_array_less( core95.getVRF(1), core90.getVRF(1))
        assert_allclose( ones([3+1,3+1]), (core95double.getVRF(1) / core95.getVRF(1)) * (core95half.getVRF(1) / core95.getVRF(1)) )
        
        assert_allclose( core90.getGamma(10.0, 5.0), core90.getGamma(11.0, 5.0) )
        assert_allclose( core90.getGamma(10.0, 5.0), core90.getGamma(10.0, 6.0) )
        assert_allclose( core95.getGamma(10.0, 5.0), core95half.getGamma(10.0, 5.0) ) 
        assert_allclose( core95.getGamma(10.0, 5.0), core95double.getGamma(10.0, 5.0) ) 
    
    @testcase 
    def test9NSwitch(self) -> None:
        '''@emp : ICore'''
        '''@fmp : ICore'''
        '''@order : int'''
        '''@tau : float'''
        '''@itau : int'''
        '''@taus : array'''
        '''@theta : float'''
        '''@itheta : int'''
        '''@thetas : array'''
        '''@n : int'''
        '''@nThetas : int'''
        '''@nTaus : int'''
        
        taus = array([0.01, 0.1, 1, 10, 100]);
        nTaus = len(taus);
        thetas = array([0.90, 0.95, 0.99, 0.999])
        nThetas = len(thetas);
        for order in range(0,5+1) :
            for itheta in range(0, nThetas):
                theta = thetas[itheta]
                for itau in range(0, nTaus):
                    tau = taus[itau]
                    emp = _makeEmpCore(order, tau)
                    fmp = _makeFmpCore(order, tau, theta)
                    n = int(nSwitch( order, theta ))
                    assert( fmp.getFirstVRF(0)/emp.getFirstVRF(n) < 1.25 )
#                     print('%2d, %8.3f, %7.5f, %8.1f, %6.2f, %6.2f, %6.2f' %
#                         (order, tau, theta, n, fmp.getFirstVRF(0)/emp.getFirstVRF(n-1), fmp.getFirstVRF(0)/emp.getFirstVRF(n), fmp.getFirstVRF(0)/emp.getFirstVRF(n+1)))
        
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()