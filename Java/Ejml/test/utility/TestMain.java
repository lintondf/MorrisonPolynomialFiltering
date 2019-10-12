/**
 * 
 */
package utility;

import org.junit.Test;

import java.util.Arrays;
import java.util.HashMap;

//import static org.junit.Assert.*;

import java.util.List;

import org.ejml.data.DMatrixRMaj;
import org.ejml.dense.row.CommonOps_DDRM;
import org.ejml.ops.MatrixIO;

import polynomialfiltering.main.FilterStatus;
import ucar.nc2.Group;
import java.sql.DriverManager;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;



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
	static double maxErrorA;
	static double maxErrorB;
	static String prefix = "";
	
	public static void assert_almost_equal( double A, double B ) {
		double log2Error = compareDoubles(A, B);
		if (log2Error > maxLog2Error) {
			maxLog2Error = log2Error;
			maxErrorA = A;
			maxErrorB = B;
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
	
	private static HashMap<String, Double> maxErrors = new HashMap<>();
	
	public static double assert_report(String from, int id) {
		double result = maxLog2Error;
		if (id >= 0)
			from += Integer.toString(id);
		System.out.printf("%-72s: %10.2f units; %.15g %.15g\n", from, maxLog2Error, maxErrorA, maxErrorB);
		if (connection != null) {
			try {
				Statement statement = connection.createStatement();
		        ResultSet rs = statement.executeQuery("select * from errors WHERE target='Java/EJML' AND test='" + from + "'");
		        while(rs.next()) {
		        	//System.out.println(rs.getString("target") + " " + rs.getString("test") + " : " + rs.getDouble("bits"));
		        	assertTrue(Math.abs(rs.getDouble("bits") - maxLog2Error) <= 0.01);
		        }
			} catch (Exception x) {
				x.printStackTrace();
			}
			
		}
		maxLog2Error = 0;
		maxErrorA = maxErrorB = 0;
		return result;
	}

    private static Connection connect(String path) {
        // SQLite connection string
        String url = "jdbc:sqlite:" + path;
        Connection conn = null;
        try {
            conn = DriverManager.getConnection(url);
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
        return conn;
    }
	
	private static Connection connection;
	
	public static void assert_clear() {
		if (connection == null) {
			String path = TestData.testDataPath("FloatingPointDifferences.sqlite");
			connection = connect(path);
		}
		maxLog2Error = 0;		
		maxErrorA = maxErrorB = 0;
	}
	
	protected static double ulpError( double A, double B ) {
		if (A == 0.0 && B == 0.0)
			return 0.0;
		double maxError = Math.abs(A - B);
		double max = Math.max( Math.abs(A), Math.abs(B));
		if (maxError/max < 1e-16)
			return 0.5;
		double ulp = Math.ulp(max);
		double lre = -Math.log(maxError/max)/Math.log(2.0);
		return Math.min(Math.log(maxError/ulp)/Math.log(2.0), lre);
	}
	
	final static double MAX_BITS = 2048.0;
	final static double BITS_SCALE = 1.0;
	final static double DBL_MIN = Double.MIN_VALUE;
	final static double DBL_MAX = Double.MAX_VALUE;
	final static double DBL_EPSILON = Double.longBitsToDouble(971l << 52);
	final static double LOG_OFFSET = -37.0; // Math.log(DBL_MIN) + 707.5;
	final static double _DBL_TOL_MULT = 100.0;
	final static double TolAtEPS = DBL_EPSILON * _DBL_TOL_MULT; 
	final static double TolAtMIN = DBL_MIN * _DBL_TOL_MULT;
	final static double onePlusTol = 1.0 + DBL_EPSILON * _DBL_TOL_MULT;
	final static double oneMinusTol = 1.0 - DBL_EPSILON * _DBL_TOL_MULT;

	private static double bits( double x) {
		double logx = Math.log(Math.abs(x));
	    return logx - LOG_OFFSET;
	}

	protected static double compareDoubles( double a, double b) {

	    if (Double.isNaN(a)) {
	        if (Double.isNaN(b))
	            return 0.0;
	        else
	            return MAX_BITS*BITS_SCALE;       
	    } else {
	        if (Double.isNaN(b))
	            return MAX_BITS*BITS_SCALE;
	    }
	    if (Double.isInfinite(a)) {
	        if (Double.isInfinite(b))
	            return 0.0;
	        else
	            return MAX_BITS*BITS_SCALE;       
	    } else {
	        if (Double.isInfinite(b))
	            return MAX_BITS*BITS_SCALE;
	    }
	   if (a == b) 
		   return 0.0;
	   
	   // machinery for "close enough"
	   //

	   // type identification, storage
	    double ratio;
	    double fabsa = Math.abs(a);
	    double fabsb = Math.abs(b);

	   // test for closeness to 0
	   if ( 0.0 == a ) // check if |b| is "close enough" to 0 
	      return bits(a)*BITS_SCALE; // (typedQty::TolAtEPS() > (0.0 > b ? -b : b));  
	   if ( 0.0 == b ) // check if |a| is "close enough" to 0 
	      return bits(b)*BITS_SCALE; // (typedQty::TolAtEPS() > (0.0 > a ? -a : a));  

	   // test for closeness to each other
	   if (TolAtMIN > fabsb) { 
	      // |b| is indistinguishable from 0
	      if (TolAtMIN > (0.0 > a ? -a : a)) 
	    	  return 0.0; 
	      // . . . but |a| is distinguishable from 0
	      return bits(a)*BITS_SCALE;
	   } else if (TolAtMIN < fabsa) {
	      // |a| and |b| are distinguishable from 0, take ratio 
	      // avoid overflow if |a| is very large and |b| is very small
	      if ( (fabsb < 1.0) 
	        && (fabsa > fabsb * DBL_MAX) ) 
	    	  return MAX_BITS*BITS_SCALE;
	      // avoid underflow if |a| is very small and |b| is very large 
	      if ( (fabsb > 1.0) 
	        && (fabsa < fabsb * DBL_MIN) ) 
	    	  return MAX_BITS*BITS_SCALE;
	      // this must be signed
	      ratio = a/b;
	   } else {
	      // |b| is distinguishable from 0
	      // |a| is indistinguishable from 0 
	      return bits(b)*BITS_SCALE;
	   };

	   // only if signed ratio is indistinguishable from +1 then equality true
	   if ( (onePlusTol > ratio) 
	         && (oneMinusTol < ratio)) 
		   return 0.0;

	   // they're different 
	   return bits(ratio-1.0)*BITS_SCALE;    
	}
	
	public static void logDifferences(TestData archive, Group g, DMatrixRMaj A, DMatrixRMaj B ) {
		DMatrixRMaj d = new DMatrixRMaj( A.numRows, 5 );
//		CommonOps_DDRM.subtract(A, B, d);
//		CommonOps_DDRM.abs(d, d);
		for (int i = 0; i < A.numRows; i++) {
			d.unsafe_set(i, 0, i);
			d.unsafe_set(i, 1, A.unsafe_get(i, 5));
			d.unsafe_set(i, 2, B.unsafe_get(i, 5));
			d.unsafe_set(i, 3, A.unsafe_get(i, 5)-B.unsafe_get(i, 5));
			d.unsafe_set(i, 4, compareDoubles(A.unsafe_get(i, 5), B.unsafe_get(i, 5)));
		}
		archive.putArray(g, "compare", d);
	}
	
	@Test
	public void testTesting() {
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
		assert_report("Expect 0.0", -1);
		assert_almost_equal(2.0, A);
		assert_report("Expect 37.0", -1);
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
		double b = assert_report("Should be 0.0", -1);
		double c = Math.nextAfter(a, a+1);
		assert_almost_equal( a, c );
		b = assert_report("Expect 0.0", -1);
		double[] expecting = {0, 7.07, 9.37, 11.67, 13.97, 16.28, 18.58, 20.88, 23.18, 25.49, 27.79, 30.09, 32.39, 34.60, 36.31, 36.90};
		for (int j = -14; j <= 1; j++) {
			double p = Math.pow(10.0, j);
			assert_clear();
			assert_almost_equal( a, a+p );
			if (Math.abs(maxLog2Error - expecting[14+j]) > 0.01) {
				System.err.println("assert_almost_equal double incorrect");
				System.err.printf("%d %10g %10g %6.2f %6.2f\n", j, a, a+p, maxLog2Error, expecting[14+j]);
//				return;				
			}
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

	public static void main(String[] args) {
//		for (int p = -15; p < 16; p++) {
//			double x = Math.pow(10.0, p);
//			double y = 1e6;
//			double ulp = ulpError(1.0*y, y*(1.0+x));
//			System.out.printf( "%10g, %10.2f %10g\n", x, ulp, 0.5/y*Math.pow(2.0, ulp/2.0));
//		}
		if (true) {
			
			System.out.println(compareDoubles(480.4300334, 480.4300333));
			double minY = 1e6;
			for (int px = -160; px <= 160; px++) {
				for (int pe = -1600; pe <= 1600; pe++) {
					double A = Math.pow(10.0, 0.1*px);
					double e = Math.pow(10.0, 0.01*pe);
					double B = A + e;
//					double ulp = ulpError(A, B);
//					double maxError = Math.abs(A - B);
//					double max = Math.max( Math.abs(A), Math.abs(B));
//					double y = -Math.log(maxError/max)/Math.log(2.0);
//					System.out.printf( "%10g, %10g, %10.2f %10.2f\n", A, e, ulp, Math.min(ulp,y));
					double y = compareDoubles(A, B);
//					if (y == 0.0)
//					System.out.printf( "%10g, %10g, %10g, %10.4f\n", A, B, e, y);
					if (y > 0.0)
						minY = Math.min(minY, y);
				}
			}
			System.out.println(minY);
			return;
		}
		(new TestMain()).testTesting();
	}

}
