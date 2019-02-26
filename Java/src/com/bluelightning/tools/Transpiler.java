/**
 * 
 */
package com.bluelightning.tools;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Stack;

import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonToken;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.ParserRuleContext;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeListener;
import org.antlr.v4.runtime.tree.ParseTreeWalker;
import org.antlr.v4.runtime.tree.RuleNode;
import org.antlr.v4.runtime.tree.TerminalNode;

import com.bluelightning.tools.transpiler.antlr4.LcdPythonBaseListener;
import com.bluelightning.tools.transpiler.antlr4.LcdPythonBaseVisitor;
import com.bluelightning.tools.transpiler.antlr4.LcdPythonLexer;
import com.bluelightning.tools.transpiler.antlr4.LcdPythonParser;

/**
 * @author NOOK
 *
 */
public class Transpiler {
	
	protected StringBuffer errorReport = new StringBuffer();
	
	protected void reportError(ParserRuleContext context, String message ) {
		reportError( context.start, message );
	}
	
	protected void reportError(Token token, String message ) {
		String r = String.format("ERROR [L%5d:C%3d]: %s\n", token.getLine(), token.getCharPositionInLine(), message );
		errorReport.append(r);
	}

	protected Map<Object, String> valueMap = new HashMap<>();
	
	protected static class Scope {
		protected String[] qualifiers; // e.g. com.bluelightning.Filtering
		public enum Level {
			MODULE, FUNCTION, CLASS, MEMBER,
		};
		protected Level  level;
		protected String qString;
		
		protected Scope() {}
		
		public Scope( Level level, List<String> qualifiers) {
			this.level = level;
			this.qualifiers = qualifiers.toArray( new String[qualifiers.size()] );
			StringBuffer sb = new StringBuffer();
			for (String name : qualifiers) {
				sb.append(name);
				sb.append('/');
			}
			qString = sb.toString();			
		}
		
		public Scope getChild( Level childLevel, String childName ) {
//			System.out.println( this.toString() );
			Scope scope = new Scope();
			switch (level) {
			case MODULE: 
				switch (childLevel) {
				case FUNCTION:
				case CLASS:
					scope.level = childLevel;
					break;
				default:
					return null;
				}
				break; 
			case FUNCTION:
				return null;
			case CLASS:
				if (childLevel == Level.FUNCTION)
					scope.level = Level.MEMBER;
				else
					return null;
				break;
			case MEMBER:
				return null;
			}			
			scope.qualifiers = new String[this.qualifiers.length+1];
			StringBuffer sb = new StringBuffer();
			for (int i = 0; i < qualifiers.length; i++) {
				sb.append(qualifiers[i]);
				sb.append('/');
				scope.qualifiers[i] = qualifiers[i];
			}
			sb.append(childName);
			sb.append('/');
			scope.qualifiers[this.qualifiers.length] = childName;
			scope.qString = sb.toString();			
			return scope;
		}
		
		public Scope getParent() {
			Scope scope = new Scope();
			switch (level) {
			case MODULE:
				return null;
			case FUNCTION:
				scope.level = Level.MODULE;
				break;
			case CLASS:
				scope.level = Level.MODULE;
				break;
			case MEMBER:
				scope.level = Level.CLASS;
				break;
			}
			scope.qualifiers = new String[this.qualifiers.length-1];
			StringBuffer sb = new StringBuffer();
			for (int i = 0; i < qualifiers.length; i++) {
				sb.append(qualifiers[i]);
				sb.append('/');
				scope.qualifiers[i] = qualifiers[i];
			}
			scope.qString = sb.toString();			
			return scope;
		}
		
		@Override
		public String toString() {
			return qString;
		}
		
	}

	protected Map<Object, Scope> scopeMap = new HashMap<>();
	
	protected static class Symbol {
		protected String name;
		protected String type;
		protected Scope  scope;
		
		public String toString() {
			return String.format("%s : %s", name, type );
		}
		
		public Symbol( Scope scope, String name, String type ) {
			this.name = name;
			this.type = type;
			this.scope = scope;
		}
	}
	
	protected class SymbolTable {
		protected Map<String, Map<Scope, Symbol> > table = new HashMap<>();
		
