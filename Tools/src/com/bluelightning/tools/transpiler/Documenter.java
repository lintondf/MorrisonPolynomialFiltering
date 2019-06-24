/**
 * 
 */
package com.bluelightning.tools.transpiler;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.PrintWriter;
import java.io.Serializable;
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
	
	public static class ObjectDocumentation implements Serializable {
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
			this.pythonPath = "/anaconda3/bin/doxypypy";
		}
		try {
			scratch = File.createTempFile("Documenter", ".py");
			scratch.deleteOnExit();
			generators.put("Doxygen/C++", new DoxygenGenerator() );
		} catch (IOException e) {
			e.printStackTrace();
		}
		File obj = new File("documentation.obj");
		try {
			FileInputStream  fis = new FileInputStream (obj);
			ObjectInputStream  ois = new ObjectInputStream (fis);
			documentation = (HashMap<String, ObjectDocumentation>) ois.readObject();
            ois.close();
            fis.close();
		} catch (Exception x) {
			documentation.clear();
		}
	}
	
	public void close() {
		try {
			File obj = new File("documentation.obj");
			try {
	            FileOutputStream fos = new FileOutputStream(obj);
	            ObjectOutputStream oos = new ObjectOutputStream(fos);
	            oos.writeObject(documentation);
	            oos.close();
	            fos.close();
			} catch (Exception x) {
				obj.delete();
			}			
		} catch (Exception x) {
			x.printStackTrace();
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
			if (c.getSuperClassInfo() == null || c.getSuperClassInfo().superClasses.isEmpty())
				return null;
			c = Transpiler.instance().lookupClass(c.getSuperClassInfo().superClasses.get(0));
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
	
}
