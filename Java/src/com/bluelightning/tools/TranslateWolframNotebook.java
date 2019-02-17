package com.bluelightning.tools;

import java.io.IOException;
import java.io.PrintStream;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Stack;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.scijava.parse.ExpressionParser;
import org.scijava.parse.Function;
import org.scijava.parse.Group;
import org.scijava.parse.Operator;
import org.scijava.parse.Tokens;

import com.x5.template.Chunk;
import com.x5.template.Theme;

/*

 */

public class TranslateWolframNotebook {
	
	protected static Theme theme = new Theme();
	
	protected static void print( List<Object> list ) {
		for (Object obj : list) {
			System.out.printf("%-20s : %s\n", obj.toString(), obj.getClass().getName() );
		}
	}
	
	
	protected static String replaceVariableStrings( String cform, String var, int maxOrder) {
		ArrayList<String> strs = new ArrayList<>();
		ArrayList<String> reps = new ArrayList<>();
		for (int o = 0; o <= maxOrder; o++) {
			if (o == 0) {
				String s = String.format("Dt(%s)", var);
				strs.add(s);
			} else {
				String s = String.format("Dt(%s)", strs.get(o-1));
				strs.add(s);
			}
			reps.add(String.format("%s[%d]", var.toUpperCase(), o+1));
		}
		Collections.reverse(strs);
		Collections.reverse(reps);
		for (int i = 0; i < strs.size(); i++) {
			cform = cform.replace(strs.get(i), reps.get(i));
		}
		cform = cform.replace( var, String.format("%s[0]", var.toUpperCase()));
		return cform;
	}

