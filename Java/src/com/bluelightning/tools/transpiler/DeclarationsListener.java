package com.bluelightning.tools.transpiler;

import java.util.ArrayList;
import java.util.List;
import java.util.Stack;

import org.antlr.v4.runtime.CommonToken;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.RuleNode;

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

		public DeclarationsListener(Transpiler transpiler, Scope moduleScope) {
			super();
			this.transpiler = transpiler;
			this.moduleScope = moduleScope;
			scopeStack.push(moduleScope);
		}
		
		protected String getChildText( RuleNode ctx, int iChild) {
			return this.transpiler.valueMap.get(ctx.getChild(iChild).getPayload());
		}

		protected void addSymbolDimensions( Symbol symbol, String[] fields) {
			switch (fields[1]) {
			case "vector":
				if (fields.length == 3) {
					Integer[] dims = new Integer[]{ Integer.parseInt(fields[2]) };
					symbol.setDimensions(dims);
				} else {
					transpiler.reportError("Only one dimension allowed on vector: " + fields[0]);
				}
				break;
			case "array":
				if (fields.length == 4) {
					Integer[] dims = new Integer[]{ Integer.parseInt(fields[2]), Integer.parseInt(fields[3]) };
					symbol.setDimensions(dims);
				} else {
					transpiler.reportError("Two dimensions required on matrix: " + fields[0]);
				}
				break;
			default:
				transpiler.reportError("Dimensions only allowed on vector and array: " + fields[0]);
			}
		}
		
 		protected Symbol declareSymbol( Token token, String declaration ) {
			declaration = declaration.trim().replaceAll(" +", " ");
			String[] fields = declaration.split(":");
			if (fields.length >= 2) {
				Scope currentScope = scopeStack.peek();
				Symbol symbol = transpiler.symbolTable.add(currentScope, fields[0], fields[1]);
				Symbol type = transpiler.symbolTable.lookup(currentScope, fields[1]);
				if (type != null) {
					if (type.isClass()) {
//						System.out.println("declareSymbol: " + declaration + " " + type);
						List<Symbol> inheritance = transpiler.symbolTable.atScope(type.getScope());
						Scope inheritedScope = symbol.getScope().getChild(Level.CLASS, type.getName() );
						for (Symbol i : inheritance ) {
							if (i.getName().equals("__init__"))
								continue;
//							System.out.println("     " + i.isClass() + " " + i.getName() + " " + inheritedScope );
							if (i.isClass() || i.isEnum()) {
								transpiler.symbolTable.inherit(i, inheritedScope.getChild(Level.CLASS, symbol.getName()) );
							} else {
								transpiler.symbolTable.inherit(i, inheritedScope);
							}
						}
					}
				}
				if (fields.length > 2) {
					addSymbolDimensions( symbol, fields );
				}
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
			if (name.equals("virtual"))
				transpiler.dumpChildren( ctx );
			Scope functionScope = currentScope.getChild(Scope.Level.FUNCTION, name);
			if (functionScope == null) {
				this.transpiler.reportError(ctx.start, "Invalid function scope");
			}
			scopeStack.push( functionScope );
			String functionType = getChildText(ctx, 4);
			Symbol.FunctionParametersInfo fpi = new Symbol.FunctionParametersInfo();
			Symbol symbol = transpiler.symbolTable.add(currentScope, name, functionType);
			transpiler.scopeMap.put( ctx.getPayload(), functionScope );
			ParseTree parameterDeclaration = ctx.getChild(2);
			if (parameterDeclaration.getChildCount() > 2) {
				ParseTree parameters = parameterDeclaration.getChild(1);
				for (int i = 0; i < parameters.getChildCount(); i++) {
					String declaration = this.transpiler.valueMap.get(parameters.getChild(i).getPayload()).trim();
					if (declaration.equals(","))
						continue;
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
			String functionName = transpiler.valueMap.get(ctx.getChild(1).getChild(1).getPayload()).trim();
			Symbol symbol = transpiler.symbolTable.lookup(scopeStack.peek(), functionName);
			Symbol.FunctionParametersInfo fpi = symbol.getFunctionParametersInfo();
			fpi.decorators.add(decoration);
		}
		
		protected void inheritDeclarations( Scope classScope, Symbol classSymbol) {
			//System.out.println("inheritDecl " + classScope + " | " + classSymbol );
			if (classSymbol.getSuperClassInfo().superClass == null)
				return;
			Symbol superClass = transpiler.lookup(classScope, classSymbol.getSuperClassInfo().superClass);
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
 
		@Override
		public void enterClassdef(LcdPythonParser.ClassdefContext ctx) {
			Scope currentScope = scopeStack.peek();
			String name = getChildText(ctx, 1);
			Scope classScope = currentScope.getChild(Scope.Level.CLASS, name);
			if (classScope == null) {
				this.transpiler.reportError(ctx.start, "Invalid class scope");
			}
			scopeStack.push( classScope );
			Symbol symbol = transpiler.symbolTable.add(currentScope, name, "<CLASS>"); 
			Symbol.SuperClassInfo sci = new Symbol.SuperClassInfo();
			sci.superClass = null;
			if (ctx.getChildCount() >= 5) {
				sci.superClass = getChildText(ctx, 3);
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
			this.transpiler.reportError(ctx.start, "Full package imports are not allowed");
		}
		
		@Override 
		public void enterImport_from(LcdPythonParser.Import_fromContext ctx) { 
//			transpiler.dumpChildren( ctx );
			String dotted = Transpiler.deblank(ctx.getChild(1).getText());
			dotted = "/" + dotted.replace(".", "/") + "/";
			Scope packageScope = Scope.getExistingScope(dotted);
			if (packageScope != null) {
//				System.out.println("import from " + packageScope.toString() );
				transpiler.dispatcher.addImport(packageScope);
				String[] imports = Transpiler.deblank(ctx.getChild(3).getText()).split(",");
				for (String name : imports) {
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
						String[] fields = str.substring(4).replaceAll("'''", "").split("-");
						if (fields.length > 0) {
							declareSymbol( token, fields[0] );
						} else {
							this.transpiler.reportError(ctx.start, "Ill formed declaration comment: " + str );
						}
					}
				}
			}			
		}
	}