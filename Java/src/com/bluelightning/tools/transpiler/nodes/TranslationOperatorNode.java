/**
 * 
 */
package com.bluelightning.tools.transpiler.nodes;

import org.antlr.v4.runtime.ParserRuleContext;

/**
 * @author NOOK
 *
 */
public class TranslationOperatorNode extends TranslationNode {

	String operator;
	
	public TranslationOperatorNode(ParserRuleContext ctx, TranslationNode parent, String operator) {
		super(ctx, parent, "<OPERATOR>" + operator);
		this.operator = operator;
	}

	public String getOperator() {
		return operator;
	}

}
