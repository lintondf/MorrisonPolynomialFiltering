/**
 * TODO remove _ from private methods (decl and use)
 */
package com.bluelightning.tools.transpiler.cpp;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.Stack;
import java.util.TreeSet;

import org.antlr.v4.runtime.ParserRuleContext;

import com.bluelightning.tools.transpiler.AbstractLanguageTarget;
import com.bluelightning.tools.transpiler.IProgrammer;
import com.bluelightning.tools.transpiler.IProgrammer.Measurement;
import com.bluelightning.tools.transpiler.Indent;
import com.bluelightning.tools.transpiler.Scope;
import com.bluelightning.tools.transpiler.SourceCompilationListener;
import com.bluelightning.tools.transpiler.Symbol;
import com.bluelightning.tools.transpiler.Transpiler;
import com.bluelightning.tools.transpiler.Scope.Level;
import com.bluelightning.tools.transpiler.Symbol.FunctionParametersInfo;
import com.bluelightning.tools.transpiler.nodes.TranslationConstantNode;
import com.bluelightning.tools.transpiler.nodes.TranslationListNode;
import com.bluelightning.tools.transpiler.nodes.TranslationNode;
import com.bluelightning.tools.transpiler.nodes.TranslationOperatorNode;
import com.bluelightning.tools.transpiler.nodes.TranslationSubexpressionNode;
import com.bluelightning.tools.transpiler.nodes.TranslationSymbolNode;
import com.bluelightning.tools.transpiler.nodes.TranslationUnaryNode;

import freemarker.template.Configuration;
import freemarker.template.Template;
import freemarker.template.TemplateException;


public abstract class AbstractCppTarget extends AbstractLanguageTarget {
	
	protected Configuration cfg;  // FreeMarker configuration
	
	Path includeDirectory;
	Path srcDirectory;
	Path testDirectory;

	protected List<String> includeFiles = new ArrayList<>();

	protected TreeSet<String> packageAsClass = new TreeSet<String>();

	Map<String, Object> templateDataModel = new HashMap<>();
	
	protected String define;
	
	Template hpp;
	Template cpp;
	Template test;
	
	Path     hppPath;
	Path     cppPath;
	
	protected Indent hppIndent = new Indent();
	protected Indent hppPrivate = new Indent();
	protected Indent cppIndent = new Indent();
	
	protected Scope currentScope = null;
	
	public AbstractCppTarget( IProgrammer programmer, Configuration cfg, Path baseDirectory ) {
		super();
		Path includeDirectory = baseDirectory.resolve("include");
		Path srcDirectory = baseDirectory.resolve("src");
		Path testDirectory = baseDirectory.resolve("test");
		this.cfg = cfg;
		this.includeDirectory = includeDirectory;	
		this.srcDirectory = srcDirectory;
		this.testDirectory = testDirectory;
		this.programmer = programmer;
		
		try {
			
			hpp = cfg.getTemplate("Hpp.ftlh");
			cpp = cfg.getTemplate("Cpp.ftlh");
			test = cfg.getTemplate("CppTest.ftlh");
			
		} catch (IOException iox ) {
			iox.printStackTrace();
		}
	}

	protected IProgrammer programmer = null;
	
	Stack<String> namespaceStack = new Stack<String>();
	
	protected void emitBracketedList(Indent out, Scope scope, TranslationNode child, String open) {
		if (open.equals("(")) {
			programmer.openParenthesis( out );
			for (int i = 0; i < child.getChildCount(); i++) {
				if (i == 0 && child.getChild(0) instanceof TranslationSymbolNode) {
					TranslationSymbolNode tsn = (TranslationSymbolNode) child.getChild(0);
					if (tsn.getSymbol().getName().equals("self"))
						continue;
				}
				if (child.getChild(i) instanceof TranslationOperatorNode)
					continue;
				i += emitChild( out, scope, child.getChild(i));
				if (i < child.getChildCount()-1) {
					out.append(", "); //->programmer
				}
			}
			programmer.closeParenthesis( out );
		} else {
			programmer.openParenthesis( out ); //programmer.openBracket( out );
			for (int i = 0; i < child.getChildCount(); i++) {
				if (i > 0) {
					out.append(", "); //->programmer
				}
				i += emitChild( out, scope, child.getChild(i));
			}
			programmer.closeParenthesis( out );// programmer.closeBracket( out );
		}
	}


	Symbol currentClass = null;
	String currentClassName = null;
	boolean inEnum = false;
	boolean isAbstract = false;
	boolean headerOnly = false;

