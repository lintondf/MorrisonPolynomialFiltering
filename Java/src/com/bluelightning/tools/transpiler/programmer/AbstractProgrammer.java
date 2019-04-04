/**
 * 
 */
package com.bluelightning.tools.transpiler.programmer;

import java.util.HashMap;
import java.util.Map;
import java.util.Stack;

import com.bluelightning.tools.transpiler.IProgrammer;
import com.bluelightning.tools.transpiler.Indent;
import com.bluelightning.tools.transpiler.Scope;
import com.bluelightning.tools.transpiler.Symbol;
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
		parameterRemap.put("RealVector", "RealVector&");
		parameterRemap.put("RealMatrix", "RealMatrix&");
		
		simpleRemaps.put("int", new Symbol(libraryScope, "int", "int")); //TODO generic
		simpleRemaps.put("max", new Symbol(libraryScope, "max", "int")); //TODO generic
		simpleRemaps.put("min", new Symbol(libraryScope, "min", "int")); //TODO generic
			Map<String, Symbol> libraryNames = new HashMap<>();
			libraryNames.put("array",  new Symbol(libraryScope, "identity", "array") ); 
			libraryNames.put("vector", new Symbol(libraryScope, "???vector_eye???", "vector") ); //Eigen
		functionRewrites.put("eye", libraryNames);
		
	}

	Scope libraryScope = new Scope();
	Map<String, String> typeRemap = new HashMap<>();
	Map<String, String> parameterRemap = new HashMap<>();
	
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
	public String remapType( Symbol symbol ) {
		String type = symbol.getType();
		if (type.startsWith("Tuple[")) {
			type = type.substring(6, type.length()-1).trim().replaceAll(" +", "");
			String[] fields = type.split(",");
			String tuple = "std::tuple<";
			for (String field : fields) {
				String t = typeRemap.get(field);
				if (t != null)
					field = t;
				tuple += field;
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
	public void writeSymbol(Indent out, Symbol symbol) {
		if (symbol.getName().equals("self")) {
			out.append("(*this)"); 
		} else if (symbol.isClassReference()) {
			out.append("(*" + symbol.getName() + ")" );
		} else {
			String name = symbol.getName(); 
			out.append(name);
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
		// TODO Auto-generated method stub
		return null;
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#getUsings()
	 */
	@Override
	public String[] getUsings() {
		// TODO Auto-generated method stub
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
		// TODO Auto-generated method stub

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
		out.append("(");  // C++ libraries uses () for array references
	} 

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#closeBracket(com.bluelightning.tools.transpiler.CppBoostTarget.Indent)
	 */
	@Override //General
	public void closeBracket(Indent out) {
		out.append(")");
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
		// TODO Auto-generated method stub
		return null;
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#getRowColSymbol(java.lang.String)
	 */
	@Override
	public Symbol getRowColSymbol(String value) {
		// TODO Auto-generated method stub
		return null;
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.IProgrammer#getSliceSymbol(java.lang.String)
	 */
	@Override
	public Symbol getSliceSymbol(String type) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public String remapParameter(String remappedType) {
		if (parameterRemap.containsKey(remappedType)) {
			remappedType = parameterRemap.get(remappedType);
		}
		return remappedType;
	}

	@Override
	public void addParameterClass(String className) {
		if (! parameterRemap.containsKey(className)) {
			parameterRemap.put(className, "std::shared_ptr<" + className + ">");
		}
	}

}
