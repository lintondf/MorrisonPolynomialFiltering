package com.bluelightning.tools.transpiler;

import java.util.HashMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.antlr.v4.runtime.CommonToken;
import org.antlr.v4.runtime.ParserRuleContext;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.RuleNode;
import org.apache.commons.lang3.StringUtils;

import com.bluelightning.tools.transpiler.Scope.Level;
import com.bluelightning.tools.transpiler.antlr4.LcdPythonBaseListener;
import com.bluelightning.tools.transpiler.antlr4.LcdPythonParser;
import com.bluelightning.tools.transpiler.nodes.TranslationConstantNode;
import com.bluelightning.tools.transpiler.nodes.TranslationListNode;
import com.bluelightning.tools.transpiler.nodes.TranslationNode;
import com.bluelightning.tools.transpiler.nodes.TranslationOperatorNode;
import com.bluelightning.tools.transpiler.nodes.TranslationSubexpressionNode;
import com.bluelightning.tools.transpiler.nodes.TranslationSymbolNode;
import com.bluelightning.tools.transpiler.nodes.TranslationUnaryNode;
import com.bluelightning.tools.transpiler.nodes.TranslationConstantNode.Kind;
import com.bluelightning.tools.transpiler.nodes.TranslationExpressionNode;

class SourceCompilationListener extends LcdPythonBaseListener {
		
		/**
		 * 
		 */
		private final Transpiler transpiler;
		Scope scope = null;
		TranslationNode expressionRoot = null;
		HashMap<Object, TranslationNode> translateMap = null;
		boolean headerOnly;
		boolean isTest = false;
		
		protected HashMap<Object, TranslationNode> newTranslateMap() {
			HashMap<Object, TranslationNode> map = new HashMap<>();
			return map;
		}
		
		protected final Symbol undeclaredSymbol = new Symbol( new Scope(), "$declarme$", "int");
		
		/**
		 * @param transpiler
		 * @param headerOnly 
		 */
		SourceCompilationListener(Transpiler transpiler, boolean headerOnly) {
			this.transpiler = transpiler;
			scope = this.transpiler.moduleScope;
			this.headerOnly = headerOnly;
			this.isTest = isTest;
			transpiler.logger.info("module > " + scope);
		}
		
		
		SourceCompilationListener(Transpiler transpiler, Scope testScope, ParserRuleContext ctx) {
			this.transpiler = transpiler;
			scope = testScope;
			this.headerOnly = false;
			this.isTest = true;
			transpiler.logger.info("module > " + scope);
			translateMap = newTranslateMap();
		}
		
