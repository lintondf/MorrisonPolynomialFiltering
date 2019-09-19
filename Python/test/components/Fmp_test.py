'''
Created on Apr 25, 2019

@author: NOOK
'''
from docutils.nodes import target
from astropy.io.ascii.tests.common import assert_almost_equal

""" Taus for full range valid thetas [2e-16, 1-2e-16]
Gamma:  {0: 1.1102230246251565e-16, 1: 1.651158036900312e-08, 2: 0.2898979485566357, 3: 0.4627475401696348, 4: 0.5697090329565893, 5: 0.6416277095878444}
VRF:    {0: 3.0518509447574615e-05, 1: 1.4142135623842478, 2: 2.5495097571983933, 3: 3.8369548115879297, 4: 5.583955190144479, 5: 8.241797269321978}
"""

import unittest
from typing import List;

from TestSuite import slow

from numpy import array, array as vector, linspace, any, diff, log10
from numpy import arange, array2string, cov, log, var, zeros, trace, mean, std, transpose,\
    concatenate, allclose, min, max, nonzero, cumsum, histogram, where, diag, ones
from numpy import sqrt
from numpy.linalg import inv
from numpy.random import randn, seed, get_state
from numpy.testing import assert_almost_equal, assert_allclose, assert_array_less
from scipy.stats import kstest, chi2, lognorm, norm, anderson
from scipy.optimize.zeros import brentq

from runstats import Statistics

from netCDF4 import Dataset, Group
from TestSuite import testDataPath;
from TestUtilities import generateTestPolynomial, generateTestData, createTestGroup, writeTestVariable, A2S,\
    covarianceToCorrelation, assert_report, assert_clear
from TestData import TestData

from polynomialfiltering.Main import AbstractFilter, FilterStatus
from polynomialfiltering.components.RecursivePolynomialFilter import RecursivePolynomialFilter
from polynomialfiltering.components.ICore import ICore
from polynomialfiltering.components.Fmp import makeFmp, makeFmpCore

from polynomialfiltering.PythonUtilities import ignore, testcase, testclass, testclassmethod
from polynomialfiltering.PythonUtilities import assert_not_empty

from polynomialfiltering.components.Emp import makeEmp, makeEmpCore, nSwitch, nUnitLastVRF
from numpy.random.mtrand import multivariate_normal
from nose.tools import assert_equal
from numpy.core.defchararray import isdecimal


class Fmp_test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass
    
    def getMinTheta(self, order: int, tau: float) -> float:
        if (order == 0) :
            return 1e-6;
        thresholds = array([0, 1.414213562, 2.549509757, 3.836954811, 5.583955189, 8.241797269]);
        if (tau > thresholds[order]) :
            return 0.5;
        v = 1.0;
        def targetMaxDiag(t :float ) -> float:
            c = makeFmpCore(order, tau, t);
            return max(diag(c.getVRF(0))) - v;
             
        t0 = brentq( targetMaxDiag, 1e-6, 1-1e-8 );
        return t0

    def generateStates(self, cdf : Dataset) -> None:
#         print("generateStates")
#         N = array([64, 128, 5120, 512, 1024, 2048])
        setup = array([ # order, tau
            [0, 0.01],[0, 0.1], [0, 1.0], [0, 10.0],  
            [1, 0.01],[1, 0.1], [1, 1.0], [1, 10.0],  
            [2, 0.01], [2, 0.1], [2, 1.0], [2, 10.0],  
            [3, 0.01], [3, 0.1], [3, 1.0], [3, 10.0],  
            [4, 0.01],[4, 0.1], [4, 1.0], [4, 10.0],  
            [5, 0.01],[5, 0.1], [5, 1.0], [5, 10.0]
            ])

        testData = TestData()
        nPass = 0
        nFail = 0
        group = createTestGroup(cdf, 'States')
        writeTestVariable(group, 'setup', setup)
        iCase = 1;
        for i in range(0,setup.shape[0]) :
            order = int(setup[i,0])
            tau = setup[i,1]
            minTheta = self.getMinTheta(order, tau);
            thetas = linspace(minTheta, 1-1e-6, 10 )
            for theta in thetas :
                t0 = 0.0
                n = 2*max((200, int(nSwitch(order, theta)) ))
                S = zeros([order+1, order+1])
