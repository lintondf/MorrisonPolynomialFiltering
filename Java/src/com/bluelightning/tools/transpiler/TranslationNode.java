/**
 * 
 */
package com.bluelightning.tools.transpiler;

import java.util.ArrayList;
import java.util.List;

import org.apache.commons.lang3.StringUtils;


/**
 * @author NOOK
 *
 */
public class TranslationNode  {
	
	protected String name;
	protected  TranslationNode parent;
	protected List<TranslationNode> children;
	
	TranslationNode( TranslationNode parent, String name) {
		this.name = name;
		this.parent = parent;
		this.children = new ArrayList<>();
		if (parent != null) {
			parent.children.add(this);
		}
	}
	
	public String traverse( int indent ) {
		String spaces = String.format("%5d:%s", indent, StringUtils.repeat("  ", indent));
		StringBuffer sb = new StringBuffer();
		sb.append(spaces);
		sb.append( this.toString() );
		sb.append('\n');
		for (TranslationNode child : children) {
			sb.append( child.traverse(indent+1) );
		}
		return sb.toString();		
	}
	
	public String toString() {
		return String.format("%s (%d)", name, children.size() );
//		return name + " C#" + children.size() + ((parent == null) ? "?" : parent.toString());
	}

	public void adopt(TranslationNode node) {
		if (node.parent != null) {
			node.parent.removeChild(node);
		}
		node.parent = this;
		this.children.add(node);
	}
	
    public void addChild(TranslationNode node ) {
    	node.parent = this;
    	children.add(node);
    }
    
	public void removeChild(TranslationNode node) {
		children.remove(node);
	}
	
	public List<TranslationNode> getChildren() {
		return children;
	}

	public int getChildCount() {
		return children.size();
	}

	public TranslationNode getChild(int i) {
		return children.get(i);
	}
	
	public void analyze() {		
	}

	public String getName() {
		return name;
	}

	public TranslationNode getParent() {
		return parent;
	}

	
}
