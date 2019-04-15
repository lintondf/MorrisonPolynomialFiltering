package com.bluelightning.tools.transpiler;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.nio.file.Path;
import java.util.ArrayList;

import freemarker.template.Configuration;
import freemarker.template.TemplateException;

public class CppTestTarget extends AbstractCppTarget {

	public CppTestTarget(IProgrammer programmer, Configuration cfg, Path baseDirectory) {
		super(programmer, cfg, baseDirectory);
		// TODO Auto-generated constructor stub
	}

	boolean inTest = false;
	String moduleName = null;
	ArrayList<String> moduleTests = null;

	@Override
	public void startModule(Scope scope, boolean headerOnly, boolean isTest) {
		if (! isTest) {
			includeFiles.clear();
			return;
		}
		inTest = true;
		System.out.println(String.format("\nC++/%s test: ", programmer.getName()) + scope.toString() );
		this.headerOnly = headerOnly;
		
		moduleTests = new ArrayList<>();
		
		currentScope = scope;
		hppIndent = new Indent();
		hppPrivate = new Indent();
		cppIndent = new Indent();
		moduleName = scope.getLast();
		hppPath = testDirectory;
		cppPath = testDirectory;
//		StringBuilder moduleIncludeFile = new StringBuilder();
		for (int i = 0; i < scope.getLevelCount()-1; i++) {
			String level = scope.getLevel(i).toLowerCase();
//			if (i > 0) {
//				moduleIncludeFile.append(level);
//				moduleIncludeFile.append('/');
//			}
			hppPath = hppPath.resolve(level);
			cppPath = cppPath.resolve(level);
		}
//		moduleIncludeFile.append( moduleName + ".hpp" );
		hppPath = hppPath.resolve( moduleName + ".hpp" );
		cppPath = cppPath.resolve( moduleName + ".cpp" );
		System.out.println(hppPath.toString());
		if (!headerOnly) {
			System.out.println(cppPath.toString());
		}
		templateDataModel.put("scope", scope);
		define = String.format("__%sHPP", scope.toString().replace("/", "_").toUpperCase());
		templateDataModel.put("hppDefine", define);
		templateDataModel.put("systemIncludes", "");
		StringBuilder localIncludes = new StringBuilder();
		//localIncludes.append("#include <polynomialfiltering/Main.hpp>\n");
		for (String includeFile : includeFiles) {
			localIncludes.append(String.format("#include <%s>\n", includeFile));
		}
		templateDataModel.put("localIncludes", localIncludes.toString());
		templateDataModel.put("interfaceInclude", programmer.getInclude() + "\n");
		
		templateDataModel.put("moduleInclude", "");
		
		StringBuilder systemIncludes = new StringBuilder();
		systemIncludes.append("#include <math.h>\n");
		
		templateDataModel.put("systemIncludes", systemIncludes.toString());
		templateDataModel.put("hppBody", "");
		templateDataModel.put("cppBody", "");
		
		for (int i = 0; i < scope.getQualifiers().size()-1; i++) {
			cppIndent.write(String.format("namespace %s {\n", scope.getQualifiers().get(i)));
			namespaceStack.push(String.format("%s}; // namespace %s\n", hppIndent.toString(), scope.getQualifiers().get(i)));
			hppIndent.in();
			cppIndent.in();
		}
		cppIndent.write(String.format("namespace %s {\n", moduleName));
		namespaceStack.push(String.format("%s}; // namespace %s\n", cppIndent.toString(), moduleName));
		cppIndent.in();
		
		cppIndent.writeln("");
		for (String using : programmer.getUsings()) {
			cppIndent.writeln(using);
		}
		cppIndent.writeln("");
	}
	
	@Override
	public void finishModule() {
		if (! inTest) {
			return;
		}
		String qualifier = currentScope.toString().substring(1).replace("/", "::");
		while (! namespaceStack.isEmpty() ) {
			String close = namespaceStack.pop();
			hppIndent.append( close );
			cppIndent.append( close );
			hppIndent.out();
			cppIndent.out();
		}
		templateDataModel.put("cppBody", cppIndent.out.toString().replaceAll("\\(\\*([^\\)]*)\\)\\.", "$1->")); //.replace("(*this).", "this->"));
		
		Indent docIndent = new Indent();
		docIndent.append(String.format("TEST_CASE(\"%s\") {\n", moduleName ) );
		docIndent.in();
		for (String test : moduleTests) {
			docIndent.writeln( String.format("SUBCASE(\"%s\") {", test));
			docIndent.in();
			docIndent.writeln( String.format("%s%s();", qualifier, test  ) );
			docIndent.out();
			docIndent.writeln("}");
		}
		docIndent.out();
		docIndent.append("}\n");
		templateDataModel.put("doctest", docIndent.out.toString());
		try {
			cppPath.toFile().getParentFile().mkdirs();
			OutputStreamWriter out = new OutputStreamWriter(new FileOutputStream(cppPath.toFile()));
			test.process(templateDataModel, out);
			out.close();
		} catch (IOException iox ) {
			iox.printStackTrace();
		} catch (TemplateException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		inTest = false;
	}
	
	@Override
	public void startMethod(Scope scope) {
		if (inTest) {
			currentScope = scope;
			String currentFunction = scope.getLast();
			moduleTests.add(currentFunction);
		}
		super.startMethod(scope);
	}
	
	@Override
	protected String generateBodyDeclaration( String type, String currentClass, String name, String parameters ) {
		return String.format("%s%s (%s)", type, name, parameters );
	}

	
	
}