		protected static final Pattern integerPattern = Pattern.compile("^(\\d+)$");
		protected static final Pattern floatPattern = Pattern.compile("^(\\d+)\\.(\\d*)$");
		protected static final Pattern expPattern = Pattern.compile("^([-+]?\\d*\\.?\\d+)(?:[eE]([-+]?\\d+))?$");
		
		
		protected TranslationNode defaultOperandOperator( ParserRuleContext ctx, String tag ) {
			if (expressionRoot != null) {
//				System.out.println( tag + " (" + ctx.getChildCount() + ")");
//				transpiler.dumpChildren(ctx);
				TranslationNode parent = new TranslationSubexpressionNode(ctx, null, tag);
				if (ctx.getChildCount() == 1) {
					TranslationNode node = translateMap.get(ctx.getChild(0).getPayload());
					if (node == null) {
						node = getOperandNode( ctx, parent, ctx.getChild(0).getPayload());
						if (node == null) {
							String operator = this.transpiler.valueMap.get(ctx.getChild(0).getPayload());
							if (Character.isAlphabetic(operator.charAt(0))) {
								transpiler.reportError(ctx, "Undeclared symbol: " + operator);
								return new TranslationSymbolNode(ctx, null, undeclaredSymbol);
							}
							node = new TranslationOperatorNode(ctx,  parent, operator );
						}
					}
					translateMap.put( ctx.getPayload(), node );
					parent.setType( node.getType() );
					return node;
				} else if (ctx.getChildCount() == 2) {
//					transpiler.dumpChildren(ctx);
//					String lhValue = (Transpiler.instance().getValue(ctx.getChild(0).getPayload()));
//					String rhValue = (Transpiler.instance().getValue(ctx.getChild(1).getPayload()));
					TranslationNode node = new TranslationUnaryNode( ctx, parent, 
							(CommonToken) ctx.getChild(0).getPayload(), 
							translateMap.get(ctx.getChild(1).getPayload()));
				} else {
					TranslationNode node = getOperandNode( ctx, parent, ctx.getChild(0).getPayload());
					if (node == null) {
						String value = this.transpiler.valueMap.get(ctx.getChild(0).getPayload());
						this.transpiler.reportError(ctx, "Operand neither symbol nor constant nor subexpression: " + 
								ctx.getChild(0).getPayload().getClass().getSimpleName() + " : " + value);

					}
					for (int i = 1; i < ctx.getChildCount(); i += 2) {
						String operator = this.transpiler.valueMap.get(ctx.getChild(i).getPayload());
						if (operator.startsWith(".")) {
//							transpiler.dumpChildren((RuleNode) ctx.getChild(i) );
							Symbol symbol = transpiler.symbolTable.lookup(scope, operator.substring(1));
							node = new TranslationUnaryNode( ctx, parent, 
									(CommonToken) ctx.getChild(i).getChild(0).getPayload(), symbol );
						} else {
							node = new TranslationOperatorNode( ctx, parent, operator );
						}
						node = getOperandNode( ctx, parent, ctx.getChild(i+1).getPayload());
						if (node == null) {
							transpiler.reportError(ctx, "No operand node: " + (i+1));
							return null;
						}
						parent.setType( node.getType() );
					}
				}
//				parent.traverse(2); /////////////
				translateMap.put( ctx.getPayload(), parent );
				return parent;
			}	
			return null;
		}
		
		public static TranslationConstantNode getConstantNode(TranslationNode parent, Object payload, String value) {
			TranslationConstantNode node;
			if (value.startsWith("'") || value.startsWith("\"")) {
				node = new TranslationConstantNode(null,  parent, value, Kind.STRING );
				return node;
			}
			Matcher matcher = integerPattern.matcher(value);
			if (matcher.matches()) {
				node = new TranslationConstantNode(null,  parent, value, Kind.INTEGER );
				return node;				
			}
			matcher = floatPattern.matcher(value);
			if (matcher.matches()) {
				node = new TranslationConstantNode(null,  parent, value, Kind.FLOAT );
				return node;				
			}
			matcher = expPattern.matcher(value);
			if (matcher.matches()) {
				node = new TranslationConstantNode(null,  parent, value, Kind.FLOAT );
				return node;				
			}
			return null;
		}
		
		protected TranslationNode getOperandNode(ParserRuleContext context, TranslationNode parent, Object payload) {
			String value = this.transpiler.valueMap.get(payload);
			TranslationNode node = translateMap.get(payload);
			if (node != null) {
				parent.adopt( node );
				return node;
			}
			Symbol symbol = this.transpiler.symbolTable.lookup( scope, value );
			if (symbol != null) {
				node = new TranslationSymbolNode(context, parent, symbol );
				translateMap.put( payload, node );
				return node;
			}
			TranslationConstantNode tcn = getConstantNode( parent, payload, value );
			if (tcn != null) {
				translateMap.put( payload, tcn );
				return tcn;
			}
//			String[] dotted = value.split("\\.");
//			if (dotted.length > 1 && dotted[0].length() > 0 && dotted[1].length() > 0) {
//				Symbol enumSymbol = transpiler.lookup(scope, dotted[0]);
//				if (enumSymbol != null && enumSymbol.isClass()) {
//					Symbol memberSymbol = transpiler.lookup(scope.getChild(Level.CLASS, dotted[0]), dotted[1]);
//					if (memberSymbol != null) {
//						node = new TranslationSymbolNode( parent, memberSymbol );
//						translateMap.put( payload, node );
//						return node;
//					}
//				}
//			}
			return null;
		}

