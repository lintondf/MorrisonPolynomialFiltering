'''
Created on Feb 23, 2019

@author: NOOK

 netCDF4 Visual Studio https://www.unidata.ucar.edu/software/netcdf/docs/winbin.html
 C:\Program Files\netCDF 4.6.3
'''
import unittest
from netCDF4 import Dataset
from TestUtilities import *
from numpy import arange, array2string, cov, zeros, mean, std, var, diag,\
    transpose, concatenate, ceil, log2
from numpy.linalg import inv
from numpy.random import randn
from numpy.testing import assert_almost_equal
from numpy.testing import assert_allclose
from math import sqrt, sin
from runstats import Statistics
from scipy.stats._continuous_distns import chi2
from scipy.optimize.zeros import brentq


from polynomialfiltering.components.Fmp import makeFmp, makeFmpCore
from polynomialfiltering.filters.FixedMemoryPolynomialFilter import FixedMemoryFilter;

from polynomialfiltering.Main import FilterStatus
from TestSuite import testDataPath;
from TestData import TestData
from polynomialfiltering.PythonUtilities import ignore, testcase, testmethod, testclass, testclassmethod
from polynomialfiltering.PythonUtilities import assert_not_empty
from pygments.unistring import Lo
from _pickle import load


class FixedMemoryFilter_test(unittest.TestCase):
    '''@testData : TestData'''
    
    @classmethod
    def setUpClass(self):
        self.Y0 = array([1e4, 1e3, 1e2, 1e1, 1e0, 1e-1]);
 
    @classmethod
    def tearDownClass(self):
        pass
 
     
 
    @testmethod
    def executeEstimatedState(self, setup : array, data : array ) -> array:
        '''@order : int'''
        '''@window : int'''
        '''@M : int'''
        '''@iCheck : int'''
        '''@times : array'''
        '''@observations : array'''
        '''@fixed : FixedMemoryFilter'''
        '''@i : int'''
        order = int(setup[0]);
        window = int(setup[1]);
        M = int(setup[2]);
        iCheck = int(setup[3]);
        times = data[:,0:1];
        observations = data[:,1:2];
        fixed = FixedMemoryFilter(order, window);
        for i in range(0,M) :
            fixed.add(times[i], observations[i]);
        return fixed.transitionState(times[iCheck]);
                 
                 
    def generatePerfect(self, testData : TestData ) -> None:
        setup = array([None, 11, 12, 11]);
        tau = 0.1;
        N = 25;
        for order in range(0,5+1):
            setup[0] = order; 
            (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], tau, sigma=0.0)
            data = concatenate([times, observations], axis=1);
            group = testData.createTestGroup( 'testPerfect_%d' % order );
            testData.putArray(group, 'setup', setup);
            testData.putArray(group, 'data', data);
#             print('setup ',setup)
#             print('data ',data)
             
            expected = self.executeEstimatedState(setup, data);
