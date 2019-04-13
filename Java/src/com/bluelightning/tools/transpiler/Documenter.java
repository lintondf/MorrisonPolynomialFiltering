/**
 * 
 */
package com.bluelightning.tools.transpiler;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.TreeMap;

//import org.cellprofiler.javabridge.CPython;
//import org.cellprofiler.javabridge.CPython.WrappedException;

import com.bluelightning.tools.Execute;
import com.bluelightning.tools.transpiler.Scope.Level;

/**
 * @author NOOK
 *
 */
public class Documenter {
	
	public interface IGenerator {
		public String generate( String indent, String pyDoxygen );
	}
	
	public static class ObjectDocumentation {
		String  docstring;  // python docstring contents
		String  pyDoxygen;  // doxypypy converted docstring
		
		public static ObjectDocumentation none() {
			ObjectDocumentation doc = new ObjectDocumentation();
			doc.docstring = "";
			doc.pyDoxygen = "";
			return doc;
		}
	}
	
	protected HashMap<String, ObjectDocumentation> documentation = new HashMap<>();
	protected File scratch = null;
	
	protected String pythonPath;
	
	public static class DoxygenConfiguration {
		String blockCommentStart = "///// ";
		String blockComment = "/// ";
	}
	
	protected class DoxygenGenerator implements IGenerator {
		
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
	
	
//	protected DoxygenGenerator doxygenGenerator = new DoxygenGenerator();
	
	TreeMap<String, IGenerator> generators = new TreeMap<>();
	
	public Documenter() {
		String home = System.getenv("HOMEPATH");
		if (home != null) {
			this.pythonPath = home + "\\Anaconda3\\Scripts\\doxypypy.exe";
		} else {
			this.pythonPath = System.getenv("HOME") + "/anaconda3/bin/bin/doxypypy";
		}
		try {
			scratch = File.createTempFile("Documenter", ".py");
			scratch.deleteOnExit();
			generators.put("Doxygen/C++", new DoxygenGenerator() );
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	protected ObjectDocumentation findSuperDocumentation( Scope scope ) {
		ObjectDocumentation doc = null;
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
			ObjectDocumentation docObj = findSuperDocumentation( scope );
			if (docObj == null)
				return;
			documentation.put(scope.toString(), docObj);			
			return;
		} else if (doc.startsWith("\"\"\"@none")) {
			documentation.put(scope.toString(), ObjectDocumentation.none());
			return;
		}
		ObjectDocumentation docObj = documentation.get(scope.toString());
		if (docObj != null) {
			if (doc.equals(docObj.docstring)) 
				return;  // already have and up to date
		} else {
			docObj = new ObjectDocumentation();
			docObj.docstring = doc;
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
			docObj.pyDoxygen = pyDoxygen;
			documentation.put(scope.toString(), docObj);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
	}
	
	public boolean isDocumented( Scope scope ) {
		return documentation.containsKey(scope.toString());
	}
	
	public String getComments( String key, String scope, String indent ) {
		if (documentation.containsKey(scope)) {
			ObjectDocumentation doc = documentation.get(scope);
			if (doc == null || doc.pyDoxygen.isEmpty())
				return null;
			return generators.get(key).generate(indent, doc.pyDoxygen);
		}
		return null;
	}
	
	public void report() {
		System.out.println("--- DOCUMENTER ------------------");
		System.out.println( documentation.size() );
		documentation.keySet().forEach(System.out::println);
	}
	
//	public static void main(String[] args) {
//		CPython cpython = new CPython();
//        ArrayList<String> result = new ArrayList<String>();
//        Hashtable locals = new Hashtable();
//        locals.put("result", result);
//        locals.put("root", "Hello");
//        StringBuilder script = new StringBuilder();
//        script.append("import os\n");
//        script.append("import javabridge\n");
//        script.append("root = javabridge.to_string(root)");
//        script.append("result = javabridge.JWrapper(result)");
//        script.append("for path, dirnames, filenames in os.walk(root):\n");
//        script.append("  if 'waldo' in filenames:");
//        script.append("     result.add(path)");
//        try {
//			cpython.exec(script.toString(), locals, null);
//	        System.out.println(result);
//		} catch (WrappedException e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//		}
//	}
////		ArrayList<String> result = new ArrayList<String>();
////		String path = "C:\\Users\\NOOK\\GITHUB\\MorrisonPolynomialFiltering\\Python\\src\\DoxygenTest.py";
////        Hashtable locals = new Hashtable();
////        locals.put("result", result);
////        locals.put("path", path);
////        StringBuilder script = new StringBuilder();
////        script.append("import sys\n");
////        script.append("import javabridge\n");
////        script.append("class NullDevice():\r\n" + 
////        		"    def __init__(self, b):\r\n" + 
////        		"        self.buffer = b;\r\n" + 
////        		"    def write(self, s):\r\n" + 
////        		"        self.buffer.add(s);\r\n" + 
////        		"    \r\n" + 
////        		"    def flush(self):\r\n" + 
////        		"        pass\r\n" + 
////        		"\r\n" + 
////        		"\r\n" + 
////        		"");
////        script.append("path = javabridge.to_string(path)");
////        script.append("result = javabridge.JWrapper(result)");
////        script.append("runargs = [\"doxypypy\", \"-a\", \"");
////        script.append( path );
////        script.append("\"];\n");
////        script.append("    sys.argv = runargs\r\n" + 
////        		"    dev = NullDevice(result)  # redirect the real STDOUT\r\n" + 
////        		"    sys.stdout = dev;\r\n" + 
////        		"    doxypypy.main()\r\n" + 
////        		"");
////        script.append("    result = dev.buffer;");
////        try {
////			cpython.exec(script.toString(), locals, null);
////			System.out.println(result.size());
////		} catch (WrappedException e) {
////			// TODO Auto-generated catch block
////			e.printStackTrace();
////		}
//		
//	}
}
