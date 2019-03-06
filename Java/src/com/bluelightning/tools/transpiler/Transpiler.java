/** Polynomial Filtering Universal Transpiler
 * SPDX-License-Identifier: MIT
 *
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 */
package com.bluelightning.tools.transpiler;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.Writer;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonToken;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.ParserRuleContext;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeListener;
import org.antlr.v4.runtime.tree.ParseTreeWalker;
import org.antlr.v4.runtime.tree.RuleNode;
import org.antlr.v4.runtime.tree.TerminalNode;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.bluelightning.tools.transpiler.antlr4.LcdPythonBaseListener;
import com.bluelightning.tools.transpiler.antlr4.LcdPythonBaseVisitor;
import com.bluelightning.tools.transpiler.antlr4.LcdPythonLexer;
import com.bluelightning.tools.transpiler.antlr4.LcdPythonParser;
import com.bluelightning.tools.transpiler.nodes.TranslationNode;
import com.bluelightning.tools.transpiler.nodes.TranslationUnaryNode;
import com.bluelightning.tools.transpiler.programmer.BoostProgrammer;
import com.bluelightning.tools.transpiler.programmer.EigenProgrammer;

import freemarker.core.PlainTextOutputFormat;
import freemarker.template.Configuration;
import freemarker.template.Template;
import freemarker.template.TemplateException;
import freemarker.template.TemplateExceptionHandler;


/**
 * @author NOOK
 *
 */
public class Transpiler {
	
	public static class Target {
		public Path  dir;
		public String module;
		
		public Target( Path dir, String module ) {
			this.dir = dir;
			this.module = module;
		}
	}
	
	static Target[] targets = {
		//new Target(Paths.get(""), "TranspilerTest"),
		new Target(Paths.get("PolynomialFiltering"), "Main"),
//		new Target(Paths.get("PolynomialFiltering/Components"), "FixedMemoryPolynomialFilter"),
		new Target(Paths.get("PolynomialFiltering/Components"), "IRecursiveFilter"),
//		new Target(Paths.get("PolynomialFiltering/Components"), "ExpandingMemoryPolynomialFilter"),
	};
	
	protected Logger logger;
	
	protected StringBuffer errorReport = new StringBuffer();
	
	public void reportError(ParserRuleContext context, String message ) {
		reportError( context.start, message );
	}
	
	public void reportError(Token token, String message ) {
		String r = String.format("ERROR [L%5d:C%3d]: %s", token.getLine(), token.getCharPositionInLine(), message );
		reportError(r);
	}
	
	public void reportError(String r) {
		System.out.println("!!!!!!!!!!!!!! " + r );
		errorReport.append(r);
		errorReport.append('\n');
	}


	public void dumpChildren( RuleNode ctx ) {
		dumpChildren( ctx, 0 );
	}
	
	public void dumpChildren( RuleNode ctx, int indent ) {
		if (ctx.getChildCount() == 1) {
			if (ctx.getChild(0) instanceof RuleNode)
				dumpChildren( (RuleNode) ctx.getChild(0), indent+1 );
		} else {
			//parser.getRuleIndexMap().get(ctx.getRuleContext().getRuleIndex());
			System.out.println(StringUtils.repeat("  ", indent) + parser.getRuleNames()[ctx.getRuleContext().getRuleIndex()].toUpperCase() + " "
					+ ctx.getChildCount() ); // + " " + ctx.getText());
			for (int i = 0; i < ctx.getChildCount(); i++) {
				System.out.printf("%s%10d: %-30s %s\n", StringUtils.repeat("  ", indent), i,
						ctx.getChild(i).getPayload().getClass().getSimpleName(),
						valueMap.get(ctx.getChild(i).getPayload()));
				if (indent > 0) {
					if (ctx.getChild(i) instanceof RuleNode)
						dumpChildren( (RuleNode) ctx.getChild(i), indent+1 );
				}
			}
		}
	}
	
	protected Map<Object, String> valueMap = new HashMap<>();
	
	public String getValue( Object payload ) {
		return valueMap.get(payload);
	}
	
	protected Scope moduleScope = null;
	protected Map<Object, Scope> scopeMap = new HashMap<>();
	
	protected SymbolTable symbolTable = new SymbolTable(this);
	
	public Symbol lookup( Scope scope, String name ) {
		return symbolTable.lookup(scope, name);
	}

	protected void processDeclaration(Token token, Scope scope, String str) {
		String[] fields = str.split(":");
		if (fields.length == 2) {
			symbolTable.add(scope, fields[0], fields[1]);
//			System.out.println("DECLARED: " + str);
		} else {
			reportError(token, "bad declaration syntax");
		}
	}
	
