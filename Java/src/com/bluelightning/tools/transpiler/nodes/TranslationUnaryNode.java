/**
 * 
 */
package com.bluelightning.tools.transpiler.nodes;

import java.util.TreeSet;

import org.antlr.v4.runtime.CommonToken;
import org.antlr.v4.runtime.ParserRuleContext;

import com.bluelightning.tools.transpiler.Symbol;
import com.bluelightning.tools.transpiler.Transpiler;

/**
 * @author NOOK
 *
 */
public class TranslationUnaryNode extends TranslationSubexpressionNode {
	
	//public static Object staticFieldReference = new Object();  // just a placeholder for :: in C++
	public static CommonToken staticFieldReference = new CommonToken(0);
	
	CommonToken lhs;
	Object rhs;

	public TranslationUnaryNode(ParserRuleContext ctx, TranslationNode parent, CommonToken lhs, Symbol rhs) {
		super(ctx, parent, "<UNARY>:" + Transpiler.instance().getValue(lhs) + " " + rhs );
		this.lhs = lhs;
		this.rhs = rhs;
		if (rhs != null)
			setType(((Symbol) rhs).getType());
	}
	
	public TranslationUnaryNode(ParserRuleContext ctx, TranslationNode parent, CommonToken lhs, TranslationNode rhs) {
		super(ctx,parent, "<UNARY>:" + Transpiler.instance().getValue(lhs) + " " + rhs.toString() );
		this.lhs = lhs;
		this.rhs = rhs;
		setType(((TranslationNode) rhs).getType());
	}
	
	public String getLhsValue() {
		return Transpiler.instance().getValue(lhs);
	}

	public String getRhsValue() {
		return Transpiler.instance().getValue(rhs);
	}
	
	public Symbol getRhsSymbol() {
		if (rhs instanceof Symbol)
			return (Symbol) rhs;
		else
			return null;
	}

	public CommonToken getLhs() {
		return lhs;
	}

	public TranslationNode getRhsNode() {
		if (rhs instanceof TranslationNode)
			return (TranslationNode) rhs;
		else
			return null;
	}
	
	public static boolean isMinusOne(TranslationNode node) {
		if (node == null)
			return false;
		while (node.getChildCount() == 1) {
			node = node.getFirstChild();
		}
		if (! (node instanceof TranslationUnaryNode))
			return false;
		TranslationUnaryNode tun = (TranslationUnaryNode) node;
		if (tun.rhs == null)
			return false;
		if (tun.rhs instanceof TranslationConstantNode) {
			TranslationConstantNode tcn = (TranslationConstantNode) tun.rhs;
			return tcn.value.equals("1");
		}
		return false;
	}

}
