package com.bluelightning.tools.transpiler;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;

import com.bluelightning.tools.transpiler.Symbol.FunctionParametersInfo;

public class Symbol {
	
	public static class SuperClassInfo {
		public ArrayList<String> superClasses;
		
		public SuperClassInfo() {
			superClasses = new ArrayList<>();
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
	protected String initialization;
	protected boolean isForVariable;
	protected SuperClassInfo superClassInfo = null;
	protected FunctionParametersInfo functionParametersInfo = null;
	protected Symbol ancestor = null;
	protected String[] dimensions;
	protected boolean isClassRef = false;
	protected boolean isInherited = false;
	protected boolean isReturnVariable = false;
	protected boolean isAbstractClass = false;
	protected boolean isStatic = false;
	
	public boolean isInherited() {
		return isInherited;
	}

	public void setInherited(boolean isInherited) {
		this.isInherited = isInherited;
	}

	public Symbol inherit( Scope heir ) {
		Symbol that = new Symbol( heir, this.name, this.type );
		that.initialization = this.initialization;
		that.superClassInfo = this.superClassInfo;
		that.functionParametersInfo = this.functionParametersInfo;
		that.ancestor = this;
		that.isInherited = true;
		this.setStatic( this.isStatic() );
		return that;
	}
	
	public String toString() {
		String r = String.format("%s::%s : %s", scope.toString(), name, type );
		if  (superClassInfo != null) {
			r += "; supers(";
			for (String sc : superClassInfo.superClasses) {
				r += sc;
				r += ",";
			}
			r += ")";
		}
		if (functionParametersInfo != null) {
			r += "; params(";
			r += functionParametersInfo.toString();
			r += ")";
		}
		if (isClassRef)
			r += " ClassRef; ";
		if (isInherited)
			r += " INHERITED; ";
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
		if (superClassInfo.superClasses.contains("Enum")) {
			type = "<ENUM>";
		}
	}

	public FunctionParametersInfo getFunctionParametersInfo() {
		return functionParametersInfo;
	}

	public void setFunctionParametersInfo(FunctionParametersInfo functionParametersInfo) {
		this.functionParametersInfo = functionParametersInfo;
	}
	
	public Symbol getBaseSymbol() {
		if (this.isInherited) {
			Symbol current = this;
			while (current.ancestor != null)
				current = current.ancestor;
			return current;			
		}
		return null;
	}

	public boolean isStatic() {
		Symbol base = getBaseSymbol();
		if (base != null) {
			return base.isStatic;
		}
		return isStatic;
	}

	public void setStatic(boolean isStatic) {
		this.isStatic = isStatic;
	}

	public void setInitialization(String initialization) {
		this.initialization = initialization;
	}
	
	public String getInitialization() {
		return this.initialization;
	}

	public boolean isForVariable() {
		return isForVariable;
	}

	public void setForVariable(boolean isForVariable) {
		this.isForVariable = isForVariable;
	}

	public Symbol getAncestor() {
		return ancestor;
	}

	public boolean isClass() {
		return type.equals("<CLASS>") || type.equals("<ENUM>");
	}
	
	public boolean isEnum() {
		return type.equals("<ENUM>");
	}

	public boolean isPrivate() {
		if (name.startsWith("__init__"))
			return false;
		return name.startsWith("_");
	}
	
	public boolean isClassMethod() {
		if (this.functionParametersInfo == null)
			return false;
		return this.functionParametersInfo.decorators.contains("@classmethod");
	}

	public void setDimensions(String[] dims) {
		this.dimensions = dims;
	}
	
	public String[] getDimensions() {
		return this.dimensions;
	}

	public boolean isClassReference() {
		return this.isClassRef;
	}
	
	public void setClassReference( boolean tf) {
		this.isClassRef = tf;
	}
	
	public boolean isConstructor() {
		if (this.getName().equals("__init__"))
			return true;
		return this.hasDecorator("@constructor");
	}

	public boolean hasDecorator(String string) {
		if (this.functionParametersInfo == null)
			return false;
		if (this.functionParametersInfo.decorators == null || this.functionParametersInfo.decorators.isEmpty())
			return false;
		return this.functionParametersInfo.decorators.contains(string);
	}

	/**
	 * @return the isReturnVariable
	 */
	public boolean isReturnVariable() {
		return isReturnVariable;
	}

	/**
	 * @param isReturnVariable the isReturnVariable to set
	 */
	public void setReturnVariable(boolean isReturnVariable) {
		this.isReturnVariable = isReturnVariable;
	}

	/**
	 * @return the isAbstractClass
	 */
	public boolean isAbstractClass() {
		return isAbstractClass;
	}

	/**
	 * @param isAbstractClass the isAbstractClass to set
	 */
	public void setAbstractClass(boolean isAbstractClass) {
		this.isAbstractClass = isAbstractClass;
	}

	public boolean isFunction() {
		return getFunctionParametersInfo() != null;
	}
	
	public void setFunction(boolean tf) {
		if (tf) {
			this.setFunctionParametersInfo(new Symbol.FunctionParametersInfo());
		} else {
			this.setFunctionParametersInfo(null);
		}
	}
}