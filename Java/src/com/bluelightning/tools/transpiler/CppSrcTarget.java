package com.bluelightning.tools.transpiler;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.StringWriter;
import java.io.Writer;
import java.nio.file.Files;
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
		System.out.println(String.format("\nC++/%s src: ", programmer.getName()) + scope.toAnnotatedString() );
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
			String level = scope.getLevel(i);
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
		systemIncludes.append("#include <vector>\n");
		systemIncludes.append("#include <string>\n");
		systemIncludes.append("#include <memory>\n");
		
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
	
	public static String readFileToString( Path path ) {
		try {
			byte[] bytes = Files.readAllBytes(path);
			String content = new String(bytes, "UTF-8");
			return content;
		} catch (Exception x) {
			return null;
		}
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
			//System.out.println(hppFile.toString());
			StringWriter strOut = new StringWriter();
			hpp.process(templateDataModel, strOut);
			String old = readFileToString( hppPath );
			if (old == null || !old.equals(strOut.toString())) {
				hppPath.toFile().getParentFile().mkdirs();
				Writer out = new OutputStreamWriter(new FileOutputStream(hppPath.toFile()));
				out.write(strOut.toString());
				out.close();
			} else {
				System.out.println("  Unchanged: " + hppPath.toString() );
			}
			if (!headerOnly) {
				strOut = new StringWriter();
				cpp.process(templateDataModel, strOut);
				old = readFileToString( cppPath );
				if (old == null || !old.equals(strOut.toString())) {
					cppPath.toFile().getParentFile().mkdirs();
					Writer out = new OutputStreamWriter(new FileOutputStream(cppPath.toFile()));
					out.write(strOut.toString());
					out.close();
				} else {
					System.out.println("  Unchanged: " + cppPath.toString() );
				}
			}
		} catch (IOException iox ) {
			iox.printStackTrace();
		} catch (TemplateException e) {
			e.printStackTrace();
		}
	}

}
