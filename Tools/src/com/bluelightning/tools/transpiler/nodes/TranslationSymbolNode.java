/**
 * 
 */
package com.bluelightning.tools.transpiler.nodes;

import org.antlr.v4.runtime.ParserRuleContext;

import com.bluelightning.tools.transpiler.Symbol;

/**
 * @author NOOK
 *
 */
public class TranslationSymbolNode extends TranslationSubexpressionNode {

	Symbol symbol;
	
	public TranslationSymbolNode(ParserRuleContext ctx, TranslationNode parent, Symbol symbol) {
		super(ctx, parent, "<SYMBOL>" + symbol);
		this.symbol = symbol;
		if (symbol == null)
			throw new NullPointerException();
		setType(symbol.getType());
	}

	public Symbol getSymbol() {
		return symbol;
	}

}
