package com.bluelightning.tools.transpiler;

class Symbol {
	protected String name;
	protected String type;
	protected Scope  scope;
	
	public String toString() {
		return String.format("%s : %s", name, type );
	}
	
	public Symbol( Scope scope, String name, String type ) {
		this.name = name;
		this.type = type;
		this.scope = scope;
	}

	public String getName() {
		return name;
	}

	public String getType() {
		return type;
	}

	public Scope getScope() {
		return scope;
	}
}