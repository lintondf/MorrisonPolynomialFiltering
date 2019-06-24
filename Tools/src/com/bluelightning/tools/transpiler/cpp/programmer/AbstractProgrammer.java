/**
 * 
 */
package com.bluelightning.tools.transpiler.cpp.programmer;

import java.util.HashMap;
import java.util.Map;
import java.util.Stack;

import com.bluelightning.tools.transpiler.IProgrammer;
import com.bluelightning.tools.transpiler.Indent;
import com.bluelightning.tools.transpiler.Scope;
import com.bluelightning.tools.transpiler.Symbol;
import com.bluelightning.tools.transpiler.Transpiler;
import com.bluelightning.tools.transpiler.nodes.TranslationConstantNode;

/**
 * @author NOOK
 *
 */
public abstract class AbstractProgrammer implements IProgrammer {
	
	public AbstractProgrammer() {
		typeRemap.put("None", "void");
		typeRemap.put("int", "int");
		typeRemap.put("float", "double");
		typeRemap.put("vector", "RealVector");
		typeRemap.put("array", "RealMatrix");
		typeRemap.put("str", "std::string");	
		
		// try to avoid copies of matrix/vector parameters
		parameterTypeRemap.put("RealVector", "RealVector&");
		parameterTypeRemap.put("RealMatrix", "RealMatrix&");
		
		simpleRemaps.put("int", new Symbol(libraryScope, "int", "int")); //TODO generic
		simpleRemaps.put("max", new Symbol(libraryScope, "max", "int")); //TODO generic
		simpleRemaps.put("min", new Symbol(libraryScope, "min", "int")); //TODO generic
		simpleRemaps.put("chi2Cdf", new Symbol(libraryScope, "chi2Cdf", "float"));
		simpleRemaps.put("chi2Ppf", new Symbol(libraryScope, "chi2Ppf", "float"));
		simpleRemaps.put("ftestCdf", new Symbol(libraryScope, "ftestCdf", "float"));
		simpleRemaps.put("ftestPpf", new Symbol(libraryScope, "ftestPpf", "float"));
		simpleRemaps.put("assert_allclose", new Symbol(libraryScope, "assert_almost_equal", "float"));
			Map<String, Symbol> libraryNames = new HashMap<>();
			libraryNames.put("array",  new Symbol(libraryScope, "identity", "array") ); 
			libraryNames.put("vector", new Symbol(libraryScope, "???vector_eye???", "vector") ); //Eigen
		functionRewrites.put("eye", libraryNames);
		
		symbolRemap.put("self", "this");
		symbolRemap.put("True", "true");
		symbolRemap.put("False", "false");
		symbolRemap.put("None", "nullptr");
	}

	Scope libraryScope = new Scope();
	Map<String, String> typeRemap = new HashMap<>();
	Map<String, String> parameterTypeRemap = new HashMap<>(); // parameter type that should be by reference [typeName, typewithreference]
	Map<String, Scope>  pointerParameterRemap = new HashMap<>(); // parameter type that will be ptr wrapped [typeName, type scope]
	Map<String, String> symbolRemap = new HashMap<>();
	
	// index by function-name yields map indexed by type yields library name
	protected Map<String, Map<String,Symbol>> functionRewrites = new HashMap<>();
	protected Map<String, Symbol> simpleRemaps = new HashMap<>();
	
	Stack<String> parens = new Stack<>();

	protected boolean forceFloats = false;
	

	
	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#remapFunctionName(java.lang.String, java.lang.String)
	 */
	@Override //General
	public Symbol remapFunctionName( String functionName, String type ) {
		Symbol simple = simpleRemaps.get(functionName);
		if (simple != null)
			return simple;
		Map<String,Symbol> libraryNames = functionRewrites.get(functionName);
		if (libraryNames == null)
			return null;
		Symbol rename = libraryNames.get(type);
		if (rename == null)
			return null;
		return rename;
	}
	
	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#remapType(java.lang.String)
	 */
	@Override //General
	public String remapType( Scope currentScope, Symbol symbol ) {
		String type = remapTypeSymbol(currentScope, symbol);
		return type;
	}
	
	protected String remapTypeSymbol( Scope currentScope, Symbol symbol ) {
		String type = symbol.getType();
		if (type.startsWith("List[")) { 
			type = type.substring(5, type.length()-1).trim().replaceAll(" +", "");
			String[] fields = type.split(",");
			String vector = "std::vector<";
			for (String field : fields) {
				field = remapTypeString(currentScope, field);
				vector += field;
				vector += ", ";
			}
			vector = vector.substring(0, vector.length()-2) + ">"; // drop last ', ' close bracket
//			if (type.equals("str")) 
//				System.out.println(vector);
			return vector;
		}
		return remapTypeString( currentScope, type );
	}
	
	protected String remapTypeString( Scope currentScope, String typeName) {
		String t = typeRemap.get(typeName);
		if (t != null)
			return t;
		Symbol c = Transpiler.instance().lookupClass(typeName);
		if (c != null) {
			Scope typeScope = c.getScope();
			String prefix = typeScope.getVisiblityPrefix(currentScope);
			t = typeRemap.get(typeName);
			if (t != null)
				return t;
			if (! prefix.isEmpty()) {
				typeName = prefix.replace("/", "::") + typeName;
			}
			typeName = String.format("std::shared_ptr<%s>", typeName);
			return typeName;			
		} else {
			return typeName;
		}
	}
	
