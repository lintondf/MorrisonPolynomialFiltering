package com.bluelightning.tools.transpiler;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.nio.file.Path;

import freemarker.template.Configuration;
import freemarker.template.TemplateException;

public class CppSrcTarget extends AbstractCppTarget {

	public CppSrcTarget(IProgrammer programmer, Configuration cfg, Path baseDirectory) {
		super(programmer, cfg, baseDirectory);
	}
	
	boolean inTest = false;

	@Override
	public void startModule(Scope scope, boolean headerOnly, boolean isTest) {
		if (isTest) {
			inTest = true;
			return;
		}
		System.out.println(String.format("\nC++/%s src: ", programmer.getName()) + scope.toString() );
		this.headerOnly = headerOnly;
		
		currentScope = scope;
		hppIndent = new Indent();
		hppPrivate = new Indent();
		cppIndent = new Indent();
		String moduleName = scope.getLast();
		hppPath = includeDirectory;
		cppPath = srcDirectory;
		StringBuilder moduleIncludeFile = new StringBuilder();
		for (int i = 0; i < scope.getLevelCount()-1; i++) {
			String level = scope.getLevel(i).toLowerCase();
//			if (i > 0) {
				moduleIncludeFile.append(level);
				moduleIncludeFile.append('/');
//			}
			hppPath = hppPath.resolve(level);
			cppPath = cppPath.resolve(level);
		}
		hppPath = hppPath.resolve( moduleName + ".hpp" );
		cppPath = cppPath.resolve( moduleName + ".cpp" );
		moduleIncludeFile.append( moduleName + ".hpp" );
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
		includeFiles.clear();
		templateDataModel.put("localIncludes", localIncludes.toString());
		templateDataModel.put("interfaceInclude", programmer.getInclude() + "\n");
		
		templateDataModel.put("moduleInclude", moduleIncludeFile.toString());
		
		StringBuilder systemIncludes = new StringBuilder();
		systemIncludes.append("#include <math.h>\n");
		
		templateDataModel.put("systemIncludes", systemIncludes.toString());
		templateDataModel.put("hppBody", "");
		templateDataModel.put("cppBody", "");
		
		for (int i = 0; i < scope.getQualifiers().size()-1; i++) {
			hppIndent.write(String.format("namespace %s {\n", scope.getQualifiers().get(i)));
			cppIndent.write(String.format("namespace %s {\n", scope.getQualifiers().get(i)));
			namespaceStack.push(String.format("%s}; // namespace %s\n", hppIndent.toString(), scope.getQualifiers().get(i)));
			hppIndent.in();
			cppIndent.in();
		}
		
		for (String using : programmer.getUsings()) {
			cppIndent.writeln(using);
		}
		cppIndent.writeln("");
	}
	
	@Override
	public void finishModule() {
		if (inTest) {
			inTest = false;
			namespaceStack.clear();
			return;
		}
		while (! namespaceStack.isEmpty() ) {
			String close = namespaceStack.pop();
			hppIndent.append( close );
			cppIndent.append( close );
			hppIndent.out();
			cppIndent.out();
		}
		templateDataModel.put("hppBody", hppIndent.out.toString());
		if (!headerOnly) {
			templateDataModel.put("cppBody", cppIndent.out.toString().replaceAll("\\(\\*([^\\)]*)\\)\\.", "$1->")); //.replace("(*this).", "this->"));
		}
		try {
			hppPath.toFile().getParentFile().mkdirs();
			Writer out = new OutputStreamWriter(new FileOutputStream(hppPath.toFile()));
			//System.out.println(hppFile.toString());
			hpp.process(templateDataModel, out);
			out.close();
			if (!headerOnly) {
				cppPath.toFile().getParentFile().mkdirs();
				out = new OutputStreamWriter(new FileOutputStream(cppPath.toFile()));
				cpp.process(templateDataModel, out);
				out.close();
			}
		} catch (IOException iox ) {
			iox.printStackTrace();
		} catch (TemplateException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	
}
