/**
 * 
 */
package com.bluelightning.tools.transpiler.java;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.StringWriter;
import java.io.Writer;
import java.nio.file.Path;
import java.util.List;

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
public class JavaSrcTarget extends AbstractJavaTarget {

	public JavaSrcTarget(EjmlProgrammer programmer, Configuration cfg, Path baseDirectory) {
		super(programmer, cfg, baseDirectory);
		imports.add("org.ejml.data.DMatrixRMaj");
		imports.add("org.ejml.dense.row.CommonOps_DDRM");
	}

	boolean inTest = false;
	String moduleName = null;
	String packageName = null;

	@Override
	public void startModule(Scope scope, boolean headerOnly, boolean isTest) {
		if (isTest) {
			inTest = true;
			ExpressionCompiler.isTest = true;
			return;
		}
		System.out.println(String.format("\nJava/%s src: ", programmer.getName()) + scope.toAnnotatedString() );
		int containedClasses = 0;
		int staticFunctions = 0;
		List<Symbol> syms = Transpiler.instance().getSymbolTable().atScope(scope);
		for (Symbol s : syms) {
			if (s.isClass() && ! s.isInherited())
				containedClasses++;
			if (s.isFunction() && s.getScope().getLevel() == Scope.Level.MODULE)
				staticFunctions++;
		}
		if (containedClasses > 1  && ! scope.getLast().equals("Main")) {
			packageName = scope.getLast().toLowerCase();
			System.out.println("PACKAGE: " + packageName);
		}
		if (staticFunctions > 0) {
			System.out.printf("%s: %d classes; %d static functions\n", packageName, containedClasses, staticFunctions);
		}
	}
	
	@Override
	public void finishModule() {
		if (inTest) {
			inTest = false;
			ExpressionCompiler.isTest = false;
			return;
		}
		if (packageName != null) {
			if (indent.sb.length() > 0) {
//				System.out.println(currentScope);
//				System.out.println(indent.sb.toString());
				Symbol c = Transpiler.instance().getSymbolTable().add(currentScope, currentScope.getLast(), currentScope.getLast());
				c.setSuperClassInfo( new Symbol.SuperClassInfo() );
				String[] lines = indent.sb.toString().split("\n");
				indent = new Indent();
				startClass(currentScope);
				for (String line : lines) {
					indent.writeln(line);
				}
				finishClass(currentScope);
				System.out.println(indent.sb.toString());
			}
			packageName = null;
		}
	}

	@Override
	public void startClass(Scope scope) {
		if (inTest)
			return;
		currentScope = scope;
		indent = new Indent();
		moduleName = scope.getLast();
		srcPath = srcDirectory.resolve("src");
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
		super.startClass(scope);
	}

	@Override
	public void finishClass(Scope scope) {
		if (inTest)
			return;
		super.finishClass(scope);
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
	}

	@Override
	public boolean isTestTarget() {
		return false;
	}	
}
