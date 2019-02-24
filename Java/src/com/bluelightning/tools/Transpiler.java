/**
 * 
 */
package com.bluelightning.tools;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;

import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonToken;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.ParserRuleContext;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeListener;
import org.antlr.v4.runtime.tree.ParseTreeWalker;
import org.antlr.v4.runtime.tree.RuleNode;
import org.antlr.v4.runtime.tree.TerminalNode;

import com.bluelightning.tools.antlr4.Python3BaseListener;
import com.bluelightning.tools.antlr4.Python3BaseVisitor;
import com.bluelightning.tools.antlr4.Python3Lexer;
import com.bluelightning.tools.antlr4.Python3Parser;

/**
 * @author NOOK
 *
 */
public class Transpiler {

	// protected class LcdPythonVisitor extends Python3BaseVisitor<String> {
	// @Override public String visitTerm(Python3Parser.TermContext ctx) {
	// System.out.println(ctx);
	// return visitChildren(ctx);
	// }
	// }

	protected void ruleAllDescendants(ParseTreeListener listener, ParserRuleContext ctx) {
		for (int i = 0; i < ctx.getChildCount(); i++) {
			ParseTree tree = ctx.getChild(i);
			if (tree instanceof ParserRuleContext) {
				ParserRuleContext prc = (ParserRuleContext) tree.getPayload();
				prc.enterRule(listener);
				ruleAllDescendants(listener, prc);
			} else if (tree instanceof TerminalNode) {
				// TerminalNode tn = (TerminalNode) tree.getPayload();
			} else {
				System.out.println("???" + tree.getClass().getName());
			}
		}
	}

	// How to nest listeners:
	// http://jakubdziworski.github.io/java/2016/04/01/antlr_visitor_vs_listener.html

	protected class ExpressionTranpiler {
		public ExpressionTranpiler() {
		}

		// public String
	}

	protected class ExpressionVisitor extends Python3BaseVisitor<String> {

		@Override
		public String visitChildren(RuleNode node) {
			StringBuffer result = new StringBuffer();
			for (int i = 0; i < node.getChildCount(); i++) {
				ParseTree child = node.getChild(i);
				if (child.getPayload() instanceof CommonToken) {
					result.append(child.getText());
				} else {
					result.append(this.visit(child));
				}
				result.append(' ');
			}
			return result.toString();
		}

		/**
		 * {@inheritDoc}
		 *
		 * <p>
		 * The default implementation returns the result of calling
		 * {@link #visitChildren} on {@code ctx}.
		 * </p>
		 */
		@Override
		public String visitStmt(Python3Parser.StmtContext ctx) {
			return visitChildren(ctx) + "\n";
		}

		/**
		 * {@inheritDoc}
		 *
		 * <p>
		 * The default implementation returns the result of calling
		 * {@link #visitChildren} on {@code ctx}.
		 * </p>
		 */
		@Override
		public String visitExpr_stmt(Python3Parser.Expr_stmtContext ctx) {
			return visitChildren(ctx);
		}

		/**
		 * {@inheritDoc}
		 *
		 * <p>
		 * The default implementation returns the result of calling
		 * {@link #visitChildren} on {@code ctx}.
		 * </p>
		 */
		@Override
		public String visitFuncdef(Python3Parser.FuncdefContext ctx) {
			return visitChildren(ctx) + "\n";
		}

		/**
		 * {@inheritDoc}
		 *
		 * <p>
		 * The default implementation returns the result of calling
		 * {@link #visitChildren} on {@code ctx}.
		 * </p>
		 */
		@Override
		public String visitAtom(Python3Parser.AtomContext ctx) {
			StringBuffer result = new StringBuffer();
			for (int i = 0; i < ctx.getChildCount(); i++) {
				ParseTree child = ctx.getChild(i);
				if (child.getPayload() instanceof CommonToken) {
					result.append(child.getText());
					result.append(' ');
				} else {
					result.append(this.visit(child));
					result.append(' ');
				}
			}
			return result.toString();
		}
	}

	protected class ExpressionListener extends Python3BaseListener {
		
		Map<Object, String> valueMap = new HashMap<Object, String>();

		@Override
		public void enterExpr_stmt(Python3Parser.Expr_stmtContext ctx) {
			System.out.println(
					">EXPR_STMT: " + ctx.getText() + " " + ctx.getRuleIndex() + " " + ctx.getRuleContext().getText());
//			ruleAllDescendants(this, ctx);
		}

		@Override
		public void exitExpr_stmt(Python3Parser.Expr_stmtContext ctx) {
			System.out.println(
					"<EXPR_STMT: " + ctx.getText() + " " + ctx.getRuleIndex() + " " + ctx.getRuleContext().getText());
		}

