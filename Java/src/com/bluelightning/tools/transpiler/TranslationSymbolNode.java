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
		if (symbol == null)
			throw new NullPointerException();
	}

	public Symbol getSymbol() {
		return symbol;
	}

}
