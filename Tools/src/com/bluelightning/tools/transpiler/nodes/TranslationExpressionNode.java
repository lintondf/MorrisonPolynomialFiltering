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

	public TranslationExpressionNode(ParserRuleContext ctx, String name) {
		super(ctx, null, name);
	}
	
}