#                 print(order, tau, theta, n, int(nSwitch(order, theta)))
                if (n > 1000*(order+1) ) : # skip extremely long runs
                    break;
                caseGroup = createTestGroup(group, 'Case_%d' % iCase)
                iCase += 1
                nTrials = 25;
                # variance of sample variances for a standard normal distribtion
                varVar = (nTrials-1)**2/nTrials**3 * 3 - (nTrials-1)*(nTrials-3)/nTrials**3 * 1**2
                for it in range(0,nTrials) :
                    f = makeFmp(order, tau, theta);
#                     Y = generateTestPolynomial( order, n, t0, tau )
                    Y = f.getCore().getGamma(0.0, 1.0) * randn(1,order+1)
                    Y.shape = [order+1]
                    R = 10.0
                    (times, truth, observations, noise) = generateTestData(order, n, 0.0, Y[0:order+1], tau, sigma=R)
                    expected = zeros([n, order+1])            
                    residuals = zeros([n, order+1])            
                    R = std(noise)
                    V = R**2 * f.core.getVRF(0)
#                     D = sqrt(diag(V))
                    Y0 = multivariate_normal(Y, V); # Y + D * randn(Y.shape[0]) # 
                    if (it == 0) :
                        testData.putInteger(caseGroup, 'order', order)
                        testData.putScalar(caseGroup, 'tau', tau)
                        testData.putScalar(caseGroup, 'theta', theta)
                        testData.putArray(caseGroup, 'Y0', Y0)
                        testData.putArray(caseGroup, 'times', times)
                        testData.putArray(caseGroup, 'observations', observations)
                        testData.putArray(caseGroup, 'truth', truth)
                    f.start(0.0, Y0)
#                     tchi2 = chi2.ppf(0.95, df=order+1)
                    for j in range(0,times.shape[0]) :
                        Zstar = f.predict(times[j][0])
                        e = observations[j] - Zstar[0]
                        f.update(times[j][0], Zstar, e)
                        expected[j,:] = f.getState();
                        residuals[j,:] = f.getState() - truth[j,:]
#                     print(A2S(residuals))
                    if (it == 0) :
                        testData.putArray(caseGroup, 'expected', expected)
                    C = cov(residuals, rowvar=False)
#                     if (it == 0) :
#                         print(A2S(V))
#                     print(A2S(C))
#                     if (any(C < 0.0)) :
#                         print(A2S(C))
#                         print(A2S(V))
                    CV = (C/V);
                    S = S + CV;
