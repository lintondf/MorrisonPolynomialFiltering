package com.bluelightning.tools.transpiler.nodes;

import java.util.Arrays;
import java.util.List;

import org.antlr.v4.runtime.ParserRuleContext;

import com.bluelightning.tools.transpiler.Symbol;

public class TranslationSubexpressionNode extends TranslationNode {
	
	public TranslationSubexpressionNode(ParserRuleContext ctx, TranslationNode parent, String name) {
		super(ctx, parent, "SUBEXPRESSION::" + name);
	}
	
	@Override
	public String toString() {
		return super.toString() + " : " + getType();
	}
	
}
