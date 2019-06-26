/**
 * 
 */
package com.bluelightning.tools.transpiler.java.programmer;

import com.bluelightning.tools.transpiler.IProgrammer;
import com.bluelightning.tools.transpiler.Indent;
import com.bluelightning.tools.transpiler.Scope;
import com.bluelightning.tools.transpiler.Symbol;
import com.bluelightning.tools.transpiler.nodes.TranslationConstantNode;

/**
 * @author lintondf
 *
 */
public class AbstractProgrammer implements IProgrammer {

	@Override
	public String getName() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public String getInclude() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public String[] getUsings() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public void addParameterClass(String className) {
		// TODO Auto-generated method stub

	}

	@Override
	public void startExpression(Indent out) {
		// TODO Auto-generated method stub

	}

	@Override
	public void writeAssignmentTarget(Indent out, Symbol symbol) {
		// TODO Auto-generated method stub

	}

	@Override
	public void finishExpression(Indent out) {
		// TODO Auto-generated method stub

	}

	@Override
	public String rewriteSymbol(Scope scope, Symbol symbol) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public void writeOperator(Indent out, String operator) {
		// TODO Auto-generated method stub

	}

	@Override
	public boolean isSpecialTerm(String operator, String lhsType, String rhsType) {
		// TODO Auto-generated method stub
		return false;
	}

	@Override
	public void writeSpecialTerm(Indent out, String operator, Indent lhs, Indent rhs) {
		// TODO Auto-generated method stub

	}

	@Override
	public void openParenthesis(Indent out) {
		// TODO Auto-generated method stub

	}

	@Override
	public void closeParenthesis(Indent out) {
		// TODO Auto-generated method stub

	}

	@Override
	public void openBracket(Indent out) {
		// TODO Auto-generated method stub

	}

	@Override
	public void closeBracket(Indent out) {
		// TODO Auto-generated method stub

	}

	@Override
	public void writeConstant(Indent out, TranslationConstantNode node) {
		// TODO Auto-generated method stub

	}

	@Override
	public void forceFloatConstants(boolean tf) {
		// TODO Auto-generated method stub

	}

	@Override
	public Symbol getDimensionSymbol(String type, String value) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Symbol getRowColSymbol(String value) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Symbol getSliceSymbol(String type) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Symbol remapFunctionName(String functionName, String type) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public String remapType(Scope currentScope, Symbol symbol) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public String remapTypeParameter(Scope currentScope, String remappedType) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public String remapSymbolUsages(Scope currentScope, Symbol symbol) {
		// TODO Auto-generated method stub
		return null;
	}

}
