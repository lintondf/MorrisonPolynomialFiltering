/**
 * 
 */
package com.bluelightning.tools.transpiler.nodes;

/**
 * @author NOOK
 *
 */
public class TranslationOperatorNode extends TranslationNode {

	String operator;
	
	public TranslationOperatorNode(TranslationNode parent, String operator) {
		super(parent, "<OPERATOR>" + operator);
		this.operator = operator;
	}

	public String getOperator() {
		return operator;
	}

}
