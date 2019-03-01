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
import java.util.Set;
import java.util.Stack;
import java.util.TreeSet;

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
			return StringUtils.repeat("  ", 2*level);
		}
		
		public void writeln( StringBuilder out, String text ) {
			out.append(toString());
			out.append(text);
			out.append('\n');
		}
	}
	
	protected Indent indent = new Indent();
	protected Scope currentScope = null;
	
	Set<String> ignoredSuperClasses = new TreeSet<>();
	
	
	public static class BoostProgrammer {
		
		Stack<String> parens = new Stack<>();
		private Map<String, String> typeRemap = new HashMap<>();
		
		public BoostProgrammer() {
			typeRemap.put("None", "void");
			typeRemap.put("int", "long");
			typeRemap.put("float", "double");
			typeRemap.put("vector", "RealVector");
			typeRemap.put("array", "RealMatrix");
			typeRemap.put("str", "std::string");			
		}
		
		public String remapType( String type ) {
			String t = typeRemap.get(type);
			if (t != null)
				return t;
			return type;
		}
		
		public void startExpression( StringBuilder out ) {
		}
		
		public void writeAssignmentTarget( StringBuilder out, Symbol symbol) {
			out.append(symbol.getName());
			out.append(" = ");
		}
		
		public void finishExpression( StringBuilder out ) {
			while (! parens.isEmpty() ) {
				out.append( parens.pop() );
			}
		}

		public void writeSymbol(StringBuilder out, Symbol symbol) {
			out.append(symbol.getName());
		}

		public void writeOperator(StringBuilder out, String operator) {
			out.append(operator);
		}

		public void openParenthesis(StringBuilder out) {
			out.append('(');
		}

		public void closeParenthesis(StringBuilder out) {
			out.append(')');
		}
	}
	
	public CppBoostTarget( Configuration cfg, Path outputDirectory ) {
		this.cfg = cfg;
		this.outputDirectory = outputDirectory;	
		
		ignoredSuperClasses.add("ABC");
		
		try {
			
			hpp = cfg.getTemplate("CppBoost_hpp.ftlh");
			cpp = cfg.getTemplate("CppBoost_cpp.ftlh");
			
		} catch (IOException iox ) {
			iox.printStackTrace();
		}
	}

	protected BoostProgrammer programmer = new BoostProgrammer();
	
	Stack<String> namespaceStack = new Stack<String>();
	
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
		hppBody = new StringBuilder();
		cppBody = new StringBuilder();
		
		for (int i = 0; i < scope.qualifiers.length-1; i++) {
			hppBody.append(indent.toString());
			hppBody.append(String.format("namespace %s {\n", scope.qualifiers[i]));
			cppBody.append(indent.toString());
			cppBody.append(String.format("namespace %s {\n", scope.qualifiers[i]));
			namespaceStack.push(String.format("%s}; // namespace %s\n", indent.toString(), scope.qualifiers[i]));
			indent.in();
		}
	}
	
	String currentClass = null;
	boolean inEnum = false;

	@Override
	public void startClass(Scope scope) {
		currentScope = scope;
		currentClass = scope.getLast();
		// hpp
		String decl = "class " + currentClass;
		Symbol symbol = Transpiler.instance().symbolTable.lookup(currentScope, currentClass);
		if (symbol != null) {
			if (symbol != null && !symbol.getSuperClassInfo().superClass.isEmpty()) {
				String superClass = symbol.getSuperClassInfo().superClass;
				if (!ignoredSuperClasses.contains(superClass)) {
					decl += " : public " + symbol.getSuperClassInfo().superClass;
				}
				if (superClass.equals("Enum")) {
					inEnum = true;
					decl = "enum " + currentClass;
				}
			}
		}
		hppBody.append( String.format("%s%s {\n", indent.toString(), decl));
		indent.in();
		indent.writeln(hppBody, "public:\n");
		indent.in();
	}

	@Override
	public void finishClass(Scope scope) {
		inEnum = false;
		currentScope = scope;
		// hpp
		indent.out();
		indent.out();
		hppBody.append( String.format("%s}; // class %s \n", indent.toString(), currentClass));
		currentClass = null;
	}

	@Override
	public void startMethod(Scope scope) {
		currentScope = scope;
		String currentFunction = scope.getLast();
		Symbol symbol = Transpiler.instance().symbolTable.lookup(currentScope.getParent(), currentFunction);
		Symbol.FunctionParametersInfo fpi = symbol.getFunctionParametersInfo();
		if (symbol != null && fpi != null) {
			if (currentClass == null) { // non-class function
				//TODO
			} else { // class member
				String name = symbol.getName();
				String type = programmer.remapType(symbol.getType()) + " ";
				if (name.equals("__init__")) {
					name = currentClass;
					type = "";
				}
				System.out.println(">>> " + currentClass + "::" + currentFunction + fpi.toString());
				hppBody.append( indent.toString() );
				StringBuilder p = new StringBuilder();
				for (Symbol parameter : fpi.parameters ) {
					if (parameter.getName().equals("self"))
						continue;
					if (p.length() != 0)
						p.append(", ");
					p.append("const ");
					p.append(programmer.remapType(parameter.getType()));
					p.append(" ");
					//TODO default values
					p.append( parameter.getName() );
				}
				String decl = String.format("%s%s(%s)", type, name, p.toString() ); 
				if (fpi.decorators.contains("@classmethod")) {
					hppBody.append("static ");
				}
				hppBody.append(decl);
				
				if (fpi.decorators.contains("@abstractmethod")) {
					hppBody.append(" = 0");
				}
				hppBody.append(";\n");
				if (! fpi.decorators.contains("@abstractmethod")) {
					decl = String.format("%s%s::%s (%s)", type, currentClass, name, p.toString() );
					if (fpi.decorators.contains("@classmethod")) {
						cppBody.append(" static");
					}
					cppBody.append(decl);
					cppBody.append(" {\n");
				}
			}
		}
		indent.in();		
	}

	@Override
	public void finishMethod(Scope scope) {
		currentScope = scope;
		indent.out();
		indent.writeln(cppBody, "}");
		// TODO Auto-generated method stub
		
	}

	@Override
	public void finishModule() {
		while (! namespaceStack.isEmpty() ) {
			String close = namespaceStack.pop();
			hppBody.append( close );
			cppBody.append( close );
			indent.out();
		}
		templateDataModel.put("hppBody", hppBody.toString());
		templateDataModel.put("cppBody", cppBody.toString());
		try {
			Writer out = new OutputStreamWriter(System.out);
			//System.out.println(hppFile.toString());
			hpp.process(templateDataModel, out);
			System.out.println();
			//System.out.println(cppFile.toString());
			cpp.process(templateDataModel, out);
			System.out.println();
		} catch (IOException iox ) {
			iox.printStackTrace();
		} catch (TemplateException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	protected boolean isList(TranslationNode root) {
		return (root instanceof TranslationListNode);
	}

	protected boolean isOperator(TranslationNode root, String op) {
		if (root instanceof TranslationOperatorNode) {
			return ((TranslationOperatorNode) root).getOperator().equals(op);
		}
		return false;
	}

	protected boolean isSymbol(TranslationNode root) {
		return (root instanceof TranslationSymbolNode);
	}
	
	protected void traverseEmitter(Scope scope, TranslationNode root, int iChild) {
		while (iChild < root.getChildCount()) {
			TranslationNode child = root.getChild(iChild);
			if (child instanceof TranslationSymbolNode) {
				programmer.writeSymbol( cppBody, ((TranslationSymbolNode) child).getSymbol() );
			} else if (child instanceof TranslationOperatorNode) {
				programmer.writeOperator( cppBody, ((TranslationOperatorNode) child).getOperator() );
			} else if (child instanceof TranslationListNode) {
				String open = ((TranslationListNode) child).getListOpen();
				if (open.equals("(")) {
					programmer.openParenthesis( cppBody );
					traverseEmitter( scope, child, 0);
					programmer.closeParenthesis( cppBody );
				}
			} else {
				traverseEmitter( scope, child, 0);				
			}
			iChild++;
		}
	}
	
	@Override
	public void emitExpressionStatement(Scope scope, TranslationNode root) {
//		cppBody.append(scope.toString());
//		cppBody.append('\n');
//		cppBody.append(root.traverse(0));
//		cppBody.append('\n');
		StringBuilder out = cppBody;
		if (inEnum)
			out = hppBody;
		out.append( indent.toString() );
		programmer.startExpression(out);
		cppBody.append(indent.toString());
		if (root.getChildCount() > 2 && isOperator(root.getChild(1), "=")) { // assignment
			if (isSymbol(root.getChild(0))) { // simple symbol
				Symbol symbol = ((TranslationSymbolNode)root.getChild(0)).getSymbol();
				programmer.writeAssignmentTarget(out, symbol);
				traverseEmitter( scope, root, 2 );
			} else {
				System.out.println("?1 " + root.getChild(0).getClass().getSimpleName() + " " + root.getChild(0).toString() );				
			}
		} else if (root.getChildCount() > 0) { // function call
			System.out.println("?2 " + root.getChild(0).getClass().getSimpleName() + " " + root.getChild(0).toString() );				
		}
		programmer.finishExpression(out);
		if (inEnum) {
			out.append(",");			
		} else {
			out.append(";");
		}

		out.append('\n');
	}

	@Override
	public void emitSymbolDeclaration(Symbol symbol) {
		String cppType = programmer.typeRemap.get(symbol.getType());
		if (cppType == null) {
			cppType = symbol.getType();
		}
		if (cppType.equals("enum"))
			return;
		String declaration = String.format("%s %s", cppType, symbol.getName() );
		switch (currentScope.getLevel()) {
		case MODULE: 
			indent.writeln(cppBody, declaration + ";");
			break;
		case FUNCTION:
			indent.writeln(cppBody, declaration + ";");
			break;
		case CLASS:
			indent.writeln(hppBody, declaration + ";");
			indent.writeln(cppBody, currentScope.getLast() + "::" + declaration + ";");
			break;
		case MEMBER:
			indent.writeln(hppBody, declaration + ";");
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
