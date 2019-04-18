package com.bluelightning.tools.transpiler;

import com.bluelightning.tools.transpiler.nodes.TranslationConstantNode;
import com.bluelightning.tools.transpiler.nodes.TranslationNode;

public interface IProgrammer {
	
	String getName();
	
	String getInclude();
	
	String[] getUsings();
	
	void addParameterClass( String className );

	void startExpression(Indent out);

	void writeAssignmentTarget(Indent out, Symbol symbol);

	void finishExpression(Indent out);

	String rewriteSymbol(Scope scope, Symbol symbol);

	void writeOperator(Indent out, String operator );
	
	boolean isSpecialTerm( String operator, String lhsType, String rhsType );
	
	void writeSpecialTerm(Indent out, String operator, Indent lhs, Indent rhs );

	void openParenthesis(Indent out);

	void closeParenthesis(Indent out);

	void openBracket(Indent out);

	void closeBracket(Indent out);

	void writeConstant(Indent out, TranslationConstantNode node);
	
	void forceFloatConstants(boolean tf);

	Symbol getDimensionSymbol(String type, String value);

	Symbol getRowColSymbol(String value);

	Symbol getSliceSymbol(String type);

	Symbol remapFunctionName(String functionName, String type);

	String remapType(Scope currentScope, Symbol symbol);

	String remapTypeParameter(Scope currentScope, String remappedType);
	
	String remapSymbolUsages( Scope currentScope, Symbol symbol);

}