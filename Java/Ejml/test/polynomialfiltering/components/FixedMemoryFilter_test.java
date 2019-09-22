/***** /polynomialfiltering/components/FixedMemoryFilter_test/
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
import polynomialfiltering.components.fixedmemorypolynomialfilter.FixedMemoryFilter;
import polynomialfiltering.components.FixedMemoryFilter_test.TestFixedMemoryFilter;

 
public class FixedMemoryFilter_test {
    
    public DMatrixRMaj executeEstimatedState (final DMatrixRMaj setup, final DMatrixRMaj data) {
        int order;
        int window;
        int M;
        int iCheck;
        DMatrixRMaj times = new DMatrixRMaj();
        DMatrixRMaj observations = new DMatrixRMaj();
        FixedMemoryFilter fixed = new FixedMemoryFilter();
                
        //  order = int(setup(0))
        double     td1 = setup.get(0);
        order = (int) td1;
                
        //  window = int(setup(1))
        double     td3 = setup.get(1);
        window = (int) td3;
                
        //  M = int(setup(2))
        double     td5 = setup.get(2);
        M = (int) td5;
                
        //  iCheck = int(setup(3))
        double     td7 = setup.get(3);
        iCheck = (int) td7;
                
        //  times = data( : , 0 : (1-1))
        times.reshape( ((data.numRows)-0), 1 );
        CommonOps_DDRM.extract( data, 0, data.numRows, 0, 1, times );
                
        //  observations = data( : , 1 : (2-1))
        observations.reshape( ((data.numRows)-0), 1 );
        CommonOps_DDRM.extract( data, 0, data.numRows, 1, 2, observations );
        fixed = new FixedMemoryFilter(order, window);
        for (int i = 0; i < M; i++) {
                        
            //  fixed.add(times(i), observations(i))
            double     td15 = times.get(i);
            double     td16 = observations.get(i);
            fixed.add(td15, td16);
        }
        
        //  fixed.transitionState(times(iCheck))
        double     td18 = times.get(iCheck);
        return  fixed.transitionState(td18);
    }
    
    
    public DMatrixRMaj executeVRF (final DMatrixRMaj setup, final DMatrixRMaj data) {
        int order;
        int window;
        int M;
        int iCheck;
        DMatrixRMaj times = new DMatrixRMaj();
        DMatrixRMaj observations = new DMatrixRMaj();
        FixedMemoryFilter fixed = new FixedMemoryFilter();
                
        //  order = int(setup(0))
        double     td1 = setup.get(0);
        order = (int) td1;
                
        //  window = int(setup(1))
        double     td3 = setup.get(1);
        window = (int) td3;
                
        //  M = int(setup(2))
        double     td5 = setup.get(2);
        M = (int) td5;
                
        //  iCheck = int(setup(3))
        double     td7 = setup.get(3);
        iCheck = (int) td7;
                
        //  times = data( : , 0 : (1-1))
        times.reshape( ((data.numRows)-0), 1 );
        CommonOps_DDRM.extract( data, 0, data.numRows, 0, 1, times );
                
        //  observations = data( : , 1 : (2-1))
        observations.reshape( ((data.numRows)-0), 1 );
        CommonOps_DDRM.extract( data, 0, data.numRows, 1, 2, observations );
        fixed = new FixedMemoryFilter(order, window);
        for (int i = 0; i < M; i++) {
                        
            //  fixed.add(times(i), observations(i))
            double     td15 = times.get(i);
            double     td16 = observations.get(i);
            fixed.add(td15, td16);
        }
        
        //  asssignment.dummy = return ( fixed.getVRF())
        DMatrixRMaj tm20 = fixed.getVRF();
        return tm20;
    }
    
    
    @Test
    public void test1CheckPerfect () {
        List<String> matches;
        double tau;
        int N;
        Group group;
        DMatrixRMaj setup = new DMatrixRMaj();
        int order;
        DMatrixRMaj data = new DMatrixRMaj();
        DMatrixRMaj actual = new DMatrixRMaj();
        DMatrixRMaj expected = new DMatrixRMaj();
        TestData testData = new TestData();
        assert_clear();
        testData = new TestData("FixedMemoryFiltering.nc");
        matches = testData.getMatchingGroups("testPerfect_");
        assert_not_empty(matches);
                
        tau = 0.1;
                
        N = 25;
        for (int i = 0; i < numElements(matches); i++) {
            group = testData.getGroup(matches.get(i));
            setup = testData.getArray(group, "setup");
                        
            //  order = int(setup(0))
            double     td2 = setup.get(0);
            order = (int) td2;
            data = testData.getArray(group, "data");
                        
            actual = this.executeEstimatedState(setup, data);
            expected = testData.getArray(group, "expected");
                        
            assert_almost_equal(expected, actual);
        }
                
        testData.close();
        assert_report("FixedMemoryFilter_test/test1CheckPerfect");
    }
    
    
    @Test
    public void test1CheckNoisy () {
        List<String> matches;
        double tau;
        int N;
        Group group;
        DMatrixRMaj setup = new DMatrixRMaj();
        int order;
        DMatrixRMaj data = new DMatrixRMaj();
        DMatrixRMaj actual = new DMatrixRMaj();
        DMatrixRMaj expected = new DMatrixRMaj();
        TestData testData = new TestData();
        assert_clear();
        testData = new TestData("FixedMemoryFiltering.nc");
        matches = testData.getMatchingGroups("testNoisy_");
        assert_not_empty(matches);
                
        tau = 0.1;
                
        N = 25;
        for (int i = 0; i < numElements(matches); i++) {
            group = testData.getGroup(matches.get(i));
            setup = testData.getArray(group, "setup");
                        
            //  order = int(setup(0))
            double     td2 = setup.get(0);
            order = (int) td2;
            data = testData.getArray(group, "data");
                        
            actual = this.executeEstimatedState(setup, data);
            expected = testData.getArray(group, "expected");
                        
            assert_almost_equal(expected, actual);
        }
                
        testData.close();
        assert_report("FixedMemoryFilter_test/test1CheckNoisy");
    }
    
    
    @Test
    public void test1CheckMidpoints () {
        List<String> matches;
        double tau;
        int N;
        int M;
        int window;
        int iCheck;
        Group group;
        DMatrixRMaj setup = new DMatrixRMaj();
        int offset;
        int order;
        DMatrixRMaj data = new DMatrixRMaj();
        DMatrixRMaj actual = new DMatrixRMaj();
        DMatrixRMaj expected = new DMatrixRMaj();
        TestData testData = new TestData();
        assert_clear();
        testData = new TestData("FixedMemoryFiltering.nc");
        matches = testData.getMatchingGroups("testMidpoints_");
        assert_not_empty(matches);
                
        tau = 0.1;
                
        N = 25;
                
        order = 2;
                
        window = 11;
                
        M = 12;
                
        offset = M - window;
        for (int i = 0; i < numElements(matches); i++) {
            group = testData.getGroup(matches.get(i));
            setup = testData.getArray(group, "setup");
                        
            //  order = int(setup(0))
            double     td3 = setup.get(0);
            order = (int) td3;
                        
            //  window = int(setup(1))
            double     td5 = setup.get(1);
            window = (int) td5;
                        
            //  M = int(setup(2))
            double     td7 = setup.get(2);
            M = (int) td7;
                        
            //  iCheck = int(setup(3))
            double     td9 = setup.get(3);
            iCheck = (int) td9;
            data = testData.getArray(group, "data");
                        
            actual = this.executeEstimatedState(setup, data);
            expected = testData.getArray(group, "expected");
                        
            assert_almost_equal(expected, actual);
        }
                
        testData.close();
        assert_report("FixedMemoryFilter_test/test1CheckMidpoints");
    }
    
    
    @Test
    public void test1CheckVrfs () {
        List<String> matches;
        double tau;
        int N;
        int M;
        int window;
        int iCheck;
        Group group;
        DMatrixRMaj setup = new DMatrixRMaj();
        int order;
        int offset;
        DMatrixRMaj data = new DMatrixRMaj();
        DMatrixRMaj actual = new DMatrixRMaj();
        DMatrixRMaj expected = new DMatrixRMaj();
        TestData testData = new TestData();
        assert_clear();
        testData = new TestData("FixedMemoryFiltering.nc");
        matches = testData.getMatchingGroups("testVRF_");
        assert_not_empty(matches);
                
        tau = 0.1;
                
        N = 25;
                
        order = 2;
                
        window = 11;
                
        M = 12;
                
        offset = M - window;
        for (int i = 0; i < numElements(matches); i++) {
            group = testData.getGroup(matches.get(i));
            setup = testData.getArray(group, "setup");
                        
            //  order = int(setup(0))
            double     td3 = setup.get(0);
            order = (int) td3;
                        
            //  window = int(setup(1))
            double     td5 = setup.get(1);
            window = (int) td5;
                        
            //  M = int(setup(2))
            double     td7 = setup.get(2);
            M = (int) td7;
                        
            //  iCheck = int(setup(3))
            double     td9 = setup.get(3);
            iCheck = (int) td9;
            data = testData.getArray(group, "data");
                        
            actual = this.executeVRF(setup, data);
            expected = testData.getArray(group, "expected");
                        
            assert_almost_equal(expected, actual);
        }
                
        testData.close();
        assert_report("FixedMemoryFilter_test/test1CheckVrfs");
    }
    
    public static class TestFixedMemoryFilter extends FixedMemoryFilter {
        
        public TestFixedMemoryFilter() {}  // auto-generated null constructor

        
        public TestFixedMemoryFilter (final int order) {
            super(order);
        }
        
        
        public int getOrder () {
            return this.order;
        }
        
        
        public int getL () {
            return this.L;
        }
        
    } // class TestFixedMemoryFilter
    
    
    @Test
    public void test9Regresssion () {
        TestFixedMemoryFilter f = new TestFixedMemoryFilter();
        FixedMemoryFilter fixed = new FixedMemoryFilter();
        DMatrixRMaj Z = new DMatrixRMaj();
        assert_clear();
        f = new TestFixedMemoryFilter(4);
        assertEqual(f.getOrder(), 4);
        assertEqual(f.getL(), 51);
        fixed = new FixedMemoryFilter(0, 5);
        assertEqual(fixed.getTau(), 0.0);
        assertEqual(fixed.getStatus(), FilterStatus.IDLE);
                
        //  Z = zeros(1, 1)
        Z.reshape(1, 1);
        CommonOps_DDRM.fill( Z, 0.0 );
                
        //  assert_almost_equal(Z, fixed.getVRF())
        DMatrixRMaj tm2 = fixed.getVRF();
        assert_almost_equal(Z, tm2);
        assertEqual(fixed.getFirstVRF(), 0);
        assertEqual(fixed.getLastVRF(), 0);
        for (int i = 0; i < 5; i++) {
            assertEqual(fixed.getN(), i);
                        
            fixed.add(i, i);
            assertEqual(fixed.getStatus(), FilterStatus.INITIALIZING);
        }
                
        fixed.add(10, 10);
        assertEqual(fixed.getStatus(), FilterStatus.RUNNING);
        assertEqual(fixed.getTime(), 10);
        assert_almost_equal(fixed.getState(), (new DMatrixRMaj(new double[] {4.0})));
        assert_report("FixedMemoryFilter_test/test9Regresssion");
    }
    
} // class FixedMemoryFilter_test

