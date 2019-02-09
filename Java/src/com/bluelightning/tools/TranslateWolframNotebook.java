package com.bluelightning.tools;

import java.io.IOException;
import java.io.PrintStream;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedList;
import java.util.List;
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

	protected static void translateNotebook( String inPath ) {
		try {
			byte[] bytes = Files.readAllBytes( Paths.get(inPath) );
			String line = new String( bytes, "UTF-8" );
			final String cformStartMarker = "\"\\<\\\"";
			final String cformFinishMarker = "\\\"\\>\"";
			int derivative = 1;
			for (int iStart = 0; iStart < line.length(); ) {
				iStart = line.indexOf(cformStartMarker, iStart);
				if (iStart < 0)
					break;
				int jFinish = line.indexOf(cformFinishMarker, iStart);
				String cform = line.substring(iStart+cformStartMarker.length(), jFinish);
				cform = cform.replaceAll("\\s", "");
				//System.out.println(cform);
				cform = cform.replace("\\\\n", "");
				cform = replaceVariableStrings(cform, "x", 10);
				cform = replaceVariableStrings(cform, "y", 10);
				cform = replaceVariableStrings(cform, "z", 10);
				//System.out.println(String.format("[%d, %d] : %s", iStart, derivative, cform));
				try {
					LinkedList<Object> list = new ExpressionParser().parsePostfix(cform);
					String[] parameters = {"X","Y","Z"};
					String signature = String.format("public static double d%dAzimuthdENU%d", derivative, derivative);
					emitJava(System.out, signature, Arrays.asList(parameters), list );
					derivative++;
				} catch (Exception x) {
					x.printStackTrace();
				}
				iStart = jFinish;
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}
	
	public static void emitJava( PrintStream out, String functionSignature, List<String> parameterNames, LinkedList<Object> list) {
		Stack<String> stack = new Stack<>();
		out.printf("%s(", functionSignature);
		if (!parameterNames.isEmpty()) {
			out.printf(" RealVector %s", parameterNames.get(0));
			for (int i = 1; i < parameterNames.size(); i++) {
				out.printf(", RealVector %s", parameterNames.get(i));
			}
			out.printf(" ) {\n");
		}
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
					if (parameterNames.contains(name)) {
						stack.push( String.format("%s.getEntry%s", name, params ));
					} else {
						switch (name) {
						case "Sqrt":
							stack.push("Math.sqrt" + params );
							break;
						case "Power":
							stack.push("POW" + params );
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
		out.println("  return " + stack.pop() + ";");
		out.printf("}\n");
	}
	
	public static void main(String[] args) {
		Chunk template = theme.makeChunk();
		try {
			byte[] bytes = Files.readAllBytes( Paths.get("src/com/bluelightning/tools/RadarCoordinatesTemplate.java") );
			template.append( new String( bytes, "UTF-8" ) );
		} catch (Exception x) {
			x.printStackTrace();
		}
		
		template.set("d1AzimuthdENU1", "autogenerated from Mathematica notebook\n        result = 1.0;");
		
		System.out.println( template.toString() );
		
		translateNotebook( "C:/Users/NOOK/Downloads/dRange.nb" );
//		try {
//			LinkedList<Object> list = new ExpressionParser().parsePostfix("(X[0]*X[1]+Y[0]*Y[1]+Z[0]*Z[1])/Sqrt(Power(X[0],2)+Power(Y[0],2)+Power(Z[0],2))");
////			System.out.println(list.toString());
//			String[] parameters = {"X","Y","Z"};
//			emitJava(System.out, "public static double dAzimuthdENU", Arrays.asList(parameters), list );
//		} catch (Exception x) {
//			x.printStackTrace();
//		}
	}

}