#                     print('%4d %8.6f, %d, %6.3f, %6.2f,  %6.3f, %6.3f' % 
#                         (it, 1-theta, order, tau, R, min(CV.flatten()), max(CV.flatten())))
                S = S / nTrials;
                S = S.flatten();
                stdVar = sqrt(varVar)
                lB = 1 - stdVar
                uB = 1 + stdVar
                pf = 'FAIL'
                if (lB <= mean(S) and mean(S) <= uB) :
                    pf = 'PASS'
                    nPass += 1
                else:
                    nFail += 1
                print( '%5d %10.3f %10.8f %7d  %10.3f, %10.3f, %10.3f, %10.3f %s' % 
                       (order, tau, theta, n, mean(S), std(S)/stdVar, min(S)/lB, max(S)/uB, pf) );
        print('%d passed; %d failed' % (nPass, nFail))
        assert_equal(nFail,0)
        
    def generateGammas(self, cdf : Dataset) -> None:
        
        self.iCase = 0;
        """
        Gamma:  {0: 1.1102230246251565e-16, 1: 1.651158036900312e-08, 2: 0.2898979485566357, 3: 0.4627475401696348, 4: 0.5697090329565893, 5: 0.6416277095878444}
        """
        self.gammaTaus = {new_list: [] for new_list in range(0,5+1)}
        testData = TestData()
        
        def isValid(G : array) -> bool:
            return (1 - max(G)) >= 0.0 and min(G) > 0.0
        
        def isMonotonic(G : array) -> bool:
            for ig in range(1, len(G)) :
                if (G[ig-1] <= G[ig]) :
                    return False;
            return True;
        
        def analyze(group : Group, order:int, tau:float, theta:float) -> array:
            f = makeFmp( order, tau, theta );
            c = f.getCore();
            G = c.getGamma(0, 1.0)
            q = 'MONOTONIC'
            for ig in range(1, len(G)) :
                if (G[ig-1] <= G[ig]) :
                    q = 'IRREGULAR'
                    break;
            if (isValid(G)) :
                v = 'STABLE'
            else :
                v = 'UNSTABLE'
            if (q == 'IRREGULAR' or v == 'UNSTABLE') :
                return G
            caseGroup = createTestGroup(group, 'Case_%d' % self.iCase)
            self.iCase += 1
            testData.putInteger(caseGroup, 'order', order)
            testData.putScalar(caseGroup, 'tau', tau)
            testData.putScalar(caseGroup, 'theta', theta)
            testData.putScalar(caseGroup, 'nS', nSwitch(order, theta))
            testData.putArray(caseGroup, 'G', G)
            print('%2d %8.2g %15.8g %15.8g %s  %s %s' % (order, nSwitch(order, theta), theta, 1-theta, A2S(G), q, v))
            return G;
        
        group = createTestGroup(cdf, 'Gammas')
        
        delta = 2.0**-32;
        while ((1-delta) != 1.0) :
            delta = delta/2
        delta = delta*2
        
            
        tau = 1.0 #  gamma vectors are not dependant on tau
        for order in range(0,5+1) :
                
            def targetValid(theta: float) -> float:
                f = makeFmp( order, tau, theta );
                c = f.getCore();
                G = c.getGamma(0, 1.0)
                return (1-2*delta - max(G))
            
            t0 = brentq( targetValid, delta, 1.0-delta, xtol=delta );
            
            def targetMonotonic( theta: float) -> bool:
                f = makeFmp( order, tau, theta );
                c = f.getCore();
                G = c.getGamma(0, 1.0)
                return isMonotonic(G)
            
            if (order > 0) :
                if (not targetMonotonic(t0)) :
                    t1 = 1.0 - delta;
                    while (abs(t0-t1) > 2*delta) :
                        th = 0.5 * (t0 + t1)
                        if (targetMonotonic(th)) :
                            t1 = th;
                        else :
                            t0 = th;
                    t0 = t1
                    
                theta = t0;
                self.gammaTaus[order] = theta;
                while (theta > 0.0) :
                    G = analyze(group, order, tau, theta)
                    if (any(G) <= 0.0) :
                        break;
                    theta = theta/2
                theta = 0.5;
                while (theta > 0.0) :
                    G = analyze(group, order, tau, 1-theta)
                    if (any(G) <= 0.0) :
                        break;
                    theta = theta/2
            else :
                self.gammaTaus[order] = delta;
                theta = 0.999;
                while (theta > 0.0) :
                    G = analyze(group, order, tau, 1-theta)
                    if (any(G) <= 0.0) :
                        break;
                    theta = theta/2
        print('Gamma: ', self.gammaTaus )
        
        
    def generateVrfs(self, cdf : Dataset) -> None:
        """
        {0: 3.0518509447574615e-05, 1: 1.4142135623842478, 2: 2.5495097571983933, 3: 3.8369548115879297, 4: 5.583955190144479, 5: 8.241797269321978}
        """
        print('test8VRF')
        testData = TestData()
        self.vrfTaus = {new_list: [0.0] for new_list in range(0,5+1)}
        group = createTestGroup(cdf, 'Vrfs')
        self.iCase = 0;
       
        def isValid(V : array) -> bool:
            try :
                if (any(V.flatten() == 0) or any(V.flatten() > 1.0)) :
                    return False
            except :
                return False
            return True
        
        def isDecreasing(V : array) -> bool:
            if (not isValid(V)) :
                return False
            for i in range(0, V.shape[0]) :
                if (any(V[i,:] != V[:,i])) :
                    return False; # not symmetric
                for j in range(i+1, V.shape[0]) :
                    if (V[i,j-1] <= V[i,j]) :
                        return False
            return True
        
        delta = 2.0**-32;
        while ((1-delta) != 1.0) :
            delta = delta/2
        delta = delta*2
        for order in range(0, 5+1) :
            print(self.vrfTaus[order])
            for ptau in range(-14, 14+1) :
                tau = 2**ptau
                
                def targetDecreasing(theta : float) -> bool:
                    try :
                        f = makeFmp( order, tau, theta );
                        V = f.getCore().getVRF(0)
                        return isDecreasing(V)
                    except :
                        return False
                    
                t0 = delta
                t1 = 1 - delta
                if (not targetDecreasing(t0)) :
                    t1 = 1.0 - delta;
                    while (abs(t0-t1) > 2*delta) :
                        th = 0.5 * (t0 + t1)
                        if (targetDecreasing(th)) :
                            t1 = th;
                        else :
                            t0 = th;
                    t0 = t1
                    
                theta = t0; # first valid theta for tau at order
                f = makeFmp( order, tau, theta );
                V = f.getCore().getVRF(0)
                lowTheta = theta;
                