		@Override
		public void enterClassdef(LcdPythonParser.ClassdefContext ctx) {
			scope = this.transpiler.scopeMap.get(ctx.getPayload());
//			System.out.println("class > " + scope);
			transpiler.dispatcher.startClass(scope);
		}
		
		@Override
		public void exitClassdef(LcdPythonParser.ClassdefContext ctx) {
			scope = scope.getParent();
//			System.out.println("class < " + scope);
			transpiler.dispatcher.finishClass(scope);
		}
		
		@Override
		public void enterFuncdef(LcdPythonParser.FuncdefContext ctx) {
			//transpiler.dumpChildren(ctx);			
			scope = this.transpiler.scopeMap.get(ctx.getPayload());
			Symbol func = transpiler.lookup(scope.getParent(), scope.getLast());
			if (func != null) {
				if (this.isTest) {
					transpiler.dispatcher.setIgnoring( ! func.hasDecorator("@testcase") );
				} else if (func.hasDecorator("@ignore")) {
					transpiler.dispatcher.setIgnoring(true);
				}
			} else {
				if (! func.isConstructor() ) {
					if (ctx.getChildCount() <= 5) {
						this.transpiler.reportError(ctx.start, "Non-Constructor functions must have declared return type");
					}
				} else {
					if (ctx.getChildCount() > 5) {
						this.transpiler.reportError(ctx.start, "Constructor functions must NOT have declared return type");
					}
				}
			}			
//			System.out.println("function > " + scope);
			transpiler.dispatcher.startMethod(scope);
		}
		
		@Override 
		public void enterSuite(LcdPythonParser.SuiteContext ctx) { 
			//transpiler.dumpChildren(ctx);						
		}
		
		@Override
		public void exitFuncdef(LcdPythonParser.FuncdefContext ctx) {
			scope = scope.getParent();
//			System.out.println("function < " + scope);
			transpiler.dispatcher.finishMethod(scope);
			transpiler.dispatcher.setIgnoring(false);
		}
		
		@Override 
		public void enterFor_stmt(LcdPythonParser.For_stmtContext ctx) { 
			transpiler.logger.info(StringUtils.left(ctx.getText(), 80));
//			transpiler.dumpChildren(ctx);
//			defaultOperandOperator( ctx, "for_stmt" );
			String iName = transpiler.getValue( ctx.getChild(1));
//			System.out.printf("FOR %s %s\n", 
//					iName,
//					transpiler.getValue( ctx.getChild(3)));

			Symbol symbol = transpiler.lookup(scope, iName );
			if (symbol == null) {
				transpiler.reportError(ctx, "FOR variable undeclared: " + iName );
				return;
			}

			SourceCompilationListener subListener = new SourceCompilationListener(transpiler, this.headerOnly);
			subListener.expressionRoot = new TranslationSubexpressionNode(ctx, null, "FOR_STMT");
			subListener.translateMap = newTranslateMap();
			subListener.scope = symbol.getScope();
			transpiler.walker.walk(subListener, ctx.getChild(3));
			transpiler.dispatcher.emitForStatement(symbol, subListener.translateMap.get(ctx.getChild(3).getPayload()));
			subListener.expressionRoot = null;
		}
		
		@Override 
		public void exitFor_stmt(LcdPythonParser.For_stmtContext ctx) {
			transpiler.dispatcher.closeBlock();
		}
		
