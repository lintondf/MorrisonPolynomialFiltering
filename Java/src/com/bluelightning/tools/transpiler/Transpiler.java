/** Polynomial Filtering Universal Transpiler
 * SPDX-License-Identifier: MIT
 *
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 */
package com.bluelightning.tools.transpiler;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
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
import java.util.TreeSet;
import java.util.zip.CRC32;
import java.util.zip.Checksum;

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

import com.bluelightning.tools.transpiler.Scope.Level;
import com.bluelightning.tools.transpiler.antlr4.LcdPythonBaseListener;
import com.bluelightning.tools.transpiler.antlr4.LcdPythonBaseVisitor;
import com.bluelightning.tools.transpiler.antlr4.LcdPythonLexer;
import com.bluelightning.tools.transpiler.antlr4.LcdPythonParser;
import com.bluelightning.tools.transpiler.nodes.TranslationExpressionNode;
import com.bluelightning.tools.transpiler.nodes.TranslationNode;
import com.bluelightning.tools.transpiler.nodes.TranslationUnaryNode;
import com.bluelightning.tools.transpiler.programmer.BoostProgrammer;
import com.bluelightning.tools.transpiler.programmer.EigenProgrammer;

import freemarker.core.PlainTextOutputFormat;
import freemarker.template.Configuration;
import freemarker.template.Template;
import freemarker.template.TemplateException;
import freemarker.template.TemplateExceptionHandler;

/* TODO
 * -- this.transpiler -> Transpiler.instance()
 * -- Check for changes before writing sources; done for sources, add for tests
 * -- handle superclass init for multiple constructors
 * -- auto define missing variables as None?
 * -- direct return of vector of zeros fails
 */
/**
 * @author NOOK
 *
 */
public class Transpiler {
	
	static boolean skipUnchanged = false;
	
	public static class Target {
		public Path  dir;
		public String module;
		public boolean headerOnly;
		public boolean isTest;
		public Path   where;
		public ArrayList<String> dottedModule;
		
		public Target( Path dir, String module ) {
			this.dir = dir;
			this.module = module;
			this.headerOnly = false;
			this.isTest = false;
		}

		public Target( Path dir, String module, boolean headerOnly ) {
			this.dir = dir;
			this.module = module;
			this.headerOnly = headerOnly;
			this.isTest = false;
		}
	}
	
	public static class TestTarget extends Target {
		public TestTarget( Path dir, String module ) {
			super(dir, module);
			this.isTest = true;
			
		}
	}
	
	static Target[] targets = {
//		new Target(Paths.get(""), "TranspilerTest"),
		new Target(Paths.get("polynomialfiltering"), "Main"),
		new Target(Paths.get("polynomialfiltering/components"), "FixedMemoryPolynomialFilter"),
		new Target(Paths.get("polynomialfiltering/components"), "ICore", true),
		new Target(Paths.get("polynomialfiltering/components"), "RecursivePolynomialFilter"),
		new Target(Paths.get("polynomialfiltering/components"), "Emp"),
		new Target(Paths.get("polynomialfiltering/components"), "Fmp"),
		
		new TestTarget(Paths.get("components"), "RecursivePolynomialFilter_test"),
		new TestTarget(Paths.get("components"), "EMP_test"),
		new TestTarget(Paths.get("components"), "Fmp_test"),
//		new Target(Paths.get("polynomialfiltering/components"), "AbstractRecursiveFilter"),
//		new Target(Paths.get("polynomialfiltering/components"), "ExpandingMemoryPolynomialFilter"),
//		new Target(Paths.get("polynomialfiltering/components"), "FadingMemoryPolynomialFilter"),
//		new Target(Paths.get("polynomialfiltering/components"), "EmpFmpPair"),
//		new Target(Paths.get("polynomialfiltering/filters/controls"), "IObservationErrorModel", true),
//		new Target(Paths.get("polynomialfiltering/filters/controls"), "IJudge", true),
//		new Target(Paths.get("polynomialfiltering/filters/controls"), "IMonitor", true),
//		new Target(Paths.get("polynomialfiltering/filters/controls"), "ConstantObservationErrorModel"),
//		new Target(Paths.get("polynomialfiltering/filters/controls"), "BaseScalarJudge"),
//		//new Target(Paths.get("polynomialfiltering/filters/controls"), "BaseVectorJudge"),
//		//new Target(Paths.get("polynomialfiltering/filters/controls"), "NullMonitor"),
//		new Target(Paths.get("polynomialfiltering/filters"), "IManagedFilter", true),
//		new Target(Paths.get("polynomialfiltering/filters"), "ManagedFilterBase"),
////		new Target(Paths.get("polynomialfiltering/filters"), "ManagedScalarRecursiveFilter"),
////		new Target(Paths.get("polynomialfiltering/filters"), "ManagedScalarRecursiveFilterSet"),
//		new TestTarget(Paths.get("filters/controls"), "ConstantObservationErrorModel_test"),
	};
	
	protected Logger logger;
	
	protected StringBuffer errorReport = new StringBuffer();
	
	public void reportError(ParserRuleContext context, String message ) {
		reportError( context.start, message );
	}
	
	public void reportError(TranslationNode node, String message) {
		reportError( node.getParserRuleContext(), message );
	}
	
	public void reportError(Token token, String message ) {
		String r = String.format("ERROR [L%5d:C%3d]: %s", token.getLine(), token.getCharPositionInLine(), message );
		reportError(r);
	}
	
	public void reportError(String r) {
		if (dispatcher.amIgnoring())
			return;
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
	
	public static String deblank(String text) {
		return text.trim().replaceAll(" +", "");
	}

	protected Documenter documenter = new Documenter();
	
	public Documenter getDocumenter() {
		return documenter;
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
	
	public Symbol lookupClass( String name ) {
		return symbolTable.lookupClass(name);
	}
	
	public void inheritClassMembers( Symbol symbol, Symbol type ) {
		Scope s = type.getScope().getChild(Level.CLASS, type.getName());
		List<Symbol> inheritance = symbolTable.atScope(s);
		Symbol c = this.lookup(symbol.getScope(), type.getName());
		if (c == null) {
			symbolTable.add(symbol.getScope(), type.getName(), "<CLASS>");
		}
		Scope inheritedScope = symbol.getScope().getChild(Level.CLASS, type.getName() );
		for (Symbol i : inheritance ) {
			if (i.getName().equals("__init__"))
				continue;
//			if (type.getName().equals("TestData") || symbol.getName().equals("testData") || symbol.getName().equals("fmp"))
//				System.out.println("     " + symbol.getName() + "  " + i.isClass() + " " + i.getName() + " " + inheritedScope + " "  + s );
			if (i.isClass() || i.isEnum()) {
				symbolTable.inherit(i, inheritedScope.getChild(Level.CLASS, symbol.getName()) );
			} else {
				symbolTable.inherit(i, inheritedScope);
			}
		}
	}
	

	public void addParameterClass(String type) {
		dispatcher.addParameterClass(type);
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
		List<ILanguageTarget> ignoring = new ArrayList<>();
		
		public TargetDispatcher() {}
		
		public void addTarget( ILanguageTarget target ) {
			target.setId( targets.size() );
			targets.add(target);
		}
		
		public boolean amIgnoring() {
			return ! ignoring.isEmpty();
		}

		public void setIgnoring(boolean b) {
			if (b) {
				ignoring.clear();
				ignoring.addAll(targets);
				targets.clear();
			} else {
				if (targets.isEmpty()) {
					targets.addAll(ignoring);
					ignoring.clear();
				}
			}
		}
		
		@Override
		public void startModule(Scope scope, boolean headerOnly, boolean isTest) {
			for (ILanguageTarget target : targets) {
				target.startModule(scope, headerOnly, isTest);
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
		public void emitSymbolDeclaration(Symbol symbol, String comment) {
			for (ILanguageTarget target : targets) {
				target.emitSymbolDeclaration(symbol, comment);
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
		public void startStatement() {
			for (ILanguageTarget target : targets) {
				target.startStatement();
			}
		}

		@Override
		public void finishStatement() {
			for (ILanguageTarget target : targets) {
				target.finishStatement();
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

		@Override
		public void addImport(Scope scope) {
			for (ILanguageTarget target : targets) {
				target.addImport( scope );
			}
		}

		@Override
		public void emitIfStatement(Scope scope, TranslationNode expressionRoot) {
			for (ILanguageTarget target : targets) {
				target.emitIfStatement( scope, expressionRoot );
			}
		}

		@Override
		public void emitElseStatement() {
			for (ILanguageTarget target : targets) {
				target.emitElseStatement();
			}
		}

		@Override
		public void emitRaiseStatement(String exception) {
			for (ILanguageTarget target : targets) {
				target.emitRaiseStatement(exception);
			}
		}

		@Override
		public void emitElifStatement(Scope scope, TranslationNode expressionRoot) {
			for (ILanguageTarget target : targets) {
				target.emitElifStatement( scope, expressionRoot );
			}
		}

		@Override
		public void emitNewExpression(Scope scope, String className, TranslationNode root) {
			for (ILanguageTarget target : targets) {
				target.emitNewExpression( scope, className, root );
			}
		}

		@Override
		public void addParameterClass(String className) {
			for (ILanguageTarget target : targets) {
				target.addParameterClass( className );
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
	public LcdPythonParser parser;
	
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
		dispatcher.addTarget( new CppSrcTarget(new EigenProgrammer(), 
				cfg, Paths.get("../Cpp/Eigen/") ) );
		dispatcher.addTarget( new CppTestTarget(new EigenProgrammer(), 
				cfg, Paths.get("../Cpp/Eigen/") ) );

		Scope importScope = new Scope();
		symbolTable.add( importScope, "abs", "array");
		symbolTable.add( importScope, "array", "array");
		symbolTable.add( importScope, "copy", "array");
		symbolTable.add( importScope, "diag", "array");
		symbolTable.add( importScope, "eye", "array");
		symbolTable.add( importScope, "inv", "array" );
		symbolTable.add( importScope, "int", "integerCast" );
		symbolTable.add( importScope, "len", "int" );
		symbolTable.add( importScope, "max", "int" );  //TODO generic type
		symbolTable.add( importScope, "min", "int" );  //TODO generic type
		symbolTable.add( importScope, "None", "NULL");
		symbolTable.add( importScope, "ones", "array");
		symbolTable.add( importScope, "pow", "float");
		symbolTable.add( importScope, "log", "float");
		symbolTable.add( importScope, "exp", "float");
		symbolTable.add( importScope, "range", "range");
		symbolTable.add( importScope, "shape", "dimensions");
		symbolTable.add( importScope, "sqrt", "array");
		symbolTable.add( importScope, "solve", "array");
		symbolTable.add( importScope, "super", "super" );
		symbolTable.add( importScope, "transpose", "array");
		symbolTable.add( importScope, "zeros", "array");
		symbolTable.add( importScope, "NotImplementedError", "exception");
		symbolTable.add( importScope, "chi2Cdf", "float");
		symbolTable.add( importScope, "chi2Ppf", "float");
		symbolTable.add( importScope, "ftestCdf", "float");
		symbolTable.add( importScope, "ftestPpf", "float");
		symbolTable.add( importScope, "True", "bool");
		symbolTable.add( importScope, "False", "bool");
		symbolTable.add( importScope, "assert_allclose", "None");
		symbolTable.add( importScope, "assert_almost_equal", "None");
		symbolTable.add( importScope, "assert_array_less", "None");
		symbolTable.add( importScope, "assert_not_empty", "None");
		
		valueMap.put( TranslationUnaryNode.staticFieldReference, "::");

	}
	
	HashMap<String, Long> moduleChecksums = new HashMap<>();
	
	public void compile(Path where, List<String> dottedModule, boolean headerOnly, boolean isTest) {
		if (isTest) {
			if (Transpiler.instance().lookupClass("TestData") == null) {
				Scope scope = new Scope();
				Transpiler.instance().symbolTable.add(scope, "TestData", "<CLASS>");
				scope = scope.getChild(Level.CLASS, "TestData");
				Transpiler.instance().symbolTable.add(scope, "testDataPath", "str");
				Transpiler.instance().symbolTable.add(scope, "getMatchingGroups", "List[str]");
				Transpiler.instance().symbolTable.add(scope, "getGroupVariable", "array");
				Transpiler.instance().symbolTable.add(scope, "close", "None");
				Symbol make = Transpiler.instance().symbolTable.add(scope, "make", "TestData");
			}			
		}
		
		String module = dottedModule.get(dottedModule.size()-1);
		Long checksumValue = null;
		String pathString = null;
		try {
			Path path = where.resolve(module + ".py");
			pathString = path.toString();
			byte[] bytes = Files.readAllBytes(path);
			Checksum checksum = new CRC32();
			checksum.update(bytes, 0, bytes.length);
			checksumValue = checksum.getValue();
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
		
		LcdPythonLexer java8Lexer = new LcdPythonLexer(CharStreams.fromString(content));
		CommonTokenStream tokens = new CommonTokenStream(java8Lexer);
		parser = new LcdPythonParser(tokens);
		ParseTree tree = parser.file_input();
		
		// PASS 1 - fully populate parse tree contents map
		PopulateListener populateListener = new PopulateListener();
		walker = new ParseTreeWalker();
		walker.walk(populateListener, tree);
		
		// PASS 2 - handle all imports, variable, function, and class declarations
		DeclarationsListener declarationsListener = new DeclarationsListener(this, moduleScope, isTest);
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
		
		boolean skip = false;
		Long prior = moduleChecksums.get(pathString);
		if (prior != null) {
			skip = checksumValue.equals(prior);
			if (pathString.contains("_test"))
				skip = false;  // TODO
		}
		if (skip && skipUnchanged) {
			System.out.println("No source code changes; skipping code generation..");
		} else {
			skipUnchanged = false;  // compile after first change detected
			dispatcher.startModule(moduleScope, headerOnly, isTest);
			LcdPythonBaseListener listener = null;
			if (! isTest) {
				listener = new SourceCompilationListener(this, headerOnly);
			} else {
				listener = new TestCompilationListener();
			}
			walker.walk(listener, tree);
			dispatcher.finishModule();			
		}
		
		if (errorReport.length() > 0) {
			System.err.println("\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n");
			System.err.println(errorReport.toString());
		} else {
			if (!skip)
				moduleChecksums.put(pathString, checksumValue);
			System.out.println("\nNO ERRORS\n\n");
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

	public static void xmain(String[] args) {
		compileGrammar( "data", "LcdPython.g4",
		      "src/com/bluelightning/tools/transpiler/antlr4/" );		
	}
	
	static TreeSet<String> srcs = new TreeSet<>();
	
	protected static void scan( File d ) {
		for (File f : d.listFiles()) {
			if (f.getName().startsWith(".") || f.getName().startsWith("__"))
				continue;
			if (f.isFile())
				srcs.add(f.getPath().substring(14).replace(".py", ""));
			if (f.isDirectory())
				scan(f);
		}		
	}
	

	protected void saveModuleChecksums() {
		File obj = new File("moduleChecksums.obj");
		try {
            FileOutputStream fos = new FileOutputStream(obj);
            ObjectOutputStream oos = new ObjectOutputStream(fos);
            oos.writeObject(moduleChecksums);
            oos.close();
            fos.close();
		} catch (Exception x) {
			obj.delete();
		}
	}

	@SuppressWarnings("unchecked")
	protected void loadModuleChecksums() {
		File obj = new File("moduleChecksums.obj");
		moduleChecksums = new HashMap<>();
		try {
			FileInputStream  fis = new FileInputStream (obj);
			ObjectInputStream  ois = new ObjectInputStream (fis);
			moduleChecksums = (HashMap<String, Long>) ois.readObject();
            ois.close();
            fis.close();
		} catch (Exception x) {
			moduleChecksums.clear();
		}
	}
	


	/**
	 * @param args
	 */
	public static void main(String[] args) {
		Transpiler transpiler = new Transpiler();
		transpiler.loadModuleChecksums();
		
		Path base = Paths.get("../Python/src");
		Path dir = base.resolve("polynomialfiltering");
		File d = dir.toFile();
		scan(d);
		srcs.remove("polynomialfiltering\\PythonUtilities"); // never do be transpiled
		Path testBase = Paths.get("../Python/test");
		for (Target target : targets) {
			Path srcWhere = base;
			Path testWhere = testBase;
			ArrayList<String> dottedModule = new ArrayList<>();
			for (int i = 0; i < target.dir.getNameCount(); i++) {
				if (! target.dir.getName(i).toString().isEmpty()) {
					dottedModule.add( target.dir.getName(i).toString());
					srcWhere = srcWhere.resolve(target.dir.getName(i).toString());
					testWhere = testWhere.resolve(target.dir.getName(i).toString());
				}
			}
			dottedModule.add(target.module);
			System.out.println(String.join("\\", dottedModule));
			srcs.remove( String.join("\\", dottedModule) );
			target.where = (target.isTest) ? testWhere : srcWhere;
			target.dottedModule = dottedModule;
			transpiler.compile( target.where, target.dottedModule, target.headerOnly, target.isTest);
		}
		transpiler.saveModuleChecksums();
		transpiler.documenter.close();

		System.out.printf("Compiled %d targets\n", targets.length);
		System.out.println();
		transpiler.symbolTable.report(transpiler.documenter);
//		System.out.println();
//		transpiler.documenter.report();
		for (String missed : srcs) {
			System.out.println("Missed: " + missed);
		}
	}
}
