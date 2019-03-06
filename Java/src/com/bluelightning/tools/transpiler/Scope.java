package com.bluelightning.tools.transpiler;

import java.util.HashMap;
import java.util.List;


public class Scope {
	
		protected static HashMap<String, Scope> scopeMap = new HashMap<>();
		
		public static Scope getExistingScope( String qString ) {
			return scopeMap.get(qString);
		}
		
		protected String[] qualifiers; // e.g. com.bluelightning.Filtering
		public enum Level {
			IMPORT, MODULE, FUNCTION, CLASS, MEMBER,
		};
		protected Level  level;
		protected String qString;
		
		public Scope() {
			level = Level.IMPORT;
			this.qualifiers = new String[] {""};
			this.qString = "/";
			scopeMap.put(this.qString, this);
		}
		
		public Scope( Scope.Level level, List<String> qualifiers) {
			this.level = level;
			this.qualifiers = qualifiers.toArray( new String[qualifiers.size()] );
			StringBuffer sb = new StringBuffer();
			for (String name : qualifiers) {
				sb.append(name);
				sb.append('/');
			}
			qString = sb.toString();			
			scopeMap.put(this.qString, this);
		}
		
		public String getLast() {
			return qualifiers[ qualifiers.length-1 ];
		}
		
		public Scope getChild( Scope.Level childLevel, String childName ) {
//			System.out.println( this.toString() );
			Scope scope = new Scope();
			switch (level) {
			case IMPORT:
				switch (childLevel) {
				case MODULE:
					scope.level = childLevel;
					break;
				default:
					return null;
				}
				break; 
				
			case MODULE: 
				switch (childLevel) {
				case MODULE: 
				case FUNCTION:
				case CLASS:
					scope.level = childLevel;
					break;
				default:
					return null;
				}
				break; 
			case FUNCTION:
				return null;
			case CLASS:
				if (childLevel == Level.FUNCTION)
					scope.level = Level.MEMBER;
				else
					return null;
				break;
			case MEMBER:
				return null;
			}	
//			if (childName.equals(qualifiers[qualifiers.length-1])) {
//				System.err.println("Double Qualifiers: " + this.toString() + " + " + childName );
//			}
			scope.qualifiers = new String[this.qualifiers.length+1];
			StringBuffer sb = new StringBuffer();
			for (int i = 0; i < qualifiers.length; i++) {
				sb.append(qualifiers[i]);
				sb.append('/');
				scope.qualifiers[i] = qualifiers[i];
			}
			sb.append(childName);
			sb.append('/');
			scope.qualifiers[this.qualifiers.length] = childName;
			scope.qString = sb.toString();			
			scopeMap.put(scope.qString, scope);
			return scope;
		}
		
		public Scope getParent() {
			Scope scope = new Scope();
			switch (level) {
			case IMPORT:
				return null;
			case MODULE:
				scope.level = Level.MODULE;
				break;
			case FUNCTION:
				scope.level = Level.MODULE;
				break;
			case CLASS:
				scope.level = Level.MODULE;
				break;
			case MEMBER:
				scope.level = Level.CLASS;
				break;
			}
			if (this.qualifiers.length == 0)
				return null;
			scope.qualifiers = new String[this.qualifiers.length-1];
			StringBuffer sb = new StringBuffer();
			for (int i = 0; i < scope.qualifiers.length; i++) {
				sb.append(qualifiers[i]);
				sb.append('/');
				scope.qualifiers[i] = qualifiers[i];
			}
			scope.qString = sb.toString();			
			scopeMap.put(scope.qString, scope);
			return scope;
		}
		
		@Override
		public String toString() {
			return qString;
		}

		public Scope.Level getLevel() {
			return level;
		}

		public int getLevelCount() {
			return qualifiers.length;
		}
		
		public String getLevel(int level) {
			return qualifiers[level];
		}
		
	}