#                 print(order, tau, theta, isDecreasing(V))
                if (self.vrfTaus[order] == 0.0 and theta == delta) :
                    tau1 = tau  # at tau1 is good VRF at theta == delta
                    tau0 = tau/2 # was not good at tau/2
                    while (abs(tau1-tau0) > 1e-9) :
                        tau = 0.5*(tau1 + tau0)
                        f = makeFmp( order, tau, delta );
                        V = f.getCore().getVRF(0)
#                         print(order, tau, isDecreasing(V))
                        if (isDecreasing(V)) :
                            tau1 = tau
                        else :
                            tau0 = tau
                    f = makeFmp( order, tau1, delta );
                    V = f.getCore().getVRF(0)
#                     print(order, tau1, delta, isDecreasing(V)) 
                    self.vrfTaus[order] = tau1   
                
                t0 = lowTheta
                t1 = 1-delta
                if (not targetDecreasing(t1)) :
                    while (abs(t0-t1) > 2*delta) :
                        th = 0.5 * (t0 + t1)
                        if (targetDecreasing(th)) :
                            t1 = th;
                        else :
                            t0 = th;
                    t0 = t1
                else :
                    t0 = t1
                highTheta = t0
                print(order, tau, lowTheta, highTheta, log10(1-lowTheta), log10(1-highTheta)) 
                for ps in linspace(log10(1-lowTheta), log10(1-highTheta), 10, endpoint=True) :
                    theta = 1-10**ps;
                    f = makeFmp( order, tau, theta );
                    V = f.getCore().getVRF(0)
                    caseGroup = createTestGroup(group, 'Case_%d' % self.iCase)
                    self.iCase += 1
                    testData.putInteger(caseGroup, 'order', order)
                    testData.putScalar(caseGroup, 'tau', tau)
                    testData.putScalar(caseGroup, 'theta', theta)
                    testData.putArray(caseGroup, 'V', V)
                    print(order, tau, theta, isDecreasing(V))
                
