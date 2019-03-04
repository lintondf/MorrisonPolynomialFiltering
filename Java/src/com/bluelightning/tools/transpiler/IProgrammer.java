package com.bluelightning.tools.transpiler;

import com.bluelightning.tools.transpiler.CppTarget.Indent;

public interface IProgrammer {

	Symbol remapFunctionName(String functionName, String type);

	String remapType(String type);

	void startExpression(Indent out);

	void writeAssignmentTarget(Indent out, Symbol symbol);

	void finishExpression(Indent out);

	void writeSymbol(Indent out, Symbol symbol);

	void writeOperator(Indent out, String operator);

	void openParenthesis(Indent out);

	void closeParenthesis(Indent out);

	void openBracket(Indent out);

	void closeBracket(Indent out);

	void writeConstant(Indent out, TranslationConstantNode node);

}