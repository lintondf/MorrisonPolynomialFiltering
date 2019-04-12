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
from PolynomialFiltering.PythonUtilities import ignore

class TestConstantObservationErrorModel(unittest.TestCase):

    cdf = None;

    @classmethod
    def setUpClass(cls):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        pass


    def tearDown(self):
        pass

    @ignore
    def test0Generate(self):
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
            writeTestVariable(group, 'outputCovariance', Q)
            Q = model.getPrecisionMatrix(None, 0.0, array([0]), -1);
            assert_almost_equal(inputInverse[0,0], Q)
            writeTestVariable(group, 'outputInverse', Q)

        for e in [-1, 0] :
            group = createTestGroup(cdf, 'testScalar_%d' % iTest );
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
            writeTestVariable(group, 'outputCovariance', Q)
            Q = model.getPrecisionMatrix(None, 0.0, array([0]), -1);
            assert_almost_equal(inputInverse[0,0], Q)
            writeTestVariable(group, 'outputInverse', Q)

        for e in [-1, 0, 1, 2] :
            group = createTestGroup(cdf, 'testScalar_%d' % iTest );
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
                writeTestVariable(group, 'outputCovariance', Q)
                Q = model.getPrecisionMatrix(None, 0.0, array([0]), iE);
                assert_almost_equal(inputInverse, Q)
                writeTestVariable(group, 'outputInverse', Q)
            else :
                Q = model.getCovarianceMatrix(None, 0.0, array([0]), iE);
                assert_almost_equal(inputCovariance[iE,iE], Q)
                writeTestVariable(group, 'outputCovariance', Q)
                Q = model.getPrecisionMatrix(None, 0.0, array([0]), iE);
                assert_almost_equal(inputInverse[iE,iE], Q)
                writeTestVariable(group, 'outputInverse', Q)
        cdf.close();

    def test1Check(self):
        path = testDataPath('testConstantObservationErrorModel.nc');
        cdf = Dataset(path, "r", format="NETCDF4");
        group = cdf.groups['testConstantObservationErrorModel'];
        print(group.variables["input_0"][:]);
        cdf.close();
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testConstantObservationErrorModel']
    unittest.main()