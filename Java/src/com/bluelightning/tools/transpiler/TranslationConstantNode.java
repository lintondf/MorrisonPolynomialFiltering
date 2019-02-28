/**
 * 
 */
package com.bluelightning.tools.transpiler;

/**
 * @author NOOK
 *
 */
public class TranslationConstantNode extends TranslationNode {

	String value;
	
	TranslationConstantNode(TranslationNode parent, String value) {
		super(parent, "<CONSTANT>" + value);
		this.value = value;
	}

	public String getValue() {
		return value;
	}

}
