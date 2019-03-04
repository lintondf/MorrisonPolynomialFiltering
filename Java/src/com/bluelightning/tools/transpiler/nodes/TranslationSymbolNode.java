/**
 * 
 */
package com.bluelightning.tools.transpiler.nodes;

import com.bluelightning.tools.transpiler.Symbol;

/**
 * @author NOOK
 *
 */
public class TranslationSymbolNode extends TranslationNode {

	Symbol symbol;
	
	public TranslationSymbolNode(TranslationNode parent, Symbol symbol) {
		super(parent, "<SYMBOL>" + symbol);
		this.symbol = symbol;
		if (symbol == null)
			throw new NullPointerException();
	}

	public Symbol getSymbol() {
		return symbol;
	}

}
