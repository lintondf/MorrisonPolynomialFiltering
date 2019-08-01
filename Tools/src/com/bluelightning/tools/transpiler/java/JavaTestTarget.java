/**
 * 
 */
package com.bluelightning.tools.transpiler.java;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.nio.file.Path;
import java.util.ArrayList;

import com.bluelightning.tools.transpiler.Indent;
import com.bluelightning.tools.transpiler.Scope;
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
		if (! inTest) {
			return;
		}
		super.startClass(scope);
	}

	@Override
	public void finishClass(Scope scope) {
		if (! inTest) {
			return;
		}
		super.finishClass(scope);
	}

	public JavaTestTarget(EjmlProgrammer programmer, Configuration cfg, Path baseDirectory) {
		super(programmer, cfg, baseDirectory);
		imports.add("org.ejml.data.DMatrixRMaj");
		imports.add("org.ejml.dense.row.CommonOps_DDRM");
	}

	boolean inTest = false;
	String moduleName = null;
	ArrayList<Scope> moduleTests = null;

	@Override
	public void startModule(Scope scope, boolean headerOnly, boolean isTest) {
		if (! isTest) {
			imports.clear();
			return;
		}
		inTest = true;
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
		//super.startModule(scope, headerOnly, isTest);
	}
	
	@Override
	public void finishModule() {
		if (! inTest) {
			return;
		}
		inTest = false;
		ExpressionCompiler.isTest = false;
	}
	
}
