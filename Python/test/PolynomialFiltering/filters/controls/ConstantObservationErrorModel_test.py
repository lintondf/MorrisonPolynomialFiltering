'''
Created on Apr 11, 2019

@author: NOOK
'''
import unittest
from numpy import cov
from numpy.linalg import inv
from numpy.random import randn
from numpy.testing import assert_almost_equal
from netCDF4 import Dataset
from TestUtilities import *
from TestSuite import testDataPath;
from PolynomialFiltering.filters.controls.ConstantObservationErrorModel import ConstantObservationErrorModel
from PolynomialFiltering.PythonUtilities import ignore, testcase
from TestData import TestData

class TestConstantObservationErrorModel(unittest.TestCase):
    '''@cdf : Dataset'''
    cdf = None;

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

    def test0Generate(self):
        '''@path : str'''
        '''@cdf : Dataset'''
        '''@iTest : int'''
        '''@e : int'''
        '''@group : Dataset'''
        '''@inputCovariance : array'''
        '''@inputInverse : array'''
        '''@element : vector'''
        path = testDataPath('testConstantObservationErrorModel.nc');
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
    def test1Scalar(self):
        testData = TestData.make('testConstantObservationErrorModel.nc')
        matches = testData.getMatchingGroups('testScalar_')
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
    def test2Matrix(self):
        testData = TestData.make('testConstantObservationErrorModel.nc')
        matches = testData.getMatchingGroups('testMatrix_')
        for i in range(0, len(matches)) :
            element = testData.getGroupVariable(matches[i], 'element')
            inputCovariance = testData.getGroupVariable(matches[i], 'inputCovariance')
            inputInverse = testData.getGroupVariable(matches[i], 'inputInverse')
            iE = int(element[0]);
            model = ConstantObservationErrorModel(inputCovariance[0,0]);
            Q = model.getCovarianceMatrix(None, 0.0, array([0]), iE);
            assert_almost_equal(inputCovariance[0,0], Q)
            Q = model.getPrecisionMatrix(None, 0.0, array([0]), iE);
            assert_almost_equal(inputInverse[0,0], Q)        
        testData.close()

    @testcase
    def test3MatrixMatrix(self):
        testData = TestData.make('testConstantObservationErrorModel.nc')
        matches = testData.getMatchingGroups('testMatrixMatrix_')
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

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testConstantObservationErrorModel']
    unittest.main()