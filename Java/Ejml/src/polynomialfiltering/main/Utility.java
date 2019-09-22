package polynomialfiltering.main;

import java.util.ArrayList;

import org.ejml.data.DMatrixRMaj;

public class Utility {
	
	public static class ValueError extends RuntimeException {
		public ValueError(String message) {
			super(message);
		}
	}
	
	public static <T> int numElements( ArrayList<T> list) {
		return list.size();
	}
	
	public static DMatrixRMaj ones( int r, int c ) {
		return new DMatrixRMaj(r, c);
	}
	
	public static int numElements( DMatrixRMaj m) {
		return m.getNumElements();
	}

	public static int numRows( DMatrixRMaj m) {
		return m.getNumRows();
	}

	public static int numCols( DMatrixRMaj m) {
		return m.getNumCols();
	}

}
