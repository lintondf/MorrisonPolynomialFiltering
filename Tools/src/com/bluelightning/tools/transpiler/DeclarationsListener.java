package com.bluelightning.tools.transpiler;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Stack;

import org.antlr.v4.runtime.CommonToken;
import org.antlr.v4.runtime.RuleContext;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.RuleNode;
import org.apache.commons.lang3.StringUtils;

import com.bluelightning.tools.transpiler.Scope.Level;
import com.bluelightning.tools.transpiler.antlr4.LcdPythonBaseListener;
import com.bluelightning.tools.transpiler.antlr4.LcdPythonParser;
import com.bluelightning.tools.transpiler.antlr4.LcdPythonParser.SuiteContext;
import com.bluelightning.tools.transpiler.antlr4.LcdPythonParser.TestContext;

class DeclarationsListener extends LcdPythonBaseListener {

		/**
		 * 
		 */
		private final Transpiler transpiler;
		protected Scope moduleScope;
		Stack<Scope> scopeStack = new Stack<>();
		boolean isTest = false;
		
		int classdefContextIndex = -1;
		int funcdefContextIndex = -1;

		public DeclarationsListener(Transpiler transpiler, Scope moduleScope, boolean isTest) {
			super();
			this.transpiler = transpiler;
			this.moduleScope = moduleScope;
			this.isTest = isTest;
			scopeStack.push(moduleScope);
			Map<String, Integer> map = transpiler.parser.getRuleIndexMap();
			classdefContextIndex = map.get("classdef");
			funcdefContextIndex = map.get("funcdef");
		}
		
		protected String getChildText( RuleNode ctx, int iChild) {
			return this.transpiler.valueMap.get(ctx.getChild(iChild).getPayload());
		}

		protected void addSymbolDimensions( Symbol symbol, String[] fields) {
			switch (fields[1]) {
			case "vector":
				if (fields.length == 3) {
					String[] dims = new String[]{ fields[2].trim() };
					symbol.setDimensions(dims);
				} else {
					transpiler.reportError("Only one dimension allowed on vector: " + fields[0]);
				}
				break;
			case "array":
				if (fields.length == 4) {
					String[] dims = new String[]{ fields[2].trim(), fields[3].trim() };
					symbol.setDimensions(dims);
				} else {
					transpiler.reportError("Two dimensions required on matrix: " + fields[0]);
				}
				break;
			default:
				transpiler.reportError("Dimensions only allowed on vector and array: " + fields[0]);
			}
		}
		
		
		/*
		 * '''@ <name> : <type> {: <dim1-str> {: <dim2-str>}} '''
		 */
		protected Symbol declareSymbol( Token token, String declaration ) {
			declaration = declaration.trim().replaceAll(" +", " ");
			String[] fields = declaration.split(":");
			if (fields.length >= 2) {
				Scope currentScope = scopeStack.peek();
				fields[0] = fields[0].trim();
				fields[1] = fields[1].trim();
				if (fields[1].startsWith("'")) { 
					fields[1] = fields[1].substring(1, fields[1].length()-1);
					declaration = declaration.replace("'", "");
				}
				Symbol symbol = transpiler.symbolTable.add(currentScope, fields[0], fields[1]);
				Symbol type = transpiler.symbolTable.lookup(currentScope, fields[1]);
				if (type != null) {
					if (type.isClass()) {
						transpiler.inheritClassMembers(symbol, type);
					}
				}
				if (fields.length > 2) {
					addSymbolDimensions( symbol, fields );
				}
//				if (declaration.contains("testData"))
//					System.out.println(symbol.toString());
				return symbol;
			} else {
				this.transpiler.reportError(token, "Ill-formed declaration: " + declaration );
			}
			return null;
		}
		