		@Override 
		public void enterIf_stmt(LcdPythonParser.If_stmtContext ctx) { 
			transpiler.logger.info(StringUtils.left(ctx.getText(), 80));
			
			SourceCompilationListener subListener = new SourceCompilationListener(transpiler, this.headerOnly);
			subListener.expressionRoot = new TranslationExpressionNode(ctx, "IF_STMT");
			subListener.translateMap = newTranslateMap();
			subListener.scope = scope;
			transpiler.walker.walk(subListener, ctx.getChild(1));
			TranslationNode condition = subListener.translateMap.get(ctx.getChild(1).getPayload());
//			if (ctx.getStart().getLine() == 58) {
//				transpiler.dumpChildren(ctx);
//				System.out.println( condition.traverse(1));
//			}
			transpiler.dispatcher.emitIfStatement(scope, condition);
			subListener.expressionRoot = null;
			
		}
		
		@Override 
		public void exitIf_stmt(LcdPythonParser.If_stmtContext ctx) { 
			transpiler.dispatcher.closeBlock();
		}
		
		@Override public void enterElif_stmt(LcdPythonParser.Elif_stmtContext ctx) { 
			transpiler.logger.info(StringUtils.left(ctx.getText(), 80));
			SourceCompilationListener subListener = new SourceCompilationListener(transpiler, this.headerOnly);
			subListener.expressionRoot = new TranslationExpressionNode(ctx, "IF_STMT");
			subListener.translateMap = newTranslateMap();
			subListener.scope = scope;
			transpiler.walker.walk(subListener, ctx.getChild(1));
			TranslationNode condition = subListener.translateMap.get(ctx.getChild(1).getPayload());
//			System.out.println( condition.traverse(1));
			transpiler.dispatcher.emitElifStatement( scope, condition );
			subListener.expressionRoot = null;
		}
		
		@Override 
		public void enterElse_stmt(LcdPythonParser.Else_stmtContext ctx) { 
			transpiler.logger.info(StringUtils.left(ctx.getText(), 80));
//			transpiler.dumpChildren(ctx);
			transpiler.dispatcher.emitElseStatement();
		}
		
		
		@Override 
		public void enterReturn_stmt(LcdPythonParser.Return_stmtContext ctx) {
			transpiler.logger.info(StringUtils.left(ctx.getText(), 80));
			expressionRoot = new TranslationExpressionNode(ctx, "RETURN_STMT");
			translateMap = new HashMap<>();
			
		}
		
		// return_stmt: 'return' (testlist)?;
		@Override 
		public void exitReturn_stmt(LcdPythonParser.Return_stmtContext ctx) { 
			transpiler.logger.info(StringUtils.left(ctx.getText(), 80));
			String line = ctx.getText();
			transpiler.dispatcher.emitReturnStatement();
			if (ctx.getChildCount() > 1) {
				expressionRoot = translateMap.get( ctx.getChild(1).getPayload() );
//				System.out.println("RETURN< " + line );
//				System.out.println( expressionRoot.traverse(1));
				if (expressionRoot.getFirstChild() instanceof TranslationSymbolNode) {
					// handle special case of returning new object
					TranslationSymbolNode tsn = (TranslationSymbolNode) expressionRoot.getFirstChild();
					if (tsn.getSymbol().isClass() && !tsn.getSymbol().isEnum()) {
						if (! (tsn.getRightSibling() instanceof TranslationUnaryNode)) {
							//transpiler.dispatcher.emitNewExpression(scope, tsn.getSymbol().getName(), expressionRoot);
							transpiler.dispatcher.emitSubExpression(scope, expressionRoot);
							transpiler.dispatcher.finishStatement();
							expressionRoot = null;
							return;
						}
					}
				}
				transpiler.dispatcher.emitSubExpression(scope, expressionRoot);
				transpiler.dispatcher.finishStatement();
				expressionRoot = null;
			}
		}
		
		
		//raise_stmt: 'raise' (test ('from' test)?)?;
		@Override 
		public void exitRaise_stmt(LcdPythonParser.Raise_stmtContext ctx) {
			transpiler.logger.info(StringUtils.left(ctx.getText(), 80));
//			transpiler.dumpChildren(ctx);
			String line = ctx.getChild(1).getText();
//			System.out.println(line);
			transpiler.dispatcher.emitRaiseStatement(line);
			transpiler.dispatcher.finishStatement();
		}
		
//		public static class DeclarationComment {
//			public String name;
//			public String type;
//			public String comment;
//			
//			public DeclarationComment( String value ) {
//				name = "";
//				type = "";
//				comment = null;
//				String[] fields = value.trim().split("|");
//				if (fields.length > 1)
//					comment = fields[1];
//				value = fields[0].replaceAll(" +", "");
//				
//				value = value.trim().replaceAll(" +", "");
//				String[] fields = value.substring(4).replaceAll("'''", "").split("|"); // drop any comments
//				fields = fields[0].split(":");
//				
//			}
//		}
		