#             tauFullRange = self.vrfTaus[order]
#             for ptau in range(-14, 14+1) :
#                 tau = 2**ptau
# #             for theta in (0.1, 0.25, 0.5, 0.75, 0.90, 0.95, 0.99, 0.999) :
#                 if (theta < t0) : 
#                     continue
#                 f = makeFmp( order, tau, theta );
#                 V = f.getCore().getVRF(0)
#                 if (isValid(V)) :
#                     C, d = covarianceToCorrelation(V)
#                     print(order, tau, theta, isDecreasing(V))
#                     print(A2S(C))
        print('VR: ', self.vrfTaus)

    
    def xtest0Generate(self):
#         order = 5
#         tau = 0.01
#         for i in range(1,6) :
#             theta = 1-10**-i
#             f = makeFmp(order, tau, theta);
#             print('VRF', order, tau, theta)
#             print(A2S(f.core._getVRF(tau, theta)))
#         
        print("test0Generate")
        path = testDataPath('testFMP.nc');
        cdf = Dataset(path, "w", format="NETCDF4");
        self.generateStates(cdf)
        self.generateGammas(cdf)
        self.generateVrfs(cdf)
        cdf.close()


   
    @testcase
    def test1CheckStates(self):
        '''@testData : TestData'''
        '''@matches : List[str]'''
        '''@order : int'''
        '''@setup : array'''
        '''@states : Group'''
        '''@cases : List[str]'''
        '''@caseName : str'''
        '''@caseGroup : Group'''
        '''@tau : float'''
        '''@theta : float'''
        '''@Y0 : array'''
        '''@times : array'''
        '''@observations : array'''
        '''@truth : array'''
        '''@expected : array'''
        '''@actual : array'''
        '''@f : RecursivePolynomialFilter'''
        '''@i : int'''
        '''@j : int'''
        '''@Zstar : array'''
        '''@e : float'''
        
#         print("test1CheckStates")
        assert_clear()
        testData = TestData('testFMP.nc')
        matches = testData.getMatchingGroups('States')
        assert_not_empty(matches)
        setup = testData.getGroupVariable(matches[0], 'setup')
        states = testData.getGroup(matches[0])
        cases = testData.getMatchingSubGroups(states, "Case_");
        for i in range(0, len(cases)) :
            caseName = cases[i]
            caseGroup = testData.getSubGroup(states, caseName)
            order = testData.getInteger(caseGroup, 'order')
            tau = testData.getScalar(caseGroup, 'tau')
            theta = testData.getScalar(caseGroup, 'theta')
            Y0 = testData.getArray(caseGroup, 'Y0')
            times = testData.getArray(caseGroup, 'times')
            observations = testData.getArray(caseGroup, 'observations')
            truth = testData.getArray(caseGroup, 'truth')
            
            expected = testData.getArray(caseGroup, 'expected')
            actual = zeros([times.shape[0], order+1]) 
                       
#             print('%2d %6.3f %15.8g %8.2g  %s' % (order, tau, theta, nSwitch(order,theta), A2S(Y0)) )
            
            f = makeFmp(order, tau, theta);
            f.start(0.0, Y0)
            for j in range(0,times.shape[0]) :
                Zstar = f.predict(times[j,0])
                e = observations[j] - Zstar[0]
                f.update(times[j,0], Zstar, e)
                actual[j,:] = transpose(f.getState());
            
            assert_allclose(actual, expected)
        self.assertGreaterEqual(32.0, assert_report("Fmp_test/test1CheckStates"))
        testData.close()
           
    @testcase     
    def test1CheckGammas(self) -> None:
        '''@testData : TestData'''
        '''@matches : List[str]'''
        '''@order : int'''
        '''@setup : array'''
        '''@states : Group'''
        '''@cases : List[str]'''
        '''@i : int'''
        '''@caseName : str'''
        '''@caseGroup : Group'''
        '''@tau : float'''
        '''@theta : float'''
        '''@Y0 : array'''
        '''@times : array'''
        '''@observations : array'''
        '''@truth : array'''
        '''@expectedG : array'''
        '''@actualG : array'''
        '''@nS : float'''
        '''@f : RecursivePolynomialFilter'''
        
