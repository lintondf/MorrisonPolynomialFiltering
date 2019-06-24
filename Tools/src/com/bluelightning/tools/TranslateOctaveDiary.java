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
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.bluelightning.tools.transpiler.Transpiler;

/**
 * @author NOOK
 *
 */
public class TranslateOctaveDiary {
	
	public static final String EMP_CURRENT = "current-estimate";
	public static final String EMP_ONESTEP = "one-step";
	public static final String FMP_CURRENT = "current-estimate";
	public static final String FMP_ONESTEP = "one-step";
	
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
//						System.out.println(key + " "+ block);
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
	
	public static Pattern element = Pattern.compile("V\\[(\\d),(\\d)\\]");

	public void refactorEmpLines(Iterator<String> it) {
		String line = null;
		String vFirst = null;
		String vLast = null;
		ArrayList<String> diag = new ArrayList<>();
		ArrayList<String> offdiag = new ArrayList<>();
		while (it.hasNext()) {
			line = it.next().trim();
			Matcher match = element.matcher(line);
			if (match.find()) {
				if (match.group(1).equals(match.group(2))) { // diagonal
					diag.add(line);
					if (match.group(1).equals("0"))
						vFirst = line;
					else
						vLast = line;
				} else {
					offdiag.add(line);
				}
			}
		}
		if (vLast != null) {
			diag.remove(vLast);								
		} else {
			vLast = vFirst;
		}
//		System.out.println(vFirst);
//		System.out.println(vLast);
//		diag.forEach(System.out::println);
//		offdiag.forEach(System.out::println);
	
		diag.remove(vFirst);
		System.out.println("    def _getFirstVRF(self, n : int, tau : float ) -> float:");
		System.out.printf( "        return %s;\n\n", vFirst.substring(7));
		System.out.println("    def _getLastVRF(self, n : int, tau : float ) -> float:");
		System.out.printf( "        return %s;\n\n", vLast.substring(7));
		System.out.println("    def _getDiagonalVRF(self, n : int, tau : float ) -> array:");
		System.out.println("        V = allocate_V;");
		System.out.printf("        %sself._getFirstVRF(n, tau);\n", vFirst.substring(0, 7));
		for (String d : diag) {
			System.out.println("        " + d );
		}
		if (vFirst != vLast) {
			System.out.printf("        %sself._getLastVRF(n, tau);\n", vLast.substring(0, 7));								
		}
		System.out.println("        return V;\n");
		System.out.println("    def _getVRF(self, n : int, tau : float ) -> array:");
		System.out.println("        V = self._getDiagonalVRF(n, tau)");
		for (String d : offdiag) {
			System.out.println("        " + d );
		}
		System.out.println("        return V;\n");
	}

	
	public void writeEmpPython() {
		int order = 0;
		while (true) {
			String key = String.format("EMP%d %s", order, EMP_CURRENT);
			List<String> block = codeBlocks.get(key);
			if (block == null)
				break;
			System.out.println(key);
			refactorEmpLines(block.iterator());
			order++;
		}
	}
	
	
	public void refactorFmpLines(Iterator<String> it) {
		String line = null;
		while (it.hasNext()) {
			line = it.next().trim();
			Matcher match = element.matcher(line);
			if (match.find()) {
				int iStart = line.indexOf('=');
				if (line.charAt(iStart+1) != 'V') {
					line = RefactorVrfMethods.floatConstants(line, iStart+1);
				}
				System.out.println(line);
			}
		}
	}
	
	
	public void writeFmpPython() {
		int order = 0;
		while (true) {
			String key = String.format("FMP%d %s", order, FMP_CURRENT);
			List<String> block = codeBlocks.get(key);
			if (block == null)
				break;
			System.out.println(key);
			refactorFmpLines(block.iterator());
			order++;
		}
	}
	
	
	
	
	public TranslateOctaveDiary(String classBase, String which, String diaryPath, String srcPath ) {
		try {
			byte[] bytes = Files.readAllBytes( Paths.get(diaryPath) );
			diary = Arrays.asList( new String( bytes, "UTF-8" ).split("\n") );
			loadCodeBlocks();
//			writeEmpPython();
			writeFmpPython();
		} catch (Exception x) {
			x.printStackTrace();
		}
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		new TranslateOctaveDiary( "FMP", FMP_ONESTEP, 
				"C:\\Users\\NOOK\\GITHUB\\MorrisonPolynomialFiltering\\Java\\data\\FMP_diary.txt",
				"C:\\Users\\NOOK\\GITHUB\\MorrisonPolynomialFiltering\\Python\\src\\PolynomialFiltering\\Components\\FadingMemoryPolynomialFilter.py" );
//		new TranslateOctaveDiary( "EMP", EMP_ONESTEP, 
//				"C:\\Users\\NOOK\\GITHUB\\MorrisonPolynomialFiltering\\Java\\data\\EMP_diary.txt",
//				"C:\\Users\\NOOK\\GITHUB\\MorrisonPolynomialFiltering\\Python\\src\\PolynomialFiltering\\Components\\ExpandingMemoryPolynomialFilter.py" );
	}

}
