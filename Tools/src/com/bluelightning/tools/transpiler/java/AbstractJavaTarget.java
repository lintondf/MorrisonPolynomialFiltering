/**
 * 
 */
package com.bluelightning.tools.transpiler.java;

import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Stack;
import java.util.TreeSet;

import org.antlr.v4.runtime.ParserRuleContext;
import org.ejml.equation.ManagerTempVariables;

import com.bluelightning.tools.transpiler.AbstractLanguageTarget;
import com.bluelightning.tools.transpiler.IProgrammer;
import com.bluelightning.tools.transpiler.Indent;
import com.bluelightning.tools.transpiler.Scope;
import com.bluelightning.tools.transpiler.Scope.Level;
import com.bluelightning.tools.transpiler.SourceCompilationListener;
import com.bluelightning.tools.transpiler.Symbol;
import com.bluelightning.tools.transpiler.Transpiler;
import com.bluelightning.tools.transpiler.IProgrammer.IExpressionCompiler;
import com.bluelightning.tools.transpiler.IProgrammer.Measurement;
import com.bluelightning.tools.transpiler.java.programmer.AbstractProgrammer;
import com.bluelightning.tools.transpiler.java.programmer.EjmlProgrammer;
import com.bluelightning.tools.transpiler.nodes.TranslationConstantNode;
import com.bluelightning.tools.transpiler.nodes.TranslationExpressionNode;
import com.bluelightning.tools.transpiler.nodes.TranslationListNode;
import com.bluelightning.tools.transpiler.nodes.TranslationNode;
import com.bluelightning.tools.transpiler.nodes.TranslationOperatorNode;
import com.bluelightning.tools.transpiler.nodes.TranslationSubexpressionNode;
import com.bluelightning.tools.transpiler.nodes.TranslationSymbolNode;
import com.bluelightning.tools.transpiler.nodes.TranslationUnaryNode;

import freemarker.template.Configuration;
import freemarker.template.Template;

/**
 * @author lintondf
 *
 */
public abstract class AbstractJavaTarget extends AbstractLanguageTarget{
	
	AbstractProgrammer programmer;
	Path 	    srcDirectory;
	Path        srcPath;
	Template    java;
	Map<String, Object> templateDataModel = new HashMap<>();
	ManagerTempVariables         tempManager;
	TreeSet<String> declaredTemps = new TreeSet<>();
	
	protected List<String> imports = new ArrayList<>();
	
	public static class StaticImport {
		public String name;
		public String type;
	}
	protected List<StaticImport> staticImports = new ArrayList<>();
	
	Indent      indent;

	protected Scope currentScope = null;
	
	Stack<Symbol> currentClass = new Stack<>();
	String currentClassName = null;
	boolean inEnum = false;
	boolean isAbstract = false;
	
	protected final Scope exceptionScope = new Scope()
			.getChild(Level.MODULE, "polynomialfiltering")
			.getChild(Level.MODULE, "main")
			.getChild(Level.CLASS, "Utility");

	public AbstractJavaTarget(EjmlProgrammer programmer, Configuration cfg, Path baseDirectory) {
		super();
		this.programmer = programmer;
		this.srcDirectory = baseDirectory;
		
		try {
			
			java = cfg.getTemplate("Java.ftlh");
			
		} catch (IOException iox ) {
			iox.printStackTrace();
		}
	}

	@Override
	public void startClass(Scope scope) {
		tempManager = new ManagerTempVariables();
		currentScope = scope;
		currentClassName = scope.getLast();
		String decl = "public ";
		Symbol symbol = Transpiler.instance().lookup(currentScope, currentClassName);
		currentClass.push( symbol );
		if (symbol != null) {
			if (symbol.isPrivate())
				decl = "private ";
			if (symbol.isStatic())
				decl += "static ";
			if (symbol.isAbstractClass())
				decl += "abstract ";
			decl += "class " + currentClassName;
			if (symbol != null && symbol.getSuperClassInfo().superClasses != null) {
				String separator = " extends ";
				for (String superClass : symbol.getSuperClassInfo().superClasses) {
					if (superClass.equals("Enum")) {
						inEnum = true;
						decl = decl.replace("class", "enum");
					} else if (!ignoredSuperClasses.contains(superClass)) {
						decl += separator + superClass;
						separator = " implements ";
						Symbol c = Transpiler.instance().lookupClass(superClass);
						if (c != null) {
							addImport( c.getScope().getChild(Level.CLASS, superClass));
						}
					}
				}
			}
		}
		String headerScope = currentScope.toString();
		String headerComments = Transpiler.instance().getDocumenter().getComments("Doxygen/C++", headerScope, indent.get());
		if (headerComments != null) {
			headerComments = headerComments.replace("///// @brief", "///// @class " + currentClassName + "\n" + indent.get() +"/// @brief");
			indent.append("\n");
			indent.append(headerComments);
		}
		
		indent.writeln(String.format("%s {", decl));
		indent.in();
	}

