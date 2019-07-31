package com.bluelightning.tools.transpiler;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import com.bluelightning.tools.transpiler.Scope.Level;

import java.util.TreeMap;

public class SymbolTable {
		/**
		 * 
		 */
		private final Transpiler transpiler;

		/**
		 * @param transpiler
		 */
		SymbolTable(Transpiler transpiler) {
			this.transpiler = transpiler;
		}

		protected Map<String, Map<String, Symbol> > table = new TreeMap<>();
		
		public String toString() {
			StringBuffer sb = new StringBuffer();
			for (String name : table.keySet()) {
				sb.append( String.format("  {%s}\n", name) );
				Map<String, Symbol> aliases = table.get(name);
				for (String scope : aliases.keySet()) {
					sb.append( String.format("    {%s}\n", scope.toString() ));
					sb.append( String.format("      {%s}[%s]\n", aliases.get(scope).toString(), aliases.get(scope).getScope().getLevel().toString()));
				}
			}
			return sb.toString();
		}
		
		public Symbol add( Scope scope, String name, String type ) {
			name = name.trim();
			type = type.trim();
//			System.err.println(scope + "::" + name + "+" );
			Map<String, Symbol> aliases = table.get(name);
			if (aliases == null) {
				aliases = new HashMap<>();
			}
			Symbol symbol = new Symbol( scope, name, type);
			aliases.put( scope.toString(), symbol ); //TODO collisions
			table.put(name,  aliases);
//			System.err.println(lookup(scope,name));
			transpiler.valueMap.put(symbol, name );
			return symbol;
		}
		
		public Symbol inherit( Symbol base, Scope scope ) {
//			System.out.println("inherit: " + base.toString());
//			System.out.println("         " + scope.toString());
			Symbol i = base.inherit(scope);
			Map<String, Symbol> aliases = table.get(i.getName());
			aliases.put( scope.toString(), i ); //TODO collisions
			table.put(i.getName(),  aliases);
			return i;
		}
		
		public Symbol lookupClass( String name ) {
			return lookupClass(name, false);
		}
		
		public Symbol lookupClass( String name, boolean orEnum ) {
			name = name.trim();
			if (name.startsWith("List[")) {
				name = name.substring(5, name.length()-1);
			}
			Map<String, Symbol> aliases = table.get(name);
			if (aliases == null) {
				return null;
			}
			Iterator<Symbol> it = aliases.values().iterator();
			while (it.hasNext()) {
				Symbol c = it.next();
				if (! c.isInherited() ) {
					if (c.isEnum())
						return (orEnum) ? c : null;
					if (c.isClass())
						return c;
					else
						return null;					
				}
			}
			return null;
		}
		
		public Symbol lookup( Scope scope, String name ) {
			name = name.trim();
//			System.err.println(scope + "::" + name + "?" );
			Map<String, Symbol> aliases = table.get(name);
			if (aliases == null) {
//				System.err.println("Unknown in any scope: {" + name + "}" );
				return null;
			}
			Symbol symbol = null;
			while (scope != null) {
				symbol = aliases.get(scope.toString());
				if (symbol != null) {
					return symbol;
				}
				scope = scope.getParent();
			}
//			System.err.println(name + " NOT FOUND ANYWHERE");
			return null;
		}
		
		public List<Symbol> atScope( Scope scope ) {
			ArrayList<Symbol> out = new ArrayList<>();
			for (Map<String, Symbol> aliases : table.values()) {
				for (String symbolScope : aliases.keySet()) {
					if (symbolScope.equals(scope.toString())) {
						out.add(aliases.get(symbolScope));
					}
				}
			}
			return out;
		}
		
		public List<Symbol> getStaticFunctions() {
			ArrayList<Symbol> out = new ArrayList<>();
			for (Map<String, Symbol> aliases : table.values()) {
				for (Symbol symbol : aliases.values()) {
					if (symbol.isFunction() && symbol.getScope().getLevel() == Scope.Level.CLASS) {
						out.add(symbol);
					}
				}
			}
			return out;			
		}
		
		private void addShorter( TreeMap<String, Symbol> map, Symbol symbol) {
			Symbol that = map.get(symbol.getName());
			if (that == null) {
				map.put(symbol.getName(), symbol);
			} else {
				if (symbol.getScope().toString().length() < that.getScope().toString().length()) {
					map.put(symbol.getName(), symbol);
				}
			}
		}
		
		public void report(Documenter documenter) {
			System.out.println("--- SYMBOL TABLE ------------------");
			System.out.println( "-- UNDOCUMENTED --\n" );
			
			TreeMap<String, Symbol> enums = new TreeMap<>();
			TreeMap<String, Symbol> classes = new TreeMap<>();
			TreeMap<String, Symbol> methods = new TreeMap<>();
			
			for (Map<String, Symbol> occurences : table.values() ) {
				for (Symbol symbol : occurences.values()) {
					if (symbol.isInherited)
						continue;
					if (symbol.isEnum()) {
//						System.out.println("ENUM " + symbol.getName() );
						addShorter(enums, symbol);
					} else if (symbol.isClass()) {
//						System.out.println("CLASS " + symbol.getName() + " " + symbol.getScope().toString() );						
						addShorter(classes, symbol);
					} else if (symbol.getFunctionParametersInfo() != null) {
						addShorter(methods, symbol);
					} else if (symbol.getScope().getLevel() == Level.CLASS) {
//						System.out.println("MEMBER: " + symbol );
					}
				}
			}
			for (String name : enums.keySet() ) {
				Symbol symbol = enums.get(name);
				Scope objectScope = symbol.scope.getChild(Level.CLASS, symbol.getName());
				if (!documenter.isDocumented(objectScope)) {
					System.out.printf("Enum %-25s ", name);
					System.out.println( documenter.isDocumented(objectScope) + " " + objectScope);
				}
			}
			for (String name : classes.keySet() ) {
				Symbol symbol = classes.get(name);
				Scope objectScope = symbol.scope.getChild(Level.CLASS, symbol.getName());
				if (!documenter.isDocumented(objectScope)) {
					System.out.printf("Class %-25s ", name);
					System.out.println( documenter.isDocumented(objectScope) + " " + objectScope);
				}
			}
			for (String name : methods.keySet() ) {
				Symbol symbol = methods.get(name);
				Scope objectScope = symbol.scope.getChild(Level.MEMBER, symbol.getName());
				if (objectScope == null) {
					objectScope = symbol.scope.getChild(Level.FUNCTION, symbol.getName());
				}
				if (!documenter.isDocumented(objectScope)) {
					System.out.printf("Member %-35s ", name);
					System.out.println( documenter.isDocumented(objectScope) + " " + objectScope);
				}
			}
		}
		
	}