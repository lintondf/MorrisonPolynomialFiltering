'''
Created on Apr 11, 2019

@author: NOOK
'''
import unittest
from polynomialfiltering.PythonUtilities import ignore, testcase, testclass, testclassmethod

from time import perf_counter
from numpy import array, array as vector, mean, interp
from numpy import cov, zeros, diag, sqrt
from numpy.linalg import inv
from numpy.random import randn
from numpy.testing import assert_almost_equal
from netCDF4 import Dataset
from TestUtilities import createTestGroup, writeTestVariable
from TestSuite import testDataPath;
from polynomialfiltering.PythonUtilities import ignore, testcase
from TestData import TestData, A2S
from polynomialfiltering.PythonUtilities import assert_not_empty

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


from polynomialfiltering.Main import AbstractFilter, AbstractFilterWithCovariance, FilterStatus
from polynomialfiltering.filters.ManagedFilterBase import ManagedFilterBase;
from polynomialfiltering.components.Emp import makeEmp

from polynomialfiltering.filters.controls.errormodel.ConstantObservationErrorModel import ConstantObservationErrorModel
from polynomialfiltering.filters.controls.errormodel.FixedSampleErrorModel import FixedSampleErrorModel
from polynomialfiltering.filters.controls.errormodel.ObservationDifferencesErrorModel import ObservationDifferencesErrorModel
from polynomialfiltering.filters.controls.errormodel.PairResidualsErrorModel import PairResidualsErrorModel
from polynomialfiltering.filters.PairedPolynomialFilter import PairedPolynomialFilter
from polynomialfiltering.filters.FixedMemoryPolynomialFilter import FixedMemoryFilter