		@Override
		public void enterExpr_stmt(LcdPythonParser.Expr_stmtContext ctx) {
			transpiler.logger.info(StringUtils.left(ctx.getText(), 80));
			String value = this.transpiler.valueMap.get(ctx.getPayload());
			if (value.startsWith("'''")) {
				if (value.startsWith("'''@")) {
					value = value.trim().substring(4).replaceAll("'''", "");
					String[] comments = value.split("\\|"); // extract any comments
					String comment = null;
					if (comments.length > 1)
						comment = comments[1];
					value = comments[0].trim().replaceAll(" +", "");
					String[] fields = value.split(":");
					Symbol symbol = transpiler.symbolTable.lookup(scope, fields[0]);
					if (symbol != null) {
						transpiler.dispatcher.emitSymbolDeclaration(symbol, comment);
					}
				}				
			} else if (value.startsWith("\"\"\"")) {
			} else {
//				System.out.println("EXPR_STMT> [{" + value + "}] <- " + ctx.toStringTree(transpiler.parser));
//				this.transpiler.dumpChildren( ctx, 1 );
				expressionRoot = new TranslationExpressionNode(ctx, value);
				translateMap = new HashMap<>();
			} 
		}

		@Override
		public void exitExpr_stmt(LcdPythonParser.Expr_stmtContext ctx) {
			transpiler.logger.info(StringUtils.left(ctx.getText(), 80));
			if (expressionRoot != null) {
				TranslationNode expr = defaultOperandOperator( ctx, expressionRoot.getName() );
				expressionRoot.replace( expr );
				while (expressionRoot.getChildCount() == 1) {
					expr = expressionRoot.getChild(0);
					if (expr.getChildCount() == 0)
						break;
					expressionRoot = expr;
				}
//				System.out.println("EXPR_STMT< " + expr.toString() );
//				System.out.println( expr.traverse(1));
				if (ctx.getText().trim().startsWith("super().__init__")) {
					// ignore
				} else if ( ! transpiler.valueMap.get(ctx.getPayload()).startsWith("'''@")) {
					if (expressionRoot.getChildCount() > 2) {
						if (expressionRoot.getChild(1) instanceof TranslationOperatorNode) {
							TranslationOperatorNode ton = (TranslationOperatorNode) expressionRoot.getChild(1);
							if (ton.getOperator().equals("=")) {
								if (expressionRoot.getChild(0) instanceof TranslationSymbolNode) {
									TranslationSymbolNode tsn = (TranslationSymbolNode) expressionRoot.getChild(0);
									Symbol c = transpiler.lookupClass( tsn.getSymbol().getType() );
									if (c != null) {
										transpiler.dispatcher.startStatement();
										transpiler.dispatcher.emitSubExpression(scope, expressionRoot.getChild(0));
										transpiler.dispatcher.emitSubExpression(scope, expressionRoot.getChild(1));
										boolean newExpression = true;
										if (expressionRoot.getChild(2).getChildCount() >= 2) {
											if (expressionRoot.getChild(2).getChild(1) instanceof TranslationUnaryNode) {
												newExpression = false;
											}
										}
										if (newExpression) {
											//transpiler.dispatcher.emitNewExpression(scope, tsn.getSymbol().getType(), expressionRoot.getChild(2));
											transpiler.dispatcher.emitSubExpression(scope, expressionRoot.getChild(2));
										} else {
											transpiler.dispatcher.emitSubExpression(scope, expressionRoot.getChild(2));
										}
										transpiler.dispatcher.finishStatement();
										expressionRoot = null;
										return;
									}
								}
							}
						}
					}
					transpiler.dispatcher.emitExpressionStatement(scope, expressionRoot);
				}
			}
			expressionRoot = null;
		}		
		
