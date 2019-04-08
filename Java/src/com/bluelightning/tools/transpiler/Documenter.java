/**
 * 
 */
package com.bluelightning.tools.transpiler;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashMap;

import com.bluelightning.tools.Execute;
import com.bluelightning.tools.transpiler.Scope.Level;

/**
 * @author NOOK
 *
 */
public class Documenter {
	
	protected HashMap<String, String> documentation = new HashMap<>();
	protected File scratch = null;
	
	final static String pythonPath = "C:\\Users\\NOOK\\Anaconda3\\Scripts\\doxypypy.exe";
	
	public static class DoxygenConfiguration {
		String blockCommentStart = "///// ";
		String blockComment = "/// ";
	}
	
	protected class DoxygenGenerator {
		
		protected DoxygenConfiguration configuration = new DoxygenConfiguration();
		
		public DoxygenGenerator() {
		}
		
		public void configure(DoxygenConfiguration c) {
			configuration = c;
		}
		
		public String generate( String indent, String pyDoxygen ) {
			StringBuilder out = new StringBuilder();
			String[] lines = pyDoxygen.split("\n");
			for (String line : lines ) {
				if (line.startsWith("## ")) {
					if (line.startsWith("## @brief")) {
						line = line.replaceAll("## @brief", configuration.blockCommentStart + "@brief");
					} else {
						line = line.replace("## ", configuration.blockComment);
					}
				} else if (line.startsWith("#")) {
					line = line.replace( "#", configuration.blockComment);
				}
				out.append(indent);
				out.append(line);
				out.append('\n');
			}
			return out.toString();
		}
	}
	
	
	protected DoxygenGenerator doxygenGenerator = new DoxygenGenerator();
	
	public Documenter() {
		try {
			scratch = File.createTempFile("Documenter", ".py");
			scratch.deleteOnExit();
			//scratch = new File("C:\\Users\\NOOK\\GITHUB\\MorrisonPolynomialFiltering\\Python\\src\\DoxygenTest.py");
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	protected String findSuperDocumentation( Scope scope ) {
		String doc = null;
		if (scope.getLevel() != Level.MEMBER)
			return null;
		Scope s = scope.getParent();
		if (s == null)
			return null;
		Symbol c = Transpiler.instance().lookup(s.getParent(), s.getLast() ); // symbol for containing class
		while (c != null) {
			if (c.getSuperClassInfo() == null || c.getSuperClassInfo().superClass.isEmpty())
				return null;
			c = Transpiler.instance().lookupClass(c.getSuperClassInfo().superClass);
			if (c == null)
				return null;			
			Symbol m = Transpiler.instance().lookup(c.getScope().getChild(Level.CLASS, c.getName()), scope.getLast() );
			if (m != null) {
				doc = documentation.get(m.getScope().toString() + scope.getLast() + "/");
				if (doc != null)
					return doc;
			}
		}
		return doc;
	}
	
	public void putDocumentation( Scope scope, String doc ) {
		if (doc.startsWith("\"\"\"@super")) {
			doc = findSuperDocumentation( scope );
			if (doc == null)
				return;
			documentation.put(scope.toString(), doc);			
			return;
		} else if (doc.startsWith("\"\"\"@none")) {
			documentation.put(scope.toString(), "");
			return;
		}
		try {
			PrintWriter w = new PrintWriter(scratch);
			String[] lines = doc.split("\n");
			for (String line : lines ) {
				w.println(line.trim());
			}
			w.close();
			String[] args = new String[] {pythonPath, "-a", scratch.getAbsolutePath() };
			String pyDoxygen = Execute.run(args);
			pyDoxygen = pyDoxygen.replace("# @return\n#", "# @return  ");  //doxypypy inserts a line break contra doxygen examples
			documentation.put(scope.toString(), pyDoxygen);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
	}
	
	public boolean isDocumented( Scope scope ) {
		return documentation.containsKey(scope.toString());
	}
	
	public void configureDoxygen(DoxygenConfiguration c) {
		doxygenGenerator.configure(c);
	}
	
	public String getDoxygenComments( String scope, String indent ) {
		if (documentation.containsKey(scope)) {
			String doc = documentation.get(scope);
			if (doc == null || doc.isEmpty())
				return null;
			return doxygenGenerator.generate(indent, doc);
		}
//		System.out.println("NO COMMENT: " + scope.toString());
		return null;
	}
	
	public void report() {
		System.out.println("--- DOCUMENTER ------------------");
		System.out.println( documentation.size() );
		documentation.keySet().forEach(System.out::println);
	}
	
}
