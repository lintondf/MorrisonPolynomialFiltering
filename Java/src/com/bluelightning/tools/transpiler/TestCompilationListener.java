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
	}

	@Override
	public void enterFuncdef(LcdPythonParser.FuncdefContext ctx) {
		//transpiler.dumpChildren(ctx);			
		Scope scope = Transpiler.instance().scopeMap.get(ctx.getPayload());
		Symbol func = Transpiler.instance().lookup(scope.getParent(), scope.getLast());
		if (func != null) {
			if (func.hasDecorator("@testcase")) {
				System.out.println("TESTCASE: " + func.toString() );
				Symbol symbol = Transpiler.instance().symbolTable.add(scope, "testData", "TestData");
				Symbol type = Transpiler.instance().lookup(new Scope(), "TestData");
				Transpiler.instance().inheritClassMembers(func, symbol);
				SourceCompilationListener source = new SourceCompilationListener(Transpiler.instance(), scope, ctx );
				Transpiler.instance().walker.walk(source, ctx);
			}
		}			
	}
	
}
