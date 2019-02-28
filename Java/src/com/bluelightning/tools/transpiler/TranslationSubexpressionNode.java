package com.bluelightning.tools.transpiler;

import java.util.Arrays;
import java.util.List;

public class TranslationSubexpressionNode extends TranslationNode {
	
	protected String type;

	TranslationSubexpressionNode(TranslationNode parent, String name) {
		super(parent, name);
	}
	
	public String getType() {
		return type;
	}
	
	@Override
	public String toString() {
		return super.toString() + " : " + type;
	}
	
	final static List<String> precedence = Arrays.asList(new String[] {"int", "float", "array"});
	
	@Override
	public void analyze() {
		if (!children.isEmpty()) {
			//System.out.println("analyze() " + name );
			int typeIndex = 0;
			for (TranslationNode child : children) {
				if (child instanceof TranslationSymbolNode) {
					TranslationSymbolNode tsn = (TranslationSymbolNode) child;
					//System.out.println("  " + tsn.getSymbol().getName() + " : " + tsn.getSymbol().getType());
					int i2 = precedence.indexOf(tsn.getSymbol().getType() );
					if (i2 > typeIndex)
						typeIndex = i2;
				} else if (child instanceof TranslationOperatorNode) {
					TranslationOperatorNode ton = (TranslationOperatorNode) child;
					//System.out.println("  " + ton.getOperator());
//				} else {
//					Transpiler.instance().reportError("TranslationSubexpressionNode::analyze  " + child.getClass().getSimpleName() );					
				}
			}
			this.type = precedence.get(typeIndex);
		}
	}
}
