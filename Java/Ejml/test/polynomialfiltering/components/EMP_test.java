/***** /polynomialfiltering/components/EMP_test/
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
import polynomialfiltering.components.RecursivePolynomialFilter;
import polynomialfiltering.components.ICore;
import polynomialfiltering.components.EMP_test.RecursivePolynomialFilterMock;
import static polynomialfiltering.components.Emp.makeEmp;
import static polynomialfiltering.components.Emp.nUnitLastVRF;
import static polynomialfiltering.components.Emp.makeEmpCore;
import static polynomialfiltering.components.Emp.nSwitch;

 
public class EMP_test {
    public static class RecursivePolynomialFilterMock extends RecursivePolynomialFilter {
        
        public RecursivePolynomialFilterMock() {}  // auto-generated null constructor

        
        public RecursivePolynomialFilterMock (final int order, final double tau, final ICore core) {
            super(order,tau,core);
        }
        
        
        public void setN (final int n) {
                        
            this.n = n;
        }
        
    } // class RecursivePolynomialFilterMock
    
    
    @Test
    public void test1CheckVRF () {
        TestData testData = new TestData();
        List<String> matches;
        DMatrixRMaj setup = new DMatrixRMaj();
        int N;
        DMatrixRMaj taus = new DMatrixRMaj();
        int nTaus;
        DMatrixRMaj expected = new DMatrixRMaj();
        int offset;
        double tau;
        ICore core;
        RecursivePolynomialFilter rf = new RecursivePolynomialFilter();
        RecursivePolynomialFilterMock f = new RecursivePolynomialFilterMock();
        DMatrixRMaj V = new DMatrixRMaj();
        DMatrixRMaj E = new DMatrixRMaj();
        assert_clear();
        testData = new TestData("testEMP.nc");
        matches = testData.getMatchingGroups("VRF_");
        assert_not_empty(matches);
        for (int order = 0; order < numElements(matches); order++) {
            setup = testData.getGroupVariable(matches.get(order), "setup");
                        
            //  N = int(setup(0))
            double     td2 = setup.get(0);
            N = (int) td2;
            taus = testData.getGroupVariable(matches.get(order), "taus");
            expected = testData.getGroupVariable(matches.get(order), "expected");
                        
            offset = 0;
                        
            nTaus = taus.getNumElements();
            for (int itau = 0; itau < nTaus; itau++) {
                                
                tau = taus.get(itau);
                rf = Emp.makeEmp(order, tau);
                f = new RecursivePolynomialFilterMock(order, tau, rf.getCore());
                for (int iN = order + 1; iN < N; iN++) {
                                        
                    f.setN(iN + 0);
                                        
                    V = f.getVRF();
                                        
                    //  E = expected(offset : (offset + order + 1-1),  : )
                    E.reshape( (((offset+order+1)+0)-offset), ((expected.numCols)-0) );
                    CommonOps_DDRM.extract( expected, offset, (offset+order+1)+0, 0, expected.numCols, E );
                                        
                    assert_almost_equal(V, E);
                    offset += order + 1;
                }
            }
        }
                
        testData.close();
        assertGreaterEqual(0.0, assert_report("Emp_test/test1CheckVRF"));
    }
    
    
    @Test
    public void test2CheckStates () {
        TestData testData = new TestData();
        List<String> matches;
        int order;
        DMatrixRMaj setup = new DMatrixRMaj();
        DMatrixRMaj taus = new DMatrixRMaj();
        DMatrixRMaj expected = new DMatrixRMaj();
        DMatrixRMaj actual = new DMatrixRMaj();
        DMatrixRMaj times = new DMatrixRMaj();
        DMatrixRMaj observations = new DMatrixRMaj();
        DMatrixRMaj Zstar = new DMatrixRMaj();
        DMatrixRMaj diff = new DMatrixRMaj();
        double tau;
        ICore core;
        RecursivePolynomialFilter f = new RecursivePolynomialFilter();
        double e;
        assert_clear();
        testData = new TestData("testEMP.nc");
        matches = testData.getMatchingGroups("States");
        assert_not_empty(matches);
        setup = testData.getGroupVariable(matches.get(0), "setup");
        matches = testData.getMatchingGroups("States_Case_");
        assert_not_empty(matches);
        for (int i = 0; i < numElements(matches); i++) {
                        
            //  order = int(setup(i, 0))
            double     td2 = setup.get(i, 0);
            order = (int) td2;
                        
            tau = setup.get(i, 1);
            times = testData.getGroupVariable(matches.get(i), "times");
            observations = testData.getGroupVariable(matches.get(i), "observations");
            expected = testData.getGroupVariable(matches.get(i), "expected");
                        
            //  actual = zeros(expected.getNumRows(), expected.getNumCols())
            actual.reshape(expected.getNumRows(), expected.getNumCols());
            CommonOps_DDRM.fill( actual, 0.0 );
            f = Emp.makeEmp(order, tau);
                        
            //  f.start(0.0, expected(0,  : ))
            DMatrixRMaj tm10 = new DMatrixRMaj( 1, ((expected.numCols)-0) );
            CommonOps_DDRM.extract( expected, 0, 1, 0, expected.numCols, tm10 );
            f.start(0.0, tm10);
            for (int j = 0; j < times.getNumRows(); j++) {
                                
                //  Zstar = f.predict(times(j, 0))
                double     td15 = times.get(j, 0);
                Zstar = f.predict(td15);
                                
                //  e = observations(j) - Zstar(0)
                double     td17 = observations.get(j);
                double     td18 = Zstar.get(0);
                e = td17 - td18;
                                
                //  f.update(times(j, 0), Zstar, e)
                double     td20 = times.get(j, 0);
                DMatrixRMaj tm21 = f.update(td20, Zstar, e);
                                
                //  actual(j,  : ) = transpose(f.getState())
                DMatrixRMaj tm23 = f.getState();
                DMatrixRMaj tm24 = new DMatrixRMaj(tm23.getNumCols(), tm23.getNumRows());
                CommonOps_DDRM.transpose( tm23, tm24 );
                CommonOps_DDRM.insert( tm24, actual, j, 0 );
            }
                        
            assert_almost_equal(actual, expected);
        }
                
        testData.close();
        assertGreaterEqual(29.2, assert_report("Emp_test/test2CheckStates"));
    }
    
    
    @Test
    public void test9NUnitLastVRF () {
        ICore core;
        double tau;
        DMatrixRMaj taus = new DMatrixRMaj();
        int nTaus;
        int n;
        taus = (new DMatrixRMaj(new double[] {0.01, 0.1, 1., 10., 100.}));
        for (int order = 0; order < 5 + 1; order++) {
                        
            nTaus = taus.getNumElements();
            for (int itau = 0; itau < nTaus; itau++) {
                                
                tau = taus.get(itau);
                                
                n = Emp.nUnitLastVRF(order, tau);
                core = Emp.makeEmpCore(order, tau);
            }
        }
    }
    
    
    @Test
    public void test9Coverage () {
        assertEqual(0.0, Emp.nSwitch(0, 2.0));
    }
    
} // class EMP_test

