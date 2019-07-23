/**
 * 
 */
package com.bluelightning.tools.transpiler.java;

import java.nio.file.Path;

import com.bluelightning.tools.transpiler.java.programmer.EjmlProgrammer;

import freemarker.template.Configuration;

/**
 * @author lintondf
 *
 */
public class JavaTestTarget extends AbstractJavaTarget {

	public JavaTestTarget(EjmlProgrammer programmer, Configuration cfg, Path baseDirectory) {
		super(programmer, cfg, baseDirectory);
	}

}
