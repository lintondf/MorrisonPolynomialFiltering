package com.bluelightning.tools.transpiler.cpp;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.StringWriter;
import java.io.Writer;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.TreeSet;

import com.bluelightning.tools.transpiler.AbstractLanguageTarget;
import com.bluelightning.tools.transpiler.IProgrammer;
import com.bluelightning.tools.transpiler.Indent;
import com.bluelightning.tools.transpiler.Scope;
import com.bluelightning.tools.transpiler.Symbol;
import com.bluelightning.tools.transpiler.Transpiler;

import freemarker.template.Configuration;
import freemarker.template.TemplateException;

public class CppSrcTarget extends AbstractCppTarget {

	public CppSrcTarget(IProgrammer programmer, Configuration cfg, Path baseDirectory) {
		super(programmer, cfg, baseDirectory);
		packageAsClass = new TreeSet<String>( Arrays.asList(new String[] {"Emp", "Fmp"}));
	}
	
	boolean inTest = false;

	@Override
	public void startModule(Scope scope, boolean headerOnly, boolean isTest) {
		if (isTest) {
			inTest = true;
			return;
		}
		System.out.println(String.format("\nC++/%s src: ", programmer.getName()) + scope.toAnnotatedString() );
		System.out.println(includeFiles.toString());
		catalogContents( scope );
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
			namespaceStack.push(String.format("%s}; // namespace %s\n", hppIndent.get(), scope.getQualifiers().get(i)));
			hppIndent.in();
			cppIndent.in();
		}
		
		for (String using : programmer.getUsings()) {
			cppIndent.writeln(using);
		}

		if (packageAsClass.contains(scope.getLast())) {
			hppIndent.write(String.format("class %s {\n", scope.getLast()));
			hppIndent.in();
			hppIndent.writeln("public:");
		}
//		cppIndent.write(String.format("class %s {\n", scope.getLast()));
//		cppIndent.in();
		cppIndent.writeln("");
	}
	
	@Override
	public void finishModule() {
		if (inTest) {
			inTest = false;
			namespaceStack.clear();
			return;
		}
		if (packageAsClass.contains(currentScope.getLast())) {
			hppIndent.out();
			hppIndent.writeln("};");
		}
//		cppIndent.out();
//		cppIndent.writeln("};");
		while (! namespaceStack.isEmpty() ) {
			String close = namespaceStack.pop();
			hppIndent.append( close );
			cppIndent.append( close );
			hppIndent.out();
			cppIndent.out();
		}
		templateDataModel.put("hppBody", hppIndent.sb.toString());
		if (!headerOnly) {
			templateDataModel.put("cppBody", cppIndent.sb.toString().replaceAll("\\(\\*([^\\)]*)\\)\\.", "$1->")); //.replace("(*this).", "this->"));
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
				old = AbstractLanguageTarget.readFileToString( cppPath );
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
	
	@Override
	protected void emitStaticSymbol( Indent out, Scope scope, Symbol symbol ) {
		Symbol base = symbol.getBaseSymbol();
		if (base != null) {
			out.append( programmer.rewriteSymbol(scope, base));
		} else {
			String module = symbol.getScope().getLast();
			if (Transpiler.instance().getIgnoredModules().contains(module)) {
				out.append(symbol.getName());
			} else {
				out.append( String.format("%s::%s", module, symbol.getName()) );
			}
		}		
	}
	


	@Override
	public boolean isTestTarget() {
		return false;
	}

}
