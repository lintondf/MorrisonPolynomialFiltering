package com.bluelightning.tools.transpiler;

import org.apache.commons.lang3.StringUtils;

public class Indent {
	int level = 0;
	public StringBuilder out = new StringBuilder();;
	
	public Indent() {
		level = 0;
		this.out = out;
	}
	
	public void in() {
		level += 1;
	}

	public void out() {
		level -= 1;
	}
	
	public String toString() {
		return StringUtils.repeat("  ", 2*level);
	}
	
	public void append( String text ) {
		out.append(text);
	}
	
	public void write( String text ) {
		out.append(toString());
		out.append(text);
	}

	public void writeln( String text ) {
		out.append(toString());
		out.append(text);
		out.append('\n');
	}
}