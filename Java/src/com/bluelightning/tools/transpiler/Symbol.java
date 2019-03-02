package com.bluelightning.tools.transpiler;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;

class Symbol {
	
	public static class SuperClassInfo {
		public String superClass;
		
		public SuperClassInfo() {
			superClass = "";
		}
	}
	
	public static class FunctionParametersInfo {
		public List<Symbol> parameters;
		public Set<String>  decorators;
		
		public FunctionParametersInfo() {
			parameters = new ArrayList<>();
			decorators = new TreeSet<>();
		}
		
		public String toString() {
			StringBuilder sb = new StringBuilder();
			for (Symbol parameter : parameters) {
				sb.append( parameter.toString() );
				sb.append( "," );
			}
			sb.append( " | ");
			for (String dec : decorators) {
				sb.append(dec);
				sb.append(";");
			}
			return sb.toString();
		}
	}
	
	protected String name;
	protected String type;
	protected Scope  scope;
	protected SuperClassInfo superClassInfo = null;
	protected FunctionParametersInfo functionParametersInfo = null;
	
	public String toString() {
		String r = String.format("%s::%s : %s", scope.toString(), name, type );
		if  (superClassInfo != null) {
			r += "; supers(" +  superClassInfo.superClass + ")";
		}
		if (functionParametersInfo != null) {
			r += "; params(";
			r += functionParametersInfo.toString();
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
		if (superClassInfo.superClass.equals("Enum")) {
			type = "<ENUM>";
		}
	}

	public FunctionParametersInfo getFunctionParametersInfo() {
		return functionParametersInfo;
	}

	public void setFunctionParametersInfo(FunctionParametersInfo functionParametersInfo) {
		this.functionParametersInfo = functionParametersInfo;
	}
}