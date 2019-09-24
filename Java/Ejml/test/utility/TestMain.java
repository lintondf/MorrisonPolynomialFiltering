/**
 * 
 */
package utility;

import java.util.Arrays;

//import static org.junit.Assert.*;

import java.util.List;

import org.ejml.data.DMatrixRMaj;
import org.ejml.dense.row.CommonOps_DDRM;
import org.ejml.ops.MatrixIO;

import polynomialfiltering.main.FilterStatus;
import ucar.nc2.Group;


/**
 * @author lintondf
 *
 */
public class TestMain {
	
	//static final double threshold = 0*1.5 * 1.0E-7;
	
	public static <T> int numElements(List<T> list) {
		return list.size();
	}
	
	public static <T> void assert_not_empty( List<T> list ) {
		org.junit.Assert.assertFalse(list.isEmpty());
	}
	
	public static void assert_almost_equal( DMatrixRMaj A, DMatrixRMaj B ) {
		assertTrue( A.numCols == B.numCols);
		assertTrue( A.numRows == B.numRows);
		DMatrixRMaj d = new DMatrixRMaj( A.numRows, A.numCols );
		CommonOps_DDRM.subtract(A, B, d);
		CommonOps_DDRM.abs(d, d);
		for (int i = 0; i < A.numRows; i++) {
			for (int j = 0; j < A.numCols; j++) {
				prefix = String.format("(%d,%d)", i, j );
				assert_almost_equal( A.unsafe_get(i, j), B.unsafe_get(i, j));
			}
		}
	}
	
	public static void assert_almost_equal(double d, DMatrixRMaj q) {
		org.junit.Assert.assertTrue(q.numCols == 1);
		org.junit.Assert.assertTrue(q.numRows == 1);
		assert_almost_equal(d, q.unsafe_get(0, 0) );
	}
	
	public static void assertEqual( int a, int b) {
		org.junit.Assert.assertTrue( a == b);
	}
	
	public static void assertEqual( double a, double b) {
		org.junit.Assert.assertTrue( a == b);
	}
	
	public static void assertEqual( FilterStatus a, FilterStatus b) {
		org.junit.Assert.assertTrue( a == b);
	}
	
	public static void assertGreaterEqual(double a, double b) {
		org.junit.Assert.assertTrue( a >= b );
	}
	
	public static void assertFalse(boolean tf) {
		org.junit.Assert.assertFalse(tf);
	}
	
	public static void assertTrue(boolean tf) {
		org.junit.Assert.assertTrue(tf);
	}
	
	static double maxLog2Error = 0;
	static String prefix = "";

	public static void assert_almost_equal( double A, double B ) {
		double max = Math.max( Math.abs(A), Math.abs(B));
		double ulp = Math.ulp(max);
		double maxError = Math.abs(A - B);
		double threshold = 1.0 * ulp;
		double log2Error = Math.log(maxError/ulp)/Math.log(2.0);
		if (log2Error > maxLog2Error) {
			maxLog2Error = log2Error;
//				System.out.printf("%s %20.18e %20.18e %20.18e %20.18e %10.2f\n", prefix, A, B, maxError, maxError/max, log2Error );
		}
		prefix = "";
	}

	public static void assert_array_less( DMatrixRMaj A, DMatrixRMaj B ) {
		assertTrue( A.numCols == B.numCols);
		assertTrue( A.numRows == B.numRows);
		DMatrixRMaj d = new DMatrixRMaj( A.numRows, A.numCols );
		CommonOps_DDRM.subtract(B, A, d);
		double maxError = CommonOps_DDRM.elementMax(d);
		assertTrue( maxError > 0.0);
	}
	
	public static double assert_report(String from) {
		double result = maxLog2Error;
		System.out.printf("%-72s: %10.2f bits\n", from, maxLog2Error);
		maxLog2Error = 0;
		return result;
	}

	public static void assert_clear() {
		maxLog2Error = 0;		
	}
	