		@Override
		public void exitAnnassign(LcdPythonParser.AnnassignContext ctx) {
			defaultOperandOperator( ctx, "Annassign" );
		}

		@Override 
		public void exitArglist(LcdPythonParser.ArglistContext ctx) { 
//			transpiler.dumpChildren(ctx);
			defaultOperandOperator( ctx, "arglist" );
		}
		
		@Override 
		public void exitArgument(LcdPythonParser.ArgumentContext ctx) { 
			defaultOperandOperator( ctx, "argument" );
		}
		
		@Override
		public void exitTestlist_star_expr(LcdPythonParser.Testlist_star_exprContext ctx) {
			defaultOperandOperator( ctx, "testlist_expr" );
		}
		
		@Override
		public void exitAugassign(LcdPythonParser.AugassignContext ctx) {
			defaultOperandOperator( ctx, "augassign" );
		}

		@Override
		public void exitTest(LcdPythonParser.TestContext ctx) {
			defaultOperandOperator( ctx, "test" );
		}

		@Override
		public void exitTest_nocond(LcdPythonParser.Test_nocondContext ctx) {
			defaultOperandOperator( ctx, "test_nocond" );
		}

		@Override
		public void exitOr_test(LcdPythonParser.Or_testContext ctx) {
			defaultOperandOperator( ctx, "or_test" );
		}

		@Override
		public void exitAnd_test(LcdPythonParser.And_testContext ctx) {
			defaultOperandOperator( ctx, "and_test" );
		}

		@Override
		public void exitNot_test(LcdPythonParser.Not_testContext ctx) {
			defaultOperandOperator( ctx, "not_test"  );
		}

		@Override
		public void exitComparison(LcdPythonParser.ComparisonContext ctx) {
			defaultOperandOperator( ctx, "comparison" );
		}

		@Override
		public void exitComp_op(LcdPythonParser.Comp_opContext ctx) {
			defaultOperandOperator( ctx, "comp_op" );
		}

		@Override
		public void exitExpr(LcdPythonParser.ExprContext ctx) {
//			transpiler.dumpChildren(ctx);
			defaultOperandOperator( ctx, "exitexpr" );
		}

		@Override
		public void exitXor_expr(LcdPythonParser.Xor_exprContext ctx) {
			defaultOperandOperator( ctx, "xor_expr" );
		}

		@Override
		public void exitAnd_expr(LcdPythonParser.And_exprContext ctx) {
			defaultOperandOperator( ctx, "and_expr" );
		}

		@Override
		public void exitShift_expr(LcdPythonParser.Shift_exprContext ctx) {
			defaultOperandOperator( ctx, "shift_expr" );
		}

		//arith_expr: term (('+'|'-') term)*;
		@Override
		public void exitArith_expr(LcdPythonParser.Arith_exprContext ctx) {
			defaultOperandOperator( ctx, "Arith_expr" );
		}
		
		@Override
		public void exitTerm(LcdPythonParser.TermContext ctx) {
			defaultOperandOperator( ctx, "Term" );
		}

		@Override
		public void exitFactor(LcdPythonParser.FactorContext ctx) {
			defaultOperandOperator( ctx, "factor" );
		}

