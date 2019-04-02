/**
 * 
 */
package com.bluelightning.tools;

import java.io.File;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;

import com.bluelightning.tools.transpiler.Transpiler;

/**
 * @author NOOK
 *
 */
public class TranslateOctaveDiary {
	
	public static final String EMP_CURRENT = "0";
	public static final String EMP_ONESTEP = "1";
	public static final String FMP_CURRENT = "0";
	public static final String FMP_ONESTEP = "-1";
	
	protected List<String> diary;
	protected List<String> src;
	
	protected HashMap<String, List<String>> codeBlocks = new HashMap<>();
	
	protected Iterator<String> it;
	protected String line;
	
	protected List<String> loadBlock() {
		final String CONTINUATION = "     @";
		List<String> sb = new ArrayList<>();
		while (line.startsWith("V[")) {
			String codeLine = Transpiler.deblank(line); 
			line = it.next();
			while (line.startsWith(CONTINUATION)) {
				codeLine += Transpiler.deblank( line.substring(CONTINUATION.length()) );
				line = it.next();
			}
			codeLine = codeLine.replace("d0","");
			sb.add(codeLine + "\n");
		}
		return sb;
	}
	
	protected void loadCodeBlocks() {
		it = diary.iterator();
		String key = null;
		line = it.next();
		while (it.hasNext()) {
			System.out.println(line);
			if (line.startsWith("-----------")) {
				key = it.next().trim();
				key = key.replace("Fading Memory VRF for degree : ", "FMP");
				key = key.replace("Expanding Memory VRF for degree : ", "EMP");
				it.next(); // skip -----------
				while (it.hasNext()) {
					line = it.next();
					if (line.startsWith("V[")) {
						List<String> block = loadBlock();
						codeBlocks.put(key,  block );
						break;
					}
				}
			} else {
				line = it.next();
			}
		}
	}
	
	protected int findClass( String name ) {
		for (int i = 0; i < src.size(); i++) {
			if (src.get(i).startsWith(name))
				return i;
		}
		System.err.println("COULD NOT FIND: " + name );
		return -1;
	}
	
	protected int skipToVrf( int iClass) {
		for (int i = iClass; i < src.size(); i++) {
			if (src.get(i).trim().startsWith("def _VRF")) {
				for (int j = i+1; j < src.size(); j++) {
					if (src.get(j).trim().startsWith("V = zeros"))
						return j;
				}
				return -1;
			}
		}
		return -1;
	}
	

	protected int findReturn( int iVrf ) {		
		for (int i = iVrf; i < src.size(); i++) {
			if (src.get(i).trim().startsWith("return V;")) {
				return i;
			}
		}
		return -1;
	}
	
	public TranslateOctaveDiary(String classBase, String which, String diaryPath, String srcPath ) {
		try {
			byte[] bytes = Files.readAllBytes( Paths.get(diaryPath) );
			diary = Arrays.asList( new String( bytes, "UTF-8" ).split("\n") );
			loadCodeBlocks();
			//codeBlocks.entrySet().forEach(System.out::println);
			bytes = Files.readAllBytes( Paths.get(srcPath) );
			src = new ArrayList<String>( Arrays.asList( new String( bytes, "UTF-8" ).split("\n") ) );
			for (int order = 0; order < 6; order++) {
				int i = findClass( String.format("class %s%d", classBase, order) );
				System.out.print(i + ": " + src.get(i));
				i = skipToVrf(i);
				System.out.print(i + ": " + src.get(i));
				int j = findReturn(i);
				System.out.print(j + ": " + src.get(j));
				for (int k = i+1; k < j; k++) {
					System.out.println("Removing: " + src.get(i+1));
					src.remove(i+1);
				}
				String key = String.format("%s%d %s", classBase, order, which);
				List<String> block = codeBlocks.get( key );
				if (block == null) {
					src.add(i+1, String.format("MISSING %s", key) );
				} else {
					int indent = src.get(i).indexOf("V");
					String prefix = src.get(i).substring(0, indent);
					for (String c : block) {
						i++;
						src.add(i, prefix + c);
					}
				}
			}
			PrintWriter out = new PrintWriter( new File(srcPath) );
			src.forEach(out::print);
			out.close();
		} catch (Exception x) {
			x.printStackTrace();
		}
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		new TranslateOctaveDiary( "FMP", FMP_CURRENT, 
				"C:\\Users\\NOOK\\GITHUB\\MorrisonPolynomialFiltering\\Java\\data\\FMP_diary.txt",
				"C:\\Users\\NOOK\\GITHUB\\MorrisonPolynomialFiltering\\Python\\src\\PolynomialFiltering\\Components\\FadingMemoryPolynomialFilter.py" );
		new TranslateOctaveDiary( "EMP", EMP_CURRENT, 
				"C:\\Users\\NOOK\\GITHUB\\MorrisonPolynomialFiltering\\Java\\data\\EMP_diary.txt",
				"C:\\Users\\NOOK\\GITHUB\\MorrisonPolynomialFiltering\\Python\\src\\PolynomialFiltering\\Components\\ExpandingMemoryPolynomialFilter.py" );
	}

}
