/**
 * 
 */
package com.bluelightning.tools.transpiler;

import java.io.File;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;

import freemarker.template.Configuration;
import freemarker.template.Template;
import freemarker.template.TemplateException;

/**
 * @author NOOK
 *
 */
public class CppBoostTarget implements ILanguageTarget {
	
	protected Configuration cfg;  // FreeMarker configuration
	
	Path outputDirectory;
	
	Map<String, Object> templateDataModel = new HashMap<>();
	
	Template hpp;
	Template cpp;
	
	Path     hppFile;
	Path     cppFile;
	
	protected StringBuilder hppBody = new StringBuilder();
	protected StringBuilder cppBody = new StringBuilder();
	
	protected String define;
	
	public CppBoostTarget( Configuration cfg, Path outputDirectory ) {
		this.cfg = cfg;
		this.outputDirectory = outputDirectory;		
		try {
			
			hpp = cfg.getTemplate("CppBoost_hpp.ftlh");
			cpp = cfg.getTemplate("CppBoost_cpp.ftlh");
			
		} catch (IOException iox ) {
			iox.printStackTrace();
		}
	}

	@Override
	public void startModule(Scope scope) {
		System.out.println("CppBoost " + scope.toString() );
		
		String moduleName = scope.getLast();
		hppFile = outputDirectory.resolve( moduleName + ".hpp" );
		cppFile = outputDirectory.resolve( moduleName + ".cpp" );
		templateDataModel.put("scope", scope);
		define = String.format("__%sHPP", scope.toString().replace("/", "_").toUpperCase());
		templateDataModel.put("hppDefine", define);
		templateDataModel.put("systemIncludes", "");
		templateDataModel.put("localIncludes", "");
		templateDataModel.put("moduleInclude", hppFile.getFileName().toString());
		templateDataModel.put("systemIncludes", "");
		templateDataModel.put("hppBody", "");
		templateDataModel.put("cppBody", "");
	}
	
	String currentClass = null;

	@Override
	public void startClass(Scope scope) {
		currentClass = scope.getLast();
		// hpp
		hppBody.append( String.format("class %s {\n", currentClass));
	}

	@Override
	public void finishClass(Scope scope) {
		// hpp
		hppBody.append( String.format("}; // class %s \n", currentClass));
		currentClass = null;
	}

	@Override
	public void startMethod(Scope scope) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void finishMethod(Scope scope) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void emitExpressionStatement(Scope scope, TranslationNode root) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void finishModule() {
		templateDataModel.put("hppBody", hppBody.toString());
		templateDataModel.put("cppBody", cppBody.toString());
		try {
			Writer out = new OutputStreamWriter(System.out);
			System.out.println(hppFile.toString());
			hpp.process(templateDataModel, out);
			System.out.println(cppFile.toString());
			cpp.process(templateDataModel, out);
		} catch (IOException iox ) {
			iox.printStackTrace();
		} catch (TemplateException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
