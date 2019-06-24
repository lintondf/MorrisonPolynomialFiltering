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
import com.bluelightning.tools.transpiler.cpp.AbstractCppTarget;
import com.bluelightning.tools.transpiler.nodes.TranslationConstantNode;
import com.bluelightning.tools.transpiler.nodes.TranslationNode;

/**
 * @author NOOK
 *
 */
public class EigenProgrammer extends AbstractProgrammer {

	public EigenProgrammer() {
		super();
			Map<String, Symbol>eigenNames = new HashMap<>();
			eigenNames.put("array",  new Symbol(libraryScope, "ArrayXXd::Zero", "array")); //Eigen
			eigenNames.put("vector", new Symbol(libraryScope, "ArrayXd::Zero", "vector")); //Eigen
		functionRewrites.put("zeros", eigenNames);
	}
	
	
	@Override //Eigen?
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
		case "**":
			out.append("pow(");
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
	
	@Override //Eigen
	public String getInclude() {
		return "#include <polynomialfiltering/PolynomialFilteringEigen.hpp>";
	}

	@Override //Eigen
	public String[] getUsings() {
		String[] usingNamespaces = {
				"using namespace Eigen;",	
			};
		return usingNamespaces;
	}
	
	//Eigen
	static Symbol rowDimension = new Symbol( new Scope(), "rows", "int");
	static Symbol colDimension = new Symbol( new Scope(), "cols", "int");
	static Symbol vectorDimension = new Symbol( new Scope(), "size", "int");
	static Symbol rowAccess = new Symbol( new Scope(), "row", "array");
	static Symbol colAccess = new Symbol( new Scope(), "col", "array");
	static Symbol vectorBlock = new Symbol( new Scope(), "segment", "vector");
	static Symbol arrayBlock = new Symbol( new Scope(), "block", "array");
	

	@Override //Eigen
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

	@Override //Eigen
	public Symbol getRowColSymbol(String value) {
		switch (value) {
		case "0":
			return rowAccess;
		case "1":
			return colAccess;
		}
		return null;
	}

	@Override //Eigen
	public Symbol getSliceSymbol(String type) {
		switch (type) {
		case "vector":
			return vectorBlock;
		case "array":
			return arrayBlock;
		}
		return null;
	}


	@Override
	public String getName() {
		return "Eigen";
	}

}
