package com.bluelightning.tools.transpiler;

import java.util.HashMap;
import java.util.List;
import java.util.Stack;


public class Scope {
	
		protected static HashMap<String, Scope> scopeMap = new HashMap<>();
		
		public static Scope getExistingScope( String qString ) {
			return scopeMap.get(qString);
		}
		
//		protected String[] qualifiers; // e.g. com.bluelightning.Filtering
		public enum Level {
			IMPORT, MODULE, FUNCTION, CLASS, MEMBER,
		};
		protected Stack<String> qualifiers = new Stack<>();
		protected Stack<Level>  levels = new Stack<>();
		protected String qString;
		
		public String toAnnotatedString() {
			StringBuilder sb = new StringBuilder();
			sb.append('/');
			for (int i = 0; i < qualifiers.size(); i++) {
				sb.append( levels.get(i+1).toString() );
				sb.append(':');
				sb.append( qualifiers.get(i) );
				sb.append('/');
			}
			return sb.toString();
			
		}
		
		protected String getScopeString() {
			StringBuilder sb = new StringBuilder();
			sb.append('/');
			for (int i = 0; i < qualifiers.size(); i++) {
				sb.append( qualifiers.get(i) );
				sb.append('/');
			}
			return sb.toString();
		}
		
		public Stack<String> getQualifiers() {
			return qualifiers;
		}
		
		final static String target = "/polynomialfiltering/components/Fmp_test/generateStates/Fmp_test/";
		public Scope() {
			levels.push( Level.IMPORT );
//			qualifiers.push("");
			this.qString = getScopeString();
			scopeMap.put(this.qString, this);
			if (this.qString.equals(target)) 
				System.out.println(this);
		}
		
		private Scope( Scope that, boolean copy ) {
			if (copy) {
				this.levels.addAll( that.levels );
				this.qualifiers.addAll( that.qualifiers );
			} else {
				levels.push( Level.IMPORT );				
			}
			this.qString = this.getScopeString();
		}
		
		static public Scope reparent( Scope that, String moduleName ) {
			Scope out = new Scope(that, true);
			out.qualifiers.add(0, moduleName);
			out.levels.add(1, Level.MODULE);
			out.qString = out.getScopeString();
			scopeMap.put(out.qString, out);
			if (out.qString.equals(target)) 
				System.out.println(out);
			return out;
		}
		
		public String getLast() {
			if (qualifiers.isEmpty())
				return "";
			return qualifiers.peek();
		}
		
		public Scope getAtLevel(int level, Level last) {
			Scope scope = new Scope(this, false);
			for (int i = 1; i <= level; i++) {
				scope.qualifiers.push(this.qualifiers.get(i));
				scope.levels.push(this.levels.get(i));
			}
			scope.qString = scope.getScopeString();
			scopeMap.put(scope.qString, scope);
			return scope;
		}
		
		public Scope getChild( Scope.Level childLevel, String childName ) {
//			System.out.println( this.toString() );
			if (levels.peek() == Level.CLASS) {
				if (childLevel == Level.FUNCTION) {
					childLevel = Level.MEMBER;
				} else {
					childLevel = Level.CLASS;
				}
			} else if (levels.peek() == Level.MEMBER) {
				childLevel = Level.CLASS;
			}
			Scope scope = new Scope(this, true);
			scope.levels.push(childLevel);
			scope.qualifiers.push(childName);
			scope.qString = scope.getScopeString();
			scopeMap.put(scope.qString, scope);
			if (this.qString.equals(target)) 
				System.out.println(this);			
			return scope;
		}
		
		public Scope getParent() {
			if (this.qualifiers.isEmpty())
				return null;
			Scope scope = new Scope(this, true);
			scope.levels.pop();
			scope.qualifiers.pop();
			scope.qString = scope.getScopeString();
			scopeMap.put(scope.qString, scope);
			return scope;
		}
		
		@Override
		public String toString() {
			return qString;
		}

		public Scope.Level getLevel() {
			return levels.peek();
		}

		public int getLevelCount() {
			return qualifiers.size();
		}
		
		public String getLevel(int level) {
			return qualifiers.get(level);
		}

		public Scope.Level getLevelKind(int level) {
			return levels.elementAt(level+1);
		}
		public String getVisiblityPrefix(Scope currentScope) {
			StringBuilder sb = new StringBuilder();
			for (int i = 0; i < qualifiers.size(); i++) {
				if (i >= currentScope.qualifiers.size()) {
					for (int j = i; j < qualifiers.size(); j++) {
						if (qualifiers.get(j).equals("Main") ||
							qualifiers.get(j).equals("ExpandingMemoryPolynomialFilter") ||
							qualifiers.get(j).equals("FadingMemoryPolynomialFilter") )
							continue;
						sb.append(qualifiers.get(j));
						sb.append("/");
					}
					return sb.toString();
				} if (levels.get(i+1) != currentScope.levels.get(i+1) || 
					  !qualifiers.get(i).equals(currentScope.qualifiers.get(i))) {
					for (int j = i; j < qualifiers.size(); j++) {
						if (qualifiers.get(j).equals("Main") ||
							qualifiers.get(j).equals("ExpandingMemoryPolynomialFilter") ||
							qualifiers.get(j).equals("FadingMemoryPolynomialFilter") )
							continue;
						sb.append(qualifiers.get(j));
						sb.append("/");
					}
					return sb.toString();					
				}
			}
			return "";
		}
		
	}