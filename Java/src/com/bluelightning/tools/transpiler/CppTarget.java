/**
 * TODO docstrings
 * TODO do not declare for loop variables
 */
package com.bluelightning.tools.transpiler;

import java.io.File;
import java.io.FileOutputStream;
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


public class CppTarget implements ILanguageTarget {
	
	protected int id;
	
	protected Configuration cfg;  // FreeMarker configuration
	
	Path includeDirectory;
	Path srcDirectory;
	
	Map<String, Object> templateDataModel = new HashMap<>();
	
	protected String define;
	
	public static class Indent {
		int level = 0;
		public StringBuilder out = new StringBuilder();;
		
		public Indent() {
			level = 0;
			this.out = out;
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
		
		public void append( String text ) {
			out.append(text);
		}
		
		public void write( String text ) {
			out.append(toString());
			out.append(text);
		}

		public void writeln( String text ) {
			out.append(toString());
			out.append(text);
			out.append('\n');
		}
	}
	
	Template hpp;
	Template cpp;
	
	Path     hppPath;
	Path     cppPath;
	
	protected Indent hppIndent = new Indent();
	protected Indent cppIndent = new Indent();
	
	
	
	protected Scope currentScope = null;
	
	Set<String> ignoredSuperClasses = new TreeSet<>();
	
	
	public CppTarget( IProgrammer programmer, Configuration cfg, Path includeDirectory, Path srcDirectory ) {
		this.cfg = cfg;
		this.includeDirectory = includeDirectory;	
		this.srcDirectory = srcDirectory;
		this.programmer = programmer;
		
		ignoredSuperClasses.add("ABC");
		
		try {
			
			hpp = cfg.getTemplate("CppBoost_hpp.ftlh");
			cpp = cfg.getTemplate("CppBoost_cpp.ftlh");
			
		} catch (IOException iox ) {
			iox.printStackTrace();
		}
	}

	protected IProgrammer programmer = null;
	
	Stack<String> namespaceStack = new Stack<String>();
	
	@Override
	public void startModule(Scope scope) {
		System.out.println("CppBoost " + scope.toString() );
		
		currentScope = scope;
		hppIndent = new Indent();
		cppIndent = new Indent();
		String moduleName = scope.getLast();
		hppPath = includeDirectory;
		cppPath = srcDirectory;
		StringBuilder moduleIncludeFile = new StringBuilder();
		for (int i = 0; i < scope.getLevelCount()-1; i++) {
			String level = scope.getLevel(i).toLowerCase();
			if (i > 0) {
				moduleIncludeFile.append(level);
				moduleIncludeFile.append('/');
			}
			hppPath = hppPath.resolve(level);
			cppPath = cppPath.resolve(level);
		}
		hppPath = hppPath.resolve( moduleName + ".hpp" );
		cppPath = cppPath.resolve( moduleName + ".cpp" );
		moduleIncludeFile.append( moduleName + ".hpp" );
		System.out.println(hppPath.toString());
		System.out.println(cppPath.toString());
		templateDataModel.put("scope", scope);
		define = String.format("__%sHPP", scope.toString().replace("/", "_").toUpperCase());
		templateDataModel.put("hppDefine", define);
		templateDataModel.put("systemIncludes", "");
		String localInclude = "#include <polynomialfiltering/Main.hpp>\n";
		templateDataModel.put("localIncludes", localInclude);
		templateDataModel.put("moduleInclude", moduleIncludeFile.toString());
		
		StringBuilder systemIncludes = new StringBuilder();
		systemIncludes.append("#include <math.h>\n");
		
		templateDataModel.put("systemIncludes", systemIncludes.toString());
		templateDataModel.put("hppBody", "");
		templateDataModel.put("cppBody", "");
		
		// start at 1 to skip import scope
		for (int i = 1; i < scope.qualifiers.length-1; i++) {
			hppIndent.write(String.format("namespace %s {\n", scope.qualifiers[i]));
			cppIndent.write(String.format("namespace %s {\n", scope.qualifiers[i]));
			namespaceStack.push(String.format("%s}; // namespace %s\n", hppIndent.toString(), scope.qualifiers[i]));
			hppIndent.in();
			cppIndent.in();
		}
		
		String[] usingNamespaces = {
			"using namespace boost::numeric::ublas;",	
		};
		for (String using : usingNamespaces) {
			cppIndent.writeln(using);
		}
		cppIndent.writeln("");
	}
	
