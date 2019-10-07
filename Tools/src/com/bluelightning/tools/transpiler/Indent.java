package com.bluelightning.tools.transpiler;

import org.apache.commons.lang3.StringUtils;

public class Indent {
	private final boolean whence = false;
	
	int level = 0;
	public StringBuilder sb = new StringBuilder();;
	
	public Indent() {
		level = 0;
	}
	
	public Indent( Indent that ) {
		this.level = that.level;
	}
	
	public void in() {
		level += 1;
	}

	public void out() {
		level -= 1;
	}
	
	@Override
	public String toString() {
		return StringUtils.repeat("    ", level);
	}
	
	public String get() {
		return StringUtils.repeat("    ", level);
	}
	
	public void append( String text ) {
		sb.append(text);
		if (whence && text.endsWith("\n")) {
			deleteLast();
			StackTraceElement[] st = Thread.currentThread().getStackTrace();
			sb.append(String.format(" // %s:%s:%d\n", st[2].getFileName(), st[2].getMethodName(), st[2].getLineNumber()));			
		}
	}
	
	public void write( String text ) {
		sb.append(get());
		sb.append(text);
		if (whence && text.endsWith("\n")) {
			deleteLast();
			StackTraceElement[] st = Thread.currentThread().getStackTrace();
			sb.append(String.format(" // %s:%s:%d\n", st[2].getFileName(), st[2].getMethodName(), st[2].getLineNumber()));			
		}
	}

	public void writeln( String text ) {
		sb.append(get());
		sb.append(text);
		if (whence) {
			StackTraceElement[] st = Thread.currentThread().getStackTrace();
			sb.append(String.format(" // %s:%s:%d", st[2].getFileName(), st[2].getMethodName(), st[2].getLineNumber()));
		}
		sb.append('\n');
	}
	
	public void write() {
		sb.append(get());		
	}
	
	public void writeln() {
		sb.append(get());
		sb.append('\n');
	}

	public void deleteLast(char match) {
		if (sb.length() > 0) {
			if (sb.charAt(sb.length()-1) == match)
				sb.deleteCharAt(sb.length()-1);
		}
	}
	
	public void deleteLast() {
		if (sb.length() > 0) 
			sb.deleteCharAt(sb.length()-1);
	}
	
	public int size() {
		return sb.length();
	}

	public void deleteLast(String string) {
		for (int i = string.length()-1; i >= 0; i--) {
			deleteLast(string.charAt(i));
		}
	}

	public void deleteCurrentLine() {
		while (sb.charAt(sb.length()-1) != '\n') {
			deleteLast();
		}
	}
}