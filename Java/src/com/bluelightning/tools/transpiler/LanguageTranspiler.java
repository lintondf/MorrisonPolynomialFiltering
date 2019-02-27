package com.bluelightning.tools.transpiler;


public class LanguageTranspiler {
	public LanguageTranspiler() {
	}

	public interface ASTNode {
		public String toString();
	}

	public void emitAssignment(LanguageTranspiler.ASTNode target, LanguageTranspiler.ASTNode source) {
	}
}