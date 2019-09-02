/**
 * Runs on Mac with Mathematica installed
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
import java.util.Stack;
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
	
	protected String toHorner( int[] coef) {
		int iLast;
		for (iLast = coef.length-1; iLast >= 0; iLast--) {
			if (coef[iLast] != 0)
				break;
		}
		StringBuilder sb = new StringBuilder();
		for (int ic = 0; ic < iLast; ic++) {
			sb.append("{");
		}
		sb.append(String.format("%d*t}", coef[iLast]));
		for (int j = iLast-1; j > 0; j--) {
			sb.append(String.format("+%d}*t", coef[j]));
		}
		sb.append(String.format("+%d", coef[0]));
		return sb.toString();
	}
	
	final Pattern polyFirstTerm = Pattern.compile("([\\-|\\+]?)(\\d+\\*)?t\\*\\*(\\d+)");
	final Pattern polyTerm = Pattern.compile("([\\-|\\+]?)(\\d+)?(\\*)?(t)?(\\*\\*(\\d+))?");
	
	protected String scanTerm( String term ) {
		if (term.charAt(0) != '(')
			return term;
		StringBuilder sb = new StringBuilder();
		sb.append('(');
		Stack<Integer> j = new Stack<>();
		Stack<Integer> k = new Stack<>();
		j.push(1);
		k.push(sb.length());
		for (int i = 1; i < term.length(); i++) {
			if (term.charAt(i) == ')') {
				String inside = term.substring(j.pop(), i);
				Matcher matcher0 = polyFirstTerm.matcher(inside);
				if (matcher0.find()) { //this is a polynomial
					int[] coef = new int[20];
					Matcher matcher = polyTerm.matcher(inside);
					while (matcher.find()) {
//						System.out.print("  [");
//						for (int g = 1; g <= matcher.groupCount(); g++)
//							System.out.printf(" %d:{%s}, ", g, matcher.group(g));
//						System.out.println("]");
						if (matcher.group(2) != null || matcher.group(4) != null) {
							if (matcher.group(4) != null) { // is a t term
								String factor = "";
								if (matcher.group(1) != null)
									factor += matcher.group(1);
								if (matcher.group(2) != null)
									factor += matcher.group(2);
								else
									factor += "1";
								if (matcher.group(5) != null) { // t ** n
									coef[Integer.parseInt(matcher.group(6))] = Integer.parseInt(factor);
								} else {
									coef[1] = Integer.parseInt(factor);
								}
							} else {
								coef[0] = Integer.parseInt(matcher.group(2));
							}
						}
					}
					sb.replace(k.pop(), sb.length(), toHorner(coef));
				}
			}
			if (term.charAt(i) == '(') {
				j.push( i+1 );
				k.push( sb.length()+1 );
			}
			sb.append(term.charAt(i));
		}
		String out = sb.toString();
		out = out.replace("{",  "(").replace("}",  ")");
		return out;
	}
	
	final Pattern prefix = Pattern.compile("^\\(?\\-?\\d+(\\.0)\\/\\d+(\\.0)\\)?\\*");
	
	protected String hornerizeLower(String term) {
		String cmd = String.format("HornerForm[%s]", term.replace("**", "^"));
		String out = kernel.send(cmd);
		return out.trim().replace("^", "**");
	}
	
	protected String hornerizeUpper(String term) {
		String cmd = String.format("HornerForm[%s /. t -> (1 - s)]", term.replace("**", "^"));
		String out = kernel.send(cmd);
		return out.trim().replace("^", "**");
	}
	
	public String hornerize(String line) {
		int iEqual = line.indexOf('=');
		if (iEqual < 0 || line.charAt(iEqual+1) == 'V')
			return line;
		String lhs = line.substring(0, iEqual+1);
		String rhs = line.substring(iEqual+1);
		String term = hornerizeLower(rhs);
		term = RefactorVrfMethods.floatConstants(term,0);
		lower.add( "\t\t\t" + lhs + term );
		term = hornerizeUpper(rhs);
		term = RefactorVrfMethods.floatConstants(term,0);
		upper.add( "\t\t\t" + lhs + term );
		return lhs + term;
	}
	
	ArrayList<String> lower;
	ArrayList<String> upper;
	
	public void refactorFmpLines(Iterator<String> it) {
		lower = new ArrayList<>();
		upper = new ArrayList<>();
		String line = null;
		while (it.hasNext()) {
			line = it.next().trim();
			Matcher match = element.matcher(line);
			if (match.find()) {
				int iStart = line.indexOf('=');
				if (line.charAt(iStart+1) != 'V') {
//					System.out.println(line);
					line = hornerize(line);
//					line = RefactorVrfMethods.floatConstants(line, iStart+1);
				} else {
					lower.add("\t\t\t" + line);
					upper.add("\t\t\t" + line);
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
			System.out.println();
			System.out.println(key);
			System.out.println("        if (t < 0.5) :");
			lower.forEach(System.out::println);
			System.out.println("        else :\n" + 
					"            s = 1.0 - t;");
			upper.forEach(System.out::println);
			order++;
		}
	}
	
	
	Execute kernel;
	
	public TranslateOctaveDiary(String classBase, String which, String diaryPath, String srcPath ) {
		try {
			kernel = Execute.openMathematicaServer();
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
	 * @param argsx
	 */
	public static void main(String[] args) {
		new TranslateOctaveDiary( "FMP", FMP_ONESTEP, 
				"/Users/lintondf/GITHUB/MorrisonPolynomialFiltering/Tools/data/FMP_diary.txt",
				"/Users/lintondf/GITHUB/MorrisonPolynomialFiltering/Python/src/PolynomialFiltering/Components/FadingMemoryPolynomialFilter.py" );
//		new TranslateOctaveDiary( "EMP", EMP_ONESTEP, 
//				"C:\\Users\\NOOK\\GITHUB\\MorrisonPolynomialFiltering\\Java\\data\\EMP_diary.txt",
//				"C:\\Users\\NOOK\\GITHUB\\MorrisonPolynomialFiltering\\Python\\src\\PolynomialFiltering\\Components\\ExpandingMemoryPolynomialFilter.py" );
	}

}
