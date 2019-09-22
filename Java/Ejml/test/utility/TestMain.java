/**
 * 
 */
package utility;

//import static org.junit.Assert.*;

import java.util.List;

import org.ejml.data.DMatrixRMaj;
import org.ejml.dense.row.CommonOps_DDRM;
import org.ejml.ops.MatrixIO;

import polynomialfiltering.main.FilterStatus;


/**
 * @author lintondf
 *
 */
public class TestMain {
	
	static final double threshold = 1.5 * 1.0E-7;
	
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
		double maxError = CommonOps_DDRM.elementMax(d);
		
		if (maxError >= threshold) {
			for (int i = 0; i < A.numRows; i++) {
				for (int j = 0; j < A.numCols; j++) {
					prefix = String.format("(%d,%d)", i, j );
					assert_almost_equal( A.unsafe_get(i, j), B.unsafe_get(i, j));
				}
			}
		};
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
		if (maxError >= threshold) {
			double log2Error = Math.log(maxError/ulp)/Math.log(2.0);
			if (log2Error > maxLog2Error) {
				maxLog2Error = log2Error;
//				System.out.printf("%s %20.18e %20.18e %20.18e %20.18e %10.2f\n", prefix, A, B, maxError, maxError/max, log2Error );
			}
//			int expA = Math.getExponent(A);
//			int expB = Math.getExponent(B);
//			double mantissaA = A / Math.pow(2, expA);
//			double mantissaB = B / Math.pow(2, expB);
//			System.out.printf("   %5d %5d %20.18g %20.18g %20.18g %20.18g\n", expA, expB, mantissaA, mantissaB, mantissaA-mantissaB, Math.ulp(mantissaA) );
		}
		//assertTrue( maxError < threshold);
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

}
