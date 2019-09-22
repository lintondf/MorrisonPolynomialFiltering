/***** /polynomialfiltering/components/Pair_test/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED Java from Python Reference Implementation
 */

package polynomialfiltering.components;
 
import org.junit.Test;
import java.util.List;
import org.ejml.data.DMatrixRMaj;
import org.ejml.dense.row.CommonOps_DDRM;
import polynomialfiltering.main.FilterStatus;
import static polynomialfiltering.main.Utility.*;
import utility.TestData;
import ucar.nc2.Group;
import static utility.TestMain.*;
import polynomialfiltering.components.PairedPolynomialFilter;
import org.ejml.dense.row.MatrixFeatures_DDRM;

 
public class Pair_test {
    
    @Test
    public void test2CheckStates () {
        TestData testData = new TestData();
        Group states;
        Group caseGroup;
        List<String> matches;
        int order;
        double tau;
        double theta;
        int nS;
        int N;
        DMatrixRMaj times = new DMatrixRMaj();
        DMatrixRMaj observations = new DMatrixRMaj();
        DMatrixRMaj expectedStates = new DMatrixRMaj();
        DMatrixRMaj expectedVdiag = new DMatrixRMaj();
        DMatrixRMaj actual = new DMatrixRMaj();
        DMatrixRMaj vdiags = new DMatrixRMaj();
        PairedPolynomialFilter f = new PairedPolynomialFilter();
        DMatrixRMaj Zstar = new DMatrixRMaj();
        DMatrixRMaj diff = new DMatrixRMaj();
        double e;
        assert_clear();
        testData = new TestData("testPair.nc");
        states = testData.getGroup("States");
        matches = testData.getMatchingSubGroups(states, "Case_");
        assert_not_empty(matches);
        for (int i = 0; i < numElements(matches); i++) {
            caseGroup = testData.getSubGroup(states, matches.get(i));
            order = testData.getInteger(caseGroup, "order");
            tau = testData.getScalar(caseGroup, "tau");
            theta = testData.getScalar(caseGroup, "theta");
            nS = testData.getInteger(caseGroup, "nS");
            N = testData.getInteger(caseGroup, "N");
            times = testData.getArray(caseGroup, "times");
            observations = testData.getArray(caseGroup, "observations");
            expectedStates = testData.getArray(caseGroup, "expected");
            expectedVdiag = testData.getArray(caseGroup, "vdiags");
            f = new PairedPolynomialFilter(order, tau, theta);
                        
            //  actual = zeros(N, order + 1)
            actual.reshape(N, order + 1);
            CommonOps_DDRM.fill( actual, 0.0 );
                        
            //  vdiags = zeros(N, order + 1)
            vdiags.reshape(N, order + 1);
            CommonOps_DDRM.fill( vdiags, 0.0 );
            for (int j = 0; j < N; j++) {
                                
                //  Zstar = f.predict(times(j, 0))
                double     td8 = times.get(j, 0);
                Zstar = f.predict(td8);
                                
                //  e = observations(j) - Zstar(0)
                double     td10 = observations.get(j);
                double     td11 = Zstar.get(0);
                e = td10 - td11;
                                
                //  f.update(times(j, 0), Zstar, e)
                double     td13 = times.get(j, 0);
                DMatrixRMaj tm14 = f.update(td13, Zstar, e);
                                
                //  actual(j,  : ) = transpose(f.getState())
                DMatrixRMaj tm16 = f.getState();
                DMatrixRMaj tm17 = new DMatrixRMaj(tm16.getNumCols(), tm16.getNumRows());
                CommonOps_DDRM.transpose( tm16, tm17 );
                CommonOps_DDRM.insert( tm17, actual, j, 0 );
                                
                //  vdiags(j,  : ) = transpose(diag(f.getVRF()))
                DMatrixRMaj tm18 = f.getVRF();
                DMatrixRMaj tm19 = new DMatrixRMaj( tm18.numRows, tm18.numRows );
                if (MatrixFeatures_DDRM.isVector(tm18)) { //;
                	CommonOps_DDRM.diag(tm19, tm18.numRows, tm18.data);
                } else { //;
                	tm19.reshape( tm18.numRows, 1 );
                	CommonOps_DDRM.extractDiag(tm18, tm19);
                }//;
                tm18.reshape( tm19.numCols, tm19.numRows );
                CommonOps_DDRM.transpose( tm19, tm18 );
                CommonOps_DDRM.insert( tm18, vdiags, j, 0 );
            }
                        
            assert_almost_equal(actual, expectedStates);
                        
            assert_almost_equal(vdiags, expectedVdiag);
        }
                
        testData.close();
        assertGreaterEqual(38.0, assert_report("Pair_test/test2CheckStates"));
    }
    
    
    @Test
    public void test9Coverage () {
        PairedPolynomialFilter f = new PairedPolynomialFilter();
        DMatrixRMaj Zstar = new DMatrixRMaj();
        f = new PairedPolynomialFilter(0, 1.0, 0.5);
        f.start(0.0, (new DMatrixRMaj(new double[] {10.})));
        assertEqual(0.0, f.getTime());
        assert_almost_equal(f.getState(), (new DMatrixRMaj(new double[] {10.})));
        assertFalse(f.isFading());
        for (int t = 1; t < 1 + 3; t++) {
                        
            Zstar = f.predict(t);
                        
            DMatrixRMaj tm5 = f.update(t, Zstar, 0.0);
            assertFalse(f.isFading());
        }
                
        Zstar = f.predict(4);
                
        DMatrixRMaj tm8 = f.update(4, Zstar, 0.0);
        assertTrue(f.isFading());
    }
    
} // class Pair_test

