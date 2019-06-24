/**
 * 
 */
package com.bluelightning.tools;

import org.apache.commons.math3.linear.Array2DRowRealMatrix;
import org.apache.commons.math3.linear.RealMatrix;
import org.apache.commons.math3.linear.RealVector;

/**
 * @author NOOK
 *
 */
public abstract class AbstractRadarCoordinates {
	
	public static double POW(double a, long b) {
		long re = 1;
		while (b > 0) {
			if ((b & 1) == 1) {
				re *= a;
			}
			b >>= 1;
			a *= a;
		}
		return re;
	}

	protected abstract double d1AzimuthdENU1(RealVector E, RealVector N, RealVector U);
	protected abstract double d2AzimuthdENU2(RealVector E, RealVector N, RealVector U);
	protected abstract double d3AzimuthdENU3(RealVector E, RealVector N, RealVector U);
	protected abstract double d4AzimuthdENU4(RealVector E, RealVector N, RealVector U);
	protected abstract double d5AzimuthdENU5(RealVector E, RealVector N, RealVector U);
	
	protected abstract double d1ElevationdENU1(RealVector E, RealVector N, RealVector U);
	protected abstract double d2ElevationdENU2(RealVector E, RealVector N, RealVector U);
	protected abstract double d3ElevationdENU3(RealVector E, RealVector N, RealVector U);
	protected abstract double d4ElevationdENU4(RealVector E, RealVector N, RealVector U);
	protected abstract double d5ElevationdENU5(RealVector E, RealVector N, RealVector U);
	
	protected abstract double d1RangedENU1(RealVector E, RealVector N, RealVector U);
	protected abstract double d2RangedENU2(RealVector E, RealVector N, RealVector U);
	protected abstract double d3RangedENU3(RealVector E, RealVector N, RealVector U);
	protected abstract double d4RangedENU4(RealVector E, RealVector N, RealVector U);
	protected abstract double d5RangedENU5(RealVector E, RealVector N, RealVector U);
	
	/** ENU2AER - convert site topocentric cartesian to spherical up to the 5th derivative
	 * ENU - East, North, Up; meters; origin at the site
	 * AER - Azimuth, Elevation, Range; radians, radians, meters; 
	 * 	azimuth clockwise from North, elevation, positive up
	 * @param E - east component [meters]; optionally derivatives up to the 5th
	 * @param N - north component [meters]; optionally derivatives up to the 5th
	 * @param U - up component [meters]; optionally derivatives up to the 5th
	 * @return AER - matrix; row 0 [azimuth,elevation,range]; rows 1+ corresponding derivatives
	 */
	public RealMatrix ENU2AER( RealVector E, RealVector N, RealVector U ) {
		RealMatrix AER = new Array2DRowRealMatrix( E.getDimension(), 3 );
		AER.setEntry(0,  0, Math.atan2(N.getEntry(0), E.getEntry(0)) % (2.0*Math.PI));  // azimuth
		AER.setEntry(0,  1, Math.atan2(U.getEntry(0), Math.sqrt(POW(E.getEntry(0),2) + POW(N.getEntry(0),2))));
		AER.setEntry(0,  2, Math.sqrt(POW(E.getEntry(0),2) + POW(N.getEntry(0),2) + POW(U.getEntry(0),2)));
		if (E.getDimension() > 1) {
			AER.setEntry(1, 0, d1AzimuthdENU1(E, N, U));
			AER.setEntry(1, 1, d1ElevationdENU1(E, N, U));
			AER.setEntry(1, 2, d1RangedENU1(E, N, U));
			if (E.getDimension() > 2) {
				AER.setEntry(2, 0, d2AzimuthdENU2(E, N, U));
				AER.setEntry(2, 1, d2ElevationdENU2(E, N, U));
				AER.setEntry(2, 2, d2RangedENU2(E, N, U));
				if (E.getDimension() > 3) {
					AER.setEntry(3, 0, d3AzimuthdENU3(E, N, U));
					AER.setEntry(3, 1, d3ElevationdENU3(E, N, U));
					AER.setEntry(3, 2, d3RangedENU3(E, N, U));
					if (E.getDimension() > 4) {
						AER.setEntry(4, 0, d4AzimuthdENU4(E, N, U));
						AER.setEntry(4, 1, d4ElevationdENU4(E, N, U));
						AER.setEntry(4, 2, d4RangedENU4(E, N, U));
						if (E.getDimension() > 5) {
							AER.setEntry(5, 0, d5AzimuthdENU5(E, N, U));
							AER.setEntry(5, 1, d5ElevationdENU5(E, N, U));
							AER.setEntry(5, 2, d5RangedENU5(E, N, U));
						}
					}
				}
			}
		}
		return AER;
	}
	
