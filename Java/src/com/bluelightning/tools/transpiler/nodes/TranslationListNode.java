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
	
	@Override
	public void analyze() {
		if (children.size() == 0) {
			this.type = "None";
		} else {
			if (getChild(0) instanceof TranslationSubexpressionNode) {
				this.type = ((TranslationSubexpressionNode)getChild(0)).getType();
			} else {
				this.type = "None";
			}
		}
	}
	
}