class ObservationErrorModel_test(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass
    
    @classmethod
    def tearDownClass(self):
        pass
    
    def setUp(self):
        pass


    def tearDown(self):
        pass

    @testclass
    class ManagedFilterBaseMock(ManagedFilterBase):
        
        @testclassmethod
        def __init__(self, order : int, worker : AbstractFilter):
            super().__init__(order, worker);
        
        @testclassmethod
        def add(self, t:float, y:vector, observationId:int = 0) -> bool :
            return False;
        
        @testclassmethod
        def getCovariance(self) -> array:
            return zeros([1,1])
    
        @testclassmethod
        def getGoodnessOfFit(self) -> float:
            return 0.0;
        
        @testclassmethod
        def getFirstVRF(self) -> float:
            return 0.0;
        
        @testclassmethod
        def getLastVRF(self) -> float:
            return 0.0;
        
        @testclassmethod
        def getVRF(self) -> array:
            '''V : array'''
            V = zeros(self.order+1, self.order+1)
            return V;
        
    def xtest0ConstantObservationErrorModelGenerate(self) -> None:
        path = testDataPath('testConstantObservationErrorModel.nc');
#         print("Writing to: ", path)
        cdf = Dataset(path, "w", format="NETCDF4");
        
        iTest = 0;
        for e in [-1, 0] :
            group = createTestGroup(cdf, 'testScalar_%d' % iTest );
            iTest += 1;
            
            inputCovariance = randn(1,1);
            inputInverse = array([[1.0/inputCovariance[0,0]]]);
            
            element = array([e]);
            writeTestVariable(group, "element", element)
            writeTestVariable(group, 'inputCovariance', inputCovariance);
            writeTestVariable(group, 'inputInverse', inputInverse);
            
            x = inputCovariance[0,0];
            y = inputInverse[0,0];
            iE = int(element[0]);
            model = ConstantObservationErrorModel(x);
            Q = model.getCovarianceMatrix(None, 0.0, array([0]), iE);
            assert_almost_equal(inputCovariance[0,0], Q)
            Q = model.getPrecisionMatrix(None, 0.0, array([0]), -1);
            assert_almost_equal(inputInverse[0,0], Q)

        iTest = 0;
        for e in [-1, 0] :
            group = createTestGroup(cdf, 'testMatrix_%d' % iTest );
            iTest += 1;
            
            inputCovariance = randn(1,1);
            inputInverse = array([[1.0/inputCovariance[0,0]]]);
            
            element = array([e]);
            writeTestVariable(group, "element", element)
            writeTestVariable(group, 'inputCovariance', inputCovariance);
            writeTestVariable(group, 'inputInverse', inputInverse);
            
            iE = int(element[0]);
            model = ConstantObservationErrorModel(inputCovariance, inputInverse);
            Q = model.getCovarianceMatrix(None, 0.0, array([0]), iE);
            assert_almost_equal(inputCovariance[0,0], Q)
            Q = model.getPrecisionMatrix(None, 0.0, array([0]), -1);
            assert_almost_equal(inputInverse[0,0], Q)

        iTest = 0;
        for e in [-1, 0, 1, 2] :
            group = createTestGroup(cdf, 'testMatrixMatrix_%d' % iTest );
            iTest += 1;
            
            X = randn(100,3);
            inputCovariance = cov(X, rowvar=False);
            inputInverse = inv(inputCovariance);
            
            element = array([e]);
            writeTestVariable(group, "element", element)
            writeTestVariable(group, 'inputCovariance', inputCovariance);
            writeTestVariable(group, 'inputInverse', inputInverse);
            
            iE = int(element[0]);
            model = ConstantObservationErrorModel(inputCovariance);
            
            if (iE < 0) :
                Q = model.getCovarianceMatrix(None, 0.0, array([0]), iE);
                assert_almost_equal(inputCovariance, Q)
                Q = model.getPrecisionMatrix(None, 0.0, array([0]), iE);
                assert_almost_equal(inputInverse, Q)
            else :
                Q = model.getCovarianceMatrix(None, 0.0, array([0]), iE);
                assert_almost_equal(inputCovariance[iE,iE], Q)
                Q = model.getPrecisionMatrix(None, 0.0, array([0]), iE);
                assert_almost_equal(inputInverse[iE,iE], Q)
        cdf.close();

    @testcase
    def xtest1ConstantObservationErrorModelScalar(self) -> None: 
        '''@testData : TestData'''
        '''@matches : List[str]'''
        '''@i : int'''
        '''@iE : int'''
        '''@inputCovariance : array'''
        '''@inputInverse : array'''
        '''@element : vector'''
        '''@x : float'''
        '''@Q : array'''
        '''@model : ConstantObservationErrorModel'''
        
        testData = TestData('testConstantObservationErrorModel.nc')
        matches = testData.getMatchingGroups('testScalar_')
        assert_not_empty(matches)
        for i in range(0, len(matches)) :
            element = testData.getGroupVariable(matches[i], 'element')
            inputCovariance = testData.getGroupVariable(matches[i], 'inputCovariance')
            inputInverse = testData.getGroupVariable(matches[i], 'inputInverse')
            iE = int(element[0]);
            x = inputCovariance[0,0]
            model = ConstantObservationErrorModel(x);
            Q = model.getCovarianceMatrix(None, 0.0, array([0]), iE);
            assert_almost_equal(inputCovariance[0,0], Q)
            Q = model.getPrecisionMatrix(None, 0.0, array([0]), iE);
            assert_almost_equal(inputInverse[0,0], Q)        
        testData.close()

    @testcase
    def xtest2ConstantObservationErrorModelMatrix(self) -> None:
        '''@testData : TestData'''
        '''@matches : List[str]'''
        '''@i : int'''
        '''@iE : int'''
        '''@inputCovariance : array'''
        '''@ic : float'''
        '''@inputInverse : array'''
        '''@element : vector'''
        '''@Q : array'''
        '''@model : ConstantObservationErrorModel'''
        
        testData = TestData('testConstantObservationErrorModel.nc')
        matches = testData.getMatchingGroups('testMatrix_')
        assert_not_empty(matches)
        for i in range(0, len(matches)) :
            element = testData.getGroupVariable(matches[i], 'element')
            inputCovariance = testData.getGroupVariable(matches[i], 'inputCovariance')
            inputInverse = testData.getGroupVariable(matches[i], 'inputInverse')
            iE = int(element[0]);
            ic = inputCovariance[0,0];
            model = ConstantObservationErrorModel(ic);
            Q = model.getCovarianceMatrix(None, 0.0, array([0]), iE);
            assert_almost_equal(inputCovariance[0,0], Q)
            Q = model.getPrecisionMatrix(None, 0.0, array([0]), iE);
            assert_almost_equal(inputInverse[0,0], Q)        
        testData.close()

    @testcase
    def xtest3ConstantObservationErrorModelMatrixMatrix(self) -> None:
        '''@testData : TestData'''
        '''@matches : List[str]'''
        '''@i : int'''
        '''@iE : int'''
        '''@inputCovariance : array'''
        '''@inputInverse : array'''
        '''@element : vector'''
        '''@Q : array'''
        '''@model : ConstantObservationErrorModel'''
        
        testData = TestData('testConstantObservationErrorModel.nc')
        matches = testData.getMatchingGroups('testMatrixMatrix_')
        assert_not_empty(matches)
        for i in range(0, len(matches)) :
            element = testData.getGroupVariable(matches[i], 'element')
            inputCovariance = testData.getGroupVariable(matches[i], 'inputCovariance')
            inputInverse = testData.getGroupVariable(matches[i], 'inputInverse')
            iE = int(element[0]);
            model = ConstantObservationErrorModel(inputCovariance, inputInverse);
            if (iE < 0) :
                Q = model.getCovarianceMatrix(None, 0.0, array([0]), iE);
                assert_almost_equal(inputCovariance, Q)
                Q = model.getPrecisionMatrix(None, 0.0, array([0]), iE);
                assert_almost_equal(inputInverse, Q)        
            else :
                Q = model.getCovarianceMatrix(None, 0.0, array([0]), iE);
                assert_almost_equal(inputCovariance[iE, iE], Q)
                Q = model.getPrecisionMatrix(None, 0.0, array([0]), iE);
                assert_almost_equal(inputInverse[iE, iE], Q)        
        testData.close()
    
    @testcase
    def xtestObservationDifferencesErrorModel(self):
        testData = TestData('launchRadar')
        group = testData.getGroup('7501')
        radars = ('launch_radar_1', 'launch_radar_2', 'launch_radar_3')
        for radar in radars :
            observations = testData.getArray(group, radar)
#             print(radar, observations.shape)
#             f = makeEmp(0, 0.1)
#             m = self.ManagedFilterBaseMock( f.getOrder(), f );
            model = ObservationDifferencesErrorModel(zeros([3,3]), 15 )
            for i in range(0, observations.shape[0]) :
                if (observations[i,4] == 2) :
                    C = model.getCovarianceMatrix(None, i, observations[i,9:12])
                    print(radar, i, A2S(sqrt(diag(C).flatten())))

    
    @testcase
    def xtest0FixedSampleErrorModel(self):
        testData = TestData('launchRadar')
        group = testData.getGroup('7501')
        radars = ('launch_radar_1', 'launch_radar_2', 'launch_radar_3')
        for radar in radars :
            observations = testData.getArray(group, radar)
            model = FixedSampleErrorModel(zeros([3,3]), 25, 10 )
            for i in range(0, observations.shape[0]) :
                if (observations[i,4] == 2) :
                    C = model.getCovarianceMatrix(None, observations[i,0], observations[i,9:12])
                    print(radar, i, A2S(sqrt(diag(C).flatten())))
        
    @testcase
    def xtest9FixedSampleErrorModel(self):
        N = 25;
        M = 10
        O = randn(N,2)
        Z = zeros([2,2])
        model = FixedSampleErrorModel(Z, N, M);
        for i in range(0,N) :
            Q = model.getCovarianceMatrix(None, i, O[i:i+1,:]);
            if (i < M) :
                assert_almost_equal(Z, Q)
            else :
                assert_almost_equal(cov(O[0:i+1], rowvar=False, bias=True), Q)


    @testcase
    def test0PairResidualsErrorModel(self):
        testData = TestData('launchRadar')
        group = testData.getGroup('7501')
        radars = ('launch_radar_1', 'launch_radar_2', 'launch_radar_3')
        order = 2
        for radar in radars :
            iFirst = 0;
            iLast = 0;
            observations = testData.getArray(group, radar)
            results = zeros([observations.shape[0], 4])
            model = PairResidualsErrorModel(zeros([3, 3]), 25, order, 0.1, 0.90 )
            for i in range(0, observations.shape[0]) :
                if (observations[i,4] == 2) :
                    C = model.getCovarianceMatrix(None, observations[i,0], observations[i,9:12])
                    iFirst = min(iFirst,iLast)
                    results[iLast,0] = observations[i,0]
                    results[iLast,1:] = sqrt(diag(C).flatten())
#                     print(radar, i, A2S(sqrt(diag(C).flatten())))
                    if (results[iLast,3] > 100.0) :
                        model.dump()
                    iLast += 1
                    
            f0 = plt.figure(figsize=(10, 6))
            ax = plt.subplot(1, 1, 1)
            ax.plot(results[iFirst:iLast,0], results[iFirst:iLast,3], 'k-', label='R')
            ax.legend()
            plt.title( '%s Order %d' % (radar, order))
            plt.show()
            print(radar, mean(results[iFirst:iLast,1:], axis=0))
            print(cov(results[iFirst:iLast,1:], rowvar=False))
#             return

    def xtest0PlotRanges(self):
        plotting = True
        betData = TestData('launchBET')
        betGroup = betData.getGroup('7501')
        bet = betData.getArray(betGroup, 'ECEF')
        testData = TestData('launchRadar')
        group = testData.getGroup('7501')
        FMT = 4469086562.0-1.3390
        order = 2
        radars = ('launch_radar_1', 'launch_radar_2', 'launch_radar_3')
        for radar in radars :
            iFirst = 0;
            iLast = 0;
            taer = betData.getArray(betGroup, radar)
            observations = testData.getArray(group, radar)
            observations[:,0] -= FMT
            if (plotting) :
                f0 = plt.figure(figsize=(10, 10))
                ax = plt.subplot(3, 1, 1)
                ax.plot(observations[:,0], observations[:,4], 'k-', label='Quality')
#             ax.plot(results[iFirst:iLast,0], results[iFirst:iLast,2], 'b.', label='O')
#             ax.legend()
#             plt.title( 'Order %d' % order)
#             plt.show()
            
            filter = makeEmp(order, 0.1 )
            filter = PairedPolynomialFilter(order, 0.1, 0.90)
#             filter = FixedMemoryFilter(order, 25)
            results = zeros([observations.shape[0], 2 + order+1])
            startTime = perf_counter();
#             for iBase in range(0, observations.shape[0]-25, 25) :
#                 filter.start(observations[iBase,0], observations[iBase,11:12])
#                 for iStep in range(0,25) :
#                     i = iBase + iStep
#                     if (observations[i,4] == 2) :
#                         filter.add( observations[i,0], observations[i,11])
#                         results[iLast,0] = observations[i,0]
#                         results[iLast,1] = observations[i,11]
#                         if (filter.getStatus() == FilterStatus.RUNNING and filter.getFirstVRF() < 0.5) :
#                             results[iLast,2:] = filter.getState()
#                             error = results[iLast,1] - results[iLast,2] 
#                             iLast += 1
            iBase = 0
            filter.start(observations[iBase,0], observations[iBase,11:12])
            startTime = perf_counter();
            for iStep in range(0,observations.shape[0]) :
                i = iBase + iStep
                if (iLast >= observations.shape[0]) :
                    break
                if (observations[i,0] > 500.0) :
                    break
                if (observations[i,0] < taer[0,0]) :
                    continue
                if (observations[i,4] == 2) :
                    filter.add( observations[i,0], observations[i,11])
                    results[iLast,0] = observations[i,0]
                    results[iLast,1] = observations[i,11]
                    if (filter.getStatus() == FilterStatus.RUNNING and filter.getFirstVRF() < 0.5) :
                        results[iLast,2:] = filter.getState()
                        error = results[iLast,1] - results[iLast,2] 
                        iLast += 1
            finishTime = perf_counter();
#             results[iLast,0] = observations[-1,0];
#             results[iLast,1:] = 0
#             iLast += 1       
#             f0 = plt.figure(figsize=(10, 6))
            iaer = zeros([iLast-iFirst,3])
            iaer[:,0] = interp(results[iFirst:iLast,0], taer[:,0], taer[:,1])
            iaer[:,1] = interp(results[iFirst:iLast,0], taer[:,0], taer[:,2])
            iaer[:,2] = interp(results[iFirst:iLast,0], taer[:,0], taer[:,3])
            if (plotting) :
                ax = plt.subplot(3, 1, 2)
                ax.plot(results[iFirst:iLast,0], results[iFirst:iLast,2], 'k.', label='R')
                ax.plot(taer[:,0], taer[:,3], 'b-', label='B')
    #             ax.plot(results[iFirst:iLast,0], results[iFirst:iLast,2], 'b.', label='O')
                ax.legend()
                ax = plt.subplot(3, 1, 3)
                ax.plot(results[iFirst:iLast,0], results[iFirst:iLast,2]-iaer[:,2], 'r-', label='R-B')
                plt.title( '%s Order %d' % (radar, order))
                plt.show()
            
            t0 = results[0,0]
#             print(0, ' Start ', t0)
#             n = 0
#             for i in range(1,iLast) :
#                 if ((results[i,0]-t0) > 0.19) :
#                     print( n, ' Gap from ', results[i-1,0], ' to  ',results[i,0])
#                 t0 = results[i,0]
#                 n += 1
#             print(iLast, ' Finish ', t0)
#             print(finishTime - startTime)
            d = results[iFirst:iLast,2]-iaer[:,2]
            print(radar, d[1000], d[3000], d[1000]-d[3000])
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()