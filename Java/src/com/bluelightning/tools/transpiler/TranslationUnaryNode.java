/**
 * 
 */
package com.bluelightning.tools.transpiler;

/**
 * @author NOOK
 *
 */
public class TranslationUnaryNode extends TranslationSubexpressionNode {
	
	public static Object staticFieldReference = new Object();
	
	Object lhs;
	Object rhs;

	TranslationUnaryNode(TranslationNode parent, Object lhs, Object rhs) {
		super(parent, "<UNARY>:" + Transpiler.instance().valueMap.get(lhs) + " " + Transpiler.instance().valueMap.get(rhs) );
		this.lhs = lhs;
		this.rhs = rhs;
		if (rhs instanceof Symbol) {
			this.type = ((Symbol) rhs).getType();
		}
	}
	
	public String getLhs() {
		return Transpiler.instance().valueMap.get(lhs);
	}

	public String getRhs() {
		return Transpiler.instance().valueMap.get(rhs);
	}
	
	public Symbol getRhsSymbol() {
		if (rhs instanceof Symbol)
			return (Symbol) rhs;
		else
			return null;
	}

}