		public String toString() {
			StringBuffer sb = new StringBuffer();
			for (String name : table.keySet()) {
				sb.append( String.format("  %s\n", name) );
				Map<Scope, Symbol> aliases = table.get(name);
				for (Scope scope : aliases.keySet()) {
					sb.append( String.format("    %s\n", scope.toString() ));
					sb.append( String.format("      %s\n", aliases.get(scope).toString()));
				}
			}
			return sb.toString();
		}
		
		public void add( Scope scope, String name, String type ) {
			Map<Scope, Symbol> aliases = table.get(name);
			if (aliases == null) {
				aliases = new HashMap<>();
			}
			Symbol symbol = new Symbol( scope, name, type);
			aliases.put( scope, symbol ); //TODO collisions
			table.put(name,  aliases);
		}
		
		public Symbol lookup( Scope scope, String name ) {
			Map<Scope, Symbol> aliases = table.get(name);
			Symbol symbol = aliases.get(scope);
			if (symbol != null)
				return symbol;
			scope = scope.getParent();
			while (scope != null) {
				symbol = aliases.get(scope);
				if (symbol != null)
					return symbol;
				scope = scope.getParent();
			}
			return null;
		}
	}

	protected SymbolTable symbolTable = new SymbolTable();

	protected void processDeclaration(Token token, Scope scope, String str) {
		String[] fields = str.split(":");
		if (fields.length == 2) {
			symbolTable.add(scope, fields[0], fields[1]);
			System.out.println("DECLARED: " + str);
		} else {
			reportError(token, "bad declaration syntax");
		}
	}

	protected void defaultListener(RuleNode node) {
	}

	public static class LanguageTranspiler {
		public LanguageTranspiler() {
		}

		public interface ASTNode {
			public String toString();
		}

		public void emitAssignment(ASTNode target, ASTNode source) {
		}
	}

	/**
	 * LcdPythonPopulateListener - fully populates the value map.
	 */
	protected class PopulateListener extends LcdPythonBaseListener {
		@Override
		public void exitEveryRule(ParserRuleContext ctx) {
//			if (ctx.getChildCount() > 1) {
//				parser.getRuleIndexMap().get(ctx.getRuleContext().getRuleIndex());
//				System.out.println(parser.getRuleNames()[ctx.getRuleContext().getRuleIndex()].toUpperCase() + " "
//						+ ctx.getChildCount() + " " + ctx.getText());
//			}
			StringBuffer result = new StringBuffer();
			for (int i = 0; i < ctx.getChildCount(); i++) {
				ParseTree child = ctx.getChild(i);
				if (child.getPayload() instanceof CommonToken) {
					result.append(child.getText());
					valueMap.put(child.getPayload(), child.getText());
				} else {
					result.append(valueMap.get(child.getPayload()));
				}
				//result.append(' ');
			}
			valueMap.put(ctx.getPayload(), result.toString());
		}
	}

	protected class DeclarationsListener extends LcdPythonBaseListener {

		Stack<Scope> scopeStack = new Stack<>();

		public DeclarationsListener(Scope moduleScope) {
			super();
			scopeStack.push(moduleScope);
		}
		
		protected void dumpChildren( RuleNode ctx ) {
			if (ctx.getChildCount() > 1) {
				parser.getRuleIndexMap().get(ctx.getRuleContext().getRuleIndex());
				System.out.println(parser.getRuleNames()[ctx.getRuleContext().getRuleIndex()].toUpperCase() + " "
						+ ctx.getChildCount() + " " + ctx.getText());
				for (int i = 0; i < ctx.getChildCount(); i++) {
					System.out.printf("%10d: %s\n", i, valueMap.get(ctx.getChild(i).getPayload()));
				}
			}
		}
		
		protected String getChildText( RuleNode ctx, int iChild) {
			return valueMap.get(ctx.getChild(iChild).getPayload());
		}

		protected void declareSymbol( Token token, String declaration ) {
			declaration = declaration.trim().replaceAll(" +", " ");
			String[] fields = declaration.split(":");
			if (fields.length == 2) {
				Scope currentScope = scopeStack.peek();
				symbolTable.add(currentScope, fields[0], fields[1]);
			} else {
				reportError(token, "Ill-formed declaration: " + declaration );
			}
		}
		
		@Override
		public void enterFuncdef(LcdPythonParser.FuncdefContext ctx) {
//			dumpChildren( ctx );
			Scope currentScope = scopeStack.peek();
			String name = getChildText(ctx, 1);
			Scope functionScope = currentScope.getChild(Scope.Level.FUNCTION, name);
			if (functionScope == null) {
				reportError(ctx.start, "Invalid function scope");
			}
			scopeStack.push( functionScope );
			symbolTable.add(functionScope, name, getChildText(ctx, 4)); 
			ParseTree parameterDeclaration = ctx.getChild(2);
			if (parameterDeclaration.getChildCount() > 2) {
				ParseTree parameters = parameterDeclaration.getChild(1);
				for (int i = 0; i < parameters.getChildCount(); i++) {
					String declaration = valueMap.get(parameters.getChild(i).getPayload()).trim();
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
				reportError(ctx.start, "Invalid class scope");
			}
			scopeStack.push( classScope );
			symbolTable.add(classScope, name, "<CLASS>"); 
		}

		@Override
		public void exitClassdef(LcdPythonParser.ClassdefContext ctx) {
//			dumpChildren( ctx );
			scopeStack.pop();
		}
		
		
		@Override 
		public void enterImport_name(LcdPythonParser.Import_nameContext ctx) { 
			dumpChildren( ctx );
			reportError(ctx.start, "Full package imports are not allowed");
		}
		
		@Override 
		public void enterImport_from(LcdPythonParser.Import_fromContext ctx) { 
			dumpChildren( ctx );
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
							reportError(ctx.start, "Ill formed declaration comment: " + str );
						}
					}
				}
			}			
		}
	}

	protected class FullCoverageListener extends LcdPythonBaseListener {

		@Override
		public void enterExpr_stmt(LcdPythonParser.Expr_stmtContext ctx) {
			System.out.println(
					">EXPR_STMT: " + ctx.getText() + " " + ctx.getRuleIndex() + " " + ctx.getRuleContext().getText());
			System.out.println(ctx.toStringTree(parser));
		}

		@Override
		public void exitExpr_stmt(LcdPythonParser.Expr_stmtContext ctx) {
			for (int i = 0; i < ctx.getChildCount(); i++) {
				String value = valueMap.get(ctx.getChild(i).getPayload());
				if (value == null) {
					if (ctx.getChild(i).getPayload() instanceof CommonToken) {
						value = ((CommonToken) ctx.getChild(i).getPayload()).getText();
					} else {
						value = ctx.getChild(i).getPayload().getClass().getSimpleName();
					}
				}
				System.out.printf("EXPR_STMT< %5d: %s\n", i, value);
			}
		}

		@Override
		public void exitSingle_input(LcdPythonParser.Single_inputContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitFile_input(LcdPythonParser.File_inputContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitEval_input(LcdPythonParser.Eval_inputContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitDecorator(LcdPythonParser.DecoratorContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitDecorators(LcdPythonParser.DecoratorsContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitDecorated(LcdPythonParser.DecoratedContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitAsync_funcdef(LcdPythonParser.Async_funcdefContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitFuncdef(LcdPythonParser.FuncdefContext ctx) {
			defaultListener(ctx);
			System.out.println("FUNCDEF " + ctx.getChildCount());
			for (int i = 0; i < ctx.getChildCount(); i++) {
				String name = ctx.getChild(i).getPayload().getClass().getSimpleName();
				String value = name + ": ";
				switch (name) {
				case "CommonToken":
					value += ((CommonToken) ctx.getChild(i).getPayload()).getText();
					break;
				default:
					value = valueMap.get(ctx.getChild(i).getPayload());
					if (value == null) {
						value = name + ": " + ctx.getChild(i).toStringTree(parser);
					} else {
						value = name + ": " + value;
					}
				}
				System.out.printf("%10d %s\n", i, value);
			}
		}

		@Override
		public void exitParameters(LcdPythonParser.ParametersContext ctx) {
			defaultListener(ctx);
			System.out.println("PARAMETERS " + ctx.getChildCount());
			for (int i = 0; i < ctx.getChildCount(); i++) {
				String name = ctx.getChild(i).getPayload().getClass().getSimpleName();
				String value = name + ": ";
				switch (name) {
				case "CommonToken":
					value += ((CommonToken) ctx.getChild(i).getPayload()).getText();
					break;
				case "TypedargslistContext":
					value = name + ": " + ctx.getChild(i).toStringTree(parser);
					for (int j = 0; j < ctx.getChild(i).getChildCount(); j += 2) {
						String decl = valueMap.get(ctx.getChild(i).getChild(j).getPayload());
						System.out.printf("%12d%5d: %s\n", i, j, decl);
						decl = decl.trim().replaceAll(" +", " ");
//						processDeclaration(decl);
					}
					break;
				default:
					value = valueMap.get(ctx.getChild(i).getPayload());
					if (value == null) {
						value = name + ": " + ctx.getChild(i).toStringTree(parser);
					} else {
						value = name + ": " + value;
					}
				}
				System.out.printf("%10d %s\n", i, value);
			}
		}

		@Override
		public void exitTypedargslist(LcdPythonParser.TypedargslistContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitTfpdef(LcdPythonParser.TfpdefContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitVarargslist(LcdPythonParser.VarargslistContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitVfpdef(LcdPythonParser.VfpdefContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitStmt(LcdPythonParser.StmtContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitSimple_stmt(LcdPythonParser.Simple_stmtContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitSmall_stmt(LcdPythonParser.Small_stmtContext ctx) {
			defaultListener(ctx);
		}

		// @Override public void exitExpr_stmt(LcdPythonParser.Expr_stmtContext
		// ctx) { defaultListener(ctx); }
		@Override
		public void exitAnnassign(LcdPythonParser.AnnassignContext ctx) {
			defaultListener(ctx);
		}

		// @Override public void
		// exitTestlist_star_expr(LcdPythonParser.Testlist_star_exprContext ctx)
		// {
		// defaultListener(ctx); }
		@Override
		public void exitAugassign(LcdPythonParser.AugassignContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitDel_stmt(LcdPythonParser.Del_stmtContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitPass_stmt(LcdPythonParser.Pass_stmtContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitFlow_stmt(LcdPythonParser.Flow_stmtContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitBreak_stmt(LcdPythonParser.Break_stmtContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitContinue_stmt(LcdPythonParser.Continue_stmtContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitReturn_stmt(LcdPythonParser.Return_stmtContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitYield_stmt(LcdPythonParser.Yield_stmtContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitRaise_stmt(LcdPythonParser.Raise_stmtContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitImport_stmt(LcdPythonParser.Import_stmtContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitImport_name(LcdPythonParser.Import_nameContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitImport_from(LcdPythonParser.Import_fromContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitImport_as_name(LcdPythonParser.Import_as_nameContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitDotted_as_name(LcdPythonParser.Dotted_as_nameContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitImport_as_names(LcdPythonParser.Import_as_namesContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitDotted_as_names(LcdPythonParser.Dotted_as_namesContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitDotted_name(LcdPythonParser.Dotted_nameContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitGlobal_stmt(LcdPythonParser.Global_stmtContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitNonlocal_stmt(LcdPythonParser.Nonlocal_stmtContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitAssert_stmt(LcdPythonParser.Assert_stmtContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitCompound_stmt(LcdPythonParser.Compound_stmtContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitAsync_stmt(LcdPythonParser.Async_stmtContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitIf_stmt(LcdPythonParser.If_stmtContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitWhile_stmt(LcdPythonParser.While_stmtContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitFor_stmt(LcdPythonParser.For_stmtContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitTry_stmt(LcdPythonParser.Try_stmtContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitWith_stmt(LcdPythonParser.With_stmtContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitWith_item(LcdPythonParser.With_itemContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitExcept_clause(LcdPythonParser.Except_clauseContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitSuite(LcdPythonParser.SuiteContext ctx) {
			defaultListener(ctx);
		}

		// @Override public void exitTest(LcdPythonParser.TestContext ctx) {
		// defaultListener(ctx); }
		@Override
		public void exitTest_nocond(LcdPythonParser.Test_nocondContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitLambdef(LcdPythonParser.LambdefContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitLambdef_nocond(LcdPythonParser.Lambdef_nocondContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitOr_test(LcdPythonParser.Or_testContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitAnd_test(LcdPythonParser.And_testContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitNot_test(LcdPythonParser.Not_testContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitComparison(LcdPythonParser.ComparisonContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitComp_op(LcdPythonParser.Comp_opContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitStar_expr(LcdPythonParser.Star_exprContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitExpr(LcdPythonParser.ExprContext ctx) {
			defaultListener(ctx);
		}

		// @Override public void exitXor_expr(LcdPythonParser.Xor_exprContext
		// ctx)
		// { defaultListener(ctx); }
		// @Override public void exitAnd_expr(LcdPythonParser.And_exprContext
		// ctx)
		// { defaultListener(ctx); }
		// @Override public void
		// exitShift_expr(LcdPythonParser.Shift_exprContext
		// ctx) { defaultListener(ctx); }
		// @Override public void
		// exitArith_expr(LcdPythonParser.Arith_exprContext
		// ctx) { defaultListener(ctx); }
		// @Override public void exitTerm(LcdPythonParser.TermContext ctx) {
		// defaultListener(ctx); }
		// @Override public void exitFactor(LcdPythonParser.FactorContext ctx) {
		// defaultListener(ctx); }
		// @Override public void exitPower(LcdPythonParser.PowerContext ctx) {
		// defaultListener(ctx); }
		@Override
		public void exitAtom_expr(LcdPythonParser.Atom_exprContext ctx) {
			defaultListener(ctx);
		}

		// @Override public void exitAtom(LcdPythonParser.AtomContext ctx) {
		// defaultListener(ctx); }
		// @Override public void
		// exitTestlist_comp(LcdPythonParser.Testlist_compContext ctx) {
		// defaultListener(ctx); }
		@Override
		public void exitTrailer(LcdPythonParser.TrailerContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitSubscriptlist(LcdPythonParser.SubscriptlistContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitSubscript(LcdPythonParser.SubscriptContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitSliceop(LcdPythonParser.SliceopContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitExprlist(LcdPythonParser.ExprlistContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitTestlist(LcdPythonParser.TestlistContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitDictorsetmaker(LcdPythonParser.DictorsetmakerContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitClassdef(LcdPythonParser.ClassdefContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitArglist(LcdPythonParser.ArglistContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitArgument(LcdPythonParser.ArgumentContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitComp_iter(LcdPythonParser.Comp_iterContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitComp_for(LcdPythonParser.Comp_forContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitComp_if(LcdPythonParser.Comp_ifContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitEncoding_decl(LcdPythonParser.Encoding_declContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitYield_expr(LcdPythonParser.Yield_exprContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitYield_arg(LcdPythonParser.Yield_argContext ctx) {
			defaultListener(ctx);
		}

		// @Override
		// public void exitEveryRule(ParserRuleContext ctx) {
		// defaultListener(ctx);
		// }

		@Override
		public void exitXor_expr(LcdPythonParser.Xor_exprContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitAnd_expr(LcdPythonParser.And_exprContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitShift_expr(LcdPythonParser.Shift_exprContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitTest(LcdPythonParser.TestContext ctx) {
			defaultListener(ctx);
		}

		// arith_expr: term (('+'|'-') term)*;
		@Override
		public void exitArith_expr(LcdPythonParser.Arith_exprContext ctx) {
			defaultListener(ctx);
		}

		/**
		 * {@inheritDoc}
		 *
		 * <p>
		 * The default implementation does nothing.
		 * </p>
		 */
		@Override
		public void exitTestlist_star_expr(LcdPythonParser.Testlist_star_exprContext ctx) {
			defaultListener(ctx);
		}

		@Override
		public void exitTestlist_comp(LcdPythonParser.Testlist_compContext ctx) {
			defaultListener(ctx);
		}

		// expr: xor_expr ('|' xor_expr)*;

		// factor: ('+'|'-'|'~') factor | power;
		@Override
		public void exitFactor(LcdPythonParser.FactorContext ctx) {
			defaultListener(ctx);
		}

		// power: atom_expr ('**' factor)?;
		// children:
		// (ANY, CommonToken)* ANY
		//
		@Override
		public void exitPower(LcdPythonParser.PowerContext ctx) {
			defaultListener(ctx);
		}

		// term: factor (('*'|'@'|'/'|'%'|'//') factor)*;
		// children:
		// (ANY, CommonToken)* ANY
		@Override
		public void exitTerm(LcdPythonParser.TermContext ctx) {
			defaultListener(ctx);
		}

		/**
		 * {@inheritDoc}
		 *
		 * <p>
		 * The default implementation does nothing.
		 * </p>
		 */
		@Override
		public void exitAtom(LcdPythonParser.AtomContext ctx) {
			StringBuffer result = new StringBuffer();
			for (int i = 0; i < ctx.getChildCount(); i++) {
				ParseTree child = ctx.getChild(i);
				if (child.getPayload() instanceof CommonToken) {
					result.append(child.getText());
					result.append(' ');
				} else {
					String value = valueMap.get(child.getPayload());
					if (value != null) {
						result.append(value);
					} else {
						result.append(child.getPayload().getClass().getName() + " " + child.toStringTree());
					}
					result.append(' ');
				}
			}
			String str = result.toString();
			valueMap.put(ctx.getPayload(), str);
			str = str.trim().replaceAll(" +", " ");
			if (str.startsWith("'''@") && str.endsWith("'''")) {
				//processDeclaration(str.replaceAll("'''@", "").replaceAll("'''", ""));
			} else {
				System.out.println("ATOM: [" + str + "]");
			}
		}
	}

	// protected class LcdPythonListener extends Python3BaseListener {
	// @Override
	// public void enterStmt(LcdPythonParser.StmtContext ctx) {
	// System.out.println(">STMT");
	// }
	//
	// @Override
	// public void enterSimple_stmt(LcdPythonParser.Simple_stmtContext ctx) {
	// System.out.println(">SIMPLE_STMT");
	// }
	//
	// @Override
	// public void enterSmall_stmt(LcdPythonParser.Small_stmtContext ctx) {
	// System.out.println(">SMALL_STMT");
	// if (ctx.expr_stmt() != null) {
	// ExpressionListener expressionListener = new ExpressionListener();
	// ParseTreeWalker walker = new ParseTreeWalker();
	// walker.walk(expressionListener, ctx.expr_stmt());
	// }
	// }
	// }

	protected String content;
	protected LcdPythonParser parser;

	public Transpiler(String pythonSource) {
		try {
			byte[] bytes = Files.readAllBytes(
//					Paths.get("../Python/src/PolynomialFiltering/Main.py"));
					Paths.get("../Python/src/TranspilerTest.py"));
			content = new String(bytes, "UTF-8");
		} catch (Exception x) {
			x.printStackTrace();
			return;
		}
		// content = "A*(B+1)**-0.5";
		LcdPythonLexer java8Lexer = new LcdPythonLexer(CharStreams.fromString(content));
		CommonTokenStream tokens = new CommonTokenStream(java8Lexer);
		parser = new LcdPythonParser(tokens);
		ParseTree tree = parser.file_input();
		
		// PASS 1 - fully populate parse tree contents map
		PopulateListener populateListener = new PopulateListener();
		ParseTreeWalker walker = new ParseTreeWalker();
		walker.walk(populateListener, tree);
		
		// PASS 2 - handle all imports, variable, function, and class declarations
		Scope moduleScope = new Scope(Scope.Level.MODULE, Arrays.asList( new String[] {
				"TranspilerTest" } ) );
//				"PolynomialFiltering",
//				"Main"} ) );
		DeclarationsListener scopeListener = new DeclarationsListener(moduleScope);
		walker.walk(scopeListener, tree);
		
		System.out.println("\n\n-------------------------------------");
		System.out.println("--SYMBOL TABLE\n");
		System.out.println( symbolTable.toString() );
		if (errorReport.length() > 0) {
			System.err.println("\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n");
			System.err.println(errorReport.toString());
		} else {
			System.out.println("\n\nNO ERRORS");
		}
	}

	protected static void compileGrammar(String libPath, String gPath, String outPath) {
		File file = new File(".");
		String lwd = file.getAbsolutePath();
		System.setProperty("user.dir", libPath);

		// org.antlr.v4.Tool.main( new String[]{} ); // always show help
		String[] args = { "-lib", libPath, "-o", outPath, "-package", "com.bluelightning.tools.antlr4", "-listener",
				"-visitor", gPath };
		org.antlr.v4.Tool.main(args); // new String[]{} );
		System.setProperty("user.dir", lwd);
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// compileGrammar( "data", "LcdPython.g4",
		// "src/com/bluelightning/tools/transpiler/antlr4/" );
		Transpiler transpiler = new Transpiler("");
	}

}
