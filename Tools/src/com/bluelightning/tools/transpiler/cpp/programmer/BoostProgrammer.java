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

public class BoostProgrammer extends AbstractProgrammer {
	
	public BoostProgrammer() {
		super();

		Map<String, Symbol> boostNames = new HashMap<>();
		boostNames.put("array",  new Symbol(libraryScope, "identity_matrix<double>", "array") );
		boostNames.put("vector", new Symbol(libraryScope, "identity_vector<double>", "vector") );
		functionRewrites.put("eye", boostNames);
		boostNames = new HashMap<>();
		boostNames.put("array",  new Symbol(libraryScope, "zero_matrix<double>", "array"));
		boostNames.put("vector", new Symbol(libraryScope, "zero_vector<double>", "vector"));
		functionRewrites.put("zeros", boostNames);
	}
	

	@Override
	public String getInclude() {
		return "#include <polynomialfiltering/PolynomialFilteringBoost.hpp>";
	}

	@Override
	public String[] getUsings() {
		String[] usingNamespaces = {
				"using namespace boost::numeric::ublas;",	
			};
		return usingNamespaces;
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
	public void writeSpecialTerm(Indent out, String operator, Indent lhs, Indent rhs) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public Symbol getSliceSymbol(String type) {
		// TODO Auto-generated method stub
		return null;
	}


	@Override
	public String getName() {
		// TODO Auto-generated method stub
		return "Boost";
	}


	@Override
	public String remapSymbolUsages(Scope currentScope, Symbol symbol) {
		// TODO Auto-generated method stub
		return null;
	}

}