	public static void main(String[] args) {
		TestData testData = new TestData("test.nc");
		Group group = testData.getGroup("Test");
		if (group == null) {
			System.err.println("Test group not found");
			return;
		}
		int i = testData.getInteger(group, "i");
		if (i != 1) {
			System.err.println("i != 1: " + i);
			return;
		}
		double x = testData.getScalar(group, "x");
		if (x != 3.14) {
			System.err.println("x != 3.14: " + x);
			return;
		}
		DMatrixRMaj v = testData.getArray(group, "v");
		if (v.numRows != 3 || v.numCols != 1) {
			System.err.println("v wrong shape; should be 3,1");
			v.print();
			return;
		}
		if (v.unsafe_get(0, 0) != 1.0 || v.unsafe_get(1, 0) != 2.0 || v.unsafe_get(2, 0) != 3.0) {
			System.err.println("v content wrong; should be [1;2;3]");
			v.print();
			return;
		}
		DMatrixRMaj m = testData.getArray(group, "m");
		if (m.numRows != 2 || m.numCols != 2) {
			System.err.println("m wrong shape; should be 2, 2");
			v.print();
			return;
		}
		if (m.unsafe_get(0, 0) != 4.0 || m.unsafe_get(0, 1) != 5.0 || 
			m.unsafe_get(1, 0) != 6.0 || m.unsafe_get(1, 1) != 7.0) {
			System.err.println("m content wrong; should be [[4,5],[6,7]]");
			m.print();
			return;
		}
		assertTrue(true);
		try {
			assertTrue(false);
			System.err.println("assertTrue failed to fail");
			return;
		} catch (AssertionError ae) {}
		assertFalse(false);
		try {
			assertFalse(true);
			System.err.println("assertFalse failed to fail");
			return;
		} catch (AssertionError ae) {}
		assertGreaterEqual(3.0, 2.0);
		assertGreaterEqual(3.0, 3.0);
		try {
			assertGreaterEqual(2.0, 3.0);
			System.err.println("assertGreaterEqual failed to fail");
			return;
		} catch (AssertionError ae) {}
		assertEqual(1, 1);
		try {
			assertEqual(2,1);
			System.err.println("assertEqual int failed to fail");
			return;
		} catch (AssertionError ae) {}
		assertEqual(1.0, 1.0);
		try {
			assertEqual(2.0,1.0);
			System.err.println("assertEqual double failed to fail");
			return;
		} catch (AssertionError ae) {}
		assertEqual(FilterStatus.COASTING, FilterStatus.COASTING);
		try {
			assertEqual(FilterStatus.COASTING, FilterStatus.IDLE);
			System.err.println("assertEqual FilterStatus failed to fail");
			return;
		} catch (AssertionError ae) {}
		
		DMatrixRMaj A = new DMatrixRMaj(3,3);
		DMatrixRMaj B = new DMatrixRMaj(3,3);
		A.fill(1.0);
		B.fill(2.0);
		assert_array_less(A, B);
		try {
			assert_array_less(B, A);
			System.err.println("assert_array_less failed to fail");
			return;
		} catch (AssertionError ae) {}
		
		A.reshape(1, 1);
		A.fill(1.0);
		assert_clear();
		assert_almost_equal(1.0, A);
		assert_report("Expect 0.0");
		assert_almost_equal(2.0, A);
		assert_report("Expect 51");
		try {
			assert_almost_equal(1.0, B);			
			System.err.println("assert_almost_equal failed to fail");
			return;
		} catch (AssertionError ae) {}
		
		try {
			B.reshape(A.numRows+1, A.numCols);
			assert_almost_equal(A, B);
			System.err.println("assert_almost_equal failed to fail");
			return;
		} catch (AssertionError ae) {}
		try {
			B.reshape(A.numRows, A.numCols+1);
			assert_almost_equal(A, B);
			System.err.println("assert_almost_equal failed to fail");
			return;
		} catch (AssertionError ae) {}
		
		List<String> ls = Arrays.asList(new String[] {"a", "b"} );
		assert_not_empty( ls );
		ls = Arrays.asList(new String[] {});
		try {
			assert_not_empty( ls );
			System.err.println("assert_not_empty failed to fail");
			return;
		} catch (AssertionError ae) {}
		
		double a = 1.0;
		assert_clear();
		double b = assert_report("Should be 0.0");
		double c = Math.nextAfter(a, a+1);
		assert_almost_equal( a, c );
		b = assert_report("Expect 0.0");
		c = Math.nextAfter(c, a+1);
		assert_almost_equal( a, c );
		b = assert_report("Expect 1.0");
		c = Math.nextAfter(c, a+1);
		double[] expecting = {5.49, 8.81, 12.13, 15.46, 18.78, 22.10, 25.42, 28.75, 32.07, 35.39, 38.71, 42.03, 45.36, 48.68, 51.00, 52.32};
		for (int j = -14; j <= 1; j++) {
			double p = Math.pow(10.0, j);
			assert_clear();
			assert_almost_equal( a, a+p );
			if (Math.abs(maxLog2Error - expecting[14+j]) > 0.01) {
				System.err.println("assert_almost_equal double incorrect");
				return;				
			}
//			System.out.println(j + " " + maxLog2Error + " " + expecting[14+j]);
//			b = assert_report(String.format("Expect %5.1f", expecting[14+j]));
		}

		assert_clear();
		A.reshape(3, 3);
		B.reshape(3, 3);
		A.fill(1.0);
		for (int j = -14; j <= 1; j++) {
			double p = Math.pow(10.0, j);
			assert_clear();
			B.fill(a+p);
			assert_almost_equal( A, B );
			if (Math.abs(maxLog2Error - expecting[14+j]) > 0.01) {
				System.err.println("assert_almost_equal matrix incorrect");
				return;				
			}
//			b = assert_report(String.format("Expect %5.1f", expecting[14+j]));
		}
		System.out.println("Test of testing OK");
	}

}