	protected Configuration configure() throws IOException, TemplateException {
		Configuration cfg = new Configuration(Configuration.VERSION_2_3_27);
	
		// Specify the source where the template files come from. Here I set a
		// plain directory for it, but non-file-system sources are possible too:
		cfg.setDirectoryForTemplateLoading(new File("../Java/data/templates"));
	
		// Set the preferred charset template files are stored in. UTF-8 is
		// a good choice in most applications:
		cfg.setDefaultEncoding("UTF-8");
	
		// Sets how errors will appear.
		cfg.setTemplateExceptionHandler(TemplateExceptionHandler.RETHROW_HANDLER);
	
		// Don't log exceptions inside FreeMarker that it will thrown at you anyway:
		cfg.setLogTemplateExceptions(false);
	
		// Wrap unchecked exceptions thrown during template processing into TemplateException-s.
		cfg.setWrapUncheckedExceptions(true);	
		
		cfg.setRecognizeStandardFileExtensions(false);
		
		cfg.setWhitespaceStripping(false);
		
		cfg.setOutputFormat(PlainTextOutputFormat.INSTANCE);
		return cfg;
	}

	protected class TargetDispatcher implements ILanguageTarget {
		
		List<ILanguageTarget> targets = new ArrayList<>();
		
		public TargetDispatcher() {}
		
		public void addTarget( ILanguageTarget target ) {
			target.setId( targets.size() );
			targets.add(target);
		}

		@Override
		public void startModule(Scope scope) {
			for (ILanguageTarget target : targets) {
				target.startModule(scope);
			}
		}

		@Override
		public void startClass(Scope scope) {
			for (ILanguageTarget target : targets) {
				target.startClass(scope);
			}
		}

		@Override
		public void finishClass(Scope scope) {
			for (ILanguageTarget target : targets) {
				target.finishClass(scope);
			}
		}

		@Override
		public void startMethod(Scope scope) {
			for (ILanguageTarget target : targets) {
				target.startMethod(scope);
			}
		}

		@Override
		public void finishMethod(Scope scope) {
			for (ILanguageTarget target : targets) {
				target.finishMethod(scope);
			}
		}

		@Override
		public void emitExpressionStatement(Scope scope, TranslationNode root) {
			for (ILanguageTarget target : targets) {
				target.emitExpressionStatement(scope, root);
			}
		}

		@Override
		public void finishModule() {
			for (ILanguageTarget target : targets) {
				target.finishModule();
			}
		}

		@Override
		public void setId(int id) {
		}

		@Override
		public int getId() {
			return 0;
		}

		@Override
		public void emitSymbolDeclaration(Symbol symbol) {
			for (ILanguageTarget target : targets) {
				target.emitSymbolDeclaration(symbol);
			}
		}

		public void emitReturnStatement() {
			for (ILanguageTarget target : targets) {
				target.emitReturnStatement();
			}
		}

		@Override
		public void emitSubExpression(Scope scope, TranslationNode root) {
			for (ILanguageTarget target : targets) {
				target.emitSubExpression(scope, root);
			}
		}

		@Override
		public void emitCloseStatement() {
			for (ILanguageTarget target : targets) {
				target.emitCloseStatement();
			}
		}

		@Override
		public void closeBlock() {
			for (ILanguageTarget target : targets) {
				target.closeBlock();
			}
		}

		@Override
		public void emitForStatement(Symbol symbol, TranslationNode expressionRoot) {
			for (ILanguageTarget target : targets) {
				target.emitForStatement( symbol, expressionRoot);
			}
		}
		
	}

	protected TargetDispatcher dispatcher = new TargetDispatcher();
	
	/**
	 * LcdPythonPopulateListener - fully populates the value map.
	 */
	protected class PopulateListener extends LcdPythonBaseListener {
		@Override
		public void exitEveryRule(ParserRuleContext ctx) {
			if (parser.getRuleNames()[ctx.getRuleIndex()].equals("trailer")) {
				int limit = ctx.getChildCount();
				CommonToken token = (CommonToken) ctx.getChild(0).getPayload();
				valueMap.put(ctx.getChild(0).getPayload(), token.getText());
				switch (token.getText()) {
				case "[":
					limit--;
					valueMap.put(ctx.getChild(limit).getPayload(), ((CommonToken)ctx.getChild(limit).getPayload()).getText());
					break;
				case "(":
					limit--;
					valueMap.put(ctx.getChild(limit).getPayload(), ((CommonToken)ctx.getChild(limit).getPayload()).getText());
					break;
				case ".":
					break;
				}
				for (int i = 1; i < limit; i++) {
					if (ctx.getChild(i).getPayload() instanceof CommonToken) {
						valueMap.put(ctx.getChild(i).getPayload(), ((CommonToken)ctx.getChild(i).getPayload()).getText());
					} else {
						String value = valueMap.get(ctx.getChild(i).getPayload());
						valueMap.put(ctx.getChild(i).getPayload(), value );
					}
				}
				valueMap.put(ctx.getPayload(), ctx.getText() );
				return;
			}
			StringBuffer result = new StringBuffer();
			for (int i = 0; i < ctx.getChildCount(); i++) {
				ParseTree child = ctx.getChild(i);
				if (child.getPayload() instanceof CommonToken) {
					result.append(child.getText());
//					System.out.println( child.getText() + " : " + child.toStringTree(parser));
					valueMap.put(child.getPayload(), child.getText());
				} else {
					result.append(valueMap.get(child.getPayload()));
				}
				//result.append(' ');
			} 
			//System.out.println( result.toString() + " : " + parser.getRuleNames()[ctx.getRuleIndex()] + " / " + ctx.toStringTree(parser));
			valueMap.put(ctx.getPayload(), result.toString());
		}
	}

	

