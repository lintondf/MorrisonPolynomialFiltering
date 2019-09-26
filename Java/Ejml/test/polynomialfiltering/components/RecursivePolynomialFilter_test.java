/***** /polynomialfiltering/components/RecursivePolynomialFilter_test/
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
import polynomialfiltering.components.ICore;
import polynomialfiltering.filters.RecursivePolynomialFilter;

 

///// @class RecursivePolynomialFilter_test
/// @brief  PureObservationCore ignores predictions producing a results solely from the observation update
public class RecursivePolynomialFilter_test {
    public static class PurePredictCore extends ICore {
        protected  int order;
        
        public PurePredictCore() {}  // auto-generated null constructor

        
        public PurePredictCore (final int order) {
                        
            this.order = order;
        }
        
        
        public int getSamplesToStart () {
            return 1;
        }
        
        
        public DMatrixRMaj getGamma (final double t, final double dtau) {
            DMatrixRMaj g = new DMatrixRMaj();
                        
            //  g = zeros(this.order + 1)
            g.reshape(this.order + 1, 1);
            CommonOps_DDRM.fill( g, 0.0 );
            return g;
        }
        
        
        public DMatrixRMaj getVRF (final int n) {
            DMatrixRMaj Z = new DMatrixRMaj();
                        
            //  Z = zeros(this.order + 1, this.order + 1)
            Z.reshape(this.order + 1, this.order + 1);
            CommonOps_DDRM.fill( Z, 0.0 );
            return Z;
        }
        
        
        public double getFirstVRF (final int n) {
            return 0.0;
        }
        
        
        public double getLastVRF (final int n) {
            return 0.0;
        }
        
    } // class PurePredictCore
    
    public static class PureObservationCore extends ICore {
        protected  int order;
        
        public PureObservationCore() {}  // auto-generated null constructor

        
        public PureObservationCore (final int order) {
                        
            this.order = order;
        }
        
        
        public int getSamplesToStart () {
            return 2;
        }
        
        
        public DMatrixRMaj getGamma (final double t, final double dtau) {
            DMatrixRMaj g = new DMatrixRMaj();
                        
            //  g = 1.0 + zeros(this.order + 1)
            DMatrixRMaj tm2 = new DMatrixRMaj(this.order + 1, 1);
            CommonOps_DDRM.fill( tm2, 0.0 );
            g.reshape( tm2.numRows, tm2.numCols );
            CommonOps_DDRM.add( tm2, 1.0, g );
            return g;
        }
        
        
        public DMatrixRMaj getVRF (final int n) {
            DMatrixRMaj Z = new DMatrixRMaj();
                        
            //  Z = zeros(this.order + 1, this.order + 1)
            Z.reshape(this.order + 1, this.order + 1);
            CommonOps_DDRM.fill( Z, 0.0 );
            return Z;
        }
        
        
        public double getFirstVRF (final int n) {
            return 0.0;
        }
        
        
        public double getLastVRF (final int n) {
            return 0.0;
        }
        
    } // class PureObservationCore
    
    
    @Test
    public void test1PurePredict () {
        TestData testData = new TestData();
        List<String> matches;
        int N;
        int order;
        double tau;
        DMatrixRMaj setup = new DMatrixRMaj();
        DMatrixRMaj times = new DMatrixRMaj();
        DMatrixRMaj truth = new DMatrixRMaj();
        DMatrixRMaj observations = new DMatrixRMaj();
        DMatrixRMaj actual = new DMatrixRMaj();
        DMatrixRMaj expected = new DMatrixRMaj();
        ICore core;
        RecursivePolynomialFilter f = new RecursivePolynomialFilter();
        DMatrixRMaj Zstar = new DMatrixRMaj();
        double e;
        DMatrixRMaj V = new DMatrixRMaj();
        assert_clear();
        testData = new TestData("testRecursivePolynomialFilter.nc");
        matches = testData.getMatchingGroups("testPurePredict_");
        assert_not_empty(matches);
        for (int iMatch = 0; iMatch < numElements(matches); iMatch++) {
            setup = testData.getGroupVariable(matches.get(iMatch), "setup");
            times = testData.getGroupVariable(matches.get(iMatch), "times");
            truth = testData.getGroupVariable(matches.get(iMatch), "truth");
            observations = testData.getGroupVariable(matches.get(iMatch), "observations");
                        
            //  N = int(setup(0))
            double     td2 = setup.get(0);
            N = (int) td2;
                        
            //  order = int(setup(1))
            double     td4 = setup.get(1);
            order = (int) td4;
                        
            tau = setup.get(2);
                        
            //  actual = zeros(N, order + 1)
            actual.reshape(N, order + 1);
            CommonOps_DDRM.fill( actual, 0.0 );
                        
            //  actual(0,  : ) = truth(0,  : )
            DMatrixRMaj tm9 = new DMatrixRMaj( 1, ((truth.numCols)-0) );
            CommonOps_DDRM.extract( truth, 0, 1, 0, truth.numCols, tm9 );
            CommonOps_DDRM.insert( tm9, actual, 0, 0 );
            core = new PurePredictCore(order);
            f = new RecursivePolynomialFilter(order, tau, core);
                        
            //  f.start(times(0), truth(0,  : ))
            double     td10 = times.get(0);
            DMatrixRMaj tm11 = new DMatrixRMaj( 1, ((truth.numCols)-0) );
            CommonOps_DDRM.extract( truth, 0, 1, 0, truth.numCols, tm11 );
            f.start(td10, tm11);
            for (int i = 1; i < N; i++) {
                                
                //  Zstar = f.predict(times(i))
                double     td15 = times.get(i);
                Zstar = f.predict(td15);
                                
                //  e = observations(i) - Zstar(0)
                double     td17 = observations.get(i);
                double     td18 = Zstar.get(0);
                e = td17 - td18;
                                
                //  f.update(times(i), Zstar, e)
                double     td20 = times.get(i);
                DMatrixRMaj tm21 = f.update(td20, Zstar, e);
                                
                //  actual(i,  : ) = transpose(f.getState())
                DMatrixRMaj tm23 = f.getState();
                DMatrixRMaj tm24 = new DMatrixRMaj(tm23.getNumCols(), tm23.getNumRows());
                CommonOps_DDRM.transpose( tm23, tm24 );
                CommonOps_DDRM.insert( tm24, actual, i, 0 );
                                
                V = f.getVRF();
                                
                //  assert_almost_equal(V, zeros(order + 1, order + 1))
                DMatrixRMaj tm28 = new DMatrixRMaj(order + 1, order + 1);
                CommonOps_DDRM.fill( tm28, 0.0 );
                assert_almost_equal(V, tm28);
            }
            expected = testData.getGroupVariable(matches.get(iMatch), "expected");
                        
            assert_almost_equal(actual, expected);
        }
        assertGreaterEqual(2.6, assert_report("RecursivePolynomialFilter_test/test1PurePredict"));
                
        testData.close();
    }
    
    
    @Test
    public void test1PureObservation () {
        TestData testData = new TestData();
        List<String> matches;
        int N;
        int order;
        double tau;
        DMatrixRMaj setup = new DMatrixRMaj();
        DMatrixRMaj times = new DMatrixRMaj();
        DMatrixRMaj truth = new DMatrixRMaj();
        DMatrixRMaj observations = new DMatrixRMaj();
        DMatrixRMaj es = new DMatrixRMaj();
        DMatrixRMaj Zstars = new DMatrixRMaj();
        DMatrixRMaj innovation = new DMatrixRMaj();
        DMatrixRMaj innovations = new DMatrixRMaj();
        DMatrixRMaj actual = new DMatrixRMaj();
        DMatrixRMaj expected = new DMatrixRMaj();
        ICore core;
        RecursivePolynomialFilter f = new RecursivePolynomialFilter();
        DMatrixRMaj Zstar = new DMatrixRMaj();
        double e;
        DMatrixRMaj V = new DMatrixRMaj();
        assert_clear();
        testData = new TestData("testRecursivePolynomialFilter.nc");
        matches = testData.getMatchingGroups("testPureObservation_");
        assert_not_empty(matches);
        for (int iMatch = 0; iMatch < numElements(matches); iMatch++) {
            setup = testData.getGroupVariable(matches.get(iMatch), "setup");
            times = testData.getGroupVariable(matches.get(iMatch), "times");
            truth = testData.getGroupVariable(matches.get(iMatch), "truth");
            observations = testData.getGroupVariable(matches.get(iMatch), "observations");
                        
            //  N = int(setup(0))
            double     td2 = setup.get(0);
            N = (int) td2;
                        
            //  order = int(setup(1))
            double     td4 = setup.get(1);
            order = (int) td4;
                        
            tau = setup.get(2);
            es = testData.getGroupVariable(matches.get(iMatch), "es");
            Zstars = testData.getGroupVariable(matches.get(iMatch), "Zstars");
            innovations = testData.getGroupVariable(matches.get(iMatch), "innovations");
            expected = testData.getGroupVariable(matches.get(iMatch), "expected");
                        
            //  actual = zeros(N, order + 1)
            actual.reshape(N, order + 1);
            CommonOps_DDRM.fill( actual, 0.0 );
                        
            //  actual(0,  : ) = truth(0,  : )
            DMatrixRMaj tm9 = new DMatrixRMaj( 1, ((truth.numCols)-0) );
            CommonOps_DDRM.extract( truth, 0, 1, 0, truth.numCols, tm9 );
            CommonOps_DDRM.insert( tm9, actual, 0, 0 );
            core = new PureObservationCore(order);
            f = new RecursivePolynomialFilter(order, tau, core);
                        
            //  f.start(times(0), truth(0,  : ))
            double     td10 = times.get(0);
            DMatrixRMaj tm11 = new DMatrixRMaj( 1, ((truth.numCols)-0) );
            CommonOps_DDRM.extract( truth, 0, 1, 0, truth.numCols, tm11 );
            f.start(td10, tm11);
            for (int i = 1; i < N; i++) {
                                
                //  Zstar = f.predict(times(i))
                double     td15 = times.get(i);
                Zstar = f.predict(td15);
                                
                //  assert_almost_equal(Zstar, transpose(Zstars(i,  : )))
                DMatrixRMaj tm17 = new DMatrixRMaj( 1, ((Zstars.numCols)-0) );
                CommonOps_DDRM.extract( Zstars, i, i+1, 0, Zstars.numCols, tm17 );
                DMatrixRMaj tm18 = new DMatrixRMaj(tm17.getNumCols(), tm17.getNumRows());
                CommonOps_DDRM.transpose( tm17, tm18 );
                assert_almost_equal(Zstar, tm18);
                                
                //  e = observations(i) - Zstar(0)
                double     td20 = observations.get(i);
                double     td21 = Zstar.get(0);
                e = td20 - td21;
                                
                //  assert_almost_equal(e, es(i))
                double     td23 = es.get(i);
                assert_almost_equal(e, td23);
                                
                //  innovation = f.update(times(i), Zstar, e)
                double     td25 = times.get(i);
                innovation = f.update(td25, Zstar, e);
                                
                //  assert_almost_equal(innovation, transpose(innovations(i,  : )))
                DMatrixRMaj tm27 = new DMatrixRMaj( 1, ((innovations.numCols)-0) );
                CommonOps_DDRM.extract( innovations, i, i+1, 0, innovations.numCols, tm27 );
                DMatrixRMaj tm28 = new DMatrixRMaj(tm27.getNumCols(), tm27.getNumRows());
                CommonOps_DDRM.transpose( tm27, tm28 );
                assert_almost_equal(innovation, tm28);
                                
                //  actual(i,  : ) = transpose(f.getState())
                DMatrixRMaj tm30 = f.getState();
                DMatrixRMaj tm31 = new DMatrixRMaj(tm30.getNumCols(), tm30.getNumRows());
                CommonOps_DDRM.transpose( tm30, tm31 );
                CommonOps_DDRM.insert( tm31, actual, i, 0 );
                                
                V = f.getVRF();
                                
                //  assert_almost_equal(V, zeros(order + 1, order + 1))
                DMatrixRMaj tm35 = new DMatrixRMaj(order + 1, order + 1);
                CommonOps_DDRM.fill( tm35, 0.0 );
                assert_almost_equal(V, tm35);
            }
                        
            assert_almost_equal(actual, expected);
        }
        assertGreaterEqual(22.0, assert_report("RecursivePolynomialFilter_test/test1PureObservation"));
                
        testData.close();
    }
    
    
    @Test
    public void test9Coverage () {
        ICore core;
        RecursivePolynomialFilter f = new RecursivePolynomialFilter();
        RecursivePolynomialFilter g = new RecursivePolynomialFilter();
        String name;
        DMatrixRMaj Zstar = new DMatrixRMaj();
        DMatrixRMaj I = new DMatrixRMaj();
        assert_clear();
        core = new PureObservationCore(2);
        f = new RecursivePolynomialFilter(2, 1.0, core);
        assertEqual(2, f.getOrder());
        assertEqual(1.0, f.getTau());
        f.setName("hello");
        name = f.getName();
        assertEqual(f.getStatus(), FilterStatus.IDLE);
        f.start(0.0, (new DMatrixRMaj(new double[] {1.0, 2.0, 3.0})));
        assertEqual(f.getStatus(), FilterStatus.IDLE);
        assertEqual(f.getFirstVRF(), 0.0);
        assertEqual(f.getLastVRF(), 0.0);
                
        Zstar = f.predict(1.0);
                
        DMatrixRMaj tm2 = f.update(1.0, Zstar, 0.0);
        assertEqual(f.getStatus(), FilterStatus.INITIALIZING);
                
        Zstar = f.predict(2.0);
                
        DMatrixRMaj tm5 = f.update(2.0, Zstar, 0.0);
        assertEqual(f.getStatus(), FilterStatus.RUNNING);
        assert_almost_equal(f.getState(), (new DMatrixRMaj(new double[] {11.0, 8.0, 3.0})));
        assert_almost_equal(f.transitionState(4.0), (new DMatrixRMaj(new double[] {33.0, 14.0, 3.0})));
        assertEqual(2, f.getN());
        assertEqual(RecursivePolynomialFilter.effectiveTheta(2, 0), 0);
        assert_almost_equal(RecursivePolynomialFilter.effectiveTheta(2, 10), 0.56673);
        g = new RecursivePolynomialFilter(2, 1.0, core);
        g.copyState(f);
        assert_almost_equal(g.getState(), (new DMatrixRMaj(new double[] {11.0, 8.0, 3.0})));
        assert_report("RecursivePolynomialFilter_test/test9Coverage");
    }
    
} // class RecursivePolynomialFilter_test

