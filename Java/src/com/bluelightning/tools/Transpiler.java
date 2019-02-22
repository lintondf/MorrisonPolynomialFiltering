/**
 * 
 */
package com.bluelightning.tools;

import java.io.File;

import org.antlr.v4.runtime.ParserRuleContext;

/**
 * @author NOOK
 *
 */
public class Transpiler {
	
	protected static void compileGrammar( String gPath, String inPath, String outPath ) {
		String[] args = {
				"-lib", inPath,
				"-o", outPath,
				"-package", "com.bluelightning.tools",
				"-no-listener", "-visitor"
		};
		org.antlr.v4.Tool.main( args );
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		compileGrammar( "../Java/data/Python3.g4", "../Java/data/", "../Java/src/" );
	}

}
