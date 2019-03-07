/**
 * 
 */
package com.bluelightning.tools.transpiler.programmer;

import java.util.HashMap;
import java.util.Map;
import java.util.Stack;

import com.bluelightning.tools.transpiler.CppTarget;
import com.bluelightning.tools.transpiler.IProgrammer;
import com.bluelightning.tools.transpiler.Scope;
import com.bluelightning.tools.transpiler.Symbol;
import com.bluelightning.tools.transpiler.CppTarget.Indent;
import com.bluelightning.tools.transpiler.nodes.TranslationConstantNode;
import com.bluelightning.tools.transpiler.nodes.TranslationNode;

/**
 * @author NOOK
 *
 */
public class EigenProgrammer implements IProgrammer {

	public EigenProgrammer() {
		typeRemap.put("None", "void");
		typeRemap.put("int", "long");
		typeRemap.put("float", "double");
		typeRemap.put("vector", "RealVector");
		typeRemap.put("array", "RealMatrix");
		typeRemap.put("str", "std::string");	
		
		Scope libraryScope = new Scope();
		simpleRemaps.put("min", new Symbol(libraryScope, "std::min", "int")); //TODO generic
		Map<String, Symbol> eigenNames = new HashMap<>();
  		eigenNames.put("array",  new Symbol(libraryScope, "identity", "array") );
		eigenNames.put("vector", new Symbol(libraryScope, "???vector_eye???", "vector") );
		functionRewrites.put("eye", eigenNames);
		eigenNames = new HashMap<>();
		eigenNames.put("array",  new Symbol(libraryScope, "ArrayXXd::Zero", "array"));
		eigenNames.put("vector", new Symbol(libraryScope, "ArrayXd::Zero", "vector"));
		functionRewrites.put("zeros", eigenNames);
	}
	
	
	
	Stack<String> parens = new Stack<>();
	Map<String, String> typeRemap = new HashMap<>();
	
	// index by function-name yields map indexed by type yields boost name
	protected Map<String, Map<String,Symbol>> functionRewrites = new HashMap<>();
	protected Map<String, Symbol> simpleRemaps = new HashMap<>();

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#remapFunctionName(java.lang.String, java.lang.String)
	 */
	@Override
	public Symbol remapFunctionName( String functionName, String type ) {
		Symbol simple = simpleRemaps.get(functionName);
		if (simple != null)
			return simple;
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
		if (type.startsWith("Tuple[")) {
			type = type.substring(6, type.length()-1).trim().replaceAll(" +", "");
			String[] fields = type.split(",");
			String tuple = "std::tuple<";
			for (String field : fields) {
				tuple += remapType(field);
				tuple += ", ";
			}
			tuple = tuple.substring(0, tuple.length()-2) + ">";
			return tuple;
		}
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

	@Override
	public boolean isSpecialTerm(String operator, String lhsType, String rhsType) {
//		System.out.printf("isSpecial (%s) (%s) (%s)\n", operator, lhsType, rhsType);
		if (lhsType.equals("array") || lhsType.equals("vector")) {
			if (rhsType.equals("array") || rhsType.equals("vector")) {
				return true;
			}
		}
		return false;
	}

	@Override
	public void writeSpecialTerm(Indent out, String operator, Indent lhs, Indent rhs) {
		switch (operator) {
		case "*":
			out.append("arrayTimes(");
			out.append(lhs.out.toString());
			out.append(", ");
			out.append(rhs.out.toString());
			out.append(")");
			break;
		case "/":
			out.append("arrayDivide(");
			out.append(lhs.out.toString());
			out.append(", ");
			out.append(rhs.out.toString());
			out.append(")");
			break;
		case "%":
			out.append("arrayMod(");
			out.append(lhs.out.toString());
			out.append(", ");
			out.append(rhs.out.toString());
			out.append(")");
			break;
		case "@":
			out.append(lhs.out.toString());
			out.append(" * ");
			out.append(rhs.out.toString());
			break;
		default:
			out.append(lhs.out.toString());
			out.append(" ");
			out.append(operator);
			out.append(" ");
			out.append(rhs.out.toString());
			break;
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
		case "@":
			out.append(" * ");
			break;
		case "::":
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

	@Override
	public String getInclude() {
		return "#include <polynomialfiltering/PolynomialFilteringEigen.hpp>";
	}

	@Override
	public String[] getUsings() {
		String[] usingNamespaces = {
				"using namespace Eigen;",	
			};
		return usingNamespaces;
	}
	
	static Symbol rowDimension = new Symbol( new Scope(), "rows", "int");
	static Symbol colDimension = new Symbol( new Scope(), "cols", "int");
	static Symbol vectorDimension = new Symbol( new Scope(), "size", "int");
	static Symbol rowAccess = new Symbol( new Scope(), "row", "array");
	static Symbol colAccess = new Symbol( new Scope(), "col", "array");
	static Symbol vectorBlock = new Symbol( new Scope(), "segment", "vector");
	static Symbol arrayBlock = new Symbol( new Scope(), "block", "array");
	

	@Override
	public Symbol getDimensionSymbol(String type, String value) {
		if (type.equals("vector"))
			return vectorDimension;
		switch (value) {
		case "0":
			return rowDimension;
		case "1":
			return colDimension;
		}
		return null;
	}

	@Override
	public Symbol getRowColSymbol(String value) {
		switch (value) {
		case "0":
			return rowAccess;
		case "1":
			return colAccess;
		}
		return null;
	}

	@Override
	public Symbol getSliceSymbol(String type) {
		switch (type) {
		case "vector":
			return vectorBlock;
		case "array":
			return arrayBlock;
		}
		return null;
	}

}