#         print("test1CheckGammas")
        assert_clear()
        testData = TestData('testFMP.nc')
        matches = testData.getMatchingGroups('Gammas')
        assert_not_empty(matches)
        states = testData.getGroup(matches[0])
        cases = testData.getMatchingSubGroups(states, "Case_");
        for i in range(0, len(cases)) :
            caseName = cases[i]
            caseGroup = testData.getSubGroup(states, caseName)
            order = testData.getInteger(caseGroup, 'order')
            tau = testData.getScalar(caseGroup, 'tau')
            theta = testData.getScalar(caseGroup, 'theta')
            nS = testData.getScalar(caseGroup, 'nS')
            expectedG = testData.getArray(caseGroup, 'G')
            f = makeFmp( order, tau, theta );
            actualG = f.getCore().getGamma(0, 1.0)
            assert_allclose(nS, nSwitch(order, theta))
            assert_allclose(actualG, expectedG)
        self.assertGreaterEqual(0.0, assert_report("Fmp_test/test1CheckGammas"))
        testData.close()
            
            
    @testcase     
    def test1CheckVRF(self) -> None:
        '''@testData : TestData'''
        '''@matches : List[str]'''
        '''@order : int'''
        '''@setup : array'''
        '''@states : Group'''
        '''@cases : List[str]'''
        '''@i : int'''
        '''@caseName : str'''
        '''@caseGroup : Group'''
        '''@tau : float'''
        '''@theta : float'''
        '''@Y0 : array'''
        '''@times : array'''
        '''@observations : array'''
        '''@truth : array'''
        '''@expectedV : array'''
        '''@actualV : array'''
        '''@f : RecursivePolynomialFilter'''
#         print("test1CheckVRF")
        assert_clear()
        testData = TestData('testFMP.nc')
        matches = testData.getMatchingGroups('Vrfs')
        assert_not_empty(matches)
        states = testData.getGroup(matches[0])
        cases = testData.getMatchingSubGroups(states, "Case_");
        for i in range(0, len(cases)) :
            caseName = cases[i]
            caseGroup = testData.getSubGroup(states, caseName)
            order = testData.getInteger(caseGroup, 'order')
            tau = testData.getScalar(caseGroup, 'tau')
            theta = testData.getScalar(caseGroup, 'theta')
            expectedV = testData.getArray(caseGroup, 'V')
            f = makeFmp( order, tau, theta );
            actualV = f.getCore().getVRF(0)
            assert_allclose(actualV, expectedV)
        self.assertGreaterEqual(0.0, assert_report("Fmp_test/test1CheckVrfs"))
        testData.close()
        
        
        
    @testcase 
    def test9CoreBasic(self) -> None:
        '''@core90 : ICore'''
        '''@core95 : ICore'''
        '''@core95half : ICore'''
        '''@core95double : ICore'''
        '''@ad : array'''
        '''@ah : array'''