	protected String content;
	protected LcdPythonParser parser;
	
	protected Configuration cfg;
	
	private static Transpiler singleton = null;

	public ParseTreeWalker walker;
	
	public static Transpiler instance() { 
		return singleton;
	}

	public Transpiler() {
		singleton = this;
		
		logger = LoggerFactory.getLogger("com.bluelightning.Transpiler");
		logger.info("--------->Transpiler");
		
		try {
			cfg = configure();
		} catch (IOException | TemplateException e) {
			e.printStackTrace();
		}
		
//		dispatcher.addTarget( new CppTarget(new BoostProgrammer(), 
//				cfg, Paths.get("../Cpp/Boost/") ) );
		dispatcher.addTarget( new CppTarget(new EigenProgrammer(), 
				cfg, Paths.get("../Cpp/Eigen/") ) );

		Scope importScope = new Scope();
		symbolTable.add( importScope, "copy", "array");
		symbolTable.add( importScope, "eye", "array");
		symbolTable.add( importScope, "ones", "array");
		symbolTable.add( importScope, "inv", "array" );
		symbolTable.add( importScope, "pow", "float");
		symbolTable.add( importScope, "range", "range");
		symbolTable.add( importScope, "shape", "dimensions");
		symbolTable.add( importScope, "solve", "array");
		symbolTable.add( importScope, "super", "super" );
		symbolTable.add( importScope, "transpose", "array");
		symbolTable.add( importScope, "zeros", "array");
		symbolTable.add( importScope, "NotImplementedError", "exception");
		
		valueMap.put( TranslationUnaryNode.staticFieldReference, "::");

	}
	
	public void compile(Path where, List<String> dottedModule) {
		
		String module = dottedModule.get(dottedModule.size()-1);
		try {
			byte[] bytes = Files.readAllBytes(where.resolve(module + ".py"));
			content = new String(bytes, "UTF-8");
		} catch (Exception x) {
			x.printStackTrace();
			return;
		}
		
		Scope importScope = new Scope();
		moduleScope = importScope;
		for (String dot : dottedModule) {
			moduleScope = moduleScope.getChild(Scope.Level.MODULE, dot );
		}
		dispatcher.startModule(moduleScope);
		
		LcdPythonLexer java8Lexer = new LcdPythonLexer(CharStreams.fromString(content));
		CommonTokenStream tokens = new CommonTokenStream(java8Lexer);
		parser = new LcdPythonParser(tokens);
		ParseTree tree = parser.file_input();
		
		// PASS 1 - fully populate parse tree contents map
		PopulateListener populateListener = new PopulateListener();
		walker = new ParseTreeWalker();
		walker.walk(populateListener, tree);
		
		// PASS 2 - handle all imports, variable, function, and class declarations
		DeclarationsListener declarationsListener = new DeclarationsListener(this, moduleScope);
		walker.walk(declarationsListener, tree);
		try {
			PrintWriter sym = new PrintWriter("out/symbols.txt");
			sym.println("\n\n-------------------------------------");
			sym.println("--SYMBOL TABLE\n");
			sym.println( symbolTable.toString() );
			sym.println("\n\n-------------------------------------");
			sym.close();
		} catch (Exception x) {
			x.printStackTrace();
		}
		
		ExpressionCompilationListener expressionCompilationListener = new ExpressionCompilationListener(this);
		walker.walk(expressionCompilationListener, tree);

		dispatcher.finishModule();
		
		if (errorReport.length() > 0) {
			System.err.println("\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n");
			System.err.println(errorReport.toString());
		} else {
			System.out.println("\n\nNO ERRORS");
		}
		
	}

	protected static void compileGrammar(String libPath, String gPath, String outPath) {
		File file = new File(".");
		String lwd = file.getAbsolutePath();
		System.setProperty("user.dir", libPath);

		// org.antlr.v4.Tool.main( new String[]{} ); // always show help
		String[] args = { "-lib", libPath, "-o", outPath, "-package", "com.bluelightning.tools.antlr4", "-listener",
				"-visitor", gPath };
		org.antlr.v4.Tool.main(args); // new String[]{} );
		System.setProperty("user.dir", lwd);
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		Transpiler transpiler = new Transpiler();
		
		Path base = Paths.get("../Python/src");
		for (Target target : targets) {
			Path where = base;
			ArrayList<String> dottedModule = new ArrayList<>();
			for (int i = 0; i < target.dir.getNameCount(); i++) {
				if (! target.dir.getName(i).toString().isEmpty()) {
					dottedModule.add( target.dir.getName(i).toString());
					where = where.resolve(target.dir.getName(i).toString());
				}
			}
			dottedModule.add(target.module);
			transpiler.compile( where, dottedModule);
		}
	}


}
