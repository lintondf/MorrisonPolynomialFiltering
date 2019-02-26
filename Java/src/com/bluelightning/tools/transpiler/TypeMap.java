/**
 * 
 */
package com.bluelightning.tools.transpiler;

/**
 * @author NOOK
 *
 */
public class TypeMap {
	
	public interface Type {
		public String getName();
		public enum BaseKind {
			INTEGER, FLOAT, STRING, CLASS
		};
		public BaseKind getBaseKind();
		public String getClassName();
	}
}
