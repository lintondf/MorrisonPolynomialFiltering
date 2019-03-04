package com.bluelightning.tools.transpiler;

import java.util.HashMap;
import java.util.Map;
import java.util.Stack;

import com.bluelightning.tools.transpiler.CppTarget.Indent;

public class BoostProgrammer implements IProgrammer {
	
	Stack<String> parens = new Stack<>();
	Map<String, String> typeRemap = new HashMap<>();
	
	// index by function-name yields map indexed by type yields boost name
	protected Map<String, Map<String,Symbol>> functionRewrites = new HashMap<>();
	
	public BoostProgrammer() {
		typeRemap.put("None", "void");
		typeRemap.put("int", "long");
		typeRemap.put("float", "double");
		typeRemap.put("vector", "RealVector");
		typeRemap.put("array", "RealMatrix");
		typeRemap.put("str", "std::string");	
		
		//Map<String, Symbol>  eye->identity_matrix<double>
		//                   zeros->zero_matrix<double> | zero_vector<double>
		
		Scope libraryScope = new Scope();
		Map<String, Symbol> boostNames = new HashMap<>();
		boostNames.put("array",  new Symbol(libraryScope, "identity_matrix<double>", "array") );
		boostNames.put("vector", new Symbol(libraryScope, "identity_vector<double>", "vector") );
		functionRewrites.put("eye", boostNames);
		boostNames = new HashMap<>();
		boostNames.put("array",  new Symbol(libraryScope, "zero_matrix<double>", "array"));
		boostNames.put("vector", new Symbol(libraryScope, "zero_vector<double>", "vector"));
		functionRewrites.put("zeros", boostNames);
	}
	
	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#remapFunctionName(java.lang.String, java.lang.String)
	 */
	@Override
	public Symbol remapFunctionName( String functionName, String type ) {
		Map<String,Symbol> boostNames = functionRewrites.get(functionName);
		if (boostNames == null)
			return null;
		Symbol rename = boostNames.get(type);
		if (rename == null)
			return null;
		return rename;
	}
	
	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#remapType(java.lang.String)
	 */
	@Override
	public String remapType( String type ) {
		String t = typeRemap.get(type);
		if (t != null)
			return t;
		return type;
	}
	
	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#startExpression(com.bluelightning.tools.transpiler.CppBoostTarget.Indent)
	 */
	@Override
	public void startExpression( Indent out ) {
	}
	
	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#writeAssignmentTarget(com.bluelightning.tools.transpiler.CppBoostTarget.Indent, com.bluelightning.tools.transpiler.Symbol)
	 */
	@Override
	public void writeAssignmentTarget( Indent out, Symbol symbol) {
		out.append(symbol.getName());
		out.append(" = ");
	}
	
	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#finishExpression(com.bluelightning.tools.transpiler.CppBoostTarget.Indent)
	 */
	@Override
	public void finishExpression( Indent out ) {
		while (! parens.isEmpty() ) {
			out.append( parens.pop() );
		}
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#writeSymbol(com.bluelightning.tools.transpiler.CppBoostTarget.Indent, com.bluelightning.tools.transpiler.Symbol)
	 */
	@Override
	public void writeSymbol(Indent out, Symbol symbol) {
		if (symbol.getName().equals("self")) {
			out.append("(*this)");  
		} else {
			String name = symbol.getName(); 
			out.append(name);
		}
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#writeOperator(com.bluelightning.tools.transpiler.CppBoostTarget.Indent, java.lang.String)
	 */
	@Override
	public void writeOperator(Indent out, String operator) {
		switch (operator) {
		case ".":
			out.append(operator);				
			break;
		case ",":
			out.append(operator);
			out.append(" ");
			break;
		default:
			out.append(" ");
			out.append(operator);
			out.append(" ");
			break;
		}
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#openParenthesis(com.bluelightning.tools.transpiler.CppBoostTarget.Indent)
	 */
	@Override
	public void openParenthesis(Indent out) {
		out.append("(");
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#closeParenthesis(com.bluelightning.tools.transpiler.CppBoostTarget.Indent)
	 */
	@Override
	public void closeParenthesis(Indent out) {
		out.append(")");
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#openBracket(com.bluelightning.tools.transpiler.CppBoostTarget.Indent)
	 */
	@Override
	public void openBracket(Indent out) {
		out.append("(");  // boost uses () for array references
	} 

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#closeBracket(com.bluelightning.tools.transpiler.CppBoostTarget.Indent)
	 */
	@Override
	public void closeBracket(Indent out) {
		out.append(")");
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#writeConstant(com.bluelightning.tools.transpiler.CppBoostTarget.Indent, com.bluelightning.tools.transpiler.TranslationConstantNode)
	 */
	@Override
	public void writeConstant(Indent out, TranslationConstantNode node ) {
		switch (node.getKind()) {
		case INTEGER:
			out.append(node.getValue());
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
}