		@Override
		public void enterFuncdef(LcdPythonParser.FuncdefContext ctx) {
//			transpiler.dumpChildren( ctx );
			Scope currentScope = scopeStack.peek();
			String name = getChildText(ctx, 1);
			Scope functionScope = currentScope.getChild(Scope.Level.FUNCTION, name);
			if (functionScope == null) {
				this.transpiler.reportError(ctx.start, "Invalid function scope");
			}
			scopeStack.push( functionScope );
			String functionType = "None";
			if (getChildText(ctx,3).equals("->")) {
				functionType = getChildText(ctx, 4);
			} else if (name.equals("__init__")) {
				functionType = getChildText(ctx, 4).trim(); // super.__init__ if present
			}
			Symbol.FunctionParametersInfo fpi = new Symbol.FunctionParametersInfo();
			Symbol symbol = transpiler.symbolTable.add(currentScope, name, functionType);
			transpiler.scopeMap.put( ctx.getPayload(), functionScope );
			ParseTree parameterDeclaration = ctx.getChild(2);
//			if (name.equals("copy"))
//				transpiler.dumpChildren( ctx, 2 );
			if (parameterDeclaration.getChildCount() > 2) {
				ParseTree parameters = parameterDeclaration.getChild(1);
				for (int i = 0; i < parameters.getChildCount(); i++) {
					String declaration = this.transpiler.valueMap.get(parameters.getChild(i).getPayload()).trim();
					if (declaration.equals(",")) 
						continue;
					if (declaration.equals("*")) { // skip any unhandled varargs
						i++;
						continue;
					}
					if (declaration.equals("=")) {
						String initialization = this.transpiler.valueMap.get(parameters.getChild(i+1).getPayload()).trim();
						fpi.parameters.get(fpi.parameters.size()-1).setInitialization(initialization);
						i++;
						continue;
					}
					if ( declaration.equals("self")) {
						declaration += ":"+currentScope.getLast();
					}
					Symbol p = declareSymbol( ctx.getStart(), declaration);
					if (p == null)
						continue;
					if (! p.getName().equals("self")) {
						Symbol c = transpiler.lookupClass(p.getType());
						if (c != null) {
							p.setClassReference(true);
							transpiler.addParameterClass(p.getType());
						}
					}
					fpi.parameters.add(p);
				}
			}
			symbol.setFunctionParametersInfo(fpi);
			for (int i = 0; i < ctx.getChildCount(); i++) {
				if (ctx.getChild(i) instanceof SuiteContext) {
					String body = ctx.getChild(i).getText().trim(); 
					if (body.startsWith("super().__init__")) {
						fpi.decorators.add("@superClassConstructor");
					}
					break;
				}
			}
		}

		@Override
		public void exitFuncdef(LcdPythonParser.FuncdefContext ctx) {
//			dumpChildren( ctx );
			scopeStack.pop();
		}
		
		@Override public void exitDecorated(LcdPythonParser.DecoratedContext ctx) { 
//			transpiler.dumpChildren(ctx);
			String decoration = getChildText(ctx, 0).trim();
			RuleContext ruleContext = (RuleContext) ctx.getChild(1);
			if (ruleContext.getRuleIndex() == funcdefContextIndex) {
				String functionName = transpiler.valueMap.get(ctx.getChild(1).getChild(1).getPayload()).trim();
				Symbol symbol = transpiler.symbolTable.lookup(scopeStack.peek(), functionName);
				Symbol.FunctionParametersInfo fpi = symbol.getFunctionParametersInfo();
				fpi.decorators.add(decoration);
//				System.out.printf("DECORATE: %s %s\n", functionName, decoration );
				if (decoration.equals("@abstractmethod")) {
					symbol = transpiler.lookupClass(symbol.getScope().getLast());
					if (symbol != null) {
						symbol.setAbstractClass(true);
					}
				}
			} else {
				String className = transpiler.valueMap.get(ctx.getChild(1).getChild(1).getPayload()).trim();
				Symbol symbol = transpiler.lookupClass(className);
				Symbol.FunctionParametersInfo fpi = new Symbol.FunctionParametersInfo();
				fpi.decorators.add(decoration);
				symbol.setFunctionParametersInfo(fpi);
			}
		}
		
		protected void inheritDeclarations( Scope classScope, Symbol classSymbol) {
			//System.out.println("inheritDecl " + classScope + " | " + classSymbol );
			if (classSymbol.getSuperClassInfo().superClasses == null)
				return;
			for (String sc : classSymbol.getSuperClassInfo().superClasses) {
				Symbol superClass = transpiler.lookup(classScope, sc);
				if (superClass != null) {
					while (superClass.getAncestor() != null) {
						superClass = superClass.getAncestor();
					}
					Scope membersScope = superClass.getScope().getChild(Level.CLASS, superClass.getName());
					List<Symbol> inheritance = transpiler.symbolTable.atScope(membersScope);
					for (Symbol i : inheritance ) {
						if (i.getName().equals("__init__"))
							continue;
						//System.out.println( i.getName() + " --> " + classScope.toString() );
						transpiler.symbolTable.inherit(i, classScope);
					}
					inheritDeclarations(classScope, superClass);
				}
			}
		}
 
		@Override
		public void enterClassdef(LcdPythonParser.ClassdefContext ctx) {
			Scope currentScope = scopeStack.peek();
			String name = getChildText(ctx, 1);
			if (name.equals(currentScope.getLast())) {
				currentScope = currentScope.getParent();
			}
			Scope classScope = currentScope.getChild(Scope.Level.CLASS, name);
			if (classScope == null) {
				this.transpiler.reportError(ctx.start, "Invalid class scope");
			}
			Symbol symbol = transpiler.symbolTable.add(currentScope, name, "<CLASS>"); 
			if (this.isTest) { 
				Symbol testData = transpiler.lookupClass("TestData");
//				System.out.println("ClassDef       " + symbol );
//				System.out.println("               " + testData );
				transpiler.inheritClassMembers(symbol, testData);
			}

			scopeStack.push( classScope );
			
			Symbol.SuperClassInfo sci = new Symbol.SuperClassInfo();
			if (ctx.getChildCount() >= 5) {
				String[] text = getChildText(ctx, 3).replace(" ", "").split(",");
				for (String c : text) {
					sci.superClasses.add( c );
				}
			}
			symbol.setSuperClassInfo(sci);
			this.transpiler.scopeMap.put( ctx.getPayload(), classScope );
			
			inheritDeclarations( classScope, symbol );			
		}

