/**
 * 
 */
package com.bluelightning.tools.transpiler;

import com.bluelightning.tools.transpiler.Scope.Level;
import com.bluelightning.tools.transpiler.antlr4.LcdPythonBaseListener;
import com.bluelightning.tools.transpiler.antlr4.LcdPythonParser;

/**
 * @author NOOK
 *
 */
public class TestCompilationListener extends LcdPythonBaseListener {

	/**
	 * 
	 */
	public TestCompilationListener() {
		if (Transpiler.instance().lookupClass("TestData") == null) {
			Scope scope = new Scope();
			Transpiler.instance().symbolTable.add(scope, "TestData", "<CLASS>");
			scope = scope.getChild(Level.CLASS, "TestData");
			Transpiler.instance().symbolTable.add(scope, "testDataPath", "str");
			Transpiler.instance().symbolTable.add(scope, "getMatchingGroups", "List[str]");
			Transpiler.instance().symbolTable.add(scope, "getGroupVariable", "array");
			Transpiler.instance().symbolTable.add(scope, "close", "None");
		}
	}

	@Override
	public void enterFuncdef(LcdPythonParser.FuncdefContext ctx) {
		//transpiler.dumpChildren(ctx);			
		Scope scope = Transpiler.instance().scopeMap.get(ctx.getPayload());
		Symbol func = Transpiler.instance().lookup(scope.getParent(), scope.getLast());
		if (func != null) {
			if (func.hasDecorator("@testcase")) {
				System.out.println("TESTCASE: " + func.toString() );
				SourceCompilationListener source = new SourceCompilationListener(Transpiler.instance(), scope, ctx );
				Transpiler.instance().walker.walk(source, ctx);
			}
		}			
	}
	
}
