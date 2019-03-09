/**
 * 
 */
package com.bluelightning.tools.transpiler;

import com.bluelightning.tools.transpiler.nodes.TranslationNode;

/**
 * @author NOOK
 *
 */
public abstract class AbstractLanguageTarget implements ILanguageTarget {

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#setId(int)
	 */
	@Override
	public void setId(int id) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#getId()
	 */
	@Override
	public int getId() {
		// TODO Auto-generated method stub
		return 0;
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#addImport(com.bluelightning.tools.transpiler.Scope)
	 */
	@Override
	public void addImport(Scope scope) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#startModule(com.bluelightning.tools.transpiler.Scope)
	 */
	@Override
	public void startModule(Scope scope) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#finishModule()
	 */
	@Override
	public void finishModule() {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#startClass(com.bluelightning.tools.transpiler.Scope)
	 */
	@Override
	public void startClass(Scope scope) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#finishClass(com.bluelightning.tools.transpiler.Scope)
	 */
	@Override
	public void finishClass(Scope scope) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#startMethod(com.bluelightning.tools.transpiler.Scope)
	 */
	@Override
	public void startMethod(Scope scope) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#finishMethod(com.bluelightning.tools.transpiler.Scope)
	 */
	@Override
	public void finishMethod(Scope scope) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#emitSymbolDeclaration(com.bluelightning.tools.transpiler.Symbol)
	 */
	@Override
	public void emitSymbolDeclaration(Symbol symbol) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#emitElifStatement(com.bluelightning.tools.transpiler.Scope, com.bluelightning.tools.transpiler.nodes.TranslationNode)
	 */
	@Override
	public void emitElifStatement(Scope scope, TranslationNode expressionRoot) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#emitElseStatement()
	 */
	@Override
	public void emitElseStatement() {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#emitExpressionStatement(com.bluelightning.tools.transpiler.Scope, com.bluelightning.tools.transpiler.nodes.TranslationNode)
	 */
	@Override
	public void emitExpressionStatement(Scope scope, TranslationNode root) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#emitIfStatement(com.bluelightning.tools.transpiler.Scope, com.bluelightning.tools.transpiler.nodes.TranslationNode)
	 */
	@Override
	public void emitIfStatement(Scope scope, TranslationNode expressionRoot) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#emitForStatement(com.bluelightning.tools.transpiler.Symbol, com.bluelightning.tools.transpiler.nodes.TranslationNode)
	 */
	@Override
	public void emitForStatement(Symbol symbol, TranslationNode expressionRoot) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#emitNewExpression(com.bluelightning.tools.transpiler.Scope, java.lang.String, com.bluelightning.tools.transpiler.nodes.TranslationNode)
	 */
	@Override
	public void emitNewExpression(Scope scope, String className, TranslationNode root) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#emitRaiseStatement(java.lang.String)
	 */
	@Override
	public void emitRaiseStatement(String exception) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#emitReturnStatement()
	 */
	@Override
	public void emitReturnStatement() {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#emitSubExpression(com.bluelightning.tools.transpiler.Scope, com.bluelightning.tools.transpiler.nodes.TranslationNode)
	 */
	@Override
	public void emitSubExpression(Scope scope, TranslationNode root) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#finishStatement()
	 */
	@Override
	public void finishStatement() {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#closeBlock()
	 */
	@Override
	public void closeBlock() {
		// TODO Auto-generated method stub

	}

}
