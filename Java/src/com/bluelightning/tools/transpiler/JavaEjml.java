/**
 * 
 */
package com.bluelightning.tools.transpiler;

import org.ejml.data.*;
import org.ejml.equation.Equation;
import org.ejml.equation.Operation;
import org.ejml.equation.Sequence;

/**
 * @author linto
 * http://ejml.org/wiki/index.php?title=Download
 * Equation is list of Operations; precompile lines into static variables
 */
public class JavaEjml {

	public static void main( String[] args) {
		Equation eq = new Equation();
		DMatrixRMaj P = new DMatrixRMaj(4,4);
		eq.alias(P,"P");
		Sequence s = eq.compile("P=eye(4)+1.0", true, true);
//		for (Operation o : s.getOperations()) {
//			System.out.println(o); //.getClass().getSimpleName());
//			System.out.println(o.name());
//		}
		s.perform();
		eq.compile("P = (0.5*P) + eye(4)/3.0", true, true).perform();
		P.print();
	}
}
