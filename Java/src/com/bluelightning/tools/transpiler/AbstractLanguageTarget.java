/** TODO
 * ** Languages
 * 1. C++/Eigen
 * 2. Java/EJML
 * 3. CUDA
 * 4. Julia
 * 5. Rust
 * 6. Go
 * 7. C? de'classify' from transpiler? -> OpenCL kernels
 * 
 */
package com.bluelightning.tools.transpiler;

import java.util.Set;
import java.util.TreeSet;

import com.bluelightning.tools.transpiler.nodes.TranslationListNode;
import com.bluelightning.tools.transpiler.nodes.TranslationNode;
import com.bluelightning.tools.transpiler.nodes.TranslationOperatorNode;
import com.bluelightning.tools.transpiler.nodes.TranslationSubexpressionNode;
import com.bluelightning.tools.transpiler.nodes.TranslationSymbolNode;
import com.bluelightning.tools.transpiler.nodes.TranslationUnaryNode;

/**
 * @author NOOK
 *
 */
public abstract class AbstractLanguageTarget implements ILanguageTarget {

	protected int id;
	protected Set<String> ignoredSuperClasses = new TreeSet<>();
	
	
	
	public AbstractLanguageTarget() {
		ignoredSuperClasses.add("ABC");
				
	}

	protected boolean isList(TranslationNode root) {
		return (root instanceof TranslationListNode);
	}

	protected boolean isOperator(TranslationNode root, String op) {
		if (root instanceof TranslationOperatorNode) {
			return ((TranslationOperatorNode) root).getOperator().equals(op);
		}
		return false;
	}

	protected boolean isSymbol(TranslationNode root) {
		return (root instanceof TranslationSymbolNode);
	}
	
	protected String getAssignmentTargetType( TranslationNode child ) {
		if (child.getTop() instanceof TranslationSubexpressionNode) {
			TranslationSubexpressionNode top = (TranslationSubexpressionNode) child.getTop();
			if (top.getChildCount() > 2) {
				if (top.getChild(1) instanceof TranslationOperatorNode) {
					if (((TranslationOperatorNode)top.getChild(1)).getOperator().equals("=")) {
						TranslationNode lhs = top.getChild(0);
						while (lhs.getChildCount() > 0 &&
							   lhs instanceof TranslationSubexpressionNode) {
							lhs = lhs.getChild(0);
						}
						if (lhs instanceof TranslationSymbolNode) {
							Symbol s = ((TranslationSymbolNode) lhs).getSymbol();
							if (s.getName().equals("self")) {
								TranslationNode u = lhs.getRightSibling();
								if (u instanceof TranslationUnaryNode) {
									return ((TranslationUnaryNode) u).getType();
								} else {
									return s.getType();
								}
							} else {
								return s.getType();
							}
						}
					}
				}
			}
		}
		return child.getTop().getType();
	}
	
	
	@Override
	public void setId(int id) {
		this.id = id;
	}

	@Override
	public int getId() {
		return id;
	}


	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#addImport(com.bluelightning.tools.transpiler.Scope)
	 */
	@Override
	public void addImport(Scope scope) {
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#startModule(com.bluelightning.tools.transpiler.Scope)
	 */
	@Override
	public void startModule(Scope scope, boolean headerOnly, boolean isTest) {
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#finishModule()
	 */
	@Override
	public void finishModule() {
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#startClass(com.bluelightning.tools.transpiler.Scope)
	 */
	@Override
	public void startClass(Scope scope) {
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#finishClass(com.bluelightning.tools.transpiler.Scope)
	 */
	@Override
	public void finishClass(Scope scope) {
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#startMethod(com.bluelightning.tools.transpiler.Scope)
	 */
	@Override
	public void startMethod(Scope scope) {
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#finishMethod(com.bluelightning.tools.transpiler.Scope)
	 */
	@Override
	public void finishMethod(Scope scope) {
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#emitSymbolDeclaration(com.bluelightning.tools.transpiler.Symbol)
	 */
	@Override
	public void emitSymbolDeclaration(Symbol symbol, String comment) {
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#emitElifStatement(com.bluelightning.tools.transpiler.Scope, com.bluelightning.tools.transpiler.nodes.TranslationNode)
	 */
	@Override
	public void emitElifStatement(Scope scope, TranslationNode expressionRoot) {
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#emitElseStatement()
	 */
	@Override
	public void emitElseStatement() {
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#emitExpressionStatement(com.bluelightning.tools.transpiler.Scope, com.bluelightning.tools.transpiler.nodes.TranslationNode)
	 */
	@Override
	public void emitExpressionStatement(Scope scope, TranslationNode root) {
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#emitIfStatement(com.bluelightning.tools.transpiler.Scope, com.bluelightning.tools.transpiler.nodes.TranslationNode)
	 */
	@Override
	public void emitIfStatement(Scope scope, TranslationNode expressionRoot) {
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#emitForStatement(com.bluelightning.tools.transpiler.Symbol, com.bluelightning.tools.transpiler.nodes.TranslationNode)
	 */
	@Override
	public void emitForStatement(Symbol symbol, TranslationNode expressionRoot) {
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#emitNewExpression(com.bluelightning.tools.transpiler.Scope, java.lang.String, com.bluelightning.tools.transpiler.nodes.TranslationNode)
	 */
	@Override
	public void emitNewExpression(Scope scope, String className, TranslationNode root) {
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#emitRaiseStatement(java.lang.String)
	 */
	@Override
	public void emitRaiseStatement(String exception) {
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#emitReturnStatement()
	 */
	@Override
	public void emitReturnStatement() {
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#emitSubExpression(com.bluelightning.tools.transpiler.Scope, com.bluelightning.tools.transpiler.nodes.TranslationNode)
	 */
	@Override
	public void emitSubExpression(Scope scope, TranslationNode root) {
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#finishStatement()
	 */
	@Override
	public void finishStatement() {
	}

	/* (non-Javadoc)
	 * @see com.bluelightning.tools.transpiler.ILanguageTarget#closeBlock()
	 */
	@Override
	public void closeBlock() {
	}

}
