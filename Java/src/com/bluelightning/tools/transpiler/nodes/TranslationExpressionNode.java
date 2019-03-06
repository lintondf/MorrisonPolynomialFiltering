/**
 * 
 */
package com.bluelightning.tools.transpiler.nodes;

import org.antlr.v4.runtime.ParserRuleContext;
import org.antlr.v4.runtime.tree.ParseTree;

/**
 * @author NOOK
 *
 */
public class TranslationExpressionNode extends TranslationSubexpressionNode {

	ParserRuleContext ctx;
	
	public TranslationExpressionNode(ParserRuleContext ctx, String name) {
		super(null, name);
		this.ctx = ctx;
	}
	
	public ParserRuleContext getParserRuleContext() {
		return ctx;
	}
	
	public String toString() {
		return String.format("L%5d C%3d: %s", ctx.start.getLine(), ctx.start.getCharPositionInLine(), super.toString() );
	}

}