	@Override
	public String remapTypeParameter(Scope currentScope, String remappedType) {
		if (parameterTypeRemap.containsKey(remappedType)) {
			remappedType = parameterTypeRemap.get(remappedType);
			return remappedType;
		}
		Symbol c = Transpiler.instance().lookupClass(remappedType);
		if (c != null) {
			remappedType += "&";
		}
		return remappedType;
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#startExpression(com.bluelightning.tools.transpiler.CppBoostTarget.Indent)
	 */
	@Override //General
	public void startExpression( Indent out ) {
	}
	
	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#writeAssignmentTarget(com.bluelightning.tools.transpiler.CppBoostTarget.Indent, com.bluelightning.tools.transpiler.Symbol)
	 */
	@Override //General
	public void writeAssignmentTarget( Indent out, Symbol symbol) {
		out.append(symbol.getName());
		out.append(" = ");
	}
	
	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#finishExpression(com.bluelightning.tools.transpiler.CppBoostTarget.Indent)
	 */
	@Override //General
	public void finishExpression( Indent out ) {
		while (! parens.isEmpty() ) {
			out.append( parens.pop() );
		}
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#writeSymbol(com.bluelightning.tools.transpiler.CppBoostTarget.Indent, com.bluelightning.tools.transpiler.Symbol)
	 */
	@Override //General
	public String rewriteSymbol(Scope scope, Symbol symbol) {
		String rewrite = symbolRemap.get(symbol.getName());
		if (rewrite != null) {
			return rewrite;
		} else {
			String name = symbol.getName(); 
			Symbol c = Transpiler.instance().lookupClass(name);
			if (c != null) {
				String prefix = c.getScope().getVisiblityPrefix(scope).replace("/", "::");
				return prefix + name;
			} else {
				return name;
			}
		}
	}

	@Override //General
	public boolean isSpecialTerm(String operator, String lhsType, String rhsType) {
		//System.out.printf("isSpecial (%s) (%s) (%s)\n", operator, lhsType, rhsType);
		if (lhsType.equals("array") || lhsType.equals("vector")) {
			if (rhsType.equals("array") || rhsType.equals("vector")) {
				return true;
			}
		}
		if (operator.equals("**"))
			return true;
		return false;
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#getInclude()
	 */
	@Override
	public String getInclude() {
		return null;
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#getUsings()
	 */
	@Override
	public String[] getUsings() {
		return null;
	}


	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#writeOperator(com.bluelightning.tools.transpiler.CppBoostTarget.Indent, java.lang.String)
	 */
	@Override //General
	public void writeOperator(Indent out, String operator) {
		switch (operator) {
		case ".":
			out.append(operator);				
			break;
		case ",":
			out.append(operator);
			out.append(" ");
			break;
		case "@":
			out.append(" * ");
			break;
		case "::":
			out.append(operator);				
			break;
		case "->":
			out.append(operator);				
			break;
		case "or":
			out.append(" || ");
			break;
		case "and":
			out.append(" && ");
			break;
		default:
			out.append(" ");
			out.append(operator);
			out.append(" ");
			break;
		}
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#writeSpecialTerm(com.bluelightning.tools.transpiler.Indent, java.lang.String, com.bluelightning.tools.transpiler.Indent, com.bluelightning.tools.transpiler.Indent)
	 */
	@Override
	public void writeSpecialTerm(Indent out, String operator, Indent lhs, Indent rhs) {
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#openParenthesis(com.bluelightning.tools.transpiler.CppBoostTarget.Indent)
	 */
	@Override //General
	public void openParenthesis(Indent out) {
		out.append("(");
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#closeParenthesis(com.bluelightning.tools.transpiler.CppBoostTarget.Indent)
	 */
	@Override //General
	public void closeParenthesis(Indent out) {
		out.append(")");
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#openBracket(com.bluelightning.tools.transpiler.CppBoostTarget.Indent)
	 */
	@Override //General
	public void openBracket(Indent out) {
		out.append("[");  // C++ libraries uses () for array references
	} 

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#closeBracket(com.bluelightning.tools.transpiler.CppBoostTarget.Indent)
	 */
	@Override //General
	public void closeBracket(Indent out) {
		out.append("]");
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#writeConstant(com.bluelightning.tools.transpiler.CppBoostTarget.Indent, com.bluelightning.tools.transpiler.TranslationConstantNode)
	 */
	@Override //General
	public void writeConstant(Indent out, TranslationConstantNode node ) {
		switch (node.getKind()) {
		case INTEGER:
			out.append(node.getValue());
			if (forceFloats) {
				out.append(".");
			}
			break;
		case FLOAT:
			out.append(node.getValue());
			break;
		case STRING:
			String str = node.getValue();
			if (str.startsWith("'")) {  // convert to C++ double quoted
				str = str.substring(1, str.length()-1);
				str = str.replaceAll("\"", "\\\"");
				out.append( String.format("\"%s\"", str));
			} else {
				out.append( str );
			}
			break;
		}
	}

	
	@Override
	public void forceFloatConstants(boolean tf) {
		forceFloats = tf;
	}


	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#getDimensionSymbol(java.lang.String, java.lang.String)
	 */
	@Override
	public Symbol getDimensionSymbol(String type, String value) {
		return null;
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#getRowColSymbol(java.lang.String)
	 */
	@Override
	public Symbol getRowColSymbol(String value) {
		return null;
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#getSliceSymbol(java.lang.String)
	 */
	@Override
	public Symbol getSliceSymbol(String type) {
		return null;
	}

	@Override
	public void addParameterClass(String className) {
		if (! pointerParameterRemap.containsKey(className)) {
			Symbol c = Transpiler.instance().lookupClass(className);
			pointerParameterRemap.put(className, c.getScope());
		}
	}

	@Override
	public String remapSymbolUsages(Scope currentScope, Symbol symbol) {
		return symbol.getName();
	}

	
}
