package com.bluelightning.tools.transpiler;

import java.util.Stack;

import org.antlr.v4.runtime.CommonToken;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.RuleNode;

import com.bluelightning.tools.transpiler.antlr4.LcdPythonBaseListener;
import com.bluelightning.tools.transpiler.antlr4.LcdPythonParser;

class DeclarationsListener extends LcdPythonBaseListener {

		/**
		 * 
		 */
		private final Transpiler transpiler;
		Stack<Scope> scopeStack = new Stack<>();

		public DeclarationsListener(Transpiler transpiler, Scope moduleScope) {
			super();
			this.transpiler = transpiler;
			scopeStack.push(moduleScope);
		}
		
		protected String getChildText( RuleNode ctx, int iChild) {
			return this.transpiler.valueMap.get(ctx.getChild(iChild).getPayload());
		}

		protected void declareSymbol( Token token, String declaration ) {
			declaration = declaration.trim().replaceAll(" +", " ");
			String[] fields = declaration.split(":");
			if (fields.length == 2) {
				Scope currentScope = scopeStack.peek();
				this.transpiler.symbolTable.add(currentScope, fields[0], fields[1]);
			} else {
				this.transpiler.reportError(token, "Ill-formed declaration: " + declaration );
			}
		}
		
		@Override
		public void enterFuncdef(LcdPythonParser.FuncdefContext ctx) {
//			dumpChildren( ctx );
			Scope currentScope = scopeStack.peek();
			String name = getChildText(ctx, 1);
			Scope functionScope = currentScope.getChild(Scope.Level.FUNCTION, name);
			if (functionScope == null) {
				this.transpiler.reportError(ctx.start, "Invalid function scope");
			}
			scopeStack.push( functionScope );
			this.transpiler.symbolTable.add(functionScope, name, getChildText(ctx, 4)); 
			this.transpiler.scopeMap.put( ctx.getPayload(), functionScope );
			ParseTree parameterDeclaration = ctx.getChild(2);
			if (parameterDeclaration.getChildCount() > 2) {
				ParseTree parameters = parameterDeclaration.getChild(1);
				for (int i = 0; i < parameters.getChildCount(); i++) {
					String declaration = this.transpiler.valueMap.get(parameters.getChild(i).getPayload()).trim();
					if (declaration.equals(","))
						continue;
					if (declaration.equals("=")) {
						i++;
						continue;
					}
//					System.out.printf("P %10d : [%s]\n", i, declaration);
					if ( !declaration.equals("self")) {
						declareSymbol( ctx.getStart(), declaration);
					}
				}
			}
		}

		@Override
		public void exitFuncdef(LcdPythonParser.FuncdefContext ctx) {
//			dumpChildren( ctx );
			scopeStack.pop();
		}

		@Override
		public void enterClassdef(LcdPythonParser.ClassdefContext ctx) {
//			dumpChildren( ctx );
			Scope currentScope = scopeStack.peek();
			String name = getChildText(ctx, 1);
			Scope classScope = currentScope.getChild(Scope.Level.CLASS, name);
			if (classScope == null) {
				this.transpiler.reportError(ctx.start, "Invalid class scope");
			}
			scopeStack.push( classScope );
			this.transpiler.symbolTable.add(classScope, name, "<CLASS>"); 
			this.transpiler.scopeMap.put( ctx.getPayload(), classScope );
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
//			dumpChildren( ctx );
		}
		
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