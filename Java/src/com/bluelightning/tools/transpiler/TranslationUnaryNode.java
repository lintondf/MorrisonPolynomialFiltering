/**
 * 
 */
package com.bluelightning.tools.transpiler;

/**
 * @author NOOK
 *
 */
public class TranslationUnaryNode extends TranslationNode {
	
	Object lhs;
	Object rhs;

	TranslationUnaryNode(TranslationNode parent, Object lhs, Object rhs) {
		super(parent, "<UNARY>:" + Transpiler.instance().valueMap.get(lhs) + " " + Transpiler.instance().valueMap.get(rhs) );
		this.lhs = lhs;
		this.rhs = rhs;
	}

}