	@Override
	public void startClass(Scope scope) {
		hppPrivate = new Indent();
		currentScope = scope;
		currentClassName = scope.getLast();
		// hpp
		String decl = "class " + currentClassName;
		Symbol symbol = Transpiler.instance().lookup(currentScope, currentClassName);
		currentClass = symbol;
		if (symbol != null) {
			if (symbol != null && symbol.getSuperClassInfo().superClasses != null) {
				String separator = " : ";
				for (String superClass : symbol.getSuperClassInfo().superClasses) {
					if (!ignoredSuperClasses.contains(superClass)) {
						Symbol sc = Transpiler.instance().lookup(currentScope, superClass);
						if (sc != null) {
							superClass = programmer.rewriteSymbol(currentScope, sc);							
						}
						decl += separator + "public " + superClass;
						separator = ", ";
					}
					if (superClass.equals("Enum")) {
						inEnum = true;
						decl = "enum " + currentClassName;
					}
				}
			}
		}
		
		Indent where = hppIndent;
		if (symbol.hasDecorator("@testclass")) {
			where = cppIndent;
		}
		String headerScope = currentScope.toString();
		String headerComments = Transpiler.instance().getDocumenter().getComments("Doxygen/C++", headerScope, hppIndent.get());
		if (headerComments != null) {
			headerComments = headerComments.replace("///// @brief", "///// @class " + currentClass + "\n" + hppIndent.get() +"/// @brief");
			where.append("\n");
			where.append(headerComments);
		}
		where.writeln( String.format("%s {", decl));
		where.in();
		if (! inEnum) {
			where.writeln("public:");
			where.in();
		}
		if (where != cppIndent) {
			cppIndent.in();
		}
	}

	@Override
	public void finishClass(Scope scope) {
		currentScope = scope;
		Indent where = hppIndent;
		if (currentClass != null && currentClass.hasDecorator("@testclass")) {
			where = cppIndent;
		}
		if (hppPrivate.sb.length() > 0) {
			
			where.out();
			where.writeln("protected:");
			where.in();
			String[] declarations = hppPrivate.sb.toString().split("\n");
			for (String decl : declarations) {
				where.writeln(decl);
			}
		}
		// hpp
		if (! inEnum) {
			where.out();
		}
		inEnum = false;
		where.out();
		where.writeln( String.format("}; // class %s \n", currentClassName));
		if (where != cppIndent) {
			cppIndent.out();
		}
		currentClass = null;
		currentClassName = null;
	}
	
	protected void writeMethodDeclaration( Indent head) {} 

	protected String getSuperClassInitializers( Symbol symbol, String className, Scope superScope) {
		Symbol c = Transpiler.instance().lookup(superScope, className);
		String superTag = "super().__init__(";
		String scInitializers = null;
		if (symbol.getType().startsWith(superTag)) {
			scInitializers = symbol.getType().substring(superTag.length());
			int iClose = -1;
			int nesting = 0;
			for (int i = 0; i < scInitializers.length(); i++) {
				if (scInitializers.charAt(i) == '(')
					nesting++;
				else if (scInitializers.charAt(i) == ')') {
					if (nesting == 0) {
						iClose = i;
						break;
					} else {
						nesting--;
					}
				}
			}
			if (iClose < 0) {
				Transpiler.instance().reportError("Bad function declaration: " + symbol.toString() );
				iClose = scInitializers.length();
			}
			scInitializers = scInitializers.substring(0, iClose);
		}
		return scInitializers;
	}
	
