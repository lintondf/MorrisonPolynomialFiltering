/**
 * 
 */
package com.bluelightning.tools.transpiler;

/**
 * @author NOOK
 *
 */
public interface ILanguageTarget {
	
	public void startModule( Scope scope );
	
	public void finishModule();
	
	public void startClass( Scope scope );
	
	public void finishClass( Scope scope );
	
	public void startMethod( Scope scope );
	
	public void finishMethod( Scope scope );
	
	public void emitExpressionStatement( Scope scope, TranslationNode root );
	
}
