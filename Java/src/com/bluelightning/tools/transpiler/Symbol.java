package com.bluelightning.tools.transpiler;

import java.util.ArrayList;
import java.util.List;

class Symbol {
	
	public static class SuperClassInfo {
		public String superClass;
		
		public SuperClassInfo() {
			superClass = "";
		}
	}
	
	public static class FunctionParametersInfo {
		public List<Symbol> parameters;
		
		public FunctionParametersInfo() {
			parameters = new ArrayList<>();
		}
	}
	
	protected String name;
	protected String type;
	protected Scope  scope;
	protected SuperClassInfo superClassInfo = null;
	protected FunctionParametersInfo functionParametersInfo = null;
	
	public String toString() {
		String r = String.format("%s : %s", name, type );
		if  (superClassInfo != null) {
			r += "(" +  superClassInfo.superClass + ")";
		}
		if (functionParametersInfo != null) {
			r += "(";
			for (Symbol parameter : functionParametersInfo.parameters) {
				r += parameter.toString();
				r += ",";
			}
			r += ")";
		}
		return r;
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

	public SuperClassInfo getSuperClassInfo() {
		return superClassInfo;
	}

	public void setSuperClassInfo(SuperClassInfo superClassInfo) {
		this.superClassInfo = superClassInfo;
	}

	public FunctionParametersInfo getFunctionParametersInfo() {
		return functionParametersInfo;
	}

	public void setFunctionParametersInfo(FunctionParametersInfo functionParametersInfo) {
		this.functionParametersInfo = functionParametersInfo;
	}
}