	@Override
	public void startMethod(Scope scope) {
		currentScope = scope;
		String currentFunction = scope.getLast();
		Scope functionScope = scope.getParent();
		Symbol symbol = Transpiler.instance().lookup(functionScope, currentFunction);
		if (symbol == null) {
			Transpiler.instance().reportError("startMethod::Unknown symbol: " + currentFunction + " " + functionScope );
		}
		Symbol.FunctionParametersInfo fpi = symbol.getFunctionParametersInfo();
		if (symbol != null && fpi != null) {
				String name = symbol.getName();
				String remappedType = programmer.remapType(currentScope, symbol); 
				String type = remappedType + " ";
				if (symbol.isConstructor()) {
					name = currentClass.getName();
					type = "";
				}
//				System.out.println(">>> " + currentClass + "::" + currentFunction + fpi.toString());
				Indent header = new Indent();
				Indent body = new Indent();
				for (Symbol parameter : fpi.parameters ) {
					if (parameter.getName().equals("self"))
						continue;
					if (header.sb.length() != 0) {
						header.append(", ");
						body.append(", ");
					}
					header.append("const ");
					remappedType = programmer.remapType(currentScope, parameter);
					remappedType = programmer.remapTypeParameter(currentScope, remappedType);
					header.append(remappedType);
					header.append(" ");
					header.append( parameter.getName() );
					body.append("const ");
					body.append(remappedType);
					body.append(" ");
					body.append( parameter.getName() );
					if (parameter.getInitialization() != null) {
						String value = parameter.getInitialization();
						TranslationConstantNode tcn = SourceCompilationListener.getConstantNode(null, value, value);
						header.append("=");
						if (tcn == null) {
							header.append("new ");
							header.append(value);
						} else {
							programmer.writeConstant(header, tcn);
						}
					}
				}
				
				Indent where = hppIndent;
				if (symbol.isPrivate()) {
					where = hppPrivate;
//					/System.out.printf("private %s %s %s\n", symbol.getName(), name, ""+symbol.isPrivate() );
				}
				String headerScope = symbol.getScope().toString() + symbol.getName() + "/";
				String headerComments = Transpiler.instance().getDocumenter().getComments("Doxygen/C++", headerScope, where.toString());
				if (headerComments != null) {
					where.append("\n");
					where.append(headerComments);
				}
				where.write( "" );
				String decl = String.format("%s%s(%s)", type, name, header.sb.toString() ); 
				if (fpi.decorators.contains("@staticmethod") || fpi.decorators.contains("@forcestatic")) {
					symbol.setStatic(true);
					where.append("static " + decl);
				} else if (fpi.decorators.contains("@abstractmethod") ||
						   fpi.decorators.contains("@virtual")) {
					where.append("virtual " + decl);
				} else {
					where.append(decl);
				}
				
				if (symbol.isConstructor() && this.headerOnly) {
					where.append(" {}");
				} else if (fpi.decorators.contains("@abstractmethod")) {
					where.append(" = 0");
					isAbstract = true;
				}
				where.append(";\n");
				
				if (! fpi.decorators.contains("@abstractmethod")) {
					decl = generateBodyDeclaration( type, currentClass, name, symbol.getScope(), body.sb.toString() );
					if (currentClass != null) {
						String separator = " : ";
						String manualSuper = Transpiler.instance().getManualSuper(symbol.getScope().toString(), "C++");
						if (manualSuper != null && name.equals(currentClassName)) {
							decl += separator + manualSuper;
						} else if (fpi.decorators.contains("@superClassConstructor")) { // decorator inserted by Declarations listener; not in Python source
							String className = symbol.getScope().getLast();
							Scope superScope = symbol.getScope().getParent();
							Symbol c = Transpiler.instance().lookup(superScope, className);
							String scInitializers = getSuperClassInitializers( symbol, className, superScope );
//							String superTag = "super().__init__(";
//							if (symbol.getType().startsWith(superTag)) {
//								scInitializers = symbol.getType().substring(superTag.length());
//								int iClose = scInitializers.indexOf(')');
//								if (iClose < 0) {
//									Transpiler.instance().reportError("Bad function declaration: " + symbol.toString() );
//									iClose = scInitializers.length();
//								}
//								scInitializers = scInitializers.substring(0, iClose);
//							}
							for (String sc : c.getSuperClassInfo().superClasses) {
								if (sc.charAt(0) != 'I' || Character.isLowerCase(sc.charAt(1))) { // ignore interfaces
									decl += separator + sc + "("; // TODO handle passing only relevant arguments
									decl += scInitializers;
									decl += ")";
								}
							}
						}
					}
					cppIndent.writeln( decl + " {");
				}
		}
		hppIndent.in();
		cppIndent.in();
	}
	
