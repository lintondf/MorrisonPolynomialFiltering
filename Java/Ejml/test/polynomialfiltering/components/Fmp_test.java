/***** /polynomialfiltering/components/Fmp_test/
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
import polynomialfiltering.filters.RecursivePolynomialFilter;
import static polynomialfiltering.components.Fmp.makeFmp;
import static polynomialfiltering.components.Emp.nSwitch;
import polynomialfiltering.components.ICore;
import static polynomialfiltering.components.Fmp.makeFmpCore;
import static polynomialfiltering.components.Emp.makeEmpCore;

 

/// Taus for full range valid thetas [2e-16, 1-2e-16]
///  	Gamma	{0: 1.1102230246251565e-16, 1: 1.651158036900312e-08, 2: 0.2898979485566357, 3: 0.4627475401696348, 4: 0.5697090329565893, 5: 0.6416277095878444}
///  	VRF	{0: 3.0518509447574615e-05, 1: 1.4142135623842478, 2: 2.5495097571983933, 3: 3.8369548115879297, 4: 5.583955190144479, 5: 8.241797269321978}
/// 
public class Fmp_test {
    
    @Test
    public void test1CheckStates () {
        TestData testData = new TestData();
        List<String> matches;
        int order;
        DMatrixRMaj setup = new DMatrixRMaj();
        Group states;
        List<String> cases;
        String caseName;
        Group caseGroup;
        double tau;
        double theta;
        DMatrixRMaj Y0 = new DMatrixRMaj();
        DMatrixRMaj times = new DMatrixRMaj();
        DMatrixRMaj observations = new DMatrixRMaj();
        DMatrixRMaj truth = new DMatrixRMaj();
        DMatrixRMaj expected = new DMatrixRMaj();
        DMatrixRMaj actual = new DMatrixRMaj();
        RecursivePolynomialFilter f = new RecursivePolynomialFilter();
        DMatrixRMaj Zstar = new DMatrixRMaj();
        double e;
        assert_clear();
        testData = new TestData("testFMP.nc");
        matches = testData.getMatchingGroups("States");
        assert_not_empty(matches);
        setup = testData.getGroupVariable(matches.get(0), "setup");
        states = testData.getGroup(matches.get(0));
        cases = testData.getMatchingGroups("Case_");
        for (int i = 0; i < numElements(cases); i++) {
            caseName = cases.get(i);
            caseGroup = testData.getGroup(caseName);
            order = testData.getInteger(caseGroup, "order");
            tau = testData.getScalar(caseGroup, "tau");
            theta = testData.getScalar(caseGroup, "theta");
            Y0 = testData.getArray(caseGroup, "Y0");
            times = testData.getArray(caseGroup, "times");
            observations = testData.getArray(caseGroup, "observations");
            truth = testData.getArray(caseGroup, "truth");
            expected = testData.getArray(caseGroup, "expected");
                        
            //  actual = zeros(times.getNumRows(), order + 1)
            actual.reshape(times.getNumRows(), order + 1);
            CommonOps_DDRM.fill( actual, 0.0 );
            f = makeFmp(order, tau, theta);
                        
            f.start(0.0, Y0);
            for (int j = 0; j < times.getNumRows(); j++) {
                                
                //  Zstar = f.predict(times(j, 0))
                double     td11 = times.get(j, 0);
                Zstar = f.predict(td11);
                                
                //  e = observations(j) - Zstar(0)
                double     td13 = observations.get(j);
                double     td14 = Zstar.get(0);
                e = td13 - td14;
                                
                //  f.update(times(j, 0), Zstar, e)
                double     td16 = times.get(j, 0);
                DMatrixRMaj tm17 = f.update(td16, Zstar, e);
                                
                //  actual(j,  : ) = transpose(f.getState())
                DMatrixRMaj tm19 = f.getState();
                DMatrixRMaj tm20 = new DMatrixRMaj(tm19.getNumCols(), tm19.getNumRows());
                CommonOps_DDRM.transpose( tm19, tm20 );
                CommonOps_DDRM.insert( tm20, actual, j, 0 );
            }
                        
            assert_almost_equal(actual, expected);
        }
        assertGreaterEqual(32.0, assert_report("Fmp_test/test1CheckStates"));
                
        testData.close();
    }
    
    
    @Test
    public void test1CheckGammas () {
        TestData testData = new TestData();
        List<String> matches;
        int order;
        DMatrixRMaj setup = new DMatrixRMaj();
        Group states;
        List<String> cases;
        String caseName;
        Group caseGroup;
        double tau;
        double theta;
        DMatrixRMaj Y0 = new DMatrixRMaj();
        DMatrixRMaj times = new DMatrixRMaj();
        DMatrixRMaj observations = new DMatrixRMaj();
        DMatrixRMaj truth = new DMatrixRMaj();
        DMatrixRMaj expectedG = new DMatrixRMaj();
        DMatrixRMaj actualG = new DMatrixRMaj();
        double nS;
        RecursivePolynomialFilter f = new RecursivePolynomialFilter();
        assert_clear();
        testData = new TestData("testFMP.nc");
        matches = testData.getMatchingGroups("Gammas");
        assert_not_empty(matches);
        states = testData.getGroup(matches.get(0));
        cases = testData.getMatchingGroups("Gammas_Case_");
        for (int i = 0; i < numElements(cases); i++) {
            caseName = cases.get(i);
            caseGroup = testData.getGroup(caseName);
            order = testData.getInteger(caseGroup, "order");
            tau = testData.getScalar(caseGroup, "tau");
            theta = testData.getScalar(caseGroup, "theta");
            nS = testData.getScalar(caseGroup, "nS");
            expectedG = testData.getArray(caseGroup, "G");
            f = makeFmp(order, tau, theta);
            actualG = f.getCore().getGamma(0, 1.0);
                        
            assert_almost_equal(nS, nSwitch(order, theta));
                        
            assert_almost_equal(actualG, expectedG);
        }
        assertGreaterEqual(0.0, assert_report("Fmp_test/test1CheckGammas"));
                
        testData.close();
    }
    
    
    @Test
    public void test1CheckVRF () {
        TestData testData = new TestData();
        List<String> matches;
        int order;
        DMatrixRMaj setup = new DMatrixRMaj();
        Group states;
        List<String> cases;
        String caseName;
        Group caseGroup;
        double tau;
        double theta;
        DMatrixRMaj Y0 = new DMatrixRMaj();
        DMatrixRMaj times = new DMatrixRMaj();
        DMatrixRMaj observations = new DMatrixRMaj();
        DMatrixRMaj truth = new DMatrixRMaj();
        DMatrixRMaj expectedV = new DMatrixRMaj();
        DMatrixRMaj actualV = new DMatrixRMaj();
        RecursivePolynomialFilter f = new RecursivePolynomialFilter();
        assert_clear();
        testData = new TestData("testFMP.nc");
        matches = testData.getMatchingGroups("Vrfs");
        assert_not_empty(matches);
        states = testData.getGroup(matches.get(0));
        cases = testData.getMatchingGroups("Vrfs_Case_");
        for (int i = 0; i < numElements(cases); i++) {
            caseName = cases.get(i);
            caseGroup = testData.getGroup(caseName);
            order = testData.getInteger(caseGroup, "order");
            tau = testData.getScalar(caseGroup, "tau");
            theta = testData.getScalar(caseGroup, "theta");
            expectedV = testData.getArray(caseGroup, "V");
            f = makeFmp(order, tau, theta);
            actualV = f.getCore().getVRF(0);
                        
            assert_almost_equal(actualV, expectedV);
        }
        assertGreaterEqual(1.0, assert_report("Fmp_test/test1CheckVrfs"));
                
        testData.close();
    }
    
    
    @Test
    public void test9CoreBasic () {
        ICore core90;
        ICore core95;
        ICore core95half;
        ICore core95double;
        DMatrixRMaj ad = new DMatrixRMaj();
        DMatrixRMaj ah = new DMatrixRMaj();
        assert_clear();
        core90 = makeFmpCore(3, 1.0, 0.90);
        core95 = makeFmpCore(3, 1.0, 0.95);
        core95half = makeFmpCore(3, 2.0, 0.95);
        core95double = makeFmpCore(3, 0.5, 0.95);
                
        //  assert_almost_equal(core90.getVRF(1), core90.getVRF(10))
        DMatrixRMaj tm9 = core90.getVRF(1);
        DMatrixRMaj tm10 = core90.getVRF(10);
        assert_almost_equal(tm9, tm10);
        assert_array_less(core95.getVRF(1), core90.getVRF(1));
                
        //  ad = (core95double.getVRF(1) ./ core95.getVRF(1))
        DMatrixRMaj tm12 = core95double.getVRF(1);
        DMatrixRMaj tm13 = core95.getVRF(1);
        ad.reshape( tm12.numRows, tm12.numCols );
        CommonOps_DDRM.elementDiv( tm12, tm13, ad );
                
        //  ah = (core95half.getVRF(1) ./ core95.getVRF(1))
        DMatrixRMaj tm15 = core95half.getVRF(1);
        DMatrixRMaj tm16 = core95.getVRF(1);
        ah.reshape( tm15.numRows, tm15.numCols );
        CommonOps_DDRM.elementDiv( tm15, tm16, ah );
                
        //  assert_almost_equal(ones(3 + 1, 3 + 1), ad .* ah)
        DMatrixRMaj tm20 = new DMatrixRMaj( 4, 4 );
        CommonOps_DDRM.fill( tm20, 1 );
        DMatrixRMaj tm21 = new DMatrixRMaj( ad.numRows, ad.numCols );
        CommonOps_DDRM.elementMult( ad, ah, tm21 );
        assert_almost_equal(tm20, tm21);
                
        //  assert_almost_equal(core90.getGamma(10.0, 5.0), core90.getGamma(11.0, 5.0))
        DMatrixRMaj tm23 = core90.getGamma(10.0, 5.0);
        DMatrixRMaj tm24 = core90.getGamma(11.0, 5.0);
        assert_almost_equal(tm23, tm24);
                
        //  assert_almost_equal(core90.getGamma(10.0, 5.0), core90.getGamma(10.0, 6.0))
        DMatrixRMaj tm26 = core90.getGamma(10.0, 5.0);
        DMatrixRMaj tm27 = core90.getGamma(10.0, 6.0);
        assert_almost_equal(tm26, tm27);
                
        //  assert_almost_equal(core95.getGamma(10.0, 5.0), core95half.getGamma(10.0, 5.0))
        DMatrixRMaj tm29 = core95.getGamma(10.0, 5.0);
        DMatrixRMaj tm30 = core95half.getGamma(10.0, 5.0);
        assert_almost_equal(tm29, tm30);
                
        //  assert_almost_equal(core95.getGamma(10.0, 5.0), core95double.getGamma(10.0, 5.0))
        DMatrixRMaj tm32 = core95.getGamma(10.0, 5.0);
        DMatrixRMaj tm33 = core95double.getGamma(10.0, 5.0);
        assert_almost_equal(tm32, tm33);
        assert_report("Fmp_test/test9CoreBasic");
    }
    
    
    @Test
    public void test9Basic () {
        int order;
        double tau;
        double theta;
        DMatrixRMaj Y0 = new DMatrixRMaj();
        DMatrixRMaj observations = new DMatrixRMaj();
        RecursivePolynomialFilter f = new RecursivePolynomialFilter();
        double t;
        DMatrixRMaj Zstar = new DMatrixRMaj();
        double e;
        DMatrixRMaj actual = new DMatrixRMaj();
        assert_clear();
                
        order = 5;
                
        tau = 0.01;
                
        theta = 0.9885155283985784;
                
        //  actual = zeros(order + 1, 1)
        actual.reshape(order + 1, 1);
        CommonOps_DDRM.fill( actual, 0.0 );
        Y0 = (new DMatrixRMaj(new double[] { - 5.373000000000E+00,  - 1.125200000000E+01,  - 1.740600000000E+01,  - 1.565700000000E+01,  - 7.458400000000E+00,  - 1.467800000000E+00}));
        observations = (new DMatrixRMaj(new double[] { - 5.2565E+00,  - 2.8652E+00,  - 1.4812E+01, 4.6590E+00, 4.7380E+00,  - 7.3765E+00, 1.3271E+01, 7.3593E+00, 3.4308E+00,  - 1.1329E+00,  - 1.5789E+00}));
        f = makeFmp(order, tau, theta);
                
        f.start(0.0, Y0);
                
        t = 0;
                
        Zstar = f.predict(t);
        assert_almost_equal(Zstar, (new DMatrixRMaj(new double[] { - 5.373000000000E+00,  - 1.125200000000E-01,  - 1.740600000000E-03,  - 1.565700000000E-05,  - 7.458400000000E-08,  - 1.467800000000E-10})));
                
        //  e = observations(0) - Zstar(0)
        double     td7 = observations.get(0);
        double     td8 = Zstar.get(0);
        e = td7 - td8;
                
        assert_almost_equal(e, 0.11650000000000027);
                
        actual = f.update(t, Zstar, e);
        assert_almost_equal(actual, (new DMatrixRMaj(new double[] {7.800661521666E-03, 2.252446577781E-04, 3.468911273583E-06, 3.005115515478E-08, 1.388453238252E-10, 2.672957382342E-13})));
                
        actual = f.getState();
        assert_almost_equal(actual, (new DMatrixRMaj(new double[] { - 5.365199338478335,  - 11.229475534222193,  - 17.37131088726417,  - 15.62694884484522,  - 7.444515467617483,  - 1.4651270426176584})));
        t += 0.01;
                
        Zstar = f.predict(t);
        assert_almost_equal(Zstar, (new DMatrixRMaj(new double[] { - 5.47836527e+00,  - 1.14039712e-01,  - 1.75279528e-03,  - 1.57014673e-05,  - 7.45916674e-08,  - 1.46512704e-10})));
                
        //  e = observations(1) - Zstar(0)
        double     td14 = observations.get(1);
        double     td15 = Zstar.get(0);
        e = td14 - td15;
                
        assert_almost_equal(e, 2.6131652669594962);
                
        DMatrixRMaj tm18 = f.update(t, Zstar, e);
                
        actual = f.getState();
        assert_almost_equal(actual, (new DMatrixRMaj(new double[] { - 5.30339172,  - 10.89873388,  - 16.74985512,  - 15.02740172,  - 7.1477283,  - 1.405171})));
        assertGreaterEqual(24.5, assert_report("Fmp_test/test9Basic"));
    }
    
    
    @Test
    public void test9NSwitch () {
        ICore emp;
        ICore fmp;
        double tau;
        DMatrixRMaj taus = new DMatrixRMaj();
        double theta;
        DMatrixRMaj thetas = new DMatrixRMaj();
        int n;
        int nThetas;
        int nTaus;
        assert_clear();
        taus = (new DMatrixRMaj(new double[] {0.01, 0.1, 1., 10., 100.}));
                
        nTaus = taus.getNumElements();
        thetas = (new DMatrixRMaj(new double[] {0.90, 0.95, 0.99, 0.999}));
                
        nThetas = thetas.getNumElements();
        for (int order = 0; order < 5 + 1; order++) {
            for (int itheta = 0; itheta < nThetas; itheta++) {
                                
                theta = thetas.get(itheta);
                for (int itau = 0; itau < nTaus; itau++) {
                                        
                    tau = taus.get(itau);
                    emp = makeEmpCore(order, tau);
                    fmp = makeFmpCore(order, tau, theta);
                                        
                    n = (int) nSwitch(order, theta);
                }
            }
        }
    }
    
} // class Fmp_test