	String currentClass = null;
	boolean inEnum = false;
	boolean isAbstract = false;

	@Override
	public void startClass(Scope scope) {
		currentScope = scope;
		currentClass = scope.getLast();
		// hpp
		String decl = "class " + currentClass;
		Symbol symbol = Transpiler.instance().symbolTable.lookup(currentScope, currentClass);
		if (symbol != null) {
			if (symbol != null && symbol.getSuperClassInfo().superClass != null) {
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
		hppIndent.writeln( String.format("%s {", decl));
		hppIndent.in();
		cppIndent.in();
		if (! inEnum) {
			hppIndent.writeln("public:");
			hppIndent.in();
		}
	}

	@Override
	public void finishClass(Scope scope) {
		currentScope = scope;
		// hpp
		if (! inEnum) {
			hppIndent.out();
		}
		inEnum = false;
		hppIndent.out();
		cppIndent.out();
		hppIndent.writeln( String.format("}; // class %s \n", currentClass));
		currentClass = null;
	}

	@Override
	public void startMethod(Scope scope) {
		currentScope = scope;
		String currentFunction = scope.getLast();
		Scope functionScope = scope.getParent();
		Symbol symbol = Transpiler.instance().symbolTable.lookup(functionScope, currentFunction);
		if (symbol == null) {
			Transpiler.instance().reportError("startMethod::Unknown symbol: " + currentFunction + " " + functionScope );
		}
		Symbol.FunctionParametersInfo fpi = symbol.getFunctionParametersInfo();
		if (symbol != null && fpi != null) {
			if (currentClass == null) { // non-class function
				Transpiler.instance().reportError("TODO non-class function");
			} else { // class member
				String name = symbol.getName();
				String type = programmer.remapType(symbol.getType()) + " ";
				if (name.equals("__init__")) {
					name = currentClass;
					type = "";
				}
//				System.out.println(">>> " + currentClass + "::" + currentFunction + fpi.toString());
				hppIndent.write( "" );
				Indent header = new Indent();
				Indent body = new Indent();
				for (Symbol parameter : fpi.parameters ) {
					if (parameter.getName().equals("self"))
						continue;
					if (header.out.length() != 0) {
						header.append(", ");
						body.append(", ");
					}
					header.append("const ");
					header.append(programmer.remapType(parameter.getType()));
					header.append(" ");
					header.append( parameter.getName() );
					body.append("const ");
					body.append(programmer.remapType(parameter.getType()));
					body.append(" ");
					body.append( parameter.getName() );
					if (parameter.getInitialization() != null) {
						String value = parameter.getInitialization();
						TranslationConstantNode tcn = ExpressionCompilationListener.getConstantNode(null, value, value);
						header.append("=");
						programmer.writeConstant(header, tcn);
					}
				}
				String decl = String.format("%s%s(%s)", type, name, header.out.toString() ); 
				if (fpi.decorators.contains("@classmethod")) {
					hppIndent.append("static " + decl);
				} else if (fpi.decorators.contains("@abstractmethod")) {
					hppIndent.append("virtual " + decl);
				} else {
					hppIndent.append(decl);
				}
				
				if (fpi.decorators.contains("@abstractmethod")) {
					hppIndent.append(" = 0");
					isAbstract = true;
				}
				hppIndent.append(";\n");
				if (! fpi.decorators.contains("@abstractmethod")) {
					decl = String.format("%s%s::%s (%s)", type, currentClass, name, body.out.toString() );
					if (fpi.decorators.contains("@superClassConstructor")) {
						String className = symbol.getScope().getLast();
						Scope superScope = symbol.getScope().getParent();
						Symbol c = Transpiler.instance().lookup(superScope, className);
						decl += " : " + c.getSuperClassInfo().superClass + "()";
					}
					cppIndent.writeln( decl + " {");
				}
			}
		}
		hppIndent.in();
		cppIndent.in();
	}

	@Override
	public void finishMethod(Scope scope) {
		currentScope = scope;
		hppIndent.out();
		cppIndent.out();
		if (!isAbstract) {
			cppIndent.writeln("}\n");
		}
		isAbstract = false;
	}

	@Override
	public void finishModule() {
		while (! namespaceStack.isEmpty() ) {
			String close = namespaceStack.pop();
			hppIndent.append( close );
			cppIndent.append( close );
			hppIndent.out();
			cppIndent.out();
		}
		templateDataModel.put("hppBody", hppIndent.out.toString());
		templateDataModel.put("cppBody", cppIndent.out.toString().replace("(*this).", "this->"));
		try {
			Writer out = new OutputStreamWriter(new FileOutputStream(hppPath.toFile()));
			//System.out.println(hppFile.toString());
			hpp.process(templateDataModel, out);
			out.close();
			
			out = new OutputStreamWriter(new FileOutputStream(cppPath.toFile()));
			cpp.process(templateDataModel, out);
			out.close();
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
	
	protected String getAssignmentTargetType( TranslationNode child ) {
		if (child.getTop() instanceof TranslationSubexpressionNode) {
			TranslationSubexpressionNode top = (TranslationSubexpressionNode) child.getTop();
			if (top.getChildCount() > 2) {
				if (top.getChild(1) instanceof TranslationOperatorNode) {
					if (((TranslationOperatorNode)top.getChild(1)).getOperator().equals("=")) {
						TranslationNode lhs = top.getChild(0);
						while (lhs instanceof TranslationSubexpressionNode) {
							lhs = lhs.getChild(0);
						}
						// TODO self.name
						if (lhs instanceof TranslationSymbolNode) {
							Symbol s = ((TranslationSymbolNode) lhs).getSymbol();
							if (s.getName().equals("self")) {
								TranslationNode u = lhs.getRightSibling();
								if (u instanceof TranslationUnaryNode) {
									return ((TranslationUnaryNode) u).getType();
								} else {
									return s.getType();
								}
							} else {
								return s.getType();
							}
						}
					}
				}
			}
		}
		return null;
	}
	
	protected void emitBracketedList(Indent out, Scope scope, TranslationNode child, String open) {
		if (open.equals("(")) {
			programmer.openParenthesis( out );
			for (int i = 0; i < child.getChildCount(); i++) {
				if (i > 0) {
					out.append(", ");
				}
				emitChild( out, scope, child.getChild(i));
			}
			programmer.closeParenthesis( out );
		} else {
			programmer.openBracket( out );
			for (int i = 0; i < child.getChildCount(); i++) {
				if (i > 0) {
					out.append(", ");
				}
				emitChild( out, scope, child.getChild(i));
			}
			programmer.closeBracket( out );
		}
	}


	
	protected void emitChild(Indent out, Scope scope, TranslationNode child) {
		if (child instanceof TranslationSymbolNode) {
			Symbol symbol = ((TranslationSymbolNode) child).getSymbol();
			if (symbol.getScope().getLevel() == Scope.Level.IMPORT) {
				String type = getAssignmentTargetType(child);
				System.out.println( symbol.getName() + "======" + child.getTop().toString() + " / " + type );
				System.out.println( child.getTop().traverse(1));
				Symbol rename = programmer.remapFunctionName( symbol.getName(), type );
				if (rename != null) {
					symbol = rename;
				}
			}
			programmer.writeSymbol( out, symbol );
		} else if (child instanceof TranslationConstantNode) {
			programmer.writeConstant( out, (TranslationConstantNode) child );
		} else if (child instanceof TranslationOperatorNode) {
			programmer.writeOperator( out, ((TranslationOperatorNode) child).getOperator() );
		} else if (child instanceof TranslationUnaryNode) {
			TranslationUnaryNode unary = (TranslationUnaryNode) child;
			programmer.writeOperator( out, unary.getLhs() );
			Symbol symbol = unary.getRhsSymbol();
			if (symbol != null) {
				programmer.writeSymbol( out, symbol );
			} else {
				System.out.println(unary);
			}
		} else if (child instanceof TranslationListNode) {
			TranslationListNode tln = (TranslationListNode) child;
			if (tln.getListOpen().equals("(") && tln.getChildCount() == 0) {
				// may be ([...]) which compiles to LIST(:0, LIST[{LIST[...}
				TranslationNode next = tln.getRightSibling();
				if (next != null && next instanceof TranslationListNode) {
					return;
				}
			}
			if (tln.getListOpen().equals("[") && tln.getChildCount() == 1) {
				TranslationNode sublist = tln.getFirstChild();
				if (sublist != null && sublist instanceof TranslationListNode) {
					child = sublist;
				}
			}
			String open = tln.getListOpen();
			emitBracketedList( out, scope, child, open );
		} else {
			traverseEmitter( out, scope, child, 0);				
		}
	}
	
	protected void traverseEmitter(Indent out, Scope scope, TranslationNode root, int iChild) {
		while (iChild < root.getChildCount()) {
			TranslationNode child = root.getChild(iChild);
			emitChild(out, scope, child);
			iChild++;
		}
	}
	
	public void emitSubExpression(Indent out, Scope scope, TranslationNode root) {
		programmer.startExpression(out);
		if (root.getChildCount() == 0) {
			emitChild( out, scope, root);
		} else {
			traverseEmitter( out, scope, root, 0 );
		}
		programmer.finishExpression(out);
	}

	
	@Override
	public void emitSubExpression(Scope scope, TranslationNode root) {
		emitSubExpression( cppIndent, scope, root);
	}
	
	@Override
	public void emitExpressionStatement(Scope scope, TranslationNode root) {
		Indent out = cppIndent;
		if (inEnum) {
			out = hppIndent;
			out.write( "" );
		} else {
			out.write( "" );
		}
		emitSubExpression( out, scope, root );
		if (inEnum) {
			out.append(",");			
		} else {
			out.append(";");
		}
		out.append("\n");
	}

	@Override
	public void emitSymbolDeclaration(Symbol symbol) {
		String cppType = programmer.remapType(symbol.getType());
		if (cppType == null) {
			cppType = symbol.getType();
		}
		if (cppType.equals("enum"))
			return;
		String declaration = String.format("%s %s", cppType, symbol.getName() );
		switch (currentScope.getLevel()) {
		case MODULE: 
			cppIndent.writeln( declaration + ";");
			break;
		case FUNCTION:
			cppIndent.writeln( declaration + ";");
			break;
		case CLASS:
			hppIndent.writeln( declaration + ";");
			if (symbol.isStatic()) {
				cppIndent.writeln( String.format("%s %s::%s;", 
						cppType, currentScope.getLast(), symbol.getName()) );
			}
			break;
		case MEMBER:
			cppIndent.writeln( declaration + ";");
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

	@Override
	public void emitReturnStatement() {
		cppIndent.write("return ");
//		System.out.println("return<"+cppIndent.out.toString() +">");
	}

	@Override
	public void emitCloseStatement() {
		cppIndent.append(";\n");
	}

	@Override
	public void emitForStatement(Symbol symbol, TranslationNode atomExpr) {
//		System.out.println(atomExpr.traverse(1));
		TranslationSymbolNode tsn = (TranslationSymbolNode) atomExpr.getChild(0); // range
		TranslationListNode tln = (TranslationListNode) atomExpr.getChild(1);
		cppIndent.write( String.format("for (%s %s = ", 
				programmer.remapType( symbol.getType() ), 
				symbol.getName()));
		emitSubExpression( symbol.getScope(), tln.getChild(0) );
		cppIndent.append( String.format("; %s < ", symbol.getName()));
		emitSubExpression( symbol.getScope(), tln.getChild(1) );
		cppIndent.append( String.format("; %s++) {\n", symbol.getName()) );
		cppIndent.in();
	}

	@Override
	public void closeBlock() {
		cppIndent.out();
		cppIndent.writeln( "}");
	}

}