	protected String generateBodyDeclaration( String type, Symbol currentClass, String name, Scope scope, String parameters ) {
		if (currentClass != null) {
			name = currentClass.getName() + "::" + name;
			if (packageAsClass.contains(currentClass.getScope().getLast())) {
				name = currentClass.getScope().getLast() + "::" + name;
			}
		} else {
			if (packageAsClass.contains(scope.getLast())) {
				name = scope.getLast() + "::" + name;
			}
		}
		return String.format("%s%s (%s)", type, name, parameters );
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

	private int emitChild(Indent out, Scope scope, TranslationNode child, Symbol symbol) {
		if (symbol.getScope().getLevel() == Scope.Level.IMPORT) {
			String type = getAssignmentTargetType(child);
			Symbol rename = programmer.remapFunctionName( symbol.getName(), type );
			if (rename != null) {
				symbol = rename;
			}
			// special handling for array initialization
			if (symbol.getName().equals("array") || symbol.getName().equals("vector")) { 
				Indent gather = new Indent();
				while (child.getChildCount() == 0) {
					child = child.getRightSibling();
				}
				programmer.forceFloatConstants(true);
				traverseEmitter( gather, scope, child, 0 );
				programmer.forceFloatConstants(false);
				
				String values = gather.sb.toString(); 
				
				out.append( programmer.generateVectorInitializer( values ) );

				return 2;
			} else if (symbol.getName().equals("len")) {
				Indent gather = new Indent();
				while (child.getChildCount() == 0) {
					child = child.getRightSibling();
				}
				traverseEmitter( gather, scope, child, 0 );
				
				String values = gather.sb.toString(); 
				
				out.append(programmer.getMeasurement(values, Measurement.NUMBER_OF_ELEMENTS)); 
				return 2;
			}
		}
		if (symbol.getName().equals("self")) {
			if (child.getRightSibling() instanceof TranslationUnaryNode) {
				TranslationUnaryNode unary = (TranslationUnaryNode) child.getRightSibling();
				if (unary.getRhsSymbol() != null && unary.getRhsSymbol().isClassMethod()) {
					Symbol c = Transpiler.instance().lookup(symbol.getScope(), unary.getRhsSymbol().getScope().getLast());
					if (c != null && c.isClass()) 
						symbol = c;
				}
			}
		}
		Symbol c = Transpiler.instance().lookupClass(symbol.getName());
		if (c != null && child.getRightSibling() != null && child.getRightSibling() instanceof TranslationListNode) { // create an object
			String rewrite = programmer.rewriteSymbol( scope, symbol );
			emitNewExpression( scope, rewrite, child );
		} else if (symbol.isStatic()) {
			emitStaticSymbol( out, scope, symbol );
		} else {
			out.append( programmer.rewriteSymbol( scope, symbol ) );
		}
		return -1;
	}
	
	abstract protected void emitStaticSymbol( Indent out, Scope scope, Symbol symbol );
	
	protected int emitChild(Indent out, Scope scope, TranslationUnaryNode unary) {
		Symbol symbol = unary.getRhsSymbol();
		TranslationNode node = unary.getRhsNode();
		if (symbol != null) {
			if (symbol.isClassMethod()) {
				if (unary.getLeftSibling() != null && unary.getLeftSibling() instanceof TranslationSymbolNode) {
					TranslationSymbolNode s = (TranslationSymbolNode) unary.getLeftSibling();
					if (s.getSymbol().isClass()) {
						out.append("::");
						out.append(symbol.getName());
						return 0;
					}
				}
				programmer.writeOperator( out, "::" );
			} else {
				if (unary.getLeftSibling() != null && unary.getLeftSibling() instanceof TranslationUnaryNode) {
					TranslationUnaryNode u = (TranslationUnaryNode) unary.getLeftSibling();
					if (u.getRhsSymbol() != null) {
						Symbol type = Transpiler.instance().lookup(currentScope, u.getRhsSymbol().getType());
						if (type != null && type.isClass() && !type.isEnum()) {
							programmer.writeOperator( out, "->" );
						} else {
							programmer.writeOperator( out, unary.getLhsValue() );
						}
					}
				} else if (unary.getLeftSibling() != null && unary.getLeftSibling() instanceof TranslationSymbolNode) {
					TranslationSymbolNode s = (TranslationSymbolNode) unary.getLeftSibling();
					if (s.getSymbol().isClass()) {
						programmer.writeOperator( out, "::" );
					} else if (s.getSymbol().getName().equals("self") && symbol.isClass()) {
						out.deleteLast("this");
						out.append(String.format("std::make_shared<%s>", symbol.getName()));
						TranslationSubexpressionNode right = (TranslationSubexpressionNode) unary.getRightSibling();
						emitChild( out, scope, right );
						return 1;
					} else {
						Symbol type = Transpiler.instance().lookup(currentScope, s.getType());
						if (type != null && type.isClass() && !type.isEnum()) {
							programmer.writeOperator( out, "->" );
						} else {
							programmer.writeOperator( out, unary.getLhsValue() );
						}
					}
				} else if (unary.getLeftSibling() != null && unary.getLeftSibling() instanceof TranslationListNode) {
					TranslationListNode s = (TranslationListNode) unary.getLeftSibling();
					Symbol type = Transpiler.instance().lookupClass(s.getType()); 
					if (type != null && type.isClass() && !type.isEnum()) {
						programmer.writeOperator( out, "->" );
					} else {
						programmer.writeOperator( out, unary.getLhsValue() );
					}
				} else {
					programmer.writeOperator( out, unary.getLhsValue() );
				}
			}
			if (symbol.getName().equals("shape")) {
				if (unary.getRightSibling() == null) {
					Transpiler.instance().logger().error("No right sibling on 'shape'");
					return 1;
				}
				TranslationNode which = unary.getRightSibling().getFirstChild();
				if (which instanceof TranslationConstantNode) {
					TranslationNode left = unary.getLeftSibling();
					Symbol leftSymbol;
					if (left instanceof TranslationSymbolNode) {
						TranslationSymbolNode tsn = (TranslationSymbolNode) left;
						leftSymbol = tsn.getSymbol();
					} else if (left instanceof TranslationUnaryNode) {
						leftSymbol = ((TranslationUnaryNode) left).getRhsSymbol();
					} else {
						leftSymbol = null;
						Transpiler.instance().logger().error("Unexpected left-hand class: " + left.getClass());
						return 1;						
					}
					TranslationConstantNode tcn = (TranslationConstantNode) which;
					symbol = programmer.getDimensionSymbol( leftSymbol.getType(), tcn.getValue() );
					out.append( programmer.rewriteSymbol( scope, symbol ) );
					programmer.openParenthesis( out );
					programmer.closeParenthesis( out );
					return 1;
				}
			} else {
				out.append( programmer.rewriteSymbol( scope, symbol ) );
				if (unary.getChildCount() == 0 && unary.getRightSibling() == null && 
						symbol.getFunctionParametersInfo() != null) {
					programmer.openParenthesis( out );
					programmer.closeParenthesis( out );						
				}
			}
		} else if (node != null) {
			programmer.writeOperator( out, unary.getLhsValue() );
			emitChild( out, scope, unary.getRhsNode() );
		} else {
			Transpiler.instance().reportError(unary.getTop(), "Bad unary node: " + unary.toString() );
		}
		return -1;
	}
	
	
	protected int emitChild(Indent out, Scope scope, TranslationListNode tln) {
		if (tln.getListOpen().equals("(") && tln.getChildCount() == 0) {
			// may be ([...]) which compiles to LIST(:0, LIST[{LIST[...}
			TranslationNode next = tln.getRightSibling();
			if (next != null && next instanceof TranslationListNode) {
				return 0; // no skip
			}
		}
		if (tln.getListOpen().equals("[") && tln.getChildCount() == 1) {
			TranslationNode sublist = tln.getFirstChild();
			if (sublist != null && sublist instanceof TranslationListNode) {
				TranslationNode child = sublist;
				tln = (TranslationListNode) child;
			}
		}
		if (tln.getListOpen().equals("[")) {
			Symbol array = null;
			if (tln.getLeftSibling() instanceof TranslationSymbolNode) {
				array = ((TranslationSymbolNode) tln.getLeftSibling()).getSymbol();
			} else if (tln.getLeftSibling() instanceof TranslationUnaryNode) {
				array = ((TranslationUnaryNode) tln.getLeftSibling()).getRhsSymbol();
			}
			if ( tln.isArraySlice() ) {
				if (array == null) {
					Transpiler.instance().reportError(tln.getTop(), "Bracket list follows non-symbol");
					return 0;
				}
				Symbol slice = programmer.getSliceSymbol(array.getType());
				programmer.writeOperator(out, ".");
				switch (tln.getChildCount()) {
				case 0: 
					break;
					
				case 1: // [i] || [:]
					out.append( programmer.rewriteSymbol( scope, slice ) );
					programmer.openParenthesis( out );
					if (tln.getChild(0) instanceof TranslationOperatorNode) {  //->programmer
						// [:] -> block(0,0,rows(),cols()) / segment(0,size())
						if (array.getType().equals("vector")) {
							out.append("0, ");
							out.append(programmer.getMeasurement(array.getName(), Measurement.NUMBER_OF_ELEMENTS));
						} else {
							out.append("0, 0, ");
							out.append(programmer.getMeasurement(array.getName(), Measurement.NUMBER_OF_ROWS));
							out.append(", "); 								
							out.append(programmer.getMeasurement(array.getName(), Measurement.NUMBER_OF_COLUMNS));
						}
					} else {  //->programmer
						// [i:m] -> block(i,0,m,1) / segment(i,m)
						TranslationNode subscript = tln.getChild(0);							
						if (array.getType().equals("vector")) {
							emitChild(out, scope, subscript.getChild(0));
							out.append(", ");
							emitChild(out, scope, subscript.getChild(2));
						} else {
							emitChild(out, scope, subscript.getChild(0));
							out.append(", 0, ");
							emitChild(out, scope, subscript.getChild(2));
							out.append(", "); 								
							out.append("1 ");						
						}
					}
					break;
					
				case 2: // [:,j] || [i,:] || [i:n,j] || [i,j:m] || [i:n,j:m]
					if (tln.getChild(0) instanceof TranslationOperatorNode) {  // [:,j] - get column; [:,j:k] - get slice
						Symbol which = programmer.getRowColSymbol("1");
						out.append( programmer.rewriteSymbol( scope, which ) );
						programmer.openParenthesis( out );
						if (tln.getChild(1).getChildCount() > 0) {
							emitChild(out, scope, tln.getChild(1).getFirstChild());							
						} else {
							emitChild(out, scope, tln.getChild(1));
						}
					} else if (tln.getChild(1) instanceof TranslationOperatorNode) {  // [i,:] - get row; [j:k,:] - get slice
						if (tln.getChild(0).getChildCount() > 0) { // [i:n,:]
							out.append( programmer.rewriteSymbol( scope, slice ) );
							programmer.openParenthesis( out );
							TranslationNode subscript0 = tln.getChild(0);
							emitChild(out, scope, subscript0.getChild(0));
							out.append(", "); //->programmer
							out.append("0");
							out.append(", "); //->programmer
							emitChild(out, scope, subscript0.getChild(2));
							TranslationOperatorNode minus = new TranslationOperatorNode(tln.getParserRuleContext(), null, "-");
							emitChild(out, scope, minus);
							emitChild(out, scope, subscript0.getChild(0));								
							out.append(", "); 	 //->programmer															
							out.append(programmer.getMeasurement(array.getName(), Measurement.NUMBER_OF_COLUMNS));
						} else {
							Symbol which = programmer.getRowColSymbol("0");
							out.append( programmer.rewriteSymbol( scope, which ) );
							programmer.openParenthesis( out );
							emitChild(out, scope, tln.getChild(0));
						}
					} else { 
						/* [i:n,j]   LIST[2]{subscript[3]{expr,:,expr}, expr}
						 *    -> block(i, j, n, 1)
						 * [i,j:m]   LIST[2]{expr, subscript[3]{expr,:,expr}}
						 *    -> block(i, j, 1, m)
						 * [i:n,j:m] LIST[2]{subscript[3]{expr,:,expr}, subscript[3]{expr,:,expr}}
						 *    -> block(i,j,n,m)
						 */
						out.append( programmer.rewriteSymbol( scope, slice ) );
						programmer.openParenthesis( out );
						if (tln.getChild(0).getChildCount() > 0 && tln.getChild(1).getChildCount() > 0) { // [i:n,j:m]
							TranslationNode subscript0 = tln.getChild(0);
							TranslationNode subscript1 = tln.getChild(1);
							//TODO check child(1) is in fact :
							emitChild(out, scope, subscript0.getChild(0));
							out.append(", "); //->programmer
							emitChild(out, scope, subscript1.getChild(0));
							out.append(", "); //->programmer
							emitChild(out, scope, subscript0.getChild(2));
							TranslationOperatorNode minus = new TranslationOperatorNode(tln.getParserRuleContext(), null, "-");
							emitChild(out, scope, minus);
							emitChild(out, scope, subscript0.getChild(0));								
							out.append(", "); 	 //->programmer							
							emitChild(out, scope, subscript1.getChild(2));
							emitChild(out, scope, minus);
							emitChild(out, scope, subscript1.getChild(0));								
						} else if (tln.getChild(0).getChildCount() > 0) { // [i:n,j]
							TranslationNode subscript0 = tln.getChild(0);
							TranslationNode subscript1 = tln.getChild(1);
							emitChild(out, scope, subscript0.getChild(0));
							out.append(", "); //->programmer
							emitChild(out, scope, subscript1);
							out.append(", "); //->programmer
							emitChild(out, scope, subscript0.getChild(2));
							out.append(", 1 "); 	 //->programmer															
						} else if (tln.getChild(1).getChildCount() > 0) { // [i,j:m]
							TranslationNode subscript0 = tln.getChild(0);
							TranslationNode subscript1 = tln.getChild(1);
							out.append( programmer.rewriteSymbol( scope, slice ) );
							programmer.openParenthesis( out );
							emitChild(out, scope, subscript0);
							out.append(", "); //->programmer
							emitChild(out, scope, subscript1.getChild(0));								
							out.append(", 1,  "); //->programmer
							emitChild(out, scope, subscript1.getChild(2));
							TranslationOperatorNode minus = new TranslationOperatorNode(tln.getParserRuleContext(), null, "-");
							emitChild(out, scope, minus);
							emitChild(out, scope, subscript1.getChild(0));								
						} else {
							Transpiler.instance().reportError(tln.getParserRuleContext(), "Impossible slice/non-slice");
						}
					}
					break;
				}
				programmer.closeParenthesis( out );
				return 0;
			} else if (tln.getLeftSibling() != null) {  // non-slice access
				boolean isListAccess = false;
				if (tln.getLeftSibling() instanceof TranslationSymbolNode) {
					Symbol source = ((TranslationSymbolNode) tln.getLeftSibling()).getSymbol();
//					System.out.println("Symbol: " + source);
					if (source != null && source.getType().startsWith("List["))
						isListAccess = true;
				} else if (tln.getLeftSibling() instanceof TranslationUnaryNode) {
					Symbol source = ((TranslationUnaryNode) tln.getLeftSibling()).getRhsSymbol();
//					System.out.println("Unary: " + source);
					if (source != null && source.getType().startsWith("List["))
						isListAccess = true;
				}
//				System.out.println( tln.getLeftSibling().toString() );
//				System.out.println(tln.traverse(1)); ////@@
				if (isListAccess)
					programmer.openBracket(out);
				else
					programmer.openParenthesis( out );
				for (int i = 0; i < tln.getChildCount(); i++) {
					TranslationNode subscript = tln.getChild(i);
					if (i != 0)
						out.append(", "); //->programmer
					if (TranslationUnaryNode.isMinusOne(tln.getChild(i))) {
						//out.append(array.getName());
						if (i == 0) {
							out.append(programmer.getMeasurement(array.getName(), Measurement.NUMBER_OF_ROWS));
							out.append("-1");
						} else {
							out.append(programmer.getMeasurement(array.getName(), Measurement.NUMBER_OF_COLUMNS));
							out.append("-1");							
						}
					} else {
						emitChild(out, scope, tln.getChild(i));
					}
				}
				if (isListAccess)
					programmer.closeBracket(out);
				else
					programmer.closeParenthesis( out ); 
				return 0;
			}
		}
		String open = tln.getListOpen();
		emitBracketedList( out, scope, tln, open );
		return -1;
	}
	
	protected int emitChild(Indent out, Scope scope, TranslationNode child) { 
		if (child instanceof TranslationSymbolNode) {
			Symbol symbol = ((TranslationSymbolNode) child).getSymbol();
			int r = emitChild(out, scope, child, symbol);
			if (r >= 0)
				return r;
		} else if (child instanceof TranslationConstantNode) {
			programmer.writeConstant( out, (TranslationConstantNode) child );
		} else if (child instanceof TranslationOperatorNode) {
			TranslationOperatorNode ton = (TranslationOperatorNode) child;
			programmer.writeOperator( out, ton.getOperator());
		} else if (child instanceof TranslationUnaryNode) {
			TranslationUnaryNode unary = (TranslationUnaryNode) child;
			int r = emitChild(out, scope, unary);
			if (r >= 0)
				return r;
		} else if (child instanceof TranslationListNode) {
			TranslationListNode tln = (TranslationListNode) child;
			int r = emitChild(out, scope, tln);
			if (r >= 0)
				return r;
		} else {
			if (child instanceof TranslationSubexpressionNode) {
				if (child.getChildCount() == 0)
					return 0;
				TranslationSubexpressionNode tsn = (TranslationSubexpressionNode) child;
				if (tsn.getName().equals("SUBEXPRESSION::Term") ||
					tsn.getName().equals("SUBEXPRESSION::Power")) {
					String operator = ((TranslationOperatorNode) tsn.getChild(1)).getOperator();
					String lhsType =  ((TranslationSubexpressionNode) tsn.getChild(0)).getType();
					if (lhsType == null)
						lhsType = tsn.getType();
					String rhsType =  ((TranslationSubexpressionNode) tsn.getChild(2)).getType();
					if (rhsType == null)
						rhsType = tsn.getType();
					if (programmer.isSpecialTerm(operator, lhsType, rhsType)) {
						Indent lhs = new Indent();
						emitChild( lhs, scope, tsn.getChild(0));
						Indent rhs = new Indent();
						emitChild( rhs, scope, tsn.getChild(2));
						programmer.writeSpecialTerm(out, operator, lhs, rhs);
						return 0;
					}
				}
			}
			traverseEmitter( out, scope, child, 0);				
		}
		return 0;  // no skip;
	}
	
	protected void traverseEmitter(Indent out, Scope scope, TranslationNode root, int iChild) {
		while (iChild < root.getChildCount()) {
			TranslationNode child = root.getChild(iChild);
			iChild += emitChild(out, scope, child);
			iChild++;
		}
	}
	
	public void emitSubExpression(Indent out, Scope scope, TranslationNode root) {
		programmer.startExpression(out);
		if (root.getChildCount() == 0) {
			emitChild( out, scope, root);
		} else {
			if (root instanceof TranslationListNode) { // tuple
				emitBracketedList(out, scope, root.getFirstChild(), "/*eSE*/(" );
				return;
			} else if (root instanceof TranslationSubexpressionNode) {
				TranslationSubexpressionNode tsn = (TranslationSubexpressionNode) root;
				if (tsn.getName().equals("SUBEXPRESSION::Term") ||
					tsn.getName().equals("SUBEXPRESSION::Power")) {
					String operator = ((TranslationOperatorNode) tsn.getChild(1)).getOperator();
					String lhsType =  ((TranslationSubexpressionNode) tsn.getChild(0)).getType();
					if (lhsType == null)
						lhsType = tsn.getType();
					String rhsType =  ((TranslationSubexpressionNode) tsn.getChild(2)).getType();
					if (rhsType == null)
						rhsType = tsn.getType();
					if (programmer.isSpecialTerm(operator, lhsType, rhsType)) {
						Indent lhs = new Indent();
						emitChild( lhs, scope, tsn.getChild(0));
						Indent rhs = new Indent();
						emitChild( rhs, scope, tsn.getChild(2));
						programmer.writeSpecialTerm(out, operator, lhs, rhs);
						return;
					}
				}
			} 
			traverseEmitter( out, scope, root, 0 );
		}
		programmer.finishExpression(out);
	}

	
	@Override
	public void emitSubExpression(Scope scope, TranslationNode root) {
		emitSubExpression( cppIndent, scope, root);
	}
	
	@Override
	public void emitNewExpression(Scope scope, String className, TranslationNode root) {
		TranslationNode list = root.getRightSibling();
		if (list == null && root.getChildCount() >= 2) {
			list = root.getChild(1);
		}
		if (list == null) {
			System.out.println(root.traverse(1)); // TODO is this just an error?
			cppIndent.append( String.format("/*eNE?*/std::shared_ptr<%s>(new ", className)); //->programmer
			emitSubExpression( cppIndent, scope, root);
		} else {
			cppIndent.append( String.format("std::make_shared<%s>", className));
		}
	}
	
	protected boolean handleConstantArrayAssignment( Indent out, Scope scope, TranslationNode root ) {
		if (root.getChildCount() == 3) {
			if (root.getChild(0) instanceof TranslationSymbolNode &&
				root.getChild(1) instanceof TranslationOperatorNode &&
				root.getChild(2) instanceof TranslationSubexpressionNode) {
				TranslationSymbolNode target = (TranslationSymbolNode) root.getChild(0);
				TranslationOperatorNode ton = (TranslationOperatorNode) root.getChild(1);
				if (ton.getOperator().equals("=") && root.getChild(2).getChildCount() > 1) {
					TranslationNode node = root.getChild(2).getChild(0);
					if (node instanceof TranslationSymbolNode) {
						TranslationSymbolNode tsn = (TranslationSymbolNode) node;
						if (tsn.getSymbol().getName().equals("array") ||
							tsn.getSymbol().getName().equals("vector")	) {
							Indent gather = new Indent();
							while (node.getChildCount() == 0) {
								node = node.getRightSibling();
							}
							programmer.forceFloatConstants(true);
							traverseEmitter( gather, scope, node, 0 );
							programmer.forceFloatConstants(false);
							
							String values = gather.sb.toString();
							out.append(target.getSymbol().getName());
							out.append(" = ");
							out.append( programmer.generateVectorInitializer( values ) );
							return true;
						}
					}
				}
			}
			return false;
		}
		return false;
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
		if (! handleConstantArrayAssignment(out, scope, root)) {
			emitSubExpression( out, scope, root );
		}
		if (inEnum) {
			out.append(",");	 //->programmer		
		} else {
			out.append(";");    //->programmer
		}
		out.append("\n");
	}

	@Override
	public void emitSymbolDeclaration(Symbol symbol, String comment) {
		if ( symbol.isForVariable() )
			return;
		String cppType = programmer.remapType(currentScope, symbol);
		if (cppType == null) {
			cppType = symbol.getType();
		}
		if (cppType.equals("enum"))
			return;
//		Symbol type = Transpiler.instance().lookup(currentScope, cppType);
//		if (type != null && type.isClass() && !type.isEnum()) {
//			cppType = String.format("std::shared_ptr<%s>", cppType );
//		}
		String declaration = String.format("%s %s", cppType, symbol.getName() );
		String[] dims = symbol.getDimensions();
		if (dims != null) {
			declaration += "(";
			declaration += dims[0];
			if (dims.length > 1) {
				declaration += ", ";
				declaration += dims[1];
			}
			declaration += ")";
		}
		String endLine = ";";
		if (comment != null) {
			endLine = String.format("; ///< %s", comment);
		}
		switch (currentScope.getLevel()) {
		case MODULE: 
			cppIndent.writeln( declaration + endLine);
			break;
		case FUNCTION:
			cppIndent.writeln( declaration + endLine);
			break;
		case CLASS:
			//hppIndent.writeln( declaration + ";");
			hppPrivate.writeln( declaration + endLine);
			if (symbol.isStatic()) {
				cppIndent.writeln( String.format("%s %s::%s;", 
						cppType, currentScope.getLast(), symbol.getName()) );
			}
			break;
		case MEMBER:
			cppIndent.writeln( declaration + endLine);
			break;
		default:
		}
	}

	@Override
	public void emitRaiseStatement(String exception) {
		cppIndent.write("throw " + exception );
	}

	@Override
	public void emitReturnStatement(Scope scope, ParserRuleContext ctx, TranslationNode expressionRoot) {
		cppIndent.write("return ");
		emitSubExpression(scope, expressionRoot);
		finishStatement();
	}

	@Override
	public void startStatement() {
		cppIndent.write("");
	}
	
	
	@Override
	public void finishStatement() {
		cppIndent.append(";\n");
	}

	@Override
	public void emitIfStatement(Scope scope, TranslationNode expressionRoot) {
		cppIndent.write("if (");
		emitSubExpression( scope, expressionRoot.getFirstChild() );
		cppIndent.append(") {\n");
		cppIndent.in();
	}

	@Override
	public void emitElifStatement(Scope scope, TranslationNode expressionRoot) {
		cppIndent.out();
		cppIndent.write("} else if (");
		emitSubExpression( scope, expressionRoot.getFirstChild() );
		cppIndent.append(") {\n");
		cppIndent.in();
	}

	@Override
	public void emitElseStatement() {
		cppIndent.out();
		cppIndent.write("} else {\n");
		cppIndent.in();
	}

	@Override
	public void emitForStatement(Symbol symbol, TranslationNode atomExpr) {
//		System.out.println(atomExpr.traverse(1));
		TranslationSymbolNode tsn = (TranslationSymbolNode) atomExpr.getChild(0); // range
		TranslationListNode tln = (TranslationListNode) atomExpr.getChild(1);
		cppIndent.write( String.format("for (%s %s = ", 
				programmer.remapType( currentScope, symbol ), 
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
	
	@Override
	public void addImport(Scope scope) {
		StringBuilder includeFile = new StringBuilder();
		for (int i = 0; i < scope.getLevelCount()-1; i++) {
			String level = scope.getLevel(i).toLowerCase();
//			if (i > 0) {
				includeFile.append(level);
				includeFile.append('/');
//			}
		}
		String file = includeFile.toString();
		if (file.endsWith("/Main/")) {
			file = file.replace("/Main/", "/Main.hpp");
		} else {
			file += scope.getLast() + ".hpp";
		};
		for (String f : includeFiles) {
			if (f.equals(file))
				return;
		}
//		System.out.printf("INCLUDE %s\n", file);
		includeFiles.add(file);
	}


	@Override
	public void addParameterClass(String className) {
		programmer.addParameterClass(className);
	}

}
