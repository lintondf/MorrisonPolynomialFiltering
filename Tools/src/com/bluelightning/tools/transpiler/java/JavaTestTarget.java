/**
 * 
 */
package com.bluelightning.tools.transpiler.java;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.StringWriter;
import java.io.Writer;
import java.nio.file.Path;
import java.util.ArrayList;

import com.bluelightning.tools.transpiler.Indent;
import com.bluelightning.tools.transpiler.Scope;
import com.bluelightning.tools.transpiler.Symbol;
import com.bluelightning.tools.transpiler.Transpiler;
import com.bluelightning.tools.transpiler.Scope.Level;
import com.bluelightning.tools.transpiler.java.programmer.EjmlProgrammer;

import freemarker.template.Configuration;
import freemarker.template.TemplateException;

/**
 * @author lintondf
 *
 */
public class JavaTestTarget extends AbstractJavaTarget {

	@Override
	public void startClass(Scope scope) {
		System.out.println("jTT::sC " + scope);
		Symbol symbol = Transpiler.instance().lookup(scope, scope.getLast());
		symbol.setStatic(true);
		super.startClass(scope);
	}

	@Override
	public void finishClass(Scope scope) {
		if (! currentClass.isEmpty() && currentClass.peek().getName().equals(scope.getLast()) ) {
			System.out.println("jTT::fC " + currentClass.peek().getName() + " " + scope.getLast());
			super.finishClass(scope);
		}
	}

	public JavaTestTarget(EjmlProgrammer programmer, Configuration cfg, Path baseDirectory) {
		super(programmer, cfg, baseDirectory);
		imports.add("java.util.ArrayList");
		imports.add("org.ejml.data.DMatrixRMaj");
		imports.add("org.ejml.dense.row.CommonOps_DDRM");
		imports.add("utility.TestData");
	}

	String moduleName = null;
	ArrayList<Scope> moduleTests = null;

	@Override
	public void startModule(Scope scope, boolean headerOnly, boolean isTest) {
		ExpressionCompiler.isTest = true;
		System.out.println(String.format("\nJava/%s test: ", programmer.getName()) + scope.toString() );
		this.headerOnly = headerOnly;
		currentScope = scope;
		indent = new Indent();
		moduleName = scope.getLast();
		srcPath = srcDirectory.resolve("test");
		StringBuilder modulePackage = new StringBuilder();
		for (int i = 0; i < scope.getLevelCount()-1; i++) {
			String level = scope.getLevel(i).toLowerCase();
			if (i > 0) {
				modulePackage.append('.');
			}
			modulePackage.append(level);
			srcPath = srcPath.resolve(level);
		}
		srcPath = srcPath.resolve( moduleName + ".java" );
		System.out.println(srcPath.toString());
		
		templateDataModel.put("scope", scope);
		
		templateDataModel.put("package", String.format("package %s;", modulePackage.toString()));
		
		templateDataModel.put("class", "");
		
		Symbol s = Transpiler.instance().getSymbolTable().add( scope, moduleName, "<CLASS>");
		Symbol.SuperClassInfo sci = new Symbol.SuperClassInfo();
		s.setSuperClassInfo(sci);
		super.startClass(scope);
	}
	
	@Override
	public void finishModule() {
		//super.finishClass(currentScope);
		StringBuilder sb = new StringBuilder();
		for (String i : imports) {
			sb.append(String.format("import %s;\n", i));
		}
		templateDataModel.put("imports", sb.toString());
		templateDataModel.put("class", indent.sb.toString() );
		indent.sb = new StringBuilder();
		try {
			//System.out.println(hppFile.toString());
			StringWriter strOut = new StringWriter();
			java.process(templateDataModel, strOut);
			String old = readFileToString( srcPath );
			if (old == null || !old.equals(strOut.toString())) {
				srcPath.toFile().getParentFile().mkdirs();
				Writer out = new OutputStreamWriter(new FileOutputStream(srcPath.toFile()));
				out.write(strOut.toString());
				out.close();
			} else {
				System.out.println("  Unchanged: " + srcPath.toString() );
			}
		} catch (IOException iox ) {
			iox.printStackTrace();
		} catch (TemplateException e) {
			e.printStackTrace();
		}
		ExpressionCompiler.isTest = false;
	}

	@Override
	public void startMethod(Scope scope) {
		System.out.println("jTT::sM " + scope);
		currentScope = scope;
		moduleTests = new ArrayList<>();
		
		String currentFunction = scope.getLast();
		Symbol cls = Transpiler.instance().lookupClass(scope.getParent().getLast());
		if (cls == null || !cls.hasDecorator("@testclass")) {
			moduleTests.add(scope);
		}
		super.startMethod(scope);
	}
	
	@Override
	public boolean isTestTarget() {
		return true;
	}
	
}