		@Override
		public void exitClassdef(LcdPythonParser.ClassdefContext ctx) {
//			dumpChildren( ctx );
			scopeStack.pop();
		}
		
		
		@Override 
		public void enterImport_name(LcdPythonParser.Import_nameContext ctx) { 
//			dumpChildren( ctx );
			if (!isTest)
				this.transpiler.reportError(ctx.start, "Full package imports are not allowed");
		}
		
		@Override 
		public void enterImport_from(LcdPythonParser.Import_fromContext ctx) { 
//			transpiler.dumpChildren( ctx );
			String dotted = Transpiler.deblank(ctx.getChild(1).getText());
			dotted = "/" + dotted.replace(".", "/") + "/";
			Scope packageScope = Scope.getExistingScope(dotted);
			if (packageScope != null) {
//				System.out.println("import from " + packageScope.toString() + " -> " + packageScope.getLevelCount() + " " + packageScope.getLast() );
//				System.out.println(dotted);
				transpiler.dispatcher.addImport(packageScope);
				String[] imports = Transpiler.deblank(ctx.getChild(3).getText()).split(",");
				for (String name : imports) {
					if (name.equals("TestData")) // ignore TestData imports
						continue;
					Symbol symbol = transpiler.lookup(packageScope, name);
					Scope membersScope = symbol.getScope().getChild(Level.CLASS, name );
					List<Symbol> inheritance = transpiler.symbolTable.atScope(membersScope);
					Scope inheritedScope = scopeStack.peek(); 
//					System.out.println("import " + membersScope.toString() + " -> " + inheritedScope );
//					System.out.println("    " + symbol );
//					System.out.println("   " + inheritance.size() + " " + symbol.isClass());
					if (symbol.isClass() || symbol.isEnum()) {
						Symbol r = transpiler.symbolTable.inherit(symbol, inheritedScope);
						inheritedScope = inheritedScope.getChild(Level.CLASS, r.getName() );
						for (Symbol i : inheritance ) {
							if (i.getName().equals("__init__"))
								continue;
//							System.out.println("     " + i.isClass() + " " + i.getName() + " " + inheritedScope );
							if (i.isClass() || i.isEnum()) {
								transpiler.symbolTable.inherit(i, inheritedScope.getChild(Level.CLASS, name) );
							} else {
								transpiler.symbolTable.inherit(i, inheritedScope);
							}
						}
					} else {
						Symbol r = transpiler.symbolTable.inherit(symbol, inheritedScope);
					}
				}
			}
		}

		@Override
		public void enterExpr_stmt(LcdPythonParser.Expr_stmtContext ctx) {
			Scope currentScope = scopeStack.peek();
			String value = this.transpiler.valueMap.get(ctx.getPayload());
			if (value.startsWith("\"\"\"")) {
				transpiler.getDocumenter().putDocumentation(currentScope, value);
			}
		}
		
		
		// for <var> in <range> :
		@Override 
		public void enterFor_stmt(LcdPythonParser.For_stmtContext ctx) {
			Scope currentScope = scopeStack.peek();
			Symbol symbol = transpiler.lookup(currentScope, ctx.getChild(1).getText());
			if (symbol != null) {
				symbol.setForVariable(true);
			}
		}
		
//		//atom_expr: (AWAIT)? atom trailer*;
//		//trailer: '(' (arglist)? ')' | '[' subscriptlist ']' | '.' NAME;				
		@Override
		public void enterAtom(LcdPythonParser.AtomContext ctx) {
			for (int i = 0; i < ctx.getChildCount(); i++) {
				if (ctx.getChild(i).getPayload() instanceof CommonToken) {
					CommonToken token = (CommonToken) ctx.getChild(i).getPayload();
					String str = token.getText();
					str = str.trim().replaceAll(" +", " ");
					if (str.startsWith("'''@")) {
						String[] fields = str.substring(4).replaceAll("'''", "").split("\\|");
						if (fields.length > 0) {
							fields[0] = fields[0].trim().replaceAll(" +", " ");
							if (fields[0].startsWith("!super!")) {
								fields = fields[0].split("!");
								Scope currentScope = scopeStack.peek().getParent();
								Transpiler.instance().addManualSuper(currentScope.toString(), fields[2], fields[3]);
							} else {
								declareSymbol( token, fields[0] );
							}
						} else {
							this.transpiler.reportError(ctx.start, "Ill formed declaration comment: " + str );
						}
					}
				}
			}			
		}
	}