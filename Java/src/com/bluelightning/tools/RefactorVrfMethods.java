/**
 * 
 */
package com.bluelightning.tools;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.zip.CRC32;
import java.util.zip.Checksum;

/**
 * @author NOOK
 *
 */
public class RefactorVrfMethods {

	public static Pattern element = Pattern.compile("V\\[(\\d),(\\d)\\]");

//	public static void refactorLines(Iterator<String> it) {
//		String line = null;
//		String vFirst = null;
//		String vLast = null;
//		ArrayList<String> diag = new ArrayList<>();
//		ArrayList<String> offdiag = new ArrayList<>();
//		while (it.hasNext()) {
//			line = it.next();
//			Matcher match = element.matcher(line);
//			if (match.find()) {
//				System.out.println(line);
//				if (match.group(1).equals(match.group(2))) { // diagonal
//					diag.add(line);
//					if (match.group(1).equals("0"))
//						vFirst = line;
//					else
//						vLast = line;
//				} else {
//					offdiag.add(line);
//				}
//			}
//		}
//		if (vLast != null) {
//			diag.remove(vLast);								
//		} else {
//			vLast = vFirst;
//		}
//		diag.remove(vFirst);
//		System.out.println("    def _getFirstVRF(self, n : float, tau : float ) -> float:");
//		System.out.printf( "        return %s;\n\n", vFirst.substring(15));
//		System.out.println("    def _getLastVRF(self, n : float, tau : float ) -> float:");
//		System.out.printf( "        return %s;\n\n", vLast.substring(15));
//		System.out.println("    def _getDiagonalVRF(self, n : float, tau : float ) -> array:");
//		System.out.println("        V = allocate_V;\n");
//		System.out.printf("%sself._getFirstVRF(n, tau);\n", vFirst.substring(0, 15));
//		diag.forEach(System.out::println);
//		if (vFirst != vLast) {
//			System.out.printf("%sself._getLastVRF(n, tau);\n", vLast.substring(0, 15));								
//		}
//		System.out.println("        return V;\n");
//		System.out.println("    def _getVRF(self, n : float, tau : float ) -> array:");
//		System.out.println("        V = self._getDiagonalVRF(n, tau)");
//		offdiag.forEach(System.out::println);
//		System.out.println("        return V;\n");
//	}
	
	protected static String floatConstants( String line, int iStart) {
		StringBuilder sb = new StringBuilder();
		for (int i = 0; i < iStart; i++) {
			sb.append(line.charAt(i));
		}
		for (int i = iStart; i < line.length(); i++) {
			if (Character.isDigit(line.charAt(i))) {
				sb.append(line.charAt(i));
				if (Character.isAlphabetic(line.charAt(i-1)))
					continue;
				boolean hasPoint = false;
				if (line.charAt(i-2) == '*' && line.charAt(i-1) == '*')
					hasPoint = true;
				i++;
				while (i < line.length()) {
					if (Character.isDigit(line.charAt(i))) {
						sb.append(line.charAt(i));											
					} else if (line.charAt(i) == '.') {
						sb.append(line.charAt(i));					
						hasPoint = true;
					} else {
						if (!hasPoint)
							sb.append(".0");
						sb.append(line.charAt(i));
						break;
					}
					i++;
				}
				if (i >= line.length()) {
					sb.append(".0");
				}
			} else {
				sb.append(line.charAt(i));
			}
		}
		return sb.toString().replace("..", ".");
	}

	/**
	 * 
	 */
	public RefactorVrfMethods() {
		try {
			Path path = Paths.get("../Python/src/polynomialfiltering/components/Emp.py");
			System.out.println( path.toAbsolutePath().toString() );
			List<String> lines = Files.readAllLines(path);
			Iterator<String> it = lines.iterator();
			while (it.hasNext()) {
				String line = it.next();
				if (line.trim().startsWith("#"))
					continue;
				Matcher match = element.matcher(line);
				if (match.find()) {
					int iStart = 1 + line.indexOf('=');
					if (! line.substring(iStart).startsWith("V[")) {
						line = floatConstants( line, iStart);
					}
					System.out.println(line);
				} else if (line.trim().startsWith("return")) {
					int iStart = line.indexOf("return ");
					iStart += "return ".length();
					line = floatConstants( line, iStart );
					System.out.println(line);
					while (it.hasNext()) {
						line = it.next();
						if (line.trim().isEmpty()) {
							System.out.println(line);
							break;
						}
						line = floatConstants( line, 0 );
						System.out.println(line);						
					}
				} else {
					System.out.println(line);
				}
//				if (line.startsWith("class")) {
//					System.out.println(line);
//					while (it.hasNext()) {
//						line = it.next();
//						if (line.trim().startsWith("def _")) {
//							String vAllocate = null;
//							String vFirst = null;
//							String vLast = null;
//							ArrayList<String> diag = new ArrayList<>();
//							ArrayList<String> offdiag = new ArrayList<>();
//							while (it.hasNext()) {
//								line = it.next();
//								if (line.trim().startsWith("V = ")) {
//									vAllocate = line;
//									break;
//								}
//							}
//							while (it.hasNext()) {
//								line = it.next();
//								if (line.trim().startsWith("return"))
//									break;
//								Matcher match = element.matcher(line);
//								if (match.find()) {
//									System.out.println(line);
//									if (match.group(1).equals(match.group(2))) { // diagonal
//										diag.add(line);
//										if (match.group(1).equals("0"))
//											vFirst = line;
//										else
//											vLast = line;
//									} else {
//										offdiag.add(line);
//									}
//								}
//							}
//							if (vLast != null) {
//								diag.remove(vLast);								
//							} else {
//								vLast = vFirst;
//							}
//							diag.remove(vFirst);
//							System.out.println("    def _getFirstVRF(self, n : int, tau : float ) -> float:");
//							System.out.printf( "        return %s;\n\n", vFirst.substring(15));
//							System.out.println("    def _getLastVRF(self, n : int, tau : float ) -> float:");
//							System.out.printf( "        return %s;\n\n", vLast.substring(15));
//							System.out.println("    def _getDiagonalVRF(self, n : int, tau : float ) -> array:");
//							System.out.println(vAllocate);
//							System.out.printf("%sself._getFirstVRF(n, tau);\n", vFirst.substring(0, 15));
//							diag.forEach(System.out::println);
//							if (vFirst != vLast) {
//								System.out.printf("%sself._getLastVRF(n, tau);\n", vLast.substring(0, 15));								
//							}
//							System.out.println("        return V;\n");
//							System.out.println("    def _getVRF(self, n : int, tau : float ) -> array:");
//							System.out.println("        V = self._getDiagonalVRF(n, tau)");
//							offdiag.forEach(System.out::println);
//							System.out.println("        return V;\n");
//							break;
//						}
//					}
//				}
			}
		} catch (Exception x) {
			x.printStackTrace();
		}
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		new RefactorVrfMethods();
	}

}
