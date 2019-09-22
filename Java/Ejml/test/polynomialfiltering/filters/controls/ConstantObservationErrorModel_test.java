/***** /polynomialfiltering/filters/controls/ConstantObservationErrorModel_test/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED Java from Python Reference Implementation
 */

package polynomialfiltering.filters.controls;
 
import org.junit.Test;
import java.util.List;
import org.ejml.data.DMatrixRMaj;
import org.ejml.dense.row.CommonOps_DDRM;
import polynomialfiltering.main.FilterStatus;
import static polynomialfiltering.main.Utility.*;
import utility.TestData;
import ucar.nc2.Group;
import static utility.TestMain.*;
import polynomialfiltering.filters.controls.ConstantObservationErrorModel;

 
public class ConstantObservationErrorModel_test {
    
    @Test
    public void test1Scalar () {
        TestData testData = new TestData();
        List<String> matches;
        int iE;
        DMatrixRMaj inputCovariance = new DMatrixRMaj();
        DMatrixRMaj inputInverse = new DMatrixRMaj();
        DMatrixRMaj element = new DMatrixRMaj();
        double x;
        DMatrixRMaj Q = new DMatrixRMaj();
        ConstantObservationErrorModel model = new ConstantObservationErrorModel();
        testData = new TestData("testConstantObservationErrorModel.nc");
        matches = testData.getMatchingGroups("testScalar_");
        assert_not_empty(matches);
        for (int i = 0; i < numElements(matches); i++) {
            element = testData.getGroupVariable(matches.get(i), "element");
            inputCovariance = testData.getGroupVariable(matches.get(i), "inputCovariance");
            inputInverse = testData.getGroupVariable(matches.get(i), "inputInverse");
                        
            //  iE = int(element(0))
            double     td2 = element.get(0);
            iE = (int) td2;
                        
            x = inputCovariance.get(0, 0);
            model = new ConstantObservationErrorModel(x);
            Q = model.getCovarianceMatrix(null, 0.0, (new DMatrixRMaj(new double[] {0.})), iE);
                        
            //  assert_almost_equal(inputCovariance(0, 0), Q)
            double     td5 = inputCovariance.get(0, 0);
            assert_almost_equal(td5, Q);
            Q = model.getPrecisionMatrix(null, 0.0, (new DMatrixRMaj(new double[] {0.})), iE);
                        
            //  assert_almost_equal(inputInverse(0, 0), Q)
            double     td7 = inputInverse.get(0, 0);
            assert_almost_equal(td7, Q);
        }
                
        testData.close();
    }
    
    
    @Test
    public void test2Matrix () {
        TestData testData = new TestData();
        List<String> matches;
        int iE;
        DMatrixRMaj inputCovariance = new DMatrixRMaj();
        double ic;
        DMatrixRMaj inputInverse = new DMatrixRMaj();
        DMatrixRMaj element = new DMatrixRMaj();
        DMatrixRMaj Q = new DMatrixRMaj();
        ConstantObservationErrorModel model = new ConstantObservationErrorModel();
        testData = new TestData("testConstantObservationErrorModel.nc");
        matches = testData.getMatchingGroups("testMatrix_");
        assert_not_empty(matches);
        for (int i = 0; i < numElements(matches); i++) {
            element = testData.getGroupVariable(matches.get(i), "element");
            inputCovariance = testData.getGroupVariable(matches.get(i), "inputCovariance");
            inputInverse = testData.getGroupVariable(matches.get(i), "inputInverse");
                        
            //  iE = int(element(0))
            double     td2 = element.get(0);
            iE = (int) td2;
                        
            ic = inputCovariance.get(0, 0);
            model = new ConstantObservationErrorModel(ic);
            Q = model.getCovarianceMatrix(null, 0.0, (new DMatrixRMaj(new double[] {0.})), iE);
                        
            //  assert_almost_equal(inputCovariance(0, 0), Q)
            double     td5 = inputCovariance.get(0, 0);
            assert_almost_equal(td5, Q);
            Q = model.getPrecisionMatrix(null, 0.0, (new DMatrixRMaj(new double[] {0.})), iE);
                        
            //  assert_almost_equal(inputInverse(0, 0), Q)
            double     td7 = inputInverse.get(0, 0);
            assert_almost_equal(td7, Q);
        }
                
        testData.close();
    }
    
    
    @Test
    public void test3MatrixMatrix () {
        TestData testData = new TestData();
        List<String> matches;
        int iE;
        DMatrixRMaj inputCovariance = new DMatrixRMaj();
        DMatrixRMaj inputInverse = new DMatrixRMaj();
        DMatrixRMaj element = new DMatrixRMaj();
        DMatrixRMaj Q = new DMatrixRMaj();
        ConstantObservationErrorModel model = new ConstantObservationErrorModel();
        testData = new TestData("testConstantObservationErrorModel.nc");
        matches = testData.getMatchingGroups("testMatrixMatrix_");
        assert_not_empty(matches);
        for (int i = 0; i < numElements(matches); i++) {
            element = testData.getGroupVariable(matches.get(i), "element");
            inputCovariance = testData.getGroupVariable(matches.get(i), "inputCovariance");
            inputInverse = testData.getGroupVariable(matches.get(i), "inputInverse");
                        
            //  iE = int(element(0))
            double     td2 = element.get(0);
            iE = (int) td2;
            model = new ConstantObservationErrorModel(inputCovariance, inputInverse);
            if (iE < 0) {
                Q = model.getCovarianceMatrix(null, 0.0, (new DMatrixRMaj(new double[] {0.})), iE);
                                
                assert_almost_equal(inputCovariance, Q);
                Q = model.getPrecisionMatrix(null, 0.0, (new DMatrixRMaj(new double[] {0.})), iE);
                                
                assert_almost_equal(inputInverse, Q);
            } else {
                Q = model.getCovarianceMatrix(null, 0.0, (new DMatrixRMaj(new double[] {0.})), iE);
                                
                //  assert_almost_equal(inputCovariance(iE, iE), Q)
                double     td6 = inputCovariance.get(iE, iE);
                assert_almost_equal(td6, Q);
                Q = model.getPrecisionMatrix(null, 0.0, (new DMatrixRMaj(new double[] {0.})), iE);
                                
                //  assert_almost_equal(inputInverse(iE, iE), Q)
                double     td8 = inputInverse.get(iE, iE);
                assert_almost_equal(td8, Q);
            }
        }
                
        testData.close();
    }
    
} // class ConstantObservationErrorModel_test

