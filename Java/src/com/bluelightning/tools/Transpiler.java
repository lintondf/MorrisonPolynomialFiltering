/**
 * 
 */
package com.bluelightning.tools;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Paths;

import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.ParserRuleContext;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeWalker;
import org.antlr.v4.runtime.tree.TerminalNode;

import com.bluelightning.tools.antlr4.Python3BaseListener;
import com.bluelightning.tools.antlr4.Python3Lexer;
import com.bluelightning.tools.antlr4.Python3Parser;

/**
 * @author NOOK
 *
 */
public class Transpiler {
	
//	protected class LcdPythonVisitor extends Python3BaseVisitor<String> {
//		@Override public String visitTerm(Python3Parser.TermContext ctx) { 
//			System.out.println(ctx);
//			return visitChildren(ctx); 
//		}		
//	}
	
	
	// How to nest listeners:
	//  http://jakubdziworski.github.io/java/2016/04/01/antlr_visitor_vs_listener.html
	
	protected class ExpressionTranpiler {
		public ExpressionTranpiler() {}
		
//		public String
	}
	
	protected class ExpressionListener extends Python3BaseListener {
		/*
		   expr_stmt: testlist_star_expr (annassign | augassign (yield_expr|testlist) | ('=' (yield_expr|testlist_star_expr))*);
              testlist_star_expr: (test|star_expr) (',' (test|star_expr))* (',')?;
                test: or_test ('if' or_test 'else' test)? | lambdef;
                  or_test:and_test ('or' and_test)*;
                    and_test: not_test ('and' not_test)*;
                      not_test: 'not' not_test | comparison;
                        comparison: expr (comp_op expr)*;
                          comp_op: '<'|'>'|'=='|'>='|'<='|'<>'|'!='|'in'|'not' 'in'|'is'|'is' 'not';
                            star_expr: '*' expr;
                              expr: xor_expr ('|' xor_expr)*;
                                xor_expr: and_expr ('^' and_expr)*;
                                  and_expr: shift_expr ('&' shift_expr)*;
                                    shift_expr: arith_expr (('<<'|'>>') arith_expr)*;
                                      arith_expr: term (('+'|'-') term)*;
                                        term: factor (('*'|'@'|'/'|'%'|'//') factor)*;
                                          factor: ('+'|'-'|'~') factor | power;
                                            power: atom_expr ('**' factor)?;
                                              atom_expr: (AWAIT)? atom trailer*;
												atom: ('(' (yield_expr|testlist_comp)? ')' |
												       '[' (testlist_comp)? ']' |
												       '{' (dictorsetmaker)? '}' |
												       NAME | NUMBER | STRING+ | '...' | 'None' | 'True' | 'False');                   
                    
                  lambdef: DO NOT SUPPORT
              annassign: ':' test ('=' test)?;
                test:
              augassign: ('+=' | '-=' | '*=' | '@=' | '/=' | '%=' | '&=' | '|=' | '^=' | '<<=' | '>>=' | '**=' | '//=');
                TERMINAL
              yield_expr: DO NOT SUPPORT
              testlist: test (',' test)* (',')?;
                test
              
             
		 */
		
		protected void ruleAllDescendants( ParserRuleContext ctx ) {
			for (int i = 0; i < ctx.getChildCount(); i++) {
				ParseTree tree = ctx.getChild(i);
				if (tree instanceof ParserRuleContext) {
					ParserRuleContext prc = (ParserRuleContext) tree.getPayload();
					prc.enterRule(this);
					ruleAllDescendants( prc );
				} else if (tree instanceof TerminalNode) {
					//TerminalNode tn = (TerminalNode) tree.getPayload();
				} else {
					System.out.println( "???" + tree.getClass().getName() );
				}
			}
		}
		
		@Override 
		public void enterExpr_stmt(Python3Parser.Expr_stmtContext ctx) { 			
			System.out.println(">EXPR_STMT: " + ctx.getText() + " " + ctx.getRuleIndex() + " " + ctx.getRuleContext().getText());
			ruleAllDescendants( ctx );
		}

	
		@Override 
		public void exitExpr_stmt(Python3Parser.Expr_stmtContext ctx) { 
			System.out.println("<EXPR_STMT: " + ctx.getText() + " " + ctx.getRuleIndex() + " " + ctx.getRuleContext().getText());
		}
		