	protected abstract double d1EastdAER1(RealVector E, RealVector N, RealVector U);
	protected abstract double d2EastdAER2(RealVector E, RealVector N, RealVector U);
	protected abstract double d3EastdAER3(RealVector E, RealVector N, RealVector U);
	protected abstract double d4EastdAER4(RealVector E, RealVector N, RealVector U);
	protected abstract double d5EastdAER5(RealVector E, RealVector N, RealVector U);

	protected abstract double d1NorthdAER1(RealVector E, RealVector N, RealVector U);
	protected abstract double d2NorthdAER2(RealVector E, RealVector N, RealVector U);
	protected abstract double d3NorthdAER3(RealVector E, RealVector N, RealVector U);
	protected abstract double d4NorthdAER4(RealVector E, RealVector N, RealVector U);
	protected abstract double d5NorthdAER5(RealVector E, RealVector N, RealVector U);

	protected abstract double d1UpdAER1(RealVector E, RealVector N, RealVector U);
	protected abstract double d2UpdAER2(RealVector E, RealVector N, RealVector U);
	protected abstract double d3UpdAER3(RealVector E, RealVector N, RealVector U);
	protected abstract double d4UpdAER4(RealVector E, RealVector N, RealVector U);
	protected abstract double d5UpdAER5(RealVector E, RealVector N, RealVector U);

	/** AER2ENU - convert site spherical to topocentric cartesian up to the 5th derivative
	 * AER - Azimuth, Elevation, Range; radians, radians, meters; 
	 * 	azimuth clockwise from North, elevation, positive up
	 * ENU - East, North, Up; meters; origin at the site
	 * @param A - azimuth component [radians]; optionally derivatives up to the 5th
	 * @param E - elevation component [radians]; optionally derivatives up to the 5th
	 * @param R - range component [meters]; optionally derivatives up to the 5th
	 * @return AER - matrix; row 0 [east,north,up]; rows 1+ corresponding derivatives
	 */
	public RealMatrix AER2ENU( RealVector A, RealVector E, RealVector R ) {
		RealMatrix ENU = new Array2DRowRealMatrix( A.getDimension(), 3 );
		ENU.setEntry(0,  0, R.getEntry(0) * Math.cos(E.getEntry(0)) * Math.sin(A.getEntry(0)) );
		ENU.setEntry(0,  1, R.getEntry(0) * Math.cos(E.getEntry(0)) * Math.cos(A.getEntry(0)) );
		ENU.setEntry(0,  2, R.getEntry(0) * Math.sin(E.getEntry(0)) );
		if (A.getDimension() > 1) {
			ENU.setEntry(1, 0, d1EastdAER1(A, E, R));
			ENU.setEntry(1, 1, d1NorthdAER1(A, E, R));
			ENU.setEntry(1, 2, d1UpdAER1(A, E, R));
			if (A.getDimension() > 2) {
				ENU.setEntry(2, 0, d2EastdAER2(A, E, R));
				ENU.setEntry(2, 1, d2NorthdAER2(A, E, R));
				ENU.setEntry(2, 2, d2UpdAER2(A, E, R));
				if (A.getDimension() > 3) {
					ENU.setEntry(3, 0, d3EastdAER3(A, E, R));
					ENU.setEntry(3, 1, d3NorthdAER3(A, E, R));
					ENU.setEntry(3, 2, d3UpdAER3(A, E, R));
					if (A.getDimension() > 4) {
						ENU.setEntry(4, 0, d4EastdAER4(A, E, R));
						ENU.setEntry(4, 1, d4NorthdAER4(A, E, R));
						ENU.setEntry(4, 2, d4UpdAER4(A, E, R));
						if (A.getDimension() > 5) {
							ENU.setEntry(5, 0, d5EastdAER5(A, E, R));
							ENU.setEntry(5, 1, d5NorthdAER5(A, E, R));
							ENU.setEntry(5, 2, d5UpdAER5(A, E, R));
						}
					}
				}
			}
		}
		return ENU;
	}
}
