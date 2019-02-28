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

import org.apache.commons.lang3.StringUtils;

import freemarker.template.Configuration;
import freemarker.template.Template;
import freemarker.template.TemplateException;

/**
 * @author NOOK
 *
 */
public class CppBoostTarget implements ILanguageTarget {
	
	protected int id;
	
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
	
	public static class Indent {
		int level = 0;
		public Indent() {
			level = 0;
		}
		
		public void in() {
			level += 1;
		}

		public void out() {
			level -= 1;
		}
		
		public String toString() {
			return StringUtils.repeat("  ", 4*level);
		}
	}
	
	protected Indent indent = new Indent();
	protected Scope currentScope = null;
	
	protected Map<String, String> typeRemap = new HashMap<>();
	
	public CppBoostTarget( Configuration cfg, Path outputDirectory ) {
		this.cfg = cfg;
		this.outputDirectory = outputDirectory;	
		
		typeRemap.put("int", "long");
		typeRemap.put("float", "double");
		typeRemap.put("vector", "RealVector");
		typeRemap.put("array", "RealMatrix");
		
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
		
		currentScope = scope;
		indent = new Indent();
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
		currentScope = scope;
		currentClass = scope.getLast();
		indent.in();
		// hpp
		hppBody.append( String.format("class %s {\n", currentClass));
	}

	@Override
	public void finishClass(Scope scope) {
		currentScope = scope;
		indent.out();
		// hpp
		hppBody.append( String.format("}; // class %s \n", currentClass));
		currentClass = null;
	}

	@Override
	public void startMethod(Scope scope) {
		currentScope = scope;
		indent.in();
		// TODO Auto-generated method stub
		
	}

	@Override
	public void finishMethod(Scope scope) {
		currentScope = scope;
		indent.out();
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

	protected void traverseEmitter(Scope scope, TranslationNode root) {
		for (TranslationNode node : root.getChildren()) {
			System.out.println(node.getClass().getSimpleName() + " " + node.toString() );
		}
	}
	
	@Override
	public void emitExpressionStatement(Scope scope, TranslationNode root) {
//		cppBody.append(scope.toString());
//		cppBody.append('\n');
//		cppBody.append(root.traverse(0));
//		cppBody.append('\n');
		cppBody.append(indent.toString());
		traverseEmitter( scope, root );
		cppBody.append('\n');
	}

	@Override
	public void emitSymbolDeclaration(Symbol symbol) {
		String cppType = typeRemap.get(symbol.getType());
		if (cppType == null) {
			cppType = symbol.getType();
		}
		String declaration = String.format("%s %s", cppType, symbol.getName() );
		switch (currentScope.getLevel()) {
		case MODULE: 
			cppBody.append( indent.toString() );
			cppBody.append( declaration );
			cppBody.append(";\n");
			break;
		case FUNCTION:
			cppBody.append( indent.toString() );
			cppBody.append( declaration );
			cppBody.append(";\n");
			break;
		case CLASS:
			hppBody.append( indent.toString() );
			hppBody.append( declaration );
			hppBody.append(";\n");
			
			cppBody.append( indent.toString() );
			cppBody.append( currentScope.getLast() + "::" + declaration );
			cppBody.append(";\n");
			break;
		case MEMBER:
			cppBody.append( indent.toString() );
			cppBody.append( declaration );
			cppBody.append(";\n");
			break;
		}
	}

	@Override
	public void setId(int id) {
		this.id = id;
	}

	@Override
	public int getId() {
		return id;
	}

}
