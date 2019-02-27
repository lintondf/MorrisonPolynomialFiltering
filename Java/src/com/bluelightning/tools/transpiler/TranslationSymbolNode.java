/**
 * 
 */
package com.bluelightning.tools.transpiler;

/**
 * @author NOOK
 *
 */
public class TranslationSymbolNode extends TranslationNode {

	Symbol symbol;
	
	TranslationSymbolNode(TranslationNode parent, Symbol symbol) {
		super(parent, "<SYMBOL>" + symbol);
		this.symbol = symbol;
	}

	public Symbol getSymbol() {
		return symbol;
	}

}