#             print(order, expected)
             
            testData.putArray(group, 'expected', expected);
            assert_allclose( expected, truth[11,:], atol=0, rtol=1e-3 )
 
    def generateNoisy(self, testData : TestData ) -> None:
        setup = array([None, 11, 12, 11]);
        tau = 0.1;
        N = 25;
        for order in range(0,5+1):
            setup[0] = order; 
            (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], tau, sigma=1.0)
            data = concatenate([times, observations], axis=1);
            group = testData.createTestGroup('testNoisy_%d' % order );
            testData.putArray(group, 'setup', setup);
            testData.putArray(group, 'data', data);
             
            expected = self.executeEstimatedState(setup, data);
             
            testData.putArray(group, 'expected', expected);
            #assert_allclose( expected, truth[11,:], atol=0, rtol=1e-2 )
 
     
    def generateMidpoints(self, testData : TestData ) -> None:
        tau = 0.1;
        N = 25;
        order = 2;
        window = 11;
        M = 12; # number of points to input
        offset = M - window;
        for iCheck in range(offset, M) :
            setup = array([order, window, M, iCheck]);
            fixed = FixedMemoryFilter(order, window);
            (times, truth, observations, noise) = generateTestData(fixed.order, N, 0.0, self.Y0[0:fixed.order+1], tau, sigma=0.0)
             
            data = concatenate([times, observations], axis=1);
            group = testData.createTestGroup( 'testMidpoints_%d' % iCheck );
            testData.putArray(group, 'setup', setup);
            testData.putArray(group, 'data', data);
             
            expected = self.executeEstimatedState(setup, data);
             
            testData.putArray(group, 'expected', expected);
            assert_allclose( truth[iCheck,:], expected );
             
    @testmethod
    def executeVRF(self, setup : array, data : array ) -> array:
        '''@order : int'''
        '''@window : int'''
        '''@M : int'''
        '''@iCheck : int'''
        '''@times : array'''
        '''@observations : array'''
        '''@fixed : FixedMemoryFilter'''
        '''@i : int'''
        order = int(setup[0]);
        window = int(setup[1]);
        M = int(setup[2]);
        iCheck = int(setup[3]);
        times = data[:,0:1];
        observations = data[:,1:2];
        fixed = FixedMemoryFilter(order, window);
        for i in range(0,M) :
            fixed.add(times[i], observations[i]);
        return fixed.getVRF();
                 
    def generateVRF(self, testData : TestData ) -> None:
        tau = 0.1;
        N = 25;
        window = 11;
        M = 12; # number of points to input
        iCheck = M-1;
        for order in range(0,5+1) :
            setup = array([order, window, M, iCheck]);
            fixed = FixedMemoryFilter(order, window);
            (times, truth, observations, noise) = generateTestData(fixed.order, N, 0.0, self.Y0[0:fixed.order+1], tau, sigma=0.0)
             
            data = concatenate([times, observations], axis=1);
            group = testData.createTestGroup('testVRF_%d' % order );
            testData.putArray(group, 'setup', setup);
            testData.putArray(group, 'data', data);
             
            expected = self.executeVRF(setup, data);
            testData.putArray(group, 'expected', expected);
         
         
    def xtestVRFStatistics(self):
        '''
         This extended numeric test validates the computed VRF matrix
         against the actual residuals for a large sample of filter runs.
         N=1000, K=5000, 492.609 seconds
        [     0.998          1          1          1          1          1          1          1          1]        
        '''
        tau = 0.1;
        N = 1000;
        order = 2;
        window = 51;
        M = window; # number of points for initial input
        setup = array([order, window, M]);
        K = 5000;
        C = zeros([K,(order+1)**2])
        for k in range(0,K) :
            fixed = FixedMemoryFilter(order, window);
            (times, truth, observations, noise) = generateTestData(fixed.order, N, 0.0, self.Y0[0:fixed.order+1], tau, sigma=1.0)
            for i in range(0,window) :
                fixed.add(times[i], observations[i]);
            results = zeros([N-window, order+1]);
            for i in range(window, N) :
                fixed.add(times[i], observations[i]);
                results[i-window,:] = fixed.getState() - truth[i,:];
            c = cov(results,rowvar=False);
            C[k,:] = c.flatten();
            V = fixed.getCovariance();
             
        E = mean(C,axis=0) / V.flatten()
        print( A2S( E ) );
        assert_allclose( E, ones([(order+1)**2]), atol=1e-2 )
         
 
    def test0Generate(self):
        testData = TestData('FixedMemoryFiltering.nc', 'w')
        
        self.generatePerfect(testData)
        self.generateNoisy(testData)
        self.generateMidpoints(testData)
        self.generateVRF(testData)
        
        testData.close()

    @testcase
    def test1CheckPerfect(self):
        '''@matches : List[str]'''
        '''@tau : float'''
        '''@N : int'''
        '''@i : int'''
        '''@group : Group'''
        '''@setup : vector'''
        '''@order : int'''
        '''@data : array'''
        '''@actual : array'''
        '''@expected : array'''
        '''@testData : TestData'''
        assert_clear()
        testData = TestData('FixedMemoryFiltering.nc')
        matches = testData.getMatchingGroups('testPerfect_')
        assert_not_empty(matches)
        tau = 0.1;
        N = 25;
        for i in range(0, len(matches)) :
            group = testData.getGroup(matches[i])
            setup = testData.getArray(group, 'setup')
            order = int(setup[0]) 
            data = testData.getArray(group, 'data');
            actual = self.executeEstimatedState(setup, data);
            expected = testData.getArray(group, 'expected');
            assert_allclose( expected, actual )
        testData.close()
        assert_report("FixedMemoryFilter_test/test1CheckPerfect")

    @testcase
    def test1CheckNoisy(self):
        '''@matches : List[str]'''
        '''@tau : float'''
        '''@N : int'''
        '''@i : int'''
        '''@group : Group'''
        '''@setup : vector'''
        '''@order : int'''
        '''@data : array'''
        '''@actual : array'''
        '''@expected : array'''
        '''@testData : TestData'''
        
        assert_clear()
        testData = TestData('FixedMemoryFiltering.nc')
        matches = testData.getMatchingGroups('testNoisy_')
        assert_not_empty(matches)
        tau = 0.1;
        N = 25;
        for i in range(0, len(matches)) :
            group = testData.getGroup(matches[i])
            setup = testData.getArray(group, 'setup')
            order = int(setup[0]) 
            data = testData.getArray(group, 'data');
            actual = self.executeEstimatedState(setup, data);
            expected = testData.getArray(group, 'expected');
            assert_allclose( expected, actual )
        testData.close()
        assert_report("FixedMemoryFilter_test/test1CheckNoisy")

    @testcase
    def test1CheckMidpoints(self):
        '''@matches : List[str]'''
        '''@tau : float'''
        '''@N : int'''
        '''@M : int'''
        '''@window : int'''
        '''@iCheck : int'''
        '''@i : int'''
        '''@group : Group'''
        '''@setup : vector'''
        '''@offset : int'''
        '''@order : int'''
        '''@data : array'''
        '''@actual : array'''
        '''@expected : array'''
        '''@testData : TestData'''
        
        assert_clear()
        testData = TestData('FixedMemoryFiltering.nc')
        matches = testData.getMatchingGroups('testMidpoints_')
        assert_not_empty(matches)
        tau = 0.1;
        N = 25;
        order = 2;
        window = 11;
        M = 12; # number of points to input
        offset = M - window;
        for i in range(0, len(matches)) :
            group = testData.getGroup(matches[i])
            setup = testData.getArray(group, 'setup')
            order = int(setup[0])
            window = int(setup[1])
            M = int(setup[2])
            iCheck = int(setup[3])
            data = testData.getArray(group, 'data');
            actual = self.executeEstimatedState(setup, data);
            expected = testData.getArray(group, 'expected');
            assert_allclose( expected, actual )
        testData.close()
        assert_report("FixedMemoryFilter_test/test1CheckMidpoints")
    
    @testcase
    def test1CheckVrfs(self):
        '''@matches : List[str]'''
        '''@tau : float'''
        '''@N : int'''
        '''@M : int'''
        '''@window : int'''
        '''@iCheck : int'''
        '''@i : int'''
        '''@group : Group'''
        '''@setup : vector'''
        '''@order : int'''
        '''@offset : int'''
        '''@data : array'''
        '''@actual : array'''
        '''@expected : array'''
        '''@testData : TestData'''
        
        assert_clear()
        testData = TestData('FixedMemoryFiltering.nc')
        matches = testData.getMatchingGroups('testVRF_')
        assert_not_empty(matches)
        tau = 0.1;
        N = 25;
        order = 2;
        window = 11;
        M = 12; # number of points to input
        offset = M - window;
        for i in range(0, len(matches)) :
            group = testData.getGroup(matches[i])
            setup = testData.getArray(group, 'setup')
            order = int(setup[0])
            window = int(setup[1])
            M = int(setup[2])
            iCheck = int(setup[3])
            data = testData.getArray(group, 'data');
            actual = self.executeVRF(setup, data);
            expected = testData.getArray(group, 'expected');
            assert_allclose( expected, actual )
        testData.close()
        assert_report("FixedMemoryFilter_test/test1CheckVrfs")

    @testclass
    class TestFixedMemoryFilter(FixedMemoryFilter): 
        @testclassmethod
        def __init__(self, order : int):
            super().__init__(order)
        
        @testclassmethod
        def getOrder(self) -> int:
            return self.order
        
        @testclassmethod
        def getL(self) -> int:
            return self.L
        

    @testcase
    def test9Regresssion(self):
        '''@f : TestFixedMemoryFilter'''
        '''@fixed : FixedMemoryFilter'''
        '''@i : int'''
        '''@Z : array'''
        assert_clear()
        f = self.TestFixedMemoryFilter(4)
        self.assertEqual(f.getOrder(), 4)
        self.assertEqual(f.getL(), 51)
        
        fixed = FixedMemoryFilter(0,5)
        self.assertEqual(fixed.getTau(), 0.0)
        self.assertEqual(fixed.getStatus(), FilterStatus.IDLE)
        Z = zeros([1, 1])
        assert_almost_equal(Z, fixed.getVRF())
        self.assertEqual(fixed.getFirstVRF(), 0)
        self.assertEqual(fixed.getLastVRF(), 0)
        for i in range(0,5) :
            self.assertEqual( fixed.getN(), i)
            fixed.add(i, i)
            self.assertEqual(fixed.getStatus(), FilterStatus.INITIALIZING)
        fixed.add(10,10)
        self.assertEqual(fixed.getStatus(), FilterStatus.RUNNING)
        self.assertEqual(fixed.getTime(), 10 )
        assert_almost_equal(fixed.getState(), array([4.0]))
        assert_report("FixedMemoryFilter_test/test9Regresssion")
            
