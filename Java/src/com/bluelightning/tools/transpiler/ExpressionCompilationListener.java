package com.bluelightning.tools.transpiler;

import java.util.HashMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.antlr.v4.runtime.CommonToken;
import org.antlr.v4.runtime.ParserRuleContext;

import com.bluelightning.tools.transpiler.antlr4.LcdPythonBaseListener;
import com.bluelightning.tools.transpiler.antlr4.LcdPythonParser;

class ExpressionCompilationListener extends LcdPythonBaseListener {
		
		/**
		 * 
		 */
		private final Transpiler transpiler;
		
		/**
		 * @param transpiler
		 */
		ExpressionCompilationListener(Transpiler transpiler) {
			this.transpiler = transpiler;
			scope = this.transpiler.moduleScope;
			System.out.println("module > " + scope);
		}

		Scope scope = null;
		TranslationNode expressionRoot = null;
		HashMap<Object, TranslationNode> translateMap = null;
		

		
		protected static final Pattern integerPattern = Pattern.compile("^(\\d+)$");
		protected static final Pattern floatPattern = Pattern.compile("^(\\d+)\\.(\\\\d*)$");
		
		protected TranslationNode defaultOperandOperator( ParserRuleContext ctx, String tag ) {
			if (expressionRoot != null) {
//				System.out.println( tag + " (" + ctx.getChildCount() + ")");
				TranslationNode parent = new TranslationNode(null, tag);
				if (ctx.getChildCount() == 1) {
					TranslationNode node = translateMap.get(ctx.getChild(0).getPayload());
					if (node == null) {
						node = getOperandNode( ctx, parent, ctx.getChild(0).getPayload());
						if (node == null) {
							String operator = this.transpiler.valueMap.get(ctx.getChild(0).getPayload());
							node = new TranslationOperatorNode( parent, operator );
						}
					}
					translateMap.put( ctx.getPayload(), node );
					return node;
				} else if (ctx.getChildCount() == 2) {
					TranslationNode node = new TranslationUnaryNode( parent, 
							ctx.getChild(0).getPayload(), ctx.getChild(1).getPayload());
				} else {
					TranslationNode node = getOperandNode( ctx, parent, ctx.getChild(0).getPayload());
					if (node == null) {
						String value = this.transpiler.valueMap.get(ctx.getChild(0).getPayload());
						this.transpiler.reportError(ctx, "Operand neither symbol nor constant nor subexpression: " + 
								ctx.getChild(0).getPayload().getClass().getSimpleName() + " : " + value);

					}
					for (int i = 1; i < ctx.getChildCount(); i += 2) {
						String operator = this.transpiler.valueMap.get(ctx.getChild(i).getPayload());
						node = new TranslationOperatorNode( parent, operator );
						node = getOperandNode( ctx, parent, ctx.getChild(i+1).getPayload());
						if (node == null) {
							transpiler.reportError(ctx, "No operand node: " + (i+1));
						}
					}
				}
				translateMap.put( ctx.getPayload(), parent );
//				System.out.println( parent.traverse(2));
				return parent;
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
				node = new TranslationSymbolNode( parent, symbol );
				translateMap.put( payload, node );
				return node;
			}
			if (value.startsWith("'") || value.startsWith("\"")) {
				node = new TranslationConstantNode( parent, value );
				translateMap.put( payload, node );
				return node;
			}
			Matcher matcher = integerPattern.matcher(value);
			if (matcher.matches()) {
				node = new TranslationConstantNode( parent, value );
				translateMap.put( payload, node );
				return node;				
			}
			matcher = floatPattern.matcher(value);
			if (matcher.matches()) {
				node = new TranslationConstantNode( parent, value );
				translateMap.put( payload, node );
				return node;				
			}
			return null;
		}

		@Override
		public void enterClassdef(LcdPythonParser.ClassdefContext ctx) {
			scope = this.transpiler.scopeMap.get(ctx.getPayload());
			System.out.println("class > " + scope);
			transpiler.dispatcher.startClass(scope);
		}
		
		@Override
		public void exitClassdef(LcdPythonParser.ClassdefContext ctx) {
			scope = scope.getParent();
			System.out.println("class < " + scope);
			transpiler.dispatcher.finishClass(scope);
		}
		
		@Override
		public void enterFuncdef(LcdPythonParser.FuncdefContext ctx) {
			scope = this.transpiler.scopeMap.get(ctx.getPayload());
			System.out.println("function > " + scope);
			transpiler.dispatcher.startMethod(scope);
		}
		
		@Override
		public void exitFuncdef(LcdPythonParser.FuncdefContext ctx) {
			scope = scope.getParent();
			System.out.println("function < " + scope);
			transpiler.dispatcher.finishMethod(scope);
		}
		
		
		@Override
		public void enterExpr_stmt(LcdPythonParser.Expr_stmtContext ctx) {
			System.out.println( ctx.toStringTree(transpiler.parser));
			String value = this.transpiler.valueMap.get(ctx.getPayload());
			if (! value.startsWith("'''")) {
				System.out.println("EXPR_STMT> [{" + value + "}]" );
//				this.transpiler.dumpChildren( ctx );
				expressionRoot = new TranslationNode(null, "EXPR_STMT");
				translateMap = new HashMap<>();
			}
		}

		@Override
		public void exitExpr_stmt(LcdPythonParser.Expr_stmtContext ctx) {
			if (expressionRoot != null) {
				TranslationNode expr = defaultOperandOperator( ctx, "Expr_stmt" );
				expressionRoot = expr; //.adopt(expr);
				System.out.println( expressionRoot.traverse(2) );
				transpiler.dispatcher.emitExpressionStatement(scope, expressionRoot);
			}
		}		
		
		@Override
		public void exitAnnassign(LcdPythonParser.AnnassignContext ctx) {
			defaultOperandOperator( ctx, "Annassign" );
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
			defaultOperandOperator( ctx, "power" );
		}

		@Override
		public void exitAtom_expr(LcdPythonParser.Atom_exprContext ctx) {
			defaultOperandOperator( ctx, "atmoexpr" );
		}

		@Override
		public void exitAtom(LcdPythonParser.AtomContext ctx) {
			defaultOperandOperator( ctx, "atom" );
		}
		
		@Override
		public void exitSubscriptlist(LcdPythonParser.SubscriptlistContext ctx) {
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
		public void exitDictorsetmaker(LcdPythonParser.DictorsetmakerContext ctx) {
			defaultOperandOperator( ctx, "dictorsetmaker" );
		}

	}