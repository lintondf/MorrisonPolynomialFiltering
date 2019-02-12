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

import org.scijava.parse.ExpressionParser;
import org.scijava.parse.Function;
import org.scijava.parse.Group;
import org.scijava.parse.Operator;
import org.scijava.parse.Tokens;

import com.x5.template.Chunk;
import com.x5.template.Theme;


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
					if (parameters.containsKey(name)) {
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
		template.set(functionSignature, "autogenerated from Mathematica notebook\n        return " + stack.pop() + ";" );
	}
	
	public static void main(String[] args) {
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
}
