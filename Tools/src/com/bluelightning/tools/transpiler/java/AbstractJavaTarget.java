/**
 * 
 */
package com.bluelightning.tools.transpiler.java;

import com.bluelightning.tools.transpiler.AbstractLanguageTarget;
import com.bluelightning.tools.transpiler.Scope;
import com.bluelightning.tools.transpiler.Symbol;
import com.bluelightning.tools.transpiler.nodes.TranslationNode;

/**
 * @author lintondf
 *
 */
public class AbstractJavaTarget extends AbstractLanguageTarget{

	@Override
	public void setId(int id) {
		// TODO Auto-generated method stub
		super.setId(id);
	}

	@Override
	public int getId() {
		// TODO Auto-generated method stub
		return super.getId();
	}

	@Override
	public void addImport(Scope scope) {
		// TODO Auto-generated method stub
		super.addImport(scope);
	}

	@Override
	public void startModule(Scope scope, boolean headerOnly, boolean isTest) {
		// TODO Auto-generated method stub
		super.startModule(scope, headerOnly, isTest);
	}

	@Override
	public void finishModule() {
		// TODO Auto-generated method stub
		super.finishModule();
	}

	@Override
	public void startClass(Scope scope) {
		// TODO Auto-generated method stub
		super.startClass(scope);
	}

	@Override
	public void finishClass(Scope scope) {
		// TODO Auto-generated method stub
		super.finishClass(scope);
	}

	@Override
	public void startMethod(Scope scope) {
		// TODO Auto-generated method stub
		super.startMethod(scope);
	}

	@Override
	public void finishMethod(Scope scope) {
		// TODO Auto-generated method stub
		super.finishMethod(scope);
	}

	@Override
	public void emitSymbolDeclaration(Symbol symbol, String comment) {
		// TODO Auto-generated method stub
		super.emitSymbolDeclaration(symbol, comment);
	}

	@Override
	public void emitElifStatement(Scope scope, TranslationNode expressionRoot) {
		// TODO Auto-generated method stub
		super.emitElifStatement(scope, expressionRoot);
	}

	@Override
	public void emitElseStatement() {
		// TODO Auto-generated method stub
		super.emitElseStatement();
	}

	@Override
	public void emitExpressionStatement(Scope scope, TranslationNode root) {
		// TODO Auto-generated method stub
		super.emitExpressionStatement(scope, root);
	}

	@Override
	public void emitIfStatement(Scope scope, TranslationNode expressionRoot) {
		// TODO Auto-generated method stub
		super.emitIfStatement(scope, expressionRoot);
	}

	@Override
	public void emitForStatement(Symbol symbol, TranslationNode expressionRoot) {
		// TODO Auto-generated method stub
		super.emitForStatement(symbol, expressionRoot);
	}

	@Override
	public void emitNewExpression(Scope scope, String className, TranslationNode root) {
		// TODO Auto-generated method stub
		super.emitNewExpression(scope, className, root);
	}

	@Override
	public void emitRaiseStatement(String exception) {
		// TODO Auto-generated method stub
		super.emitRaiseStatement(exception);
	}

	@Override
	public void emitReturnStatement() {
		// TODO Auto-generated method stub
		super.emitReturnStatement();
	}

	@Override
	public void emitSubExpression(Scope scope, TranslationNode root) {
		// TODO Auto-generated method stub
		super.emitSubExpression(scope, root);
	}

	@Override
	public void finishStatement() {
		// TODO Auto-generated method stub
		super.finishStatement();
	}

	@Override
	public void closeBlock() {
		// TODO Auto-generated method stub
		super.closeBlock();
	}

	@Override
	public void addParameterClass(String className) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void startStatement() {
		// TODO Auto-generated method stub
		
	}

}
