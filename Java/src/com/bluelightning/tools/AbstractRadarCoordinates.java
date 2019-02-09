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

	public static double POW(double a, double b) {
		return Math.pow(a, b);
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
	
	public RealMatrix ENU2AER( RealVector E, RealVector N, RealVector U ) {
		RealMatrix AER = new Array2DRowRealMatrix( E.getDimension(), 3 );
		AER.setEntry(0,  0, Math.atan2(N.getEntry(0), E.getEntry(0)));  // azimuth
		AER.setEntry(0,  1, Math.atan2(U.getEntry(0), Math.sqrt(POW(E.getEntry(0),2) + POW(N.getEntry(0),2))));
		AER.setEntry(0,  1, Math.sqrt(POW(E.getEntry(0),2) + POW(N.getEntry(0),2) + POW(U.getEntry(0),2)));
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
}