	@Override
	public void finishClass(Scope scope) {
		super.finishClass(scope);
		indent.out();
		indent.writeln("} // class " + scope.getLast());
		indent.writeln("");
		inEnum = false;
		currentClass.pop();
	}
	
	boolean headerOnly = false; //TODO?

	static class ParameterHandling {
		String name;
		String type;
		Indent value;
	};
	
	String lastConstructorClass = "";
	
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
		tempManager = new ManagerTempVariables();
		declaredTemps.clear();
		currentScope = scope;
		String currentFunction = scope.getLast();
		Scope functionScope = scope.getParent();
		Symbol symbol = Transpiler.instance().lookup(functionScope, currentFunction);
		if (symbol == null) {
			Transpiler.instance().reportError("startMethod::Unknown symbol: " + currentFunction + " " + functionScope );
			return;
		}
//		if (symbol.getScope().getLevel() == Scope.Level.MODULE) {
//			System.out.println(symbol);
//		}
		Symbol.FunctionParametersInfo fpi = symbol.getFunctionParametersInfo();
		if (symbol != null && fpi != null) {
				String name = symbol.getName();
				String remappedType = programmer.remapType(currentScope, symbol); 
				String type = remappedType + " ";
				Indent body = new Indent();
				if (symbol.isConstructor()) {
					name = currentClass.peek().getName();
					type = "";
					if (! name.equals(lastConstructorClass) && ! fpi.parameters.isEmpty() ) {
						if (fpi.parameters.size() > 1 || ! fpi.parameters.get(0).getName().equals("self")) {
							lastConstructorClass = name;
							indent.writeln();
							indent.writeln(String.format("public %s() {}  // auto-generated null constructor\n", name) );
						}
					}
				}
				int nOptional = 0;
				ArrayList<ParameterHandling> handling = new ArrayList<>();
				for (Symbol parameter : fpi.parameters ) {
					if (parameter.getName().equals("self")) {
						continue;
					}
					if (body.sb.length() != 0) {
						body.append(", ");
					}
					remappedType = programmer.remapType(currentScope, parameter);
					remappedType = programmer.remapTypeParameter(currentScope, remappedType);
					body.append("final ");
					body.append(remappedType);
					body.append(" ");
					body.append( parameter.getName() );
					ParameterHandling ph = new ParameterHandling();
					ph.name = parameter.getName();
					ph.type = remappedType;
					if (parameter.getInitialization() != null) {
						nOptional++;
						ph.value = new Indent();
						String value = parameter.getInitialization();
						TranslationConstantNode tcn = SourceCompilationListener.getConstantNode(null, value, value);
						programmer.writeConstant(ph.value, tcn);
					}
					handling.add(ph);
				} // for parameters
				
				String headerScope = symbol.getScope().toString() + symbol.getName() + "/";
				String headerComments = Transpiler.instance().getDocumenter().getComments("Doxygen/C++", headerScope, indent.get());
				if (headerComments != null) {
					indent.append("\n");
					indent.append(headerComments);
				}
				indent.writeln( "" );
				if (symbol.isPrivate()) {
					type = "protected " + type;
				} else {
					type = "public " + type;					
				}
				
				if (fpi.decorators.contains("@staticmethod") || fpi.decorators.contains("@forcestatic") ||
					symbol.getScope().getLevel() == Level.MODULE) {
					type = "static " + type;
				} else if (fpi.decorators.contains("@abstractmethod")) {
					isAbstract = true;
					type = "abstract " + type;
				}
				
				if (nOptional > 0) {
					//System.out.printf("Optional: %s %d\n", name, nOptional);
					writeOptionalParameterAliases( indent, currentClassName, type, name, handling );
				}
				
				if (Transpiler.instance().isTestCaseMethod()) {
					indent.writeln("@Test");					
				}
				String decl = generateBodyDeclaration( type, currentClassName, name, body.sb.toString() );
				if (fpi.decorators.contains("@abstractmethod")) {
					indent.writeln( decl + ";");
				} else {
					if (currentClass != null) {
						String manualSuper = Transpiler.instance().getManualSuper(symbol.getScope().toString(), "Java");
						if (manualSuper != null && name.equals(currentClassName)) {
							indent.writeln( decl + " {");
							indent.in();
							indent.writeln(manualSuper);
							indent.out(); // will be reversed below
						} else if (fpi.decorators.contains("@superClassConstructor")) { // decorator inserted by Declarations listener; not in Python source
							String className = symbol.getScope().getLast();
							Scope superScope = symbol.getScope().getParent();
							String scInitializers = getSuperClassInitializers( symbol, className, superScope );
							indent.writeln( decl + " {");
							indent.in();
							Symbol c = Transpiler.instance().lookup(superScope, className);
							for (String sc : c.getSuperClassInfo().superClasses) {
								if (sc.charAt(0) != 'I' || Character.isLowerCase(sc.charAt(1))) { // ignore interfaces
									decl = "super";
									decl += "("; 
									decl += scInitializers;
									decl += ");";
									indent.writeln(decl);
								}
							}
							indent.out(); // will be reversed below
						} else {
							indent.writeln( decl + " {");							
						}
					} else {
						indent.writeln( decl + " {");
					}
				}
		}		
		indent.in();
		if (! fpi.decorators.contains("@abstractmethod")) {
			if (! symbol.getName().equals("__init__") ) {
				switch (symbol.getType()) {
				case "None":
				case "bool":
				case "float":
				case "int":
				case "str":
				case "array":
				case "vector":
					break;
				default:
					Symbol retVar = Transpiler.instance().getSymbolTable().add(scope, String.format("_%s_return_value", symbol.getName()), symbol.getType());
					retVar.setReturnVariable(true);
					emitSymbolDeclaration( retVar, "auto-generated return variable");
				}
			}
		}
	}

	protected void writeOptionalParameterAliases(Indent indent, String currentClassName, String accessAndType, String name,
			ArrayList<ParameterHandling> handling) {
		indent.write( String.format("%s%s(", accessAndType, name) );
		boolean addComma = false;
		for (int j = 0; j < handling.size(); j++) {
			if (handling.get(j).value == null) {
				if (addComma)
					indent.append(", ");
				indent.append("final ");
				indent.append(handling.get(j).type);
				indent.append(" ");
				indent.append(handling.get(j).name);
				addComma = true;
//			} else {
//				if (addComma)
//					indent.append(", ");
//				indent.append("final ");
//				indent.append(handling.get(j).type);
//				indent.append(" ");
//				indent.append(handling.get(j).name);						
//				addComma = true;
			}
		}
		indent.append(") {\n");
		indent.in();
		indent.write("");
		String[] fields = accessAndType.split(" ");
		if (fields.length > 1 && !fields[1].equals("void")) {
			indent.append("return "); // //
		}
		if (name.equals(currentClassName)) {
			indent.append("this(");
		} else {
			indent.append(name + "(");
		}
		for (int j = 0; j < handling.size(); j++) {
			if (j > 0)
				indent.append(", ");
			if (handling.get(j).value == null) {
				indent.append(handling.get(j).name);
			} else {
				indent.append(handling.get(j).value.sb.toString());					
			}
		}
		indent.append(");\n");
		indent.out();
		indent.writeln("}");
		indent.writeln();
	}

	protected String generateBodyDeclaration( String type, String currentClass, String name, String parameters ) {
		return String.format("%s%s (%s)", type, name, parameters );
	}


	@Override
	public void finishMethod(Scope scope) {
 		currentScope = scope;
		indent.out();
		if (!isAbstract) {
			indent.writeln("}");
			indent.writeln();
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
		boolean selfReference = false;
		if (symbol.getName().equals("self")) {
			selfReference = true;
			if (child.getRightSibling() instanceof TranslationUnaryNode) {
				TranslationUnaryNode unary = (TranslationUnaryNode) child.getRightSibling();
				//System.out.println("self." + unary.getRhsSymbol());
				if (unary.getRhsSymbol() != null) {
					Symbol rhs = unary.getRhsSymbol();
					if (rhs.isClassMethod()) {
						Symbol c = Transpiler.instance().lookup(symbol.getScope(), unary.getRhsSymbol().getScope().getLast());
						if (c != null && c.isClass()) 
							symbol = c;
					} else if (rhs.isClass()) { // creating object of subclass
						if (rhs.isStatic()) {
							out.append( "new " + rhs.getName());							
						} else {
							out.append( "this.new " + rhs.getName());
						}
						return 1;
					}
				}
			}
		}
		Symbol c = Transpiler.instance().lookupClass(symbol.getName());
		String rewrite = programmer.rewriteSymbol( scope, symbol );
		if (c != null && child.getRightSibling() != null && child.getRightSibling() instanceof TranslationListNode) { // create an object
			emitNewExpression( scope, rewrite, child );
			addImport( c.getScope().getChild(Level.CLASS, rewrite) );
			out.append( "new " + rewrite);
		} else {
			if (! selfReference && ! symbol.isClass() && ! symbol.isEnum() && 
					symbol.getScope().getLevel() == Level.MODULE) {
				while (symbol.getAncestor() != null) {
					symbol = symbol.getAncestor();
				}
				addStaticImport( symbol.getScope(), symbol.getName());
				out.append(symbol.getScope().getLast());
				programmer.writeOperator( out, "." );
			}
			out.append( rewrite );
		}
		return -1;
	}
	
	protected int emitChild(Indent out, Scope scope, TranslationUnaryNode unary) {
		Symbol symbol = unary.getRhsSymbol();
		TranslationNode node = unary.getRhsNode();
		if (symbol != null) {
			if (symbol.isClassMethod()) {
				programmer.writeOperator( out, "." );
			} else {
				if (unary.getLeftSibling() != null && unary.getLeftSibling() instanceof TranslationUnaryNode) {
					TranslationUnaryNode u = (TranslationUnaryNode) unary.getLeftSibling();
					if (u.getRhsSymbol() != null) {
						Symbol type = Transpiler.instance().lookup(currentScope, u.getRhsSymbol().getType());
						if (type != null && type.isClass() && !type.isEnum()) {
							programmer.writeOperator( out, "." );
						} else {
							programmer.writeOperator( out, unary.getLhsValue() );
						}
					}
				} else if (unary.getLeftSibling() != null && unary.getLeftSibling() instanceof TranslationSymbolNode) {
					TranslationSymbolNode s = (TranslationSymbolNode) unary.getLeftSibling();
					if (s.getSymbol().isClass()) {
						if (unary.getRightSibling() != null && 
						    unary.getRightSibling() instanceof TranslationListNode &&
						    unary.getRightSibling().getFirstChild()  instanceof TranslationSymbolNode &&
						    ((TranslationSymbolNode) unary.getRightSibling().getFirstChild()).getSymbol().getName().equals("self") ) {
							out.deleteLast(s.getSymbol().getName());
							out.append("super");
						} 
						programmer.writeOperator( out, "." );							
					} else {
						Symbol type = Transpiler.instance().lookup(currentScope, s.getType());
						if (type != null && type.isClass() && !type.isEnum()) {
							programmer.writeOperator( out, "." );
						} else {
							programmer.writeOperator( out, unary.getLhsValue() );
						}
					}
				} else if (unary.getLeftSibling() != null && unary.getLeftSibling() instanceof TranslationListNode) {
					TranslationListNode s = (TranslationListNode) unary.getLeftSibling();
					Symbol type = Transpiler.instance().lookupClass(s.getType()); 
					if (type != null && type.isClass() && !type.isEnum()) {
						programmer.writeOperator( out, "." );
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
					TranslationSymbolNode tsn = (TranslationSymbolNode) unary.getLeftSibling(); 
					TranslationConstantNode tcn = (TranslationConstantNode) which;
					symbol = programmer.getDimensionSymbol( tsn.getSymbol().getType(), tcn.getValue() );
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
			String arrayReference = null;
			if (tln.getLeftSibling() instanceof TranslationSymbolNode) {
				array = ((TranslationSymbolNode) tln.getLeftSibling()).getSymbol();
				arrayReference = array.getName();
			} else if (tln.getLeftSibling() instanceof TranslationUnaryNode) {
				array = ((TranslationUnaryNode) tln.getLeftSibling()).getRhsSymbol();
				Symbol source = ((TranslationSymbolNode) tln.getLeftSibling().getLeftSibling()).getSymbol();
				arrayReference = String.format("%s$%s", programmer.rewriteSymbol(currentScope, source), array.getName());
			}
			if ( tln.isArraySlice() ) {
				if (array == null) {
					Transpiler.instance().reportError(tln.getTop(), "Bracket list follows non-symbol");
					return 0;
				}
				// [...] -> (...) Python slice to Matlab-style slice used by EJML
				programmer.openParenthesis(out);
				for (int i = 0; i < tln.getChildCount(); i++) {
					if (i > 0) {
						out.append(", ");
					}
					TranslationNode subscript = tln.getChild(i);
//					System.out.println(subscript.traverse(0));
					switch (subscript.getChildCount()) {
					default:
						emitChild(out, scope, subscript);
						break;
					case 2:  // [a:] or [:b]
						emitChild(out, scope, subscript.getChild(0));
						if (subscript.getChild(0) instanceof TranslationOperatorNode) {
							out.append("(");
						}
						emitChild(out, scope, subscript.getChild(1));							
						if (subscript.getChild(0) instanceof TranslationOperatorNode) {
							out.append("-1)");
						}
						break;
					case 3: // [a:b]
						emitChild(out, scope, subscript.getChild(0));
						emitChild(out, scope, subscript.getChild(1));
						out.append("(");
						emitChild(out, scope, subscript.getChild(2));
						out.append("-1)");
						break;
					}
					
				}
				programmer.closeParenthesis(out);
//				//Symbol slice = programmer.getSliceSymbol(array.getType());
//				//programmer.writeOperator(out, ".");
//				switch (tln.getChildCount()) {
//				case 0: 
//					break;
//					
//				case 1: // [i] || [:]
//					//out.append( programmer.rewriteSymbol( scope, slice ) );
//					programmer.openParenthesis( out );
//					if (tln.getChild(0) instanceof TranslationOperatorNode) {  //->programmer
//						// [:] -> block(0,0,rows(),cols()) / segment(0,size())
//						if (array.getType().equals("vector")) {
//							out.append(":");
////							out.append("0, ");
////							out.append(programmer.getMeasurement(array.getName(), Measurement.NUMBER_OF_ELEMENTS));
//						} else {
//							out.append(":, :");
////							out.append("0, 0, ");
////							out.append(programmer.getMeasurement(array.getName(), Measurement.NUMBER_OF_ROWS));
////							out.append(", "); 								
////							out.append(programmer.getMeasurement(array.getName(), Measurement.NUMBER_OF_COLUMNS));
//						}
//					} else {  //->programmer
//						// [i:m] -> block(i,0,m,1) / segment(i,m)
//						TranslationNode subscript = tln.getChild(0);							
//						if (array.getType().equals("vector")) {
//							emitChild(out, scope, subscript.getChild(0));
//							out.append(", ");
//							emitChild(out, scope, subscript.getChild(2));
//						} else {
//							emitChild(out, scope, subscript.getChild(0));
//							out.append(", 0, ");
//							emitChild(out, scope, subscript.getChild(2));
//							out.append(", "); 								
//							out.append("1 ");						
//						}
//					}
//					break;
//					
//				case 2: // [:,j] || [i,:] || [i:n,j] || [i,j:m] || [i:n,j:m]
//					if (tln.getChild(0) instanceof TranslationOperatorNode) {  // [:,j] - get column; [:,j:k] - get slice
//						//Symbol which = programmer.getRowColSymbol("1");
//						//out.append( programmer.rewriteSymbol( scope, which ) );
//						programmer.openParenthesis( out );
//						out.append(":, ");
//						emitChild(out, scope, tln.getChild(1));							
//					} else if (tln.getChild(1) instanceof TranslationOperatorNode) {  // [i,:] - get row; [j:k,:] - get slice
//						if (tln.getChild(0).getChildCount() > 0) { // [i:n,:]
//							//out.append( programmer.rewriteSymbol( scope, slice ) );
//							programmer.openParenthesis( out );
//							TranslationNode subscript0 = tln.getChild(0);
//							emitChild(out, scope, subscript0.getChild(0));
//							out.append(", "); //->programmer
//							out.append(":");
////							out.append(", "); //->programmer
////							emitChild(out, scope, subscript0.getChild(2));
////							TranslationOperatorNode minus = new TranslationOperatorNode(tln.getParserRuleContext(), null, "-");
////							emitChild(out, scope, minus);
////							emitChild(out, scope, subscript0.getChild(0));								
////							out.append(", "); 	 //->programmer															
////							out.append(programmer.getMeasurement(array.getName(), Measurement.NUMBER_OF_COLUMNS));
//						} else {
////							Symbol which = programmer.getRowColSymbol("0");
////							out.append( programmer.rewriteSymbol( scope, which ) );
//							programmer.openParenthesis( out );
//							emitChild(out, scope, tln.getChild(0));
//							out.append(", :");
//						}
//					} else { 
//						/* [i:n,j]   LIST[2]{subscript[3]{expr,:,expr}, expr}
//						 *    -> block(i, j, n, 1)
//						 * [i,j:m]   LIST[2]{expr, subscript[3]{expr,:,expr}}
//						 *    -> block(i, j, 1, m)
//						 * [i:n,j:m] LIST[2]{subscript[3]{expr,:,expr}, subscript[3]{expr,:,expr}}
//						 *    -> block(i,j,n,m)
//						 */
//						//out.append( programmer.rewriteSymbol( scope, slice ) );
//						programmer.openParenthesis( out );
//						if (tln.getChild(0).getChildCount() > 0 && tln.getChild(1).getChildCount() > 0) { // [i:n,j:m]
//							TranslationNode subscript0 = tln.getChild(0);
//							TranslationNode subscript1 = tln.getChild(1);
//							emitChild(out, scope, subscript0.getChild(0));
//							out.append(":"); //->programmer
//							emitChild(out, scope, subscript0.getChild(2));
//							out.append(", "); //->programmer
//							emitChild(out, scope, subscript1.getChild(0));								
//							out.append(":"); //->programmer
//							emitChild(out, scope, subscript1.getChild(2));
//						} else if (tln.getChild(0).getChildCount() > 0) { // [i:n,j]
//							TranslationNode subscript0 = tln.getChild(0);
//							TranslationNode subscript1 = tln.getChild(1);
//							emitChild(out, scope, subscript0.getChild(0));
//							out.append(": "); //->programmer
//							emitChild(out, scope, subscript0.getChild(2));
//							out.append(", "); //->programmer
//							emitChild(out, scope, subscript1);
//						} else if (tln.getChild(1).getChildCount() > 0) { // [i,j:m]
//							TranslationNode subscript0 = tln.getChild(0);
//							TranslationNode subscript1 = tln.getChild(1);
//							//out.append( programmer.rewriteSymbol( scope, slice ) );
//							programmer.openParenthesis( out );
//							emitChild(out, scope, subscript0);
//							out.append(", "); //->programmer
//							emitChild(out, scope, subscript1.getChild(0));								
//							out.append(":"); //->programmer
//							emitChild(out, scope, subscript1.getChild(2));
//						} else {
//							Transpiler.instance().reportError(tln.getParserRuleContext(), "Impossible slice/non-slice");
//						}
//					}
//					break;
//				}
//				programmer.closeParenthesis( out );
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
				if (isListAccess) {
					//programmer.openBracket(out);
					out.append(".get"); // TODO programmer
				}
				programmer.openParenthesis( out );
				for (int i = 0; i < tln.getChildCount(); i++) {
					TranslationNode subscript = tln.getChild(i);
					if (i != 0)
						out.append(", "); //->programmer
					if (TranslationUnaryNode.isMinusOne(tln.getChild(i))) {
						//out.append(array.getName());
						if (i == 0) {
							out.append(programmer.getMeasurement(arrayReference, Measurement.NUMBER_OF_ROWS));
							out.append("-1");
						} else {
							out.append(programmer.getMeasurement(arrayReference, Measurement.NUMBER_OF_COLUMNS));
							out.append("-1");							
						}
					} else {
						emitChild(out, scope, tln.getChild(i));
					}
				}
//				if (isListAccess)
//					programmer.closeBracket(out);
//				else
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
	
	public void emitSubExpression(Indent output, Scope scope, TranslationNode root) {
		boolean mustCompile = false;
		if (root instanceof TranslationExpressionNode || root instanceof TranslationSubexpressionNode) {
			mustCompile = true;
			if (root.getChildCount() >= 3 && root.getChild(0) instanceof TranslationSymbolNode && root.getChild(1) instanceof TranslationOperatorNode) {
				TranslationSymbolNode tsn = (TranslationSymbolNode) root.getChild(0);
				TranslationOperatorNode ton = (TranslationOperatorNode) root.getChild(1);
				if (ton.getOperator().equals("=")) {
					switch (tsn.getSymbol().getType()) {
					case "int":
					case "float":
					case "array":
					case "vector":
						Transpiler.instance().logger().info("eSE> " + root.getClass().getSimpleName() + " :: " + root.toString());
						break;
					default:
						Transpiler.instance().logger().info("eSE! " + root.getClass().getSimpleName() + " :: " + root.toString());
						mustCompile = false;
					}
				}
			}
		}
		Indent out = new Indent(output);
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
		if (mustCompile) {
			Transpiler.instance().logger().info("eSE< " + out.sb.toString());
			IExpressionCompiler compiler = programmer.getExpressionCompiler( scope, tempManager, isTestTarget() );
			compiler.setTemporaries(declaredTemps);			
			compiler.setStaticImports(staticImports);
			if (compiler.compile(out.sb.toString(), this.imports, currentScope) ) {
//				System.out.println(out.sb.toString() + " : " + declaredTemps.toString());
				if (! compiler.getHeader().isEmpty()) {
					output.writeln();
				}
				for (String line : compiler.getHeader()) {
					if (line.trim().isEmpty())
						continue;
					output.writeln(line.replace("$", "."));
				}
				for (String line : compiler.getCode()) {
					if (line.trim().isEmpty())
						continue;
					output.writeln(line.replace("$", "."));
				}
				output.deleteLast('\n'); // delete final ; and \n; will be added later
				output.deleteLast(';');
				return;
			}
		}
		output.append(out.sb.toString().replace("$", ".").replace("super()", "super"));
	}

	
	@Override
	public void emitSubExpression(Scope scope, TranslationNode root) {
		emitSubExpression( indent, scope, root);
	}
	
	@Override
	public void emitNewExpression(Scope scope, String className, TranslationNode root) {
//		TranslationNode list = root.getRightSibling();
//		if (list == null && root.getChildCount() >= 2) {
//			list = root.getChild(1);
//		}
//		if (list == null) {
//			System.out.println(root.traverse(1)); // TODO is this just an error?
//			indent.append( String.format("/*eNE?*/std::shared_ptr<%s>(new ", className)); //->programmer
//			emitSubExpression( indent, scope, root);
//		} else {
//			indent.append( String.format("new %s", className));
//		}
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
		Indent out = indent;
		out.write( "" );
		int where = out.size();
		if (! handleConstantArrayAssignment(out, scope, root)) {
			if (inEnum) {
				emitSubExpression( out, scope, root.getChild(0) ); // symbol only for java enum members
			} else {
				emitSubExpression( out, scope, root );
			}
		}
		if (out.size() > where) {
			if (inEnum) {
				out.append(",");	 //->programmer		
			} else {
				out.append(";");    //->programmer
			}
		}
		out.append("\n");
	}

	@Override
	public void emitSymbolDeclaration(Symbol symbol, String comment) {
		if ( symbol.isForVariable() )
			return;
		String remappedType = programmer.remapType(currentScope, symbol);
		if (remappedType == null) {
			remappedType = symbol.getType();
		}
		remappedType += "";
		Symbol c = Transpiler.instance().lookupClassOrEnum(remappedType);
		if (c != null) {
			addImport( c.getScope().getChild(Level.CLASS, remappedType));
		}
		
		if (remappedType.equals("enum"))
			return;
//		Symbol type = Transpiler.instance().lookup(currentScope, cppType);
//		if (type != null && type.isClass() && !type.isEnum()) {
//			cppType = String.format("std::shared_ptr<%s>", cppType );
//		}
		String declaration = String.format("%s %s", remappedType, symbol.getName() );
		if (symbol.getScope().getLevel() == Level.CLASS) {
			declaration = "protected  " + declaration;
		}
		String initializer = programmer.getTypeInitializer(remappedType);
		if (initializer != null) {
			declaration += " = " + initializer;
			String[] dims = symbol.getDimensions();
			if (dims != null) {
				declaration += "(";
				declaration += dims[0];
				if (dims.length > 1) {
					declaration += ", ";
					declaration += dims[1];
				} else {
					declaration += ", 1";
				}
				declaration += ")";
			} else {
				declaration += "()";
			}
		}
		String endLine = ";";
		if (comment != null) {
			endLine = String.format("; ///< %s", comment);
		}
		//System.out.println(currentScope.getLevel() + ": " +  declaration + endLine);
		switch (currentScope.getLevel()) {
		case MODULE: 
			indent.writeln( declaration + endLine);
			break;
		case FUNCTION:
			indent.writeln( declaration + endLine);
			break;
		case CLASS:
			indent.writeln( declaration + endLine);
//			indent.writeln( String.format("%s %s; // %s", 
//						remappedType, symbol.getName(), symbol.getScope().toString()) );
			break;
		case MEMBER:
			indent.writeln( declaration + endLine);
			break;
		default:
		}
	}

	@Override
	public void emitRaiseStatement(String exception) {
		//import polynomialfiltering.main.Utility.ValueError;
		int i = exception.indexOf('(');
		if (i > 0) {
			this.addImport(exceptionScope.getChild(Level.CLASS, exception.substring(0,i)));
		}
		indent.write("throw new " + exception );
	}
	
	protected String dollarize(String expr) {
		StringBuilder sb = new StringBuilder();
		sb.append(expr.charAt(0));
		for (int i = 1; i < expr.length()-1; i++) {
			if (expr.charAt(i) == '.') {
				if (Character.isAlphabetic(expr.charAt(i-1)) && Character.isAlphabetic(expr.charAt(i+1))) {
					sb.append('$');
				} else {
					sb.append(expr.charAt(i));					
				}
			} else {
				sb.append(expr.charAt(i));
			}
		}
		sb.append(expr.charAt(expr.length()-1));
		return sb.toString();
	}

	@Override
	public void emitReturnStatement(Scope scope, ParserRuleContext ctx, TranslationNode expressionRoot) {
		if (expressionRoot != null) {
			List<Symbol> symbols = Transpiler.instance().getSymbolTable().atScope(scope);
			for (Symbol retVar : symbols) {
				if (retVar.isReturnVariable()) {
					TranslationExpressionNode assignment = new TranslationExpressionNode(ctx, "rewriteReturn");
					TranslationSymbolNode target = new TranslationSymbolNode(ctx, assignment, retVar);
					TranslationOperatorNode equals = new TranslationOperatorNode(ctx, assignment, "=");
					indent.write();
					assignment.addChild(expressionRoot);
					emitSubExpression(scope, assignment);
					indent.append(";\n");
					
					indent.write("return ");
					emitSubExpression(scope, target);
					indent.append(";\n");
					return;
				}
			}
			//indent.write("return ");
			emitSubExpression(scope, expressionRoot);
			int lastEol = indent.sb.lastIndexOf("\n");
//			System.out.println(indent.sb.substring(lastEol+1));
			String str = indent.sb.substring(lastEol+1);
			int iEqual = str.indexOf('=');
			if (iEqual >= 0) {
				str = str.substring(iEqual+1);
			}
			indent.sb.replace(lastEol+1, indent.sb.length(), "");
			IExpressionCompiler compiler = programmer.getExpressionCompiler( scope, tempManager, isTestTarget() );
			compiler.setTemporaries(declaredTemps);
			compiler.setStaticImports(staticImports);
			String expr = "asssignment$dummy = return (" + str + ")";
			if (compiler.compile(dollarize(expr), this.imports, currentScope) ) {
				for (String line : compiler.getCode()) {
					indent.writeln(line.replace("$", "."));
				}
			} else {
				indent.writeln("return " + str + ";");
			}
			
		} else {
			indent.write("return");
			indent.append(";\n");
		}
	}

	@Override
	public void startStatement() {
		indent.write("");
	}
	
	
	@Override
	public void finishStatement() {
		indent.append(";\n");
	}

	@Override
	public void emitIfStatement(Scope scope, TranslationNode expressionRoot) {
		indent.write("if (");
		emitSubExpression( scope, expressionRoot.getFirstChild() );
		indent.append(") {\n");
		indent.in();
	}

	@Override
	public void emitElifStatement(Scope scope, TranslationNode expressionRoot) {
		indent.out();
		indent.write("} else if (");
		emitSubExpression( scope, expressionRoot.getFirstChild() );
		indent.append(") {\n");
		indent.in();
	}

	@Override
	public void emitElseStatement() {
		indent.out();
		indent.write("} else {\n");
		indent.in();
	}

	@Override
	public void emitForStatement(Symbol symbol, TranslationNode atomExpr) {
//		System.out.println(atomExpr.traverse(1));
		TranslationSymbolNode tsn = (TranslationSymbolNode) atomExpr.getChild(0); // range
		TranslationListNode tln = (TranslationListNode) atomExpr.getChild(1);
		indent.write( String.format("for (%s %s = ", 
				programmer.remapType( currentScope, symbol ), 
				symbol.getName()));
		emitSubExpression( symbol.getScope(), tln.getChild(0) );
		indent.append( String.format("; %s < ", symbol.getName()));
		emitSubExpression( symbol.getScope(), tln.getChild(1) );
		indent.append( String.format("; %s++) {\n", symbol.getName()) );
		indent.in();
	}

	@Override
	public void closeBlock() {
		indent.out();
		indent.writeln( "}");
	}
	
	@Override
	public void addImport(Scope scope) {
		if (scope.getLast().equals("Main") || scope.getLast().equals("TestData"))
			return;
		StringBuilder includeFile = new StringBuilder();
		for (int i = 0; i < scope.getLevelCount()-1; i++) {
			String level = scope.getLevel(i);
			if (scope.getLevelKind(i) == Level.IMPORT || scope.getLevelKind(i) == Level.MODULE) {
				level = level.toLowerCase() + "";
			}
			if (i > 0) {
				includeFile.append('.');
			}
			includeFile.append(level);
		}
		includeFile.append('.');
		includeFile.append(scope.getLast());
		String file = includeFile.toString();
		for (String f : imports) {
			if (f.equals(file))
				return;
		}
		imports.add(file);
	}
	
	public void addStaticImport( Scope scope, String function ) {
		if (scope.getLast().equals("Main") || scope.getLast().equals("TestData"))
			return;
		
		if (scope.toString().equals(currentScope.getParent().toString()))
			return;
	
		Symbol symbol = Transpiler.instance().lookup(scope, function);
		if (symbol != null) {
			StaticImport si = new StaticImport();
			si.name = scope.getLast() + "$" + function;
			si.type = symbol.getType();
			staticImports.add(si);
		}
		StringBuilder includeFile = new StringBuilder();
		for (int i = 0; i < scope.getLevelCount()-1; i++) {
			String level = scope.getLevel(i);
			if (scope.getLevelKind(i) == Level.IMPORT || scope.getLevelKind(i) == Level.MODULE) {
				level = level.toLowerCase() + "";
			}
			if (i > 0) {
				includeFile.append('.');
			}
			includeFile.append(level);
		}
		includeFile.append('.');
		includeFile.append(scope.getLast());
		includeFile.append('.');
		includeFile.append(function);
		String file = "static " + includeFile.toString();
		for (String f : imports) {
			if (f.equals(file))
				return;
		}
		imports.add(file);
	}


	@Override
	public void addParameterClass(String className) {
		programmer.addParameterClass(className);
	}

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

}
