package com.bluelightning.tools.transpiler;

import java.util.HashMap;
import java.util.Map;

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

		protected Map<String, Map<Scope, Symbol> > table = new HashMap<>();
		
		public String toString() {
			StringBuffer sb = new StringBuffer();
			for (String name : table.keySet()) {
				sb.append( String.format("  '%s'\n", name) );
				Map<Scope, Symbol> aliases = table.get(name);
				for (Scope scope : aliases.keySet()) {
					sb.append( String.format("    %s\n", scope.toString() ));
					sb.append( String.format("      '%s'\n", aliases.get(scope).toString()));
				}
			}
			return sb.toString();
		}
		
		public void add( Scope scope, String name, String type ) {
			Map<Scope, Symbol> aliases = table.get(name);
			if (aliases == null) {
				aliases = new HashMap<>();
			}
			Symbol symbol = new Symbol( scope, name.trim(), type.trim());
			aliases.put( scope, symbol ); //TODO collisions
			table.put(name.trim(),  aliases);
		}
		
		public Symbol lookup( Scope scope, String name ) {
			Map<Scope, Symbol> aliases = table.get(name);
			if (aliases == null) {
//				System.out.println("Unknown: {" + name + "}" );
				return null;
			}
			Symbol symbol = null;
			while (scope != null) {
				symbol = aliases.get(scope);
				if (symbol != null)
					return symbol;
				scope = scope.getParent();
			}
			return null;
		}
	}