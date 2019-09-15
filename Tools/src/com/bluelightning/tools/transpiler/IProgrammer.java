package com.bluelightning.tools.transpiler;

import java.util.AbstractMap;
import java.util.List;

import org.ejml.equation.ManagerTempVariables;

import com.bluelightning.tools.transpiler.java.AbstractJavaTarget.StaticImport;
import com.bluelightning.tools.transpiler.java.programmer.AbstractProgrammer;
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
	
	String getTypeInitializer( String remappedType );
	
	String remapSymbolUsages( Scope currentScope, Symbol symbol);

	String generateVectorInitializer(String values);
	
	public enum Measurement {NUMBER_OF_ELEMENTS, NUMBER_OF_ROWS, NUMBER_OF_COLUMNS };
	
	String getMeasurement( String symbol, Measurement which );
	
	public static class Pair {
		public Pair(String name, String type) {
			methodName = name;
			methodType = type;
		}
		public String methodName;
		public String methodType;
	}
	
	List<Pair> getVectorMethods();
	
	List<Pair> getMatrixMethods();
	
	public interface IExpressionCompiler {
		public void setStaticImports(List<StaticImport> staticImports);
		public boolean compile(String expression, List<String> imports, Scope currentScope );
		public List<String> getHeader();
		public List<String> getCode();
	}
	
	IExpressionCompiler getExpressionCompiler( Scope scope, ManagerTempVariables tempManager, boolean isTestTarget );

}