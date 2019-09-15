/**
 * 
 */
package com.bluelightning.tools.transpiler.java.programmer;

import java.util.Arrays;
import java.util.List;

import org.ejml.equation.ManagerTempVariables;

import com.bluelightning.tools.transpiler.Indent;
import com.bluelightning.tools.transpiler.Scope;
import com.bluelightning.tools.transpiler.Symbol;

/**
 * @author lintondf
 *
 */
public class EjmlProgrammer extends AbstractProgrammer {

	@Override
	public String getName() {
		return "Ejml";
	}

	@Override //Eigen?
	public void writeSpecialTerm(Indent out, String operator, Indent lhs, Indent rhs) {
		switch (operator) {
		case "*":
			out.append(lhs.sb.toString());
			out.append(" .* ");
			out.append(rhs.sb.toString());
			break;
		case "/":
			out.append(lhs.sb.toString());
			out.append(" ./ ");
			out.append(rhs.sb.toString());
			break;
		case "%":
			out.append("arrayMod(");
			out.append(lhs.sb.toString());
			out.append(", ");
			out.append(rhs.sb.toString());
			out.append(")");
			break;
		case "**":
			out.append("pow(");
			out.append(lhs.sb.toString());
			out.append(", ");
			out.append(rhs.sb.toString());
			out.append(")");
			break;
		case "@":
			out.append(lhs.sb.toString());
			out.append(" * ");
			out.append(rhs.sb.toString());
			break;
		default:
			out.append(lhs.sb.toString());
			out.append(" ");
			out.append(operator);
			out.append(" ");
			out.append(rhs.sb.toString());
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
	static Symbol rowDimension = new Symbol( new Scope(), "getNumRows", "int");
	static Symbol colDimension = new Symbol( new Scope(), "getNumCols", "int");
	static Symbol vectorDimension = new Symbol( new Scope(), "getNumElements", "int");
	static Symbol rowAccess = new Symbol( new Scope(), "row", "array");
	static Symbol colAccess = new Symbol( new Scope(), "col", "array");
	static Symbol vectorBlock = new Symbol( new Scope(), "segment", "vector");
	static Symbol arrayBlock = new Symbol( new Scope(), "block", "array");
	
	List<Pair> vectorMethods = Arrays.asList(
			new Pair[] {
					new Pair(vectorDimension.getName(), vectorDimension.getType()),
					new Pair(rowAccess.getName(), rowAccess.getType()),
			});
	List<Pair> matrixMethods = Arrays.asList(
			new Pair[] {
					new Pair(rowDimension.getName(), rowDimension.getType()),
					new Pair(colDimension.getName(), colDimension.getType()),
					new Pair(rowAccess.getName(), rowAccess.getType()),
					new Pair(colAccess.getName(), colAccess.getType()),
			});
	
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
	public String generateVectorInitializer(String values) {
		values = values.substring(1, values.length()-1 );
		return String.format("(new DMatrixRMaj(new double[] {%s}))", values); 
	}


	@Override
	public String getMeasurement(String symbol, Measurement which) {
		switch (which) {
		case NUMBER_OF_ELEMENTS:
			return String.format("numElements(%s)", symbol);
		case NUMBER_OF_ROWS:
			return String.format("numRows(%s)", symbol);
		case NUMBER_OF_COLUMNS:
			return String.format("numCols(%s)", symbol);
		default:
			return null;
		}
	}

	@Override
	public String getMatrixClass() {
		return "DMatrixRMaj";
	}

	@Override
	public String getVectorClass() {
		return "DMatrixRMaj";
	}
	
	@Override
	public String getTypeInitializer(String remappedType) {
		if (remappedType.equals(getMatrixClass())) {
			return String.format("new %s", getMatrixClass() );
		}
		if (remappedType.equals(getVectorClass())) {
			return String.format("new %s", getVectorClass() );
		}
		return super.getTypeInitializer(remappedType);
	}

	@Override
	public List<Pair> getVectorMethods() {
		return vectorMethods;
	}

	@Override
	public List<Pair> getMatrixMethods() {
		return matrixMethods;
	}

	@Override
	public IExpressionCompiler getExpressionCompiler( Scope scope, ManagerTempVariables tempManager, boolean isTestTarget ) {
		EjmlExpressionCompiler compiler = new EjmlExpressionCompiler(scope, this, tempManager, isTestTarget );
		return compiler;
	}

	public void addImports(List<String> imports) {
		imports.add("org.ejml.data.DMatrixRMaj");
		imports.add("org.ejml.dense.row.CommonOps_DDRM");
	}	
}