		//arith_expr: term (('+'|'-') term)*;
		@Override 
		public void enterArith_expr(Python3Parser.Arith_exprContext ctx) { 
			if (ctx.getChildCount() <= 1)
				return;
			System.out.println("ARITH_EXPR: " + ctx.getText() + " " + ctx.getRuleIndex() + " " + ctx.getRuleContext().getText());
			for (int i = 0; i < ctx.getChildCount(); i++) {
				ParseTree child = ctx.getChild(i);
				System.out.println("   " + child.getPayload().getClass().getName() + " " + child.getText() );
			}
		}
		
		//expr: xor_expr ('|' xor_expr)*;
		
		//factor: ('+'|'-'|'~') factor | power;
		@Override 
		public void exitFactor(Python3Parser.FactorContext ctx) { 
			if (ctx.getChildCount() <= 1)
				return;
			System.out.println("FACTOR: " + ctx.getText() + " " + ctx.getRuleIndex() + " " + ctx.getRuleContext().getText());
			for (int i = 0; i < ctx.getChildCount(); i++) {
				ParseTree child = ctx.getChild(i);
				System.out.println("   " + child.getPayload().getClass().getName() + " " + child.getText() );
			}
		}
		
		//power: atom_expr ('**' factor)?;
		//children:
		//  (ANY, CommonToken)* ANY
		//
		@Override 
		public void enterPower(Python3Parser.PowerContext ctx) {
			if (ctx.getChildCount() <= 1)
				return;
			System.out.println("POWER: " + ctx.getText() + " " + ctx.getRuleIndex() + " " + ctx.getRuleContext().getText());
			for (int i = 0; i < ctx.getChildCount(); i++) {
				ParseTree child = ctx.getChild(i);
				System.out.println("   " + child.getPayload().getClass().getName() + " " + child.getText() );
			}
		}

		//term: factor (('*'|'@'|'/'|'%'|'//') factor)*;
		//children:
		//  (ANY, CommonToken)* ANY
		@Override 
		public void enterTerm(Python3Parser.TermContext ctx) { 
			if (ctx.getChildCount() <= 1)
				return;
			//System.out.println(ctx.toInfoString(parser));
			//System.out.println(ctx.toStringTree(parser));
			System.out.println("TERM: " + ctx.getText() + " " + ctx.getRuleIndex() + " " + ctx.getRuleContext().getText());
			for (int i = 0; i < ctx.getChildCount(); i++) {
				ParseTree child = ctx.getChild(i);
				System.out.println("   " + child.getPayload().getClass().getName() + " " + child.getText() );
			}
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
				ctx.expr_stmt().enterRule(expressionListener);
			}
		}
	}
	
	protected String content;
	protected Python3Parser parser;
	
	public Transpiler(String pythonSource) {
		try {
			byte[] bytes = Files.readAllBytes( Paths.get("../Python/src/PolynomialFiltering/Main.py"));
			content = new String(bytes, "UTF-8");
		} catch (Exception x) {
			return;
		}
		Python3Lexer java8Lexer = new Python3Lexer(CharStreams.fromString(content));
		CommonTokenStream tokens = new CommonTokenStream(java8Lexer);
		parser = new Python3Parser(tokens);
		ParseTree tree = parser.file_input();
		ParseTreeWalker walker = new ParseTreeWalker();
		LcdPythonListener listener= new LcdPythonListener();
		walker.walk(listener, tree);
	}
	
	protected static void compileGrammar( String libPath, String gPath, String outPath ) {
		File file = new File(".");
		String lwd = file.getAbsolutePath();
		System.setProperty("user.dir", libPath);

		//org.antlr.v4.Tool.main( new String[]{} );  // always show help
		String[] args = {
				"-lib", libPath,
				"-o", outPath,
				"-package", "com.bluelightning.tools.antlr4",
				"-listener", "-visitor",
				gPath
		};
		org.antlr.v4.Tool.main( args ); // new String[]{} );
		System.setProperty("user.dir", lwd);
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		//compileGrammar( "data", "Python3.g4", "src/com/bluelightning/tools/antlr4/" );
		Transpiler transpiler = new Transpiler("");
	}

}
