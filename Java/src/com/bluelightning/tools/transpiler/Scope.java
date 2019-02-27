package com.bluelightning.tools.transpiler;

import java.util.List;


class Scope {
		protected String[] qualifiers; // e.g. com.bluelightning.Filtering
		public enum Level {
			MODULE, FUNCTION, CLASS, MEMBER,
		};
		protected Scope.Level  level;
		protected String qString;
		
		protected Scope() {}
		
		public Scope( Scope.Level level, List<String> qualifiers) {
			this.level = level;
			this.qualifiers = qualifiers.toArray( new String[qualifiers.size()] );
			StringBuffer sb = new StringBuffer();
			for (String name : qualifiers) {
				sb.append(name);
				sb.append('/');
			}
			qString = sb.toString();			
		}
		
		public String getLast() {
			return qualifiers[ qualifiers.length-1 ];
		}
		
		public Scope getChild( Scope.Level childLevel, String childName ) {
//			System.out.println( this.toString() );
			Scope scope = new Scope();
			switch (level) {
			case MODULE: 
				switch (childLevel) {
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
			return scope;
		}
		
		public Scope getParent() {
			Scope scope = new Scope();
			switch (level) {
			case MODULE:
				return null;
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
			scope.qualifiers = new String[this.qualifiers.length-1];
			StringBuffer sb = new StringBuffer();
			for (int i = 0; i < scope.qualifiers.length; i++) {
				sb.append(qualifiers[i]);
				sb.append('/');
				scope.qualifiers[i] = qualifiers[i];
			}
			scope.qString = sb.toString();			
			return scope;
		}
		
		@Override
		public String toString() {
			return qString;
		}
		
	}