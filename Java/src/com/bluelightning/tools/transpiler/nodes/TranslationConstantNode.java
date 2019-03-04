/**
 * 
 */
package com.bluelightning.tools.transpiler.nodes;

/**
 * @author NOOK
 *
 */
public class TranslationConstantNode extends TranslationNode {

	String value;
	
	public enum Kind { INTEGER, FLOAT, STRING };
	Kind   kind;
	
	public TranslationConstantNode(TranslationNode parent, String value, Kind kind) {
		super(parent, "<CONSTANT>:" + kind.toString() + " = " + value);
		this.value = value;
		this.kind = kind;
	}

	public String getValue() {
		return value;
	}

	public Kind getKind() {
		return kind;
	}

}
