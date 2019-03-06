/**
 * 
 */
package com.bluelightning.tools.transpiler.nodes;

/**
 * @author NOOK
 *
 */
public class TranslationListNode extends TranslationSubexpressionNode {
	
	protected String listOpen;

	public TranslationListNode(TranslationNode parent, String name) {
		super(parent, "<LIST>"+name);
		this.listOpen = name;
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