#         print("test9CoreBasic")
        assert_clear()
        core90 = makeFmpCore(3, 1.0, 0.90)
        core95 = makeFmpCore(3, 1.0, 0.95)
        core95half = makeFmpCore(3, 2.0, 0.95)
        core95double = makeFmpCore(3, 0.5, 0.95)
        
        assert_allclose( core90.getVRF(1), core90.getVRF(10) )  # should be time invariate
        assert_array_less( core95.getVRF(1), core90.getVRF(1))
        
        ad = (core95double.getVRF(1) / core95.getVRF(1))
        ah = (core95half.getVRF(1) / core95.getVRF(1))
        assert_allclose( ones([3+1,3+1]), ad * ah )
        
        assert_allclose( core90.getGamma(10.0, 5.0), core90.getGamma(11.0, 5.0) )
        assert_allclose( core90.getGamma(10.0, 5.0), core90.getGamma(10.0, 6.0) )
        assert_allclose( core95.getGamma(10.0, 5.0), core95half.getGamma(10.0, 5.0) ) 
        assert_allclose( core95.getGamma(10.0, 5.0), core95double.getGamma(10.0, 5.0) ) 
        assert_report("Fmp_test/test9CoreBasic")
        
    @testcase
    def test9Basic(self) -> None:
        '''@order : int'''
        '''@tau : float'''
        '''@theta : float'''
        '''@Y0 : array'''
        '''@observations : array'''
        '''@f : RecursivePolynomialFilter'''
        '''@t : float'''
        '''@Zstar : array'''
        '''@e : float'''
        '''@actual : array'''
        assert_clear()
        order = 5
        tau = 0.01
        theta = 0.9885155283985784
        actual = zeros([ order+1, 1])
        Y0 = array([ -5.373000000000E+00,-1.125200000000E+01,-1.740600000000E+01,-1.565700000000E+01,-7.458400000000E+00,-1.467800000000E+00 ]);
        observations = array([-5.2565E+00,-2.8652E+00,-1.4812E+01, 4.6590E+00, 4.7380E+00,-7.3765E+00, 1.3271E+01, 7.3593E+00, 3.4308E+00,-1.1329E+00,-1.5789E+00])
        f = makeFmp(order, tau, theta);
        f.start(0.0, Y0)
        t = 0
        Zstar = f.predict(t)
        assert_almost_equal(Zstar, array([ -5.373000000000E+00,-1.125200000000E-01,-1.740600000000E-03,-1.565700000000E-05,-7.458400000000E-08,-1.467800000000E-10 ]))            
        e = observations[0] - Zstar[0]
        assert_almost_equal(e, 0.11650000000000027)
        actual = f.update(t, Zstar, e)
        assert_almost_equal(actual, array([ 7.800661521666E-03,2.252446577781E-04,3.468911273583E-06,3.005115515478E-08,1.388453238252E-10,2.672957382342E-13 ]))

        actual = f.getState();
        assert_almost_equal(actual, array([-5.365199338478335, -11.229475534222193, -17.37131088726417, -15.62694884484522, -7.444515467617483, -1.4651270426176584]))
        t += 0.01
        Zstar = f.predict(t)
        assert_almost_equal(Zstar, array([-5.47836527e+00, -1.14039712e-01, -1.75279528e-03, -1.57014673e-05, -7.45916674e-08, -1.46512704e-10]))
        e = observations[1] - Zstar[0]
        assert_almost_equal(e, 2.6131652669594962)
        f.update(t, Zstar, e)
        actual = f.getState();
        assert_almost_equal(actual, array([ -5.30339172, -10.89873388, -16.74985512, -15.02740172,  -7.1477283,  -1.405171  ]))
        self.assertGreaterEqual(0.0, assert_report("Fmp_test/test9Basic"))
    
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
        
#         print("test9NSwitch")
        assert_clear()
        taus = array([0.01, 0.1, 1, 10, 100]);
        nTaus = len(taus);
        thetas = array([0.90, 0.95, 0.99, 0.999])
        nThetas = len(thetas);
        for order in range(0,5+1) :
            for itheta in range(0, nThetas):
                theta = thetas[itheta]
                for itau in range(0, nTaus):
                    tau = taus[itau]
                    emp = makeEmpCore(order, tau)
                    fmp = makeFmpCore(order, tau, theta)
                    n = int(nSwitch( order, theta ))
                    assert( fmp.getFirstVRF(0)/emp.getFirstVRF(n) < 1.25 )
#                     print('%2d, %8.3f, %7.5f, %8.1f, %6.2f, %6.2f, %6.2f' %
#                         (order, tau, theta, n, fmp.getFirstVRF(0)/emp.getFirstVRF(n-1), fmp.getFirstVRF(0)/emp.getFirstVRF(n), fmp.getFirstVRF(0)/emp.getFirstVRF(n+1)))
        
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()