		// arith_expr: term (('+'|'-') term)*;
		@Override
		public void exitArith_expr(Python3Parser.Arith_exprContext ctx) {
			if (ctx.getChildCount() <= 1)
				return;
			System.out.println(
					"ARITH_EXPR: " + ctx.getText() + " " + ctx.getRuleIndex() + " " + ctx.getRuleContext().getText());
			for (int i = 0; i < ctx.getChildCount(); i++) {
				ParseTree child = ctx.getChild(i);
				System.out.println("   " + child.getPayload().getClass().getName() + " " + child.getText());
			}
		}

		// expr: xor_expr ('|' xor_expr)*;

		// factor: ('+'|'-'|'~') factor | power;
		@Override
		public void exitFactor(Python3Parser.FactorContext ctx) {
			if (ctx.getChildCount() <= 1)
				return;
			System.out.println(
					"FACTOR: " + ctx.getText() + " " + ctx.getRuleIndex() + " " + ctx.getRuleContext().getText());
			for (int i = 0; i < ctx.getChildCount(); i++) {
				ParseTree child = ctx.getChild(i);
				System.out.println("   " + child.getPayload().getClass().getName() + " " + child.getText());
			}
		}

		// power: atom_expr ('**' factor)?;
		// children:
		// (ANY, CommonToken)* ANY
		//
		@Override
		public void exitPower(Python3Parser.PowerContext ctx) {
			if (ctx.getChildCount() <= 1)
				return;
			System.out.println(
					"POWER: " + ctx.getText() + " " + ctx.getRuleIndex() + " " + ctx.getRuleContext().getText());
			for (int i = 0; i < ctx.getChildCount(); i++) {
				ParseTree child = ctx.getChild(i);
				System.out.println("   " + child.getPayload().getClass().getName() + " " + child.getText());
			}
		}

		// term: factor (('*'|'@'|'/'|'%'|'//') factor)*;
		// children:
		// (ANY, CommonToken)* ANY
		@Override
		public void exitTerm(Python3Parser.TermContext ctx) {
			if (ctx.getChildCount() <= 1)
				return;
			// System.out.println(ctx.toInfoString(parser));
			// System.out.println(ctx.toStringTree(parser));
			System.out.println(
					"TERM: " + ctx.getText() + " " + ctx.getRuleIndex() + " " + ctx.getRuleContext().getText());
			for (int i = 0; i < ctx.getChildCount(); i++) {
				ParseTree child = ctx.getChild(i);
				System.out.println("   " + child.getPayload().getClass().getName() + " " + child.getText());
			}
		}
		
		/**
		 * {@inheritDoc}
		 *
		 * <p>The default implementation does nothing.</p>
		 */
		@Override 
		public void exitAtom(Python3Parser.AtomContext ctx) { 
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
			System.out.println("ATOM: " + result.toString());
		}		
	}

	protected class LcdPythonListener extends Python3BaseListener {
		@Override
		public void enterStmt(Python3Parser.StmtContext ctx) {
			System.out.println(">STMT");
		}

		@Override
		public void enterSimple_stmt(Python3Parser.Simple_stmtContext ctx) {
			System.out.println(">SIMPLE_STMT");
		}

		@Override
		public void enterSmall_stmt(Python3Parser.Small_stmtContext ctx) {
			System.out.println(">SMALL_STMT");
			if (ctx.expr_stmt() != null) {
				ExpressionListener expressionListener = new ExpressionListener();
				ParseTreeWalker walker = new ParseTreeWalker();
				walker.walk(expressionListener, ctx.expr_stmt());
			}
		}
	}

	protected String content;
	protected Python3Parser parser;

	public Transpiler(String pythonSource) {
		try {
			byte[] bytes = Files.readAllBytes(Paths.get("../Python/src/TranspilerTest.py"));
			content = new String(bytes, "UTF-8");
		} catch (Exception x) {
			x.printStackTrace();
			return;
		}
		// content = "A*(B+1)**-0.5";
		Python3Lexer java8Lexer = new Python3Lexer(CharStreams.fromString(content));
		CommonTokenStream tokens = new CommonTokenStream(java8Lexer);
		parser = new Python3Parser(tokens);
		ParseTree tree = parser.file_input();
		LcdPythonListener listener = new LcdPythonListener();
		ParseTreeWalker walker = new ParseTreeWalker();
		walker.walk(listener, tree);
		// String result = new ExpressionVisitor().visit(tree).replaceAll(" +",
		// " ");
		// System.out.println(result);
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
		// compileGrammar( "data", "Python3.g4",
		// "src/com/bluelightning/tools/antlr4/" );
		Transpiler transpiler = new Transpiler("");
	}

}
