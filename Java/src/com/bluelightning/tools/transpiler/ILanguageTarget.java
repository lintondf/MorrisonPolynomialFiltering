/**
 * 
 */
package com.bluelightning.tools.transpiler;

import com.bluelightning.tools.transpiler.nodes.TranslationNode;

/**
 * @author NOOK
 *
 */
public interface ILanguageTarget {
	
	
	public void setId(int id);
	
	public int getId();
	
	public void addImport( Scope scope);
	
	public void startModule( Scope scope );
	
	public void finishModule();
	
	public void startClass( Scope scope );
	
	public void finishClass( Scope scope );
	
	public void startMethod( Scope scope );
	
	public void finishMethod( Scope scope );
	
	public void emitSymbolDeclaration( Symbol symbol );
	
	public void emitExpressionStatement( Scope scope, TranslationNode root );
	
	public void emitSubExpression( Scope scope, TranslationNode root );
	
	public void emitReturnStatement();
	
	public void emitCloseStatement();

	public void emitForStatement(Symbol symbol, TranslationNode expressionRoot);
	
	public void closeBlock();
}
