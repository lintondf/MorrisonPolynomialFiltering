package com.bluelightning.tools.transpiler;

import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

class SymbolTable {
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

		protected Map<String, Map<String, Symbol> > table = new HashMap<>();
		
		public String toString() {
			StringBuffer sb = new StringBuffer();
			for (String name : table.keySet()) {
				sb.append( String.format("  {%s}\n", name) );
				Map<String, Symbol> aliases = table.get(name);
				for (String scope : aliases.keySet()) {
					sb.append( String.format("    {%s}\n", scope.toString() ));
					sb.append( String.format("      {%s}\n", aliases.get(scope).toString()));
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
			return symbol;
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
	}