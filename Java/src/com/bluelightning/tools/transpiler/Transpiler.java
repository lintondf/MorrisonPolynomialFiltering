/** Polynomial Filtering Universal Transpiler
 * SPDX-License-Identifier: MIT
 *
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 */
package com.bluelightning.tools.transpiler;

import java.io.File;
import java.io.IOException;
import java.io.OutputStreamWriter;
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

import com.bluelightning.tools.transpiler.antlr4.LcdPythonBaseListener;
import com.bluelightning.tools.transpiler.antlr4.LcdPythonBaseVisitor;
import com.bluelightning.tools.transpiler.antlr4.LcdPythonLexer;
import com.bluelightning.tools.transpiler.antlr4.LcdPythonParser;

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
	
	protected StringBuffer errorReport = new StringBuffer();
	
	protected void reportError(ParserRuleContext context, String message ) {
		reportError( context.start, message );
	}
	
	protected void reportError(Token token, String message ) {
		String r = String.format("ERROR [L%5d:C%3d]: %s", token.getLine(), token.getCharPositionInLine(), message );
		reportError(r);
	}
	
	public void reportError(String r) {
		System.out.println("!!!!!!!!!!!!!! " + r );
		errorReport.append(r);
		errorReport.append('\n');
	}


	protected void dumpChildren( RuleNode ctx ) {
//		if (ctx.getChildCount() > 1) {
			parser.getRuleIndexMap().get(ctx.getRuleContext().getRuleIndex());
			System.out.println(parser.getRuleNames()[ctx.getRuleContext().getRuleIndex()].toUpperCase() + " "
					+ ctx.getChildCount() + " " + ctx.getText());
			for (int i = 0; i < ctx.getChildCount(); i++) {
				System.out.printf("%10d: %-30s %s\n", i,
						ctx.getChild(i).getPayload().getClass().getSimpleName(),
						valueMap.get(ctx.getChild(i).getPayload()));
			}
//		}
	}
	
	protected Map<Object, String> valueMap = new HashMap<>();
	
	protected Scope moduleScope = null;
	protected Map<Object, Scope> scopeMap = new HashMap<>();
	
	protected SymbolTable symbolTable = new SymbolTable(this);

	protected void processDeclaration(Token token, Scope scope, String str) {
		String[] fields = str.split(":");
		if (fields.length == 2) {
			symbolTable.add(scope, fields[0], fields[1]);
			System.out.println("DECLARED: " + str);
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

	public class TargetDispatcher implements ILanguageTarget {
		
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
		
	}

	protected TargetDispatcher dispatcher = new TargetDispatcher();
	
	/**
	 * LcdPythonPopulateListener - fully populates the value map.
	 */
	protected class PopulateListener extends LcdPythonBaseListener {
		@Override
		public void exitEveryRule(ParserRuleContext ctx) {
			StringBuffer result = new StringBuffer();
			for (int i = 0; i < ctx.getChildCount(); i++) {
				ParseTree child = ctx.getChild(i);
				if (child.getPayload() instanceof CommonToken) {
					result.append(child.getText());
					valueMap.put(child.getPayload(), child.getText());
				} else {
					result.append(valueMap.get(child.getPayload()));
				}
				//result.append(' ');
			}
			valueMap.put(ctx.getPayload(), result.toString());
		}
	}

	

	protected String content;
	protected LcdPythonParser parser;
	
	protected Configuration cfg;
	
	private static Transpiler singleton = null;
	
	public static Transpiler instance() { 
		return singleton;
	}

	public Transpiler(Path where, List<String> dottedModule) {
		singleton = this;
		try {
			cfg = configure();
		} catch (IOException | TemplateException e) {
			e.printStackTrace();
		}
		
		dispatcher.addTarget( new CppBoostTarget(cfg, Paths.get("../Cpp/src/")) );
		
		String module = dottedModule.get(dottedModule.size()-1);
		
		try {
			byte[] bytes = Files.readAllBytes(where.resolve(module + ".py"));
			content = new String(bytes, "UTF-8");
		} catch (Exception x) {
			x.printStackTrace();
			return;
		}
		
		moduleScope = new Scope(Scope.Level.MODULE, dottedModule );
		dispatcher.startModule(moduleScope);

		LcdPythonLexer java8Lexer = new LcdPythonLexer(CharStreams.fromString(content));
		CommonTokenStream tokens = new CommonTokenStream(java8Lexer);
		parser = new LcdPythonParser(tokens);
		ParseTree tree = parser.file_input();
		
		// PASS 1 - fully populate parse tree contents map
		PopulateListener populateListener = new PopulateListener();
		ParseTreeWalker walker = new ParseTreeWalker();
		walker.walk(populateListener, tree);
		
		// PASS 2 - handle all imports, variable, function, and class declarations
		DeclarationsListener declarationsListener = new DeclarationsListener(this, moduleScope);
		walker.walk(declarationsListener, tree);
		if (false) {
			System.out.println("\n\n-------------------------------------");
			System.out.println("--SYMBOL TABLE\n");
			System.out.println( symbolTable.toString() );
			System.out.println("\n\n-------------------------------------");
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
		// compileGrammar( "data", "LcdPython.g4",
		// "src/com/bluelightning/tools/transpiler/antlr4/" );
		Path base = Paths.get("../Python/src");
//		Path dir = Paths.get("PolynomialFiltering");
//		String module = "Main";
		Path dir = Paths.get("");
		String module = "TranspilerTest";
		ArrayList<String> dottedModule = new ArrayList<>();
		for (int i = 0; i < dir.getNameCount(); i++) {
			if (! dir.getName(i).toString().isEmpty())
				dottedModule.add( dir.getName(i).toString());
		}
		dottedModule.add(module);
//		System.out.println(dottedModule);
		Path where = base.resolve(dir);
		Transpiler transpiler = new Transpiler(where, dottedModule);
	}


}