#     def xtest9ValidVRF(self):
#         '''
#         Find minimum viable window size by order
#         
# 0 2 [       0.5]
# 0 2 0.3333333333333321 [       0.5] [         1]
# 0 4 0.6000000000000006 [      0.25] [         1]
# 0 8 0.7777777777773525 [     0.125] [         1]
# 0 16 0.8823529411764697 [    0.0625] [         1]
# 0 32 0.9393939393939393 [    0.0312] [         1]
# 0 64 0.9692307692307692 [    0.0156] [         1]
# 0 128 0.9844961240310077 [   0.00781] [         1]
# 0 256 0.9922178988327404 [   0.00391] [         1]
# 0 512 0.9961013645224189 [   0.00195] [         1]
# 0 1024 0.998048780487805 [  0.000977] [         1]
# 0 2048 0.9990239141044412 [  0.000488] [         1]
# 0 4096 0.9995118379301928 [  0.000244] [         1]
# 0 8192 0.9997558891741393 [  0.000122] [         1]
# 0 16384 0.9998779371376827 [   6.1e-05] [         1]
# 0 32768 0.9999389667063454 [  3.05e-05] [         1]
# 0 65536 0.9999694828875301 [  1.53e-05] [         1]
# 1 3 [     0.833        0.5]
# 1 4 0.43925602296464933 [       0.7        0.2] [         1       1.69]
# 1 8 0.6724505734312713 [     0.417     0.0238] [         1       1.58]
# 1 16 0.8201816477846916 [     0.228    0.00294] [         1       1.53]
# 1 32 0.9053480308963552 [     0.119   0.000367] [         1        1.5]
# 1 64 0.9513781833747185 [    0.0611   4.58e-05] [         1       1.48]
# 1 128 0.9753499249944159 [    0.0309   5.72e-06] [         1       1.47]
# 1 256 0.9875881689530053 [    0.0155   7.15e-07] [         1       1.47]
# 1 512 0.9937721291846118 [   0.00779   8.94e-08] [         1       1.47]
# 1 1024 0.9968805432267533 [    0.0039   1.12e-08] [         1       1.47]
# 1 2048 0.9984388871769343 [   0.00195    1.4e-09] [         1       1.47]
# 1 4096 0.9992190969657603 [  0.000976   1.75e-10] [         1       1.47]
# 1 8192 0.9996094617630479 [  0.000488   2.18e-11] [         1       1.46]
# 1 16384 0.999804709193426 [  0.000244   2.73e-12] [         1       1.46]
# 1 32768 0.9999023491736896 [  0.000122   3.41e-13] [         1       1.46]
# 1 65536 0.999951173230964 [   6.1e-05   4.26e-14] [         1       1.46]
# 2 6 [     0.821      0.727      0.107]
# 2 8 0.583057925115227 [     0.708      0.315     0.0238] [         1       1.47       3.13]
# 2 16 0.7646697760206322 [     0.442     0.0423     0.0007] [         1       1.39       2.77]
# 2 32 0.8738021948477684 [     0.249    0.00555   2.16e-05] [         1       1.36       2.59]
# 2 64 0.9344748135627071 [     0.132   0.000712   6.71e-07] [         1       1.34       2.51]
# 2 128 0.9665885985830226 [    0.0682   9.02e-05    2.1e-08] [         1       1.33       2.47]
# 2 256 0.9831264055519138 [    0.0346   1.14e-05   6.55e-10] [         1       1.32       2.45]
# 2 512 0.991520489844066 [    0.0174   1.43e-06   2.05e-11] [         1       1.32       2.44]
# 2 1024 0.9957494724220399 [   0.00875   1.78e-07   6.39e-13] [         1       1.32       2.43]
# 2 2048 0.9978720311857058 [   0.00439   2.23e-08      2e-14] [         1       1.32       2.43]
# 2 4096 0.9989353378416042 [    0.0022   2.79e-09   6.25e-16] [         1       1.32       2.43]
# 2 8192 0.9994674992956603 [    0.0011   3.49e-10   1.95e-17] [         1       1.32       2.43]
# 2 16384 0.9997337072180994 [  0.000549   4.37e-11    6.1e-19] [         1       1.32       2.43]
# 2 32768 0.9998668429989992 [  0.000275   5.46e-12   1.91e-20] [         1       1.32       2.43]
# 2 65536 0.9999334188464236 [  0.000137   6.82e-13   5.96e-22] [         1       1.32       2.43]
# 3 11 [      0.79      0.655       0.15    0.00583]
# 3 16 0.714006048298417 [     0.648      0.231      0.023   0.000397] [         1       1.33       2.39       5.51]
# 3 32 0.8441263495272646 [     0.399     0.0322   0.000736   2.97e-06] [         1       1.28        2.2       4.82]
# 3 64 0.918260758333309 [     0.223    0.00428   2.35e-05    2.3e-08] [         1       1.26       2.11       4.51]
# 3 128 0.9580924003903428 [     0.118   0.000553   7.44e-07   1.79e-10] [         1       1.25       2.07       4.36]
# 3 256 0.9787746653249855 [    0.0607   7.03e-05   2.34e-08    1.4e-12] [         1       1.25       2.05       4.28]
# 3 512 0.9893178657868699 [    0.0308   8.86e-06   7.34e-10   1.09e-14] [         1       1.25       2.03       4.25]
# 3 1024 0.9946413631083735 [    0.0155   1.11e-06    2.3e-11   8.54e-17] [         1       1.25       2.03       4.23]
# 3 2048 0.9973162633920687 [   0.00778   1.39e-07   7.19e-13   6.67e-19] [         1       1.24       2.03       4.22]
# 3 4096 0.9986570239198586 [    0.0039   1.74e-08   2.25e-14   5.21e-21] [         1       1.24       2.03       4.21]
# 3 8192 0.9993282346101082 [   0.00195   2.18e-09   7.02e-16   4.07e-23] [         1       1.24       2.03       4.21]
# 3 16384 0.9996640479167898 [  0.000976   2.73e-10    2.2e-17   3.18e-25] [         1       1.24       2.03       4.21]
# 3 32768 0.9998320066049746 [  0.000488   3.41e-11   6.86e-19   2.48e-27] [         1       1.24       2.02       4.21]
# 3 65536 0.9999159989636768 [  0.000244   4.26e-12   2.14e-20   1.94e-29] [         1       1.24       2.02       4.21]
# 4 16 [     0.806      0.789      0.256     0.0238   0.000417]
# 4 16 0.6670857445321902 [     0.806      0.789      0.256     0.0238   0.000417] [         1       1.31       2.22       4.64       11.8]
# 4 32 0.8159689795428072 [     0.549      0.117    0.00846   0.000182   7.44e-07] [         1       1.24       1.98       3.92       9.42]
# 4 64 0.9026028049567045 [     0.326     0.0163   0.000278   1.43e-06   1.42e-09] [         1       1.22       1.88       3.61       8.41]
# 4 128 0.9498026063930057 [     0.178    0.00216   8.94e-06   1.13e-08   2.76e-12] [         1       1.21       1.84       3.46       7.93]
# 4 256 0.974505013988194 [    0.0932   0.000278   2.84e-07   8.89e-11   5.38e-15] [         1        1.2       1.82       3.39       7.71]
# 4 512 0.9871505625572224 [    0.0477   3.52e-05   8.95e-09   6.97e-13   1.05e-17] [         1        1.2       1.81       3.36       7.59]
# 4 1024 0.9935494245220162 [    0.0241   4.44e-06   2.81e-10   5.45e-15   2.05e-20] [         1        1.2        1.8       3.34       7.54]
# 4 2048 0.996768200986984 [    0.0121   5.57e-07   8.79e-12   4.26e-17   4.01e-23] [         1        1.2        1.8       3.33       7.51]
# 4 4096 0.9983824667417064 [   0.00609   6.97e-08   2.75e-13   3.33e-19   7.83e-26] [         1        1.2        1.8       3.33        7.5]
# 4 8192 0.9991908241880872 [   0.00305   8.72e-09    8.6e-15    2.6e-21   1.53e-28] [         1        1.2        1.8       3.33       7.49]
# 4 16384 0.9995953097051034 [   0.00152   1.09e-09   2.69e-16   2.04e-23   2.99e-31] [         1        1.2        1.8       3.33       7.49]
# 4 32768 0.9997976292436375 [  0.000763   1.36e-10    8.4e-18   1.59e-25   5.83e-34] [         1        1.2        1.8       3.33       7.49]
# 4 65536 0.9998988082181341 [  0.000381   1.71e-11   2.63e-19   1.24e-27   1.14e-36] [         1        1.2        1.8       3.33       7.49]
# 5 23 [     0.802      0.787       0.28     0.0351    0.00143   1.17e-05]
# 5 32 0.789095892383079 [     0.683      0.323      0.056    0.00349   7.16e-05   2.95e-07] [         1       1.22       1.86       3.41       7.44       19.1]
# 5 64 0.8874189225829691 [     0.433      0.047    0.00189   2.81e-05   1.39e-07   1.38e-10] [         1       1.19       1.74       3.08        6.5       16.1]
# 5 128 0.9416848213428213 [     0.246     0.0064   6.22e-05   2.25e-07   2.72e-10   6.68e-14] [         1       1.18       1.69       2.94       6.08       14.8]
# 5 256 0.970301429174764 [     0.131   0.000837      2e-06   1.78e-09   5.34e-13   3.25e-17] [         1       1.17       1.67       2.87       5.88       14.1]
# 5 512 0.9850107840333568 [     0.068   0.000107   6.33e-08    1.4e-11   1.05e-15   1.59e-20] [         1       1.17       1.66       2.84       5.78       13.8]
# 5 1024 0.9924698011242994 [    0.0346   1.35e-05   1.99e-09    1.1e-13   2.05e-18   7.75e-24] [         1       1.17       1.65       2.82       5.73       13.7]
# 5 2048 0.9962259253331627 [    0.0174    1.7e-06   6.24e-11   8.63e-16      4e-21   3.78e-27] [         1       1.17       1.65       2.81       5.71       13.6]
# 5 4096 0.9981107090767831 [   0.00875   2.13e-07   1.95e-12   6.75e-18   7.82e-24   1.85e-30] [         1       1.17       1.65       2.81       5.69       13.6]
# 5 8192 0.9990547899113236 [   0.00439   2.67e-08   6.11e-14   5.27e-20   1.53e-26   9.02e-34] [         1       1.16       1.65       2.81       5.69       13.6]
# 5 16384 0.9995272536453912 [   0.00219   3.34e-09   1.91e-15   4.12e-22   2.99e-29    4.4e-37] [         1       1.16       1.65       2.81       5.69       13.5]
# 5 32768 0.9997635914757146 [    0.0011   4.18e-10   5.98e-17   3.22e-24   5.83e-32   2.15e-40] [         1       1.16       1.65       2.81       5.68       13.5]
# 5 65536 0.9998817868987548 [  0.000549   5.22e-11   1.87e-18   2.52e-26   1.14e-34   1.05e-43] [         1       1.16       1.65       2.81       5.68       13.5]        
#         '''
#         pass
#         def isValid(V : array) -> bool:
#             try :
#                 if (any(V.flatten() == 0) or any(V.flatten() > 1.0)) :
#                     return False
#             except :
#                 return False
#             return True
#         
#         def isDecreasing(V : array) -> bool:
#             if (not isValid(V)) :
#                 return False
#             for i in range(0, V.shape[0]) :
#                 if (any(abs((V[i,:] - V[:,i])/V[i,:]) > 1e-10)) :
#                     print(i, A2S((V[i,:] - V[:,i])/V[i,:]))
#                     return False; # not symmetric
#                 for j in range(i+1, V.shape[0]) :
#                     if (V[i,j-1] <= V[i,j]) :
#                         return False
#                 if (i > 0) :
#                     if (V[i,i] > V[i-1,i-1]) :
#                         return False
#             return True
#         
#         def getV(order : int, tau : float, N : int ) -> array:
#             (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], tau, sigma=0.0)
#             fixed = FixedMemoryFilter(order, N)
#             for i in range(0,N) :
#                 fixed.add(times[i], observations[i])
#             V = fixed.getVRF()
#             return V
#         
#         def matchTheta(order : int, tau : float, V00 : float)  -> float:
#             def targetTheta(t :float ) -> float:
#                 c = makeFmpCore(order, tau, t);
#                 return max(diag(c.getVRF(0))) - V00;
#                  
#             t0 = brentq( targetTheta, 1e-6, 1-1e-8 );
#             return t0
#         
#         for order in range(0,5+1):
#             for tau in [1] : # [0.01, 0.1, 1, 10, 100] :
#                 lo = order+1
#                 hi = 4096
#                 while ((hi - lo) > 1) :
#                     N = (hi + lo) // 2
#                     V = getV( order, tau, N )
#                     (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], tau, sigma=0.0)
#                     fixed = FixedMemoryFilter(order, N)
#                     for i in range(0,N) :
#                         fixed.add(times[i], observations[i])
#                     V = fixed.getVRF()
#                     if (isDecreasing(V)) :
#                         hi = N
#                     else :
#                         lo = N
#                 N = hi
#                 V = getV( order, tau, N )
#                 print(order, N, A2S(diag(V).flatten()))
#                 lo = 2 ** ceil(log2(N))
#                 hi = 2 ** 16
#                 N = int(lo)
#                 while (N <= hi) :
#                     V = getV( order, tau, N )
#                     theta = matchTheta(order, tau, V[0,0])
#                     c = makeFmpCore(order, tau, theta);
#                     print(order, N, theta, A2S(diag(V).flatten()), A2S((diag(V)/diag(c.getVRF(0))).flatten()))
#                     N *= 2
           
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()