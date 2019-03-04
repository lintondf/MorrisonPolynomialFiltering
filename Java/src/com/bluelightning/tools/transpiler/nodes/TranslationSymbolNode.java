/**
 * 
 */
package com.bluelightning.tools.transpiler.nodes;

import com.bluelightning.tools.transpiler.Symbol;

/**
 * @author NOOK
 *
 */
public class TranslationSymbolNode extends TranslationSubexpressionNode {

	Symbol symbol;
	
	public TranslationSymbolNode(TranslationNode parent, Symbol symbol) {
		super(parent, "<SYMBOL>" + symbol);
		this.symbol = symbol;
		if (symbol == null)
			throw new NullPointerException();
		this.type = symbol.getType();
	}

	public Symbol getSymbol() {
		return symbol;
	}

}
