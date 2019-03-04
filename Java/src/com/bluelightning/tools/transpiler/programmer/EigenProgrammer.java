/**
 * 
 */
package com.bluelightning.tools.transpiler.programmer;

import com.bluelightning.tools.transpiler.CppTarget;
import com.bluelightning.tools.transpiler.IProgrammer;
import com.bluelightning.tools.transpiler.Symbol;
import com.bluelightning.tools.transpiler.CppTarget.Indent;
import com.bluelightning.tools.transpiler.nodes.TranslationConstantNode;

/**
 * @author NOOK
 *
 */
public class EigenProgrammer implements IProgrammer {

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#remapFunctionName(java.lang.String, java.lang.String)
	 */
	@Override
	public Symbol remapFunctionName(String functionName, String type) {
		// TODO Auto-generated method stub
		return null;
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#remapType(java.lang.String)
	 */
	@Override
	public String remapType(String type) {
		// TODO Auto-generated method stub
		return null;
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#startExpression(com.bluelightning.tools.transpiler.CppTarget.Indent)
	 */
	@Override
	public void startExpression(Indent out) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#writeAssignmentTarget(com.bluelightning.tools.transpiler.CppTarget.Indent, com.bluelightning.tools.transpiler.Symbol)
	 */
	@Override
	public void writeAssignmentTarget(Indent out, Symbol symbol) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#finishExpression(com.bluelightning.tools.transpiler.CppTarget.Indent)
	 */
	@Override
	public void finishExpression(Indent out) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#writeSymbol(com.bluelightning.tools.transpiler.CppTarget.Indent, com.bluelightning.tools.transpiler.Symbol)
	 */
	@Override
	public void writeSymbol(Indent out, Symbol symbol) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#writeOperator(com.bluelightning.tools.transpiler.CppTarget.Indent, java.lang.String)
	 */
	@Override
	public void writeOperator(Indent out, String operator) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#openParenthesis(com.bluelightning.tools.transpiler.CppTarget.Indent)
	 */
	@Override
	public void openParenthesis(Indent out) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#closeParenthesis(com.bluelightning.tools.transpiler.CppTarget.Indent)
	 */
	@Override
	public void closeParenthesis(Indent out) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#openBracket(com.bluelightning.tools.transpiler.CppTarget.Indent)
	 */
	@Override
	public void openBracket(Indent out) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#closeBracket(com.bluelightning.tools.transpiler.CppTarget.Indent)
	 */
	@Override
	public void closeBracket(Indent out) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#writeConstant(com.bluelightning.tools.transpiler.CppTarget.Indent, com.bluelightning.tools.transpiler.TranslationConstantNode)
	 */
	@Override
	public void writeConstant(Indent out, TranslationConstantNode node) {
		// TODO Auto-generated method stub

	}

	@Override
	public String getInclude() {
		return "#include <polynomialfiltering/PolynomialFilteringEigen.hpp>";
	}

}