	protected static List<String> translateNotebook( String inPath ) {
		List<String> result = new ArrayList<>();
		try {
			byte[] bytes = Files.readAllBytes( Paths.get(inPath) );
			String line = new String( bytes, "UTF-8" );
			line = line.replace("\n", "");
			final String cformStartMarker = "\"\\<\\";
			final String cformFinishMarker = "\\>\"";
			for (int iStart = 0; iStart < line.length(); ) {
				iStart = line.indexOf(cformStartMarker, iStart);
				if (iStart < 0)
					break;
				int jFinish = line.indexOf(cformFinishMarker, iStart);
				String cform = line.substring(iStart+cformStartMarker.length(), jFinish);
				cform = cform.replace("\"",  "");
				cform = cform.replaceAll("\\s", "");
				//System.out.println(cform);
				cform = cform.replace("\\n", "");
				cform = cform.replace("\\", "");
				cform = replaceVariableStrings(cform, "x", 10);
				cform = replaceVariableStrings(cform, "y", 10);
				cform = replaceVariableStrings(cform, "z", 10);
				result.add(cform);
				iStart = jFinish;
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
		return result;
	}
	
	// -2 not a group; -1 not a 2 item group; 0 two item group with integer 2nd; 1 two item group with non-integer 2nd
	protected static int identifyTwoItemGroup( String group ) {
		if (group.startsWith("(") && group.endsWith(")")) {
			group = group.substring(1, group.length()-1);
			String[] fields = group.split(",");
			if (fields.length >= 2) {
				if (fields[fields.length-1].matches("\\+?-?\\d+"))
					return 0;
				else 
					return 1;
			}
			return -1;
		}
		return -2;
	}
	
	public static void emitCpp( Chunk template, List<String> cforms, String signatureFormat, Map<String, String> parameters) {
		int derivative = 1;
		for (String cform : cforms) {
			try {
				System.out.println(cform);
				LinkedList<Object> list = new ExpressionParser().parsePostfix(cform);
				String signature = String.format(signatureFormat, derivative, derivative);
				emitCpp(template, signature, parameters, list );
			} catch (Exception x) {
				x.printStackTrace();
			}	
			derivative++;
		}
	}
	
	public static void emitCpp( Chunk template, String functionSignature, Map<String, String> parameters, LinkedList<Object> list) {
		System.out.println( functionSignature );
//		print(list);
		Stack<String> stack = new Stack<>();
		for (Object obj : list) {
			//System.out.printf("%s : %s\n", obj.toString(), obj.getClass().getName());
			if (Tokens.isNumber(obj)) {
				stack.push( obj.toString() );
			} else if (Tokens.isGroup(obj)) {
				StringBuffer sb = new StringBuffer();
				Group token = (Group) obj;
				Stack<String> alist = new Stack<>();
				for (int i = 0; i < token.getArity(); i++) {
					alist.push( stack.pop() );
				}
				sb.append("(");
				sb.append( alist.pop());
				while( ! alist.isEmpty() ) {
					sb.append(",");
					sb.append(alist.pop());
				}
				sb.append(")");
				stack.push( sb.toString() );
			} else if (Tokens.isOperator(obj)) {
				if (obj instanceof Function) {
					String params = stack.pop();
					String name = stack.pop();
					if (parameters.containsKey(name)) {
						stack.push( String.format("%s%s", parameters.get(name), params ));
					} else {
						switch (name) {
						case "Sqrt":
							stack.push("sqrt" + params );
							break;
						case "Power":
							int kind = identifyTwoItemGroup( params );
							if (kind < 0) System.err.println("Invalid 2-group: " + params);
							if (kind == 0)
								stack.push("POW" + params );
							else
								stack.push("pow" + params );
							break;
						case "Cos":
							stack.push("cos" + params );
							break;
						case "Sin":
							stack.push("sin" + params );
							break;
						default:
							System.err.println("Unknown function: " + name );
						}
					}
				} else {
					Operator token = (Operator) obj;
					String o1;
					String o2;
					switch (token.getArity()) {
					case 1:
						stack.push( String.format("%s(%s)", token.toString(), stack.pop()));
						break;
					case 2:
						o2 = stack.pop();
						o1 = stack.pop();
						stack.push( String.format("(%s)%s(%s)", o1, token.toString(), o2));
						break;
					default:
						System.err.println("Unexpected arity " + token.getArity() );
					}
				}
			} else if (Tokens.isVariable(obj)) {
				stack.push( obj.toString() );
			} else {
				System.err.printf("%s : %s\n", obj.toString(), obj.getClass().getName());
			}
		}
		template.set(functionSignature, "autogenerated from Mathematica notebook\n        result = " + stack.pop() + ";" );
	}
	
	public static void emitJava( Chunk template, List<String> cforms, String signatureFormat, Map<String, String> parameters) {
		int derivative = 1;
		for (String cform : cforms) {
			try {
				System.out.println(cform);
				LinkedList<Object> list = new ExpressionParser().parsePostfix(cform);
				String signature = String.format(signatureFormat, derivative, derivative);
				emitJava(template, signature, parameters, list );
			} catch (Exception x) {
				x.printStackTrace();
			}	
			derivative++;
		}
	}
	
	public static void emitJava( Chunk template, String functionSignature, Map<String, String> parameters, LinkedList<Object> list) {
		System.out.println( functionSignature );
//		print(list);
		Stack<String> stack = new Stack<>();
		for (Object obj : list) {
			//System.out.printf("%s : %s\n", obj.toString(), obj.getClass().getName());
			if (Tokens.isNumber(obj)) {
				stack.push( obj.toString() );
			} else if (Tokens.isGroup(obj)) {
				StringBuffer sb = new StringBuffer();
				Group token = (Group) obj;
				Stack<String> alist = new Stack<>();
				for (int i = 0; i < token.getArity(); i++) {
					alist.push( stack.pop() );
				}
				sb.append("(");
				sb.append( alist.pop());
				while( ! alist.isEmpty() ) {
					sb.append(",");
					sb.append(alist.pop());
				}
				sb.append(")");
				stack.push( sb.toString() );
			} else if (Tokens.isOperator(obj)) {
				if (obj instanceof Function) {
					String params = stack.pop();
					String name = stack.pop();
					if (parameters.containsKey(name)) {
						stack.push( String.format("%s.getEntry%s", parameters.get(name), params ));
					} else {
						switch (name) {
						case "Sqrt":
							stack.push("Math.sqrt" + params );
							break;
						case "Power":
							int kind = identifyTwoItemGroup( params );
							if (kind < 0) System.err.println("Invalid 2-group: " + params);
							if (kind == 0)
								stack.push("POW" + params );
							else
								stack.push("Math.pow" + params );
							break;
						case "Cos":
							stack.push("Math.cos" + params );
							break;
						case "Sin":
							stack.push("Math.sin" + params );
							break;
						default:
							System.err.println("Unknown function: " + name );
						}
					}
				} else {
					Operator token = (Operator) obj;
					String o1;
					String o2;
					switch (token.getArity()) {
					case 1:
						stack.push( String.format("%s(%s)", token.toString(), stack.pop()));
						break;
					case 2:
						o2 = stack.pop();
						o1 = stack.pop();
						stack.push( String.format("(%s)%s(%s)", o1, token.toString(), o2));
						break;
					default:
						System.err.println("Unexpected arity " + token.getArity() );
					}
				}
			} else if (Tokens.isVariable(obj)) {
				stack.push( obj.toString() );
			} else {
				System.err.printf("%s : %s\n", obj.toString(), obj.getClass().getName());
			}
		}
		template.set(functionSignature, "autogenerated from Mathematica notebook\n        result = " + stack.pop() + ";" );
	}

	public static void emitPython( Chunk template, List<String> cforms, String signatureFormat, Map<String, String> parameters) {
		int derivative = 1;
		for (String cform : cforms) {
			try {
				System.out.println(cform);
				LinkedList<Object> list = new ExpressionParser().parsePostfix(cform);
				String signature = String.format(signatureFormat, derivative, derivative);
				emitPython(template, signature, parameters, list );
			} catch (Exception x) {
				x.printStackTrace();
			}	
			derivative++;
		}
	}
	
	public static void emitPython( Chunk template, String functionSignature, Map<String, String> parameters, LinkedList<Object> list) {
		System.out.println( functionSignature );
//		print(list);
		Stack<String> stack = new Stack<>();
		for (Object obj : list) {
			//System.out.printf("%s : %s\n", obj.toString(), obj.getClass().getName());
			if (Tokens.isNumber(obj)) {
				stack.push( obj.toString() );
			} else if (Tokens.isGroup(obj)) {
				StringBuffer sb = new StringBuffer();
				Group token = (Group) obj;
				Stack<String> alist = new Stack<>();
				for (int i = 0; i < token.getArity(); i++) {
					alist.push( stack.pop() );
				}
				sb.append("(");
				sb.append( alist.pop());
				while( ! alist.isEmpty() ) {
					sb.append(",");
					sb.append(alist.pop());
				}
				sb.append(")");
				stack.push( sb.toString() );
			} else if (Tokens.isOperator(obj)) {
				if (obj instanceof Function) {
					String params = stack.pop();
					String name = stack.pop();
					if (parameters != null && parameters.containsKey(name)) {
						stack.push( String.format("%s%s", parameters.get(name), params.replace("(", "[").replace(")", "]") ));
					} else {
						switch (name) {
						case "Sqrt":
							stack.push("sqrt" + params );
							break;
						case "Power":
							stack.push("POW" + params );
							break;
						case "Cos":
							stack.push("cos" + params );
							break;
						case "Sin":
							stack.push("sin" + params );
							break;
						default:
							System.err.println("Unknown function: " + name );
						}
					}
				} else {
					Operator token = (Operator) obj;
					String o1;
					String o2;
					switch (token.getArity()) {
					case 1:
						stack.push( String.format("%s(%s)", token.toString(), stack.pop()));
						break;
					case 2:
						o2 = stack.pop();
						o1 = stack.pop();
						stack.push( String.format("(%s)%s(%s)", o1, token.toString(), o2));
						break;
					default:
						System.err.println("Unexpected arity " + token.getArity() );
					}
				}
			} else if (Tokens.isVariable(obj)) {
				stack.push( obj.toString() );
			} else {
				System.err.printf("%s : %s\n", obj.toString(), obj.getClass().getName());
			}
		}
		if (parameters != null) {
			template.set(functionSignature, "autogenerated from Mathematica notebook\n        return " + stack.pop() + ";" );
		} else {
			template.set(functionSignature, stack.pop() );
		}
	}
	
	public static void translateNotebooks(String[] args) {
		Chunk cppTemplate = theme.makeChunk();
		Chunk javaTemplate = theme.makeChunk();
		Chunk pythonTemplate = theme.makeChunk();
		try {
			byte[] bytes = Files.readAllBytes( Paths.get("../Java/src/com/bluelightning/tools/RadarCoordinatesTemplate.java") );
			javaTemplate.append( new String( bytes, "UTF-8" ) );
			bytes = Files.readAllBytes( Paths.get("../Python/src/RadarCoordinatesTemplate.py") );
			pythonTemplate.append( new String( bytes, "UTF-8" ) );
			bytes = Files.readAllBytes( Paths.get("../Cpp/src/RadarCoordinatesTemplate.hpp") );
			cppTemplate.append( new String( bytes, "UTF-8" ) );
		} catch (Exception x) {
			x.printStackTrace();
		}
		
//		template.set("d1AzimuthdENU1", "autogenerated from Mathematica notebook\n        result = 1.0;");
		
		Map<String, String> map = new HashMap<>();
		map.put( "X", "E");
		map.put( "Y", "N");
		map.put( "Z", "U");
		
		List<String> cforms = translateNotebook( "data/dAzimuth.nb" );
		emitPython( pythonTemplate, cforms, "d%dAzimuthdENU%d", map );
		emitJava( javaTemplate, cforms, "d%dAzimuthdENU%d", map );
		emitCpp( cppTemplate, cforms, "d%dAzimuthdENU%d", map );
		cforms = translateNotebook( "data/dElevation.nb" );
		emitPython( pythonTemplate, cforms, "d%dElevationdENU%d", map );
		emitJava( javaTemplate, cforms, "d%dElevationdENU%d", map );
		emitCpp( cppTemplate, cforms, "d%dElevationdENU%d", map );
		cforms = translateNotebook( "data/dRange.nb" );
		emitPython( pythonTemplate, cforms, "d%dRangedENU%d", map );
		emitJava( javaTemplate, cforms, "d%dRangedENU%d", map );
		emitCpp( cppTemplate, cforms, "d%dRangedENU%d", map );
		
		map.clear();
		map.put( "X", "A");
		map.put( "Y", "E");
		map.put( "Z", "R");

		cforms = translateNotebook( "data/dEast.nb" );
		emitPython( pythonTemplate, cforms, "d%dEastdAER%d", map );
		emitJava( javaTemplate, cforms, "d%dEastdAER%d", map );
		emitCpp( cppTemplate, cforms, "d%dEastdAER%d", map );
		cforms = translateNotebook( "data/dNorth.nb" );
		emitPython( pythonTemplate, cforms, "d%dNorthdAER%d", map );
		emitJava( javaTemplate, cforms, "d%dNorthdAER%d", map );
		emitCpp( cppTemplate, cforms, "d%dNorthdAER%d", map );
		cforms = translateNotebook( "data/dUp.nb" );
		emitPython( pythonTemplate, cforms, "d%dUpdAER%d", map );
		emitJava( javaTemplate, cforms, "d%dUpdAER%d", map );
		emitCpp( cppTemplate, cforms, "d%dUpdAER%d", map );
		
		cppTemplate.set("WARNING", "DO NOT EDIT THIS FILE!  EDIT RadarCoordinatesTemplate.java");
		String cppOutput = cppTemplate.toString();
		cppOutput = cppOutput.replace("class RadarCoordinatesTemplate", "class RadarCoordinates");
		try {
			Files.write(Paths.get("../Cpp/src/RadarCoordinates.hpp"), cppOutput.getBytes());
		} catch (IOException e) {
			e.printStackTrace();
		}

		javaTemplate.set("WARNING", "DO NOT EDIT THIS FILE!  EDIT RadarCoordinatesTemplate.java");
		String javaOutput = javaTemplate.toString();
		javaOutput = javaOutput.replace("public class RadarCoordinatesTemplate", "public class RadarCoordinates");
		try {
			Files.write(Paths.get("../Java/src/com/bluelightning/tools/RadarCoordinates.java"), javaOutput.getBytes());
		} catch (IOException e) {
			e.printStackTrace();
		}

		String pythonOutput = pythonTemplate.toString();
		pythonOutput = pythonOutput.replace("class RadarCoordinatesTemplate", "class RadarCoordinates");
		try {
			Files.write(Paths.get("../Python/src/RadarCoordinates.py"), pythonOutput.getBytes());
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	public static void mainTest_identifyTwoItemGroup(String[] args) {
		System.out.println( identifyTwoItemGroup("hello"));
		System.out.println( identifyTwoItemGroup("(1)"));
		System.out.println( identifyTwoItemGroup("(1,2,3)"));
		System.out.println( identifyTwoItemGroup("(1,2)"));
		System.out.println( identifyTwoItemGroup("(1,2.5)"));
		System.out.println( identifyTwoItemGroup("(1,2/3)"));
	}

	protected static final Pattern denomPattern = Pattern.compile( "\\((n\\+\\d?)\\)\\((\\d+)\\)$" );
	protected static final Pattern numberParen = Pattern.compile("(\\d+)\\(");
	protected static final Pattern numberN = Pattern.compile("(\\d+)n");
	protected static final Pattern uNumber = Pattern.compile("u(\\d+)");
	protected static final Pattern oneMinus = Pattern.compile("\\(1\\-t\\)(\\d*)");
	protected static final Pattern onePlus = Pattern.compile("\\(1\\+t\\)(\\d*)");
	protected static final Pattern numberT = Pattern.compile("(\\d+)t");
	
	
	protected static final String[] runN = {
			"1",
			"n",
			"n*n",
			"n*n*n",
			"n*n*n*n",
			"n*n*n*n*n",
			"n*n*n*n*n*n",
			"n*n*n*n*n*n*n",
			"n*n*n*n*n*n*n*n",
			"n*n*n*n*n*n*n*n*n",
			"n*n*n*n*n*n*n*n*n*n",
			"n*n*n*n*n*n*n*n*n*n*n",
			"n*n*n*n*n*n*n*n*n*n*n*n",
			"n*n*n*n*n*n*n*n*n*n*n*n*n",
	};
	protected static final String[] runT = {
			"1",
			"t",
			"t*t",
			"t*t*t",
			"t*t*t*t",
			"t*t*t*t*t",
			"t*t*t*t*t*t",
			"t*t*t*t*t*t*t",
			"t*t*t*t*t*t*t*t",
			"t*t*t*t*t*t*t*t*t",
			"t*t*t*t*t*t*t*t*t*t",
			"t*t*t*t*t*t*t*t*t*t*t",
			"t*t*t*t*t*t*t*t*t*t*t*t",
			"t*t*t*t*t*t*t*t*t*t*t*t*t",
	};
	
	protected static final String[] runTau = {
			"1",
			"tau",
			"tau*tau",
			"tau*tau*tau",
			"tau*tau*tau*tau",
			"tau*tau*tau*tau*tau",
			"tau*tau*tau*tau*tau*tau",
			"tau*tau*tau*tau*tau*tau*tau",
			"tau*tau*tau*tau*tau*tau*tau*tau",
			"tau*tau*tau*tau*tau*tau*tau*tau*tau",
			"tau*tau*tau*tau*tau*tau*tau*tau*tau*tau",
			"tau*tau*tau*tau*tau*tau*tau*tau*tau*tau*tau",
			"tau*tau*tau*tau*tau*tau*tau*tau*tau*tau*tau*tau",
	};
	protected static final String[] runU = {
			"1",
			"u",
			"u*u",
			"u*u*u",
			"u*u*u*u",
			"u*u*u*u*u",
			"u*u*u*u*u*u",
			"u*u*u*u*u*u*u",
			"u*u*u*u*u*u*u*u",
			"u*u*u*u*u*u*u*u*u",
			"u*u*u*u*u*u*u*u*u*u",
			"u*u*u*u*u*u*u*u*u*u*u",
			"u*u*u*u*u*u*u*u*u*u*u*u",
	};
	protected static final String[] runPlusT = {
		"1",
		"(1+t)",
		"(1+t)*(1+t)",
		"(1+t)*(1+t)*(1+t)",
		"(1+t)*(1+t)*(1+t)*(1+t)",
		"(1+t)*(1+t)*(1+t)*(1+t)*(1+t)",
		"(1+t)*(1+t)*(1+t)*(1+t)*(1+t)*(1+t)",
		"(1+t)*(1+t)*(1+t)*(1+t)*(1+t)*(1+t)*(1+t)",
		"(1+t)*(1+t)*(1+t)*(1+t)*(1+t)*(1+t)*(1+t)*(1+t)",
		"(1+t)*(1+t)*(1+t)*(1+t)*(1+t)*(1+t)*(1+t)*(1+t)*(1+t)",
		"(1+t)*(1+t)*(1+t)*(1+t)*(1+t)*(1+t)*(1+t)*(1+t)*(1+t)*(1+t)",
		"(1+t)*(1+t)*(1+t)*(1+t)*(1+t)*(1+t)*(1+t)*(1+t)*(1+t)*(1+t)*(1+t)",
	};
	protected static final String[] runMinusT = {
			"1",
			"(1-t)",
			"(1-t)*(1-t)",
			"(1-t)*(1-t)*(1-t)",
			"(1-t)*(1-t)*(1-t)*(1-t)",
			"(1-t)*(1-t)*(1-t)*(1-t)*(1-t)",
			"(1-t)*(1-t)*(1-t)*(1-t)*(1-t)*(1-t)",
			"(1-t)*(1-t)*(1-t)*(1-t)*(1-t)*(1-t)*(1-t)",
			"(1-t)*(1-t)*(1-t)*(1-t)*(1-t)*(1-t)*(1-t)*(1-t)",
			"(1-t)*(1-t)*(1-t)*(1-t)*(1-t)*(1-t)*(1-t)*(1-t)*(1-t)",
			"(1-t)*(1-t)*(1-t)*(1-t)*(1-t)*(1-t)*(1-t)*(1-t)*(1-t)*(1-t)",
			"(1-t)*(1-t)*(1-t)*(1-t)*(1-t)*(1-t)*(1-t)*(1-t)*(1-t)*(1-t)*(1-t)",
		};
	
	protected static String numerator2String( String str ) {
		for (int p = 12; p > 0; p--) {
			str = str.replaceAll(String.format("n%d", p), "(" + runN[p] + ")" );
			str = str.replaceAll(String.format("t%d", p), "(" + runT[p] + ")" );
		}
		Matcher m = numberParen.matcher(str);
		while (m.find()) {
			str = m.replaceFirst(Integer.parseInt(m.group(1)) + "*(");
			m = numberParen.matcher(str);
		}
		m = numberN.matcher(str);
		while (m.find()) {
			str = m.replaceFirst(Integer.parseInt(m.group(1)) + "*n");
			m = numberN.matcher(str);
		}
		m = numberT.matcher(str);
		while (m.find()) {
			str = m.replaceFirst(Integer.parseInt(m.group(1)) + "*t");
			m = numberT.matcher(str);
		}
		m = oneMinus.matcher(str);
		while (m.find()) {
			if (! m.group(1).isEmpty()) { 
				int p = Integer.parseInt(m.group(1));
				str = m.replaceFirst( runMinusT[p] );
				m = oneMinus.matcher(str);
			} else 
				break;
		}
		str = str.replace(")(", ")*(");
		return str;
	}
	
	protected static String denominator2String( String str ) {
		StringBuffer sb = new StringBuffer();
		for (int p = 12; p > 0; p--) {
			if (str.startsWith(String.format("tau%d(", p))) {
				sb.append("(" + runTau[p] + ")*");
			}
		}
		Matcher matcher = denomPattern.matcher(str);
		if (matcher.find()) {
//			for (int i = 0; i <= matcher.groupCount(); i++) {
//				System.out.printf("  %d %s\n", i, matcher.group(i) );
//			}
			if (matcher.groupCount() == 2) {
				int power = Integer.parseInt(matcher.group(2));
				if (matcher.group(1).startsWith("n+")) {
					int i = Integer.parseInt(matcher.group(1).substring(2));
					sb.append(String.format("(n+%d)", i));
					while (power > 1) {
						i--;
						if (i == 0)
							sb.append(String.format("*(n)"));
						else if (i > 0)
							sb.append(String.format("*(n+%d)", i));
						else
							sb.append(String.format("*(n%d)", i));
						power--;
					}
				}
			}
			str = sb.toString();
			Matcher m = numberParen.matcher(str);
			while (m.find()) {
				str = m.replaceAll(Integer.parseInt(m.group(1)) + "*(");
				m = numberParen.matcher(str);
			}
			System.out.println("FMP3: " + str);
			str = str.replace(")(", ")*(");
			System.out.println("FMP4: " + str);
		} else { // FMP pattern 
			System.out.println("FMP0: " + str);
			matcher = uNumber.matcher(str);
			while (matcher.find()) {
				int p = Integer.parseInt(matcher.group(1));
				str = matcher.replaceFirst("(" + runU[p] + ")*");
				matcher = uNumber.matcher(str);
			}
			matcher = onePlus.matcher(str);
			if (matcher.find()) {
				if (matcher.group(1).isEmpty()) {
					str = matcher.replaceFirst(runPlusT[1]);					
				} else {
					int p = Integer.parseInt(matcher.group(1));
					str = matcher.replaceFirst(runPlusT[p]);
				}
				matcher = onePlus.matcher(str);
			}
			System.out.println("FMP1: " + str);
			System.out.println("FMP2: " + str);
			Matcher m = numberT.matcher(str);
			while (m.find()) {
				str = m.replaceFirst(Integer.parseInt(m.group(1)) + "*t");
				m = numberT.matcher(str);
			}
			System.out.println("FMP3: " + str);
			m = numberParen.matcher(str);
			while (m.find()) {
				str = m.replaceAll(Integer.parseInt(m.group(1)) + "*(");
				m = numberParen.matcher(str);
			}
			str = str.replace(")(", ")*(");
			System.out.println("FMP4: " + str);
		}
		return str;
	}
	
	public static List<String> translateVRF2CForm(String[] eqns ) {
		List<String> cforms = new ArrayList<>();
		for (String eqn : eqns) {
			eqn = eqn.replace("\r\n", "").replace(" ", "").trim();
			String[] frac = eqn.split("\\|");
			System.out.printf("%s  %s\n", frac[0], frac[1]);
			String cform = String.format("(%s) / (%s)", numerator2String(frac[0]), denominator2String(frac[1]));
			cforms.add(cform);
		}
		return cforms;
	}
		
	public static String validateExpression(String expr) {

		char r[] = expr.toCharArray();
		char s[] = expr.toCharArray();
		Stack<Integer> st = new Stack<Integer>();
		int i = 0;
		while (i < s.length) 
		{
			if (s[i] == '(') {
				if (s[i + 1] == '(') {
					st.push(-i);
				} else {
					st.push(i);
				}
				i++;
			} else if (s[i] != ')' && s[i] != '(') {
				i++;
			} else if (s[i] == ')') {
				int top = st.peek();
				if (s[i - 1] == ')' && top < 0) {
					r[-top] = '$';
					r[i] = '$';
					st.pop();
				}

				else if (s[i - 1] == ')' && top > 0) {
					System.out.println("Something is wrong!!");
				}

				else if (s[i - 1] != ')' && top > 0)
					st.pop();
				i++;
			}
		}

		StringBuffer result = new StringBuffer();

		for (i = 0; i<r.length; i++) {
			if (r[i] == '$') {
				continue;
			}
			result.append(r[i]);
		}

		return result.toString();

	}	
	
	public static void mainx(String[] args) {
		//translateNotebooks(args);
		Chunk cppTemplate = theme.makeChunk();
		Chunk javaTemplate = theme.makeChunk();
		Chunk pythonTemplate = theme.makeChunk();
		for (int order = 0; order <= 5; order++) {
			pythonTemplate.append(String.format("# EMP%d VRF\n", order) );
			pythonTemplate.append("tau = self.tau;\n");
			pythonTemplate.append("return array([\n");
			for (int i = 0; i <= order; i++) {
				pythonTemplate.append( String.format("{$EMP%dVRF_%dth}", order, i));
				if (i < order) {
					pythonTemplate.append(",");
				}
				pythonTemplate.append("\n");
			}
			pythonTemplate.append("])\n");
		}
//		System.out.println(pythonTemplate.toString());

//		int order = 5;
//		List<String> cforms = translateVRF2CForm(new String[] {
//				"6 (2n+3)(3n4+18n3+113n2+258n+280)\r\n" + 
//				"|(n+1)(6)",
//				"588 (25n8+500n7+4 450n6+23 300n5+79 585n4+181 760n3\r\n" + 
//				"+267 180n2+226 920n+84 528)\r\n" + 
//				"|\r\n" + 
//				"tau2(n+6)(11)",
//				"70 560 (2n+3)(16n5+192n4+952n3+2 472n2+3 501n+2 230)\r\n" + 
//				"|\r\n" + 
//				"tau4(n+6)(11)",
//				"2 721 600 (48n4+402n3+1 274n2+1 828n+1 047)\r\n" + 
//				"|\r\n" + 
//				"tau6(n+6)(11)",
//				"50 803 200 (2n+3)(25n+62)\r\n" + 
//				"|\r\n" + 
//				"tau8(n+6)(11)",
//				"10 059 033 600\r\n" + 
//				"|\r\n" + 
//				"tau10(n+6)(11)"
//		} );
//		int order = 4;
//		List<String> cforms = translateVRF2CForm(new String[] {
//			"5 (5n4+30n3+115n2+210n+144)\r\n" + 
//			"|(n+1)(5)",
//			"100 (2n+3)(24n5+297n4+1476n3+3 777n2+5 198n+3 172)\r\n" + 
//			"|tau\r\n" + 
//			"2(n+5)(9)",
//			"35 280 (9n4+76n3+239n2+336n+185)\r\n" + 
//			"|tau\r\n" + 
//			"4(n+5)(9)",
//			"100 800 (2n+3)(32n+79)\r\n" + 
//			"|tau\r\n" + 
//			"6(n+5)(9)",
//			"25 401 600\r\n" + 
//			"|tau\r\n" + 
//			"8(n+5)(9)",
//		} );
//		int order = 3;
//		List<String> cforms = translateVRF2CForm(new String[] {
//			"4(4n3+18n2+38n+30)\r\n" + 
//			"|(n+1)(4)",
//			"200 (6n4+51n3+159n2+219n+116)\r\n" + 
//			"|tau\r\n" + 
//			"2(n+4)(7)",
//			"1440 (2n+3)(9n+22)\r\n" + 
//			"|tau\r\n" + 
//			"4(n+4)(7)",
//			"100 800\r\n" + 
//			"|tau\r\n" + 
//			"6(n+4)(7)",
//		} );
//		int order = 2;
//		List<String> cforms = translateVRF2CForm(new String[] {
//			"3(3n2+9n+8)\r\n" + 
//			"|(n+1)(3)",
//			"12(16n2+62n+57)\r\n" + 
//			"|tau\r\n" + 
//			"2(n+3)(5)",
//			"720\r\n" + 
//			"|tau\r\n" + 
//			"4(n+3)(5)",
//		} );
//		int order = 1;
//		List<String> cforms = translateVRF2CForm(new String[] {
//				"2(2n+3)\r\n" + 
//				"|(n+1)(2)",
//				"12\r\n" + 
//				"|tau\r\n" + 
//				"2(n+2)(3)"
//		} );
//		int order = 1;  // FMF
//		List<String> cforms = translateVRF2CForm(new String[] {
//				"(t 2+4t +5)(1 - t)        |   (1+t)3",
//				"2(1 - t)3 | u 2(1+t)3"
//		} );
//		int order = 2;
//		List<String> cforms = translateVRF2CForm(new String[] {
//				"(t 4+6t3 +16t 2+24t +19)(1 - t)                       |   (1+t)5",
//				"(13t 2+50t +49)(1 - t)3         |   2 u 2(1+t)5 ",
//				"6(1 - t)5|  u 4(1+t)5"
//		} );
//		int order = 3;
//		List<String> cforms = translateVRF2CForm(new String[] {
//				"  (t6+8t5+29t 4+64t3+97t 2+104t+69)(1 - t)                                     |  (1+t)7",
//				"5(53t4+298t3+762t 2+970t+581)(1 - t)3                               | 18 u 2(1+t)7",
//				"2(23t 2+76t+63)(1 - t)5              | u 4(1+t)7",
//				"20(1 - t)7   | u 6(1+t)7"
//		} );
//		int order = 4;
//		List<String> cforms = translateVRF2CForm(new String[] {
//				"(t8+10t7+46t6+130t5+2 56t 4+380t3+446t 2+4 10t+251)(1 - t)                                                  |  (1+t)9",
//				"5(449t6+2 988t5+10 013t 4+21 216t3+28 923t 2+25 588t+12 199)(1 - t)3                                                | 72 u 2(1+t)9",
//				"7(2 021t 4+10 144t3+22 746t 2+25 144t+12 521)(1 - t)5                                       | 72 u 4(1+t)9",
//				"5(113t 2+338t+253)(1 - t)7                 | 2 u 6(1+t)9",
//				"70(1 - t)9 |  u 8(1+t)9"
//		} );
		int order = 5;
		List<String> cforms = translateVRF2CForm(new String[] {
				"(t10+12t9+67t8+232t7+562t6+1 024t5 +14 84t 4+1 792t3+1 847t 2+1 572t+923)(1 - t)                                 | (1+t)11",
				"7(17 467t8+124 874t7+478 036t6+1 239 958t5+2 345 510 t4          +3 250 918t3+3 352 636t 2+2 454 074t+1 028 527)(1 - t)3                                              | 1800 u 2(1+t)11",
				"7(7 121t6+43 016t5+129 715t4+244 880t3                 +295 855t 2+225 176t+87 581)(1 - t)5                                | 72 u 4(1+t)11",
				"3(2 549t 4+12 072t3+24 926t 2+25 176t+11 117)(1 - t)7                                      |  4 u 6(1+t)11",
				"14(113t 2+316t+221)(1 - t)9                 | u8(1+t)11",
				"252(1 - t)11 |  u 10(1+t)11",
		} );
		int element = 0;
		for (String cform : cforms) {
			try {
				System.out.println(cform);
				LinkedList<Object> list = new ExpressionParser().parsePostfix(cform);
				String signature = String.format("EMP%dVRF_%dth", order, element);
				emitPython(pythonTemplate, signature, null, list );
			} catch (Exception x) {
				x.printStackTrace();
			}	
			element++;
		}
		System.out.println(pythonTemplate.toString().replace("POW", "pow"));		
		
	}
	
	protected static final Pattern powerPattern = Pattern.compile("(Power\\(([^,]*),(\\d+)\\))");
	
	protected static int[] parseIndicies( String str ) {
		String[] fields = str.split(",");
		int[] out = new int[3];
		for (int i = 0; i < 3; i++) {
			out[i] = Integer.parseInt(fields[i]);
		}
		return out;
	}
	
	protected static class CVRFElement {
		public int i;
		public int j;
		public String expression;
		
		public void setExpression( String str ) {
			this.expression = str.replace(" ", "").trim();
			if (expression.startsWith("-")) {
				expression = expression.substring(1);
			}
			Matcher matcher = powerPattern.matcher(expression);
			while (matcher.find()) {
				String sub = matcher.group(2);
				int pow = Integer.parseInt(matcher.group(3));
				StringBuffer exp = new StringBuffer();
				if (sub.length() > 1) {
					sub = String.format("(%s)", sub);
				}
				exp.append('(');
				for (int p = 0; p < pow; p++) {
					if (p > 0)
						exp.append('*');
					exp.append('(');
					exp.append(sub);
					exp.append(')');
				}
				exp.append(')');
				expression = matcher.replaceFirst(exp.toString());
				matcher = powerPattern.matcher(expression);
			}
		}
		
		public String toString() {
			return String.format("(%d,%d) = %s;", i, j, expression );
		}
	}
	
	protected static class CVRFCode {
		public String  nameOrder;  // e.g. EMP1
		public List<CVRFElement> elements = new ArrayList<>();
		
		public String toString() {
			StringBuffer sb = new StringBuffer();
			sb.append( String.format("%s\n", nameOrder) );
			for (CVRFElement element : elements ) {
				sb.append(element.toString());
				sb.append('\n');
			}
			return sb.toString();
		}
	}
	
	protected static void translateCVRFNotebook(String inPath) {
		final String[] names = {"", "EMP", "FMP"};
		int iNames = 0;
		CVRFCode code = null;
		List<String> result = new ArrayList<>();
		try {
			byte[] bytes = Files.readAllBytes( Paths.get(inPath) );
			String line = new String( bytes, "UTF-8" );
			line = line.replace("\n", "");
			final String elementStartMarker = "RowBox[{\"m\",\"=\"";
			final String indiciesStartMarker = "RowBox[{\"{\",RowBox[{";
			final String cformStartMarker = "InterpretationBox[\"\\\"";
			final String cformFinishMarker = "\\\"\"";
			for (int iStart = 0; iStart < line.length(); ) {
				iStart = line.indexOf(elementStartMarker, iStart);
				if (iStart < 0)
					break;
				int kNext = line.indexOf(elementStartMarker, iStart+elementStartMarker.length());
				iStart = line.indexOf(indiciesStartMarker, iStart);
				if (iStart < 0)
					break;
				while (iStart < kNext) {
					int jFinish = line.indexOf("}", iStart);
					String indicies = line.substring(iStart + indiciesStartMarker.length(), jFinish);
					indicies = indicies.replace("\",\"", "");
					indicies = indicies.replace("\"", "");
					int[] orderIJ = parseIndicies(indicies);
					if (orderIJ[0] == 0) {
						iNames++;
					}
					if (orderIJ[1] == 0 && orderIJ[2] == 0) {
						if (code != null)
							System.out.println(code);
						code = new CVRFCode();
						code.nameOrder = String.format("%s%d", names[iNames], orderIJ[0] );
					}
					iStart = line.indexOf(cformStartMarker, jFinish);
					jFinish = line.indexOf(cformFinishMarker, iStart);
//					System.out.println(line.substring(iStart + cformStartMarker.length(), jFinish));
					CVRFElement element = new CVRFElement();
					element.i = orderIJ[1];
					element.j = orderIJ[2];
					element.setExpression( line.substring(iStart + cformStartMarker.length(), jFinish) );
					code.elements.add(element);
					iStart = line.indexOf(indiciesStartMarker, iStart);
					if (iStart < 0)
						break;
					iStart = Math.min(kNext, iStart);
				}
			}
			if (code != null)
				System.out.println(code);
		} catch (IOException e) {
			e.printStackTrace();
		}
//		return result;
	}
	
	public static void main(String[] args) {
		translateCVRFNotebook("../Java/data/MorrisonCVRF.nb");
		Chunk cppTemplate = theme.makeChunk();
		Chunk javaTemplate = theme.makeChunk();
		Chunk pythonTemplate = theme.makeChunk();
		for (int order = 0; order <= 5; order++) {
			pythonTemplate.append(String.format("# EMP%d VRF\n", order) );
			pythonTemplate.append("tau = self.tau;\n");
			pythonTemplate.append("return array([\n");
			for (int i = 0; i <= order; i++) {
				pythonTemplate.append( String.format("{$EMP%dVRF_%dth}", order, i));
				if (i < order) {
					pythonTemplate.append(",");
				}
				pythonTemplate.append("\n");
			}
			pythonTemplate.append("])\n");
		}
		System.out.println(pythonTemplate.toString());
		pythonTemplate.set("EMP0VRF_0th", "{@EMP0VRF_0th} plus stuff");
		System.out.println(pythonTemplate.toString());

	}
	

}
