/**
 * 
 */
package com.bluelightning.tools;

import java.io.File;

import org.antlr.v4.runtime.ParserRuleContext;
import org.snt.inmemantlr.GenericParser;
import org.snt.inmemantlr.listener.DefaultTreeListener;
import org.snt.inmemantlr.tree.ParseTree;
import org.snt.inmemantlr.utils.FileUtils;

/**
 * @author NOOK
 *
 */
public class Transpiler {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		try {
			File f = new File("Java.g4");
			GenericParser gp = new GenericParser(f);
			String s = FileUtils.loadFileContent("../Java/data/Python3.g4");
	
			// this listener will create a parse tree from the java file
			DefaultTreeListener dlist = new DefaultTreeListener();
	
			gp.setListener(dlist);
			gp.compile();
	
			ParserRuleContext ctx = gp.parse(s, "compilationUnit", GenericParser.CaseSensitiveType.NONE);
			// get access to the parse tree of inmemantlr
			ParseTree pt = dlist.getParseTree();
			System.out.println(pt.toXml());
		} catch (Exception x) {
			x.printStackTrace();
		}
	}

}