		@Override
		public void exitPower(LcdPythonParser.PowerContext ctx) {
			defaultOperandOperator( ctx, "Power" );
		}

//atom_expr: (AWAIT)? atom trailer*;
//trailer: '(' (arglist)? ')' | '[' subscriptlist ']' | '.' NAME;		
		@Override
		public void exitAtom_expr(LcdPythonParser.Atom_exprContext ctx) {
			if (expressionRoot == null)
				return;
			if (ctx.getChildCount() == 1) {
				defaultOperandOperator( ctx, "atom_expr" );
			} else {
				TranslationNode parent = new TranslationSubexpressionNode(ctx, null, "atom_expr");
				String text = ctx.getChild(0).getText();
				Symbol symbol = transpiler.symbolTable.lookup(scope, text );
				if (symbol == null) {
					transpiler.reportError("atmo_expr::Unknown symbol: " + ctx.getChild(0).getText() + " " + scope);
					return;
				}
				new TranslationSymbolNode(ctx,  parent, symbol );
				for (int iTrailer = 1; iTrailer < ctx.getChildCount(); iTrailer++) {
					ParseTree trailer = ctx.getChild(iTrailer);
					for (int i = 0; i < trailer.getChildCount(); i++) {
						Object payload = trailer.getChild(i).getPayload();
						String unary = trailer.getChild(i).getText().substring(0,1); 
						switch (unary) {
						case "(":
						case "[":
//							System.out.println("Compiling LIST " + trailer.getChild(i).getText() );
							//transpiler.dumpChildren(ctx, 1);
							TranslationListNode tln = new TranslationListNode(ctx, parent, unary );
							TranslationNode left = tln.getLeftSibling();
							if (left != null) {
								tln.setType( left.getType() );
							}
							if (trailer.getChildCount() >= 2) {
								ParseTree list = trailer.getChild(1);
//								System.out.println(list.toStringTree(transpiler.parser));
								for (int iList = 0; iList < list.getChildCount(); iList += 2) {
									TranslationNode node = getOperandNode(ctx, tln, list.getChild(iList).getPayload());
									if (node == null) {
										//transpiler.dumpChildren((RuleNode) list, 1);
										transpiler.reportError("Untranlated: " + list.getChild(iList).getText() + " " + list.getChild(iList).toStringTree(transpiler.parser) );
										return;
									}
//									System.out.printf("%d %d %s\n", iTrailer, iList, node.toString() );
									translateMap.put( list.getChild(iList).getPayload(), node);
								}
							}
							translateMap.put( trailer.getChild(1).getPayload(), tln);
							break;
						case ".":
							String fieldName = trailer.getChild(i+1).getText(); 
							Symbol field = transpiler.symbolTable.lookup(scope, fieldName);
							if (field == null) {
								TranslationNode prior = parent.getLastChild();
								if (prior instanceof TranslationListNode) {
									prior = prior.getLeftSibling();
								}
								if (prior instanceof TranslationSymbolNode) {
									TranslationSymbolNode tsn = (TranslationSymbolNode) prior;
									Symbol typeClass = transpiler.lookupClass(tsn.getSymbol().getType());
									if (tsn.getSymbol().isEnum()) {
										Scope enumScope = tsn.getSymbol().getScope().getChild(Level.CLASS, tsn.getSymbol().getName());
										field = transpiler.symbolTable.lookup(enumScope, trailer.getChild(i+1).getText() );
										payload = TranslationUnaryNode.staticFieldReference;
									} else if (typeClass != null) {
										Scope objectScope = typeClass.getScope().getChild(Level.CLASS, typeClass.getName());
										field = transpiler.symbolTable.lookup(objectScope, fieldName );
									} else if (tsn.getSymbol().isClass()) {
										Scope classScope = tsn.getSymbol().getScope().getChild(Level.CLASS, tsn.getSymbol().getName());
										field = transpiler.symbolTable.lookup(classScope, trailer.getChild(i+1).getText() );
										payload = TranslationUnaryNode.staticFieldReference;										
									}
								}
								if (field == null) {
//									System.out.println(prior.getClass().getSimpleName() + " " +prior);
									if (prior instanceof TranslationUnaryNode) {
										TranslationUnaryNode tun = (TranslationUnaryNode) prior;
										Symbol s = tun.getRhsSymbol();
										if (s != null) {
											Symbol c = transpiler.lookupClass(s.getType() );
											if (c != null && c.isClass()) { 
												Scope refScope = c.getScope().getChild(Level.CLASS, c.getName());
												field = transpiler.symbolTable.lookup(refScope, fieldName );
											}
										}
									}
								}
							}
							if (field == null) {
								transpiler.reportError( ctx, "Unknown member: " + fieldName + " at " + scope );
								transpiler.dumpChildren(ctx.getParent());
							}
							new TranslationUnaryNode(ctx,  parent, (CommonToken) payload, field );
							
							break;
						}
					}
				}
				this.translateMap.put( ctx.getPayload(), parent);
			}
		}

//atom: ('(' (yield_expr|testlist_comp)? ')' |                      2 () or 3 (x)
//       '[' (testlist_comp)? ']' |
//       '{' (dictorsetmaker)? '}' |
//       NAME | NUMBER | STRING+ | '...' | 'None' | 'True' | 'False');
		@Override
		public void exitAtom(LcdPythonParser.AtomContext ctx) {
//			transpiler.dumpChildren(ctx);
			if (expressionRoot != null) {
				TranslationNode parent = new TranslationSubexpressionNode(ctx, null, "atom");
				Object payload = ctx.getChild(0).getPayload();
				TranslationNode node = getOperandNode( ctx, parent, payload);
				if (node != null && ctx.getChildCount() == 1) {  // NAME | NUMBER |  '...' | 'None' | 'True' | 'False'
					if (parent.getChildCount() == 1) {
						parent = parent.getChild(0);
					}
					translateMap.put( ctx.getPayload(), parent );
					parent.setType( node.getType() );
					return;
				}
				if (node != null) { // STRING+ 
					for (int i = 1; i < ctx.getChildCount(); i++) {
						payload = ctx.getChild(i).getPayload();
						getOperandNode( ctx, parent, payload);
					}
					if (parent.getChildCount() == 1) {
						parent = parent.getChild(0);
					}
					translateMap.put( ctx.getPayload(), parent );
					parent.setType( node.getType() );
					return;
				}
				String value = transpiler.valueMap.get(payload);
				if (value.length() != 1 || "([{".indexOf(value) == -1) {
					//transpiler.reportError(ctx, "Unexpected ATOM token: " + value );
					return;
				}
				parent = new TranslationListNode(ctx,  null, value);
//				System.out.println(ctx.toStringTree(transpiler.parser));				
				for (int i = 1; i < ctx.getChildCount()-1; i++) {
					payload = ctx.getChild(i).getPayload();
					node = translateMap.get(payload);
					if (node == null) {
						node = getOperandNode(ctx, parent, payload);
						translateMap.put( payload, node );
					}
					if (node != null) {
						parent.adopt(node);
						parent.setType( node.getType() );
					}
				}
				translateMap.put( ctx.getPayload(), parent );
			}
		}
		
		@Override
		public void exitSubscriptlist(LcdPythonParser.SubscriptlistContext ctx) {
//			transpiler.dumpChildren(ctx);
			defaultOperandOperator( ctx, "subscriptlist" );
		}

		@Override
		public void exitSubscript(LcdPythonParser.SubscriptContext ctx) {
			defaultOperandOperator( ctx, "subscript" );
		}

		@Override
		public void exitSliceop(LcdPythonParser.SliceopContext ctx) {
			defaultOperandOperator( ctx, "sliceop" );
		}

		@Override
		public void exitExprlist(LcdPythonParser.ExprlistContext ctx) {
			defaultOperandOperator( ctx, "exprlist" );
		}

		@Override
		public void exitTestlist(LcdPythonParser.TestlistContext ctx) {
			defaultOperandOperator( ctx, "testlist" );
		}

		@Override 
		public void exitTestlist_comp(LcdPythonParser.Testlist_compContext ctx) { 
			defaultOperandOperator( ctx, "testlist_comp" );
		}
		
		@Override
		public void exitDictorsetmaker(LcdPythonParser.DictorsetmakerContext ctx) {
			defaultOperandOperator( ctx, "dictorsetmaker" );
		}

	}