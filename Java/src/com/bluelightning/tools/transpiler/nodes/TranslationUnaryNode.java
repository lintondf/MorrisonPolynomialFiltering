/**
 * 
 */
package com.bluelightning.tools.transpiler.nodes;

import com.bluelightning.tools.transpiler.Symbol;
import com.bluelightning.tools.transpiler.Transpiler;

/**
 * @author NOOK
 *
 */
public class TranslationUnaryNode extends TranslationSubexpressionNode {
	
	public static Object staticFieldReference = new Object();
	
	Object lhs;
	Object rhs;

	public TranslationUnaryNode(TranslationNode parent, Object lhs, Object rhs) {
		super(parent, "<UNARY>:" + Transpiler.instance().getValue(lhs) + " " + Transpiler.instance().getValue(rhs) );
		this.lhs = lhs;
		this.rhs = rhs;
		if (rhs instanceof Symbol) {
			this.type = ((Symbol) rhs).getType();
		}
	}
	
	public String getLhs() {
		return Transpiler.instance().getValue(lhs);
	}

	public String getRhs() {
		return Transpiler.instance().getValue(rhs);
	}
	
	public Symbol getRhsSymbol() {
		if (rhs instanceof Symbol)
			return (Symbol) rhs;
		else
			return null;
	}

}
