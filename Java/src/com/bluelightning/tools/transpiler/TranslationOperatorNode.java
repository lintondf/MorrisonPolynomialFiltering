/**
 * 
 */
package com.bluelightning.tools.transpiler;

/**
 * @author NOOK
 *
 */
public class TranslationOperatorNode extends TranslationNode {

	String operator;
	
	TranslationOperatorNode(TranslationNode parent, String operator) {
		super(parent, "<OPERATOR>" + operator);
		this.operator = operator;
	}

	public String getOperator() {
		return operator;
	}

}
