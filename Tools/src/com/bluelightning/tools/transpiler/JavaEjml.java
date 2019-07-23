/**
 * 
 */
package com.bluelightning.tools.transpiler;

import org.ejml.data.*;
import org.ejml.equation.Equation;
import org.ejml.equation.Sequence;

public class JavaEjml {

	public static void main( String[] args) {
		Equation eq = new Equation();
		DMatrixRMaj P = new DMatrixRMaj(4,4);
		eq.alias(P,"P");
		Sequence s = eq.compile("P=eye(4)+1.0", true, true, true);
		s.perform();
		eq.compile("P = (0.5*P) + eye(4)/3.0", true, true, true).perform();
		P.print();
	}
}
