/**
 * 
 */
package com.bluelightning.tools.transpiler.nodes;

import org.antlr.v4.runtime.ParserRuleContext;

/**
 * @author NOOK
 *
 */
public class TranslationListNode extends TranslationSubexpressionNode {
	
	protected String listOpen;

	public TranslationListNode(ParserRuleContext ctx, TranslationNode parent, String name) {
		super(ctx, parent, "<LIST>"+name);
		this.listOpen = name;
	}
	
	@Override
	public void setType(String type) {
		int currentIndex = precedence.indexOf(this.type);
		int typeIndex = precedence.indexOf(type);
		if ( typeIndex >= 0 && currentIndex >= 0) { // update if both types are basic 
			if (typeIndex > currentIndex) { // and higher precedence
				this.type = type;
			}
		} else if (currentIndex >= 0) {
			this.type = type;
		}
		if (parent != null) {
			parent.setType(this.type);
		}
	}
	
	

	public String getListOpen() {
		return listOpen;
	}
	
	private boolean isChildSlice(TranslationNode child) {
		if (child instanceof TranslationOperatorNode) {
			if (((TranslationOperatorNode) child).getOperator().equals(":"))
				return true;
		}
		for (TranslationNode grandchild : child.children) {
			if (isChildSlice(grandchild))
				return true;
		}
		return false;
	}
	
	public boolean isArraySlice() {
		if (listOpen.equals("[")) {
			for (TranslationNode child : children) {
				if (isChildSlice(child))
					return true;
			}
		}
		return false;
	}
}
