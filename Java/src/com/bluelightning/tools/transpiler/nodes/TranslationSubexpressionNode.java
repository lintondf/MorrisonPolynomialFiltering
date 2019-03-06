package com.bluelightning.tools.transpiler.nodes;

import java.util.Arrays;
import java.util.List;
import com.bluelightning.tools.transpiler.Symbol;

public class TranslationSubexpressionNode extends TranslationNode {
	
	public TranslationSubexpressionNode(TranslationNode parent, String name) {
		super(parent, "SUBEXPRESSION::" + name);
	}
	
	@Override
	public String toString() {
		return super.toString() + " : " + getType();
	}
	
}
