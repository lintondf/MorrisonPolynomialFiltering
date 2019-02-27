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
	
	public String name;
	public TranslationNode parent;
	public List<TranslationNode> children;
	
	TranslationNode( TranslationNode parent, String name) {
		this.name = name;
		this.parent = parent;
		this.children = new ArrayList<>();
		if (parent != null) {
			parent.children.add(this);
		}
	}
	
	public String traverse( int indent ) {
		String spaces = StringUtils.repeat("  ", indent);
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
		return name + " C#" + children.size() + ((parent == null) ? "?" : parent.toString());
	}

	public void adopt(TranslationNode node) {
		if (node.parent != null) {
			node.parent.removeChild(node);
		}
		node.parent = this;
		this.children.add(node);
	}
	

	public void removeChild(TranslationNode node) {
		children.remove(node);
	}
	
}
