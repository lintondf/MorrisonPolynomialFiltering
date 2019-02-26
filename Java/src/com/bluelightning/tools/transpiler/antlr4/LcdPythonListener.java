// Generated from LcdPython.g4 by ANTLR 4.7.2
package com.bluelightning.tools.transpiler.antlr4;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link LcdPythonParser}.
 */
public interface LcdPythonListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#single_input}.
	 * @param ctx the parse tree
	 */
	void enterSingle_input(LcdPythonParser.Single_inputContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#single_input}.
	 * @param ctx the parse tree
	 */
	void exitSingle_input(LcdPythonParser.Single_inputContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#file_input}.
	 * @param ctx the parse tree
	 */
	void enterFile_input(LcdPythonParser.File_inputContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#file_input}.
	 * @param ctx the parse tree
	 */
	void exitFile_input(LcdPythonParser.File_inputContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#eval_input}.
	 * @param ctx the parse tree
	 */
	void enterEval_input(LcdPythonParser.Eval_inputContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#eval_input}.
	 * @param ctx the parse tree
	 */
	void exitEval_input(LcdPythonParser.Eval_inputContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#decorator}.
	 * @param ctx the parse tree
	 */
	void enterDecorator(LcdPythonParser.DecoratorContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#decorator}.
	 * @param ctx the parse tree
	 */
	void exitDecorator(LcdPythonParser.DecoratorContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#decorators}.
	 * @param ctx the parse tree
	 */
	void enterDecorators(LcdPythonParser.DecoratorsContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#decorators}.
	 * @param ctx the parse tree
	 */
	void exitDecorators(LcdPythonParser.DecoratorsContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#decorated}.
	 * @param ctx the parse tree
	 */
	void enterDecorated(LcdPythonParser.DecoratedContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#decorated}.
	 * @param ctx the parse tree
	 */
	void exitDecorated(LcdPythonParser.DecoratedContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#async_funcdef}.
	 * @param ctx the parse tree
	 */
	void enterAsync_funcdef(LcdPythonParser.Async_funcdefContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#async_funcdef}.
	 * @param ctx the parse tree
	 */
	void exitAsync_funcdef(LcdPythonParser.Async_funcdefContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#funcdef}.
	 * @param ctx the parse tree
	 */
	void enterFuncdef(LcdPythonParser.FuncdefContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#funcdef}.
	 * @param ctx the parse tree
	 */
	void exitFuncdef(LcdPythonParser.FuncdefContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#parameters}.
	 * @param ctx the parse tree
	 */
	void enterParameters(LcdPythonParser.ParametersContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#parameters}.
	 * @param ctx the parse tree
	 */
	void exitParameters(LcdPythonParser.ParametersContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#typedargslist}.
	 * @param ctx the parse tree
	 */
	void enterTypedargslist(LcdPythonParser.TypedargslistContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#typedargslist}.
	 * @param ctx the parse tree
	 */
	void exitTypedargslist(LcdPythonParser.TypedargslistContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#tfpdef}.
	 * @param ctx the parse tree
	 */
	void enterTfpdef(LcdPythonParser.TfpdefContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#tfpdef}.
	 * @param ctx the parse tree
	 */
	void exitTfpdef(LcdPythonParser.TfpdefContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#varargslist}.
	 * @param ctx the parse tree
	 */
	void enterVarargslist(LcdPythonParser.VarargslistContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#varargslist}.
	 * @param ctx the parse tree
	 */
	void exitVarargslist(LcdPythonParser.VarargslistContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#vfpdef}.
	 * @param ctx the parse tree
	 */
	void enterVfpdef(LcdPythonParser.VfpdefContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#vfpdef}.
	 * @param ctx the parse tree
	 */
	void exitVfpdef(LcdPythonParser.VfpdefContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#stmt}.
	 * @param ctx the parse tree
	 */
	void enterStmt(LcdPythonParser.StmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#stmt}.
	 * @param ctx the parse tree
	 */
	void exitStmt(LcdPythonParser.StmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#simple_stmt}.
	 * @param ctx the parse tree
	 */
	void enterSimple_stmt(LcdPythonParser.Simple_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#simple_stmt}.
	 * @param ctx the parse tree
	 */
	void exitSimple_stmt(LcdPythonParser.Simple_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#small_stmt}.
	 * @param ctx the parse tree
	 */
	void enterSmall_stmt(LcdPythonParser.Small_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#small_stmt}.
	 * @param ctx the parse tree
	 */
	void exitSmall_stmt(LcdPythonParser.Small_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#expr_stmt}.
	 * @param ctx the parse tree
	 */
	void enterExpr_stmt(LcdPythonParser.Expr_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#expr_stmt}.
	 * @param ctx the parse tree
	 */
	void exitExpr_stmt(LcdPythonParser.Expr_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#annassign}.
	 * @param ctx the parse tree
	 */
	void enterAnnassign(LcdPythonParser.AnnassignContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#annassign}.
	 * @param ctx the parse tree
	 */
	void exitAnnassign(LcdPythonParser.AnnassignContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#testlist_star_expr}.
	 * @param ctx the parse tree
	 */
	void enterTestlist_star_expr(LcdPythonParser.Testlist_star_exprContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#testlist_star_expr}.
	 * @param ctx the parse tree
	 */
	void exitTestlist_star_expr(LcdPythonParser.Testlist_star_exprContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#augassign}.
	 * @param ctx the parse tree
	 */
	void enterAugassign(LcdPythonParser.AugassignContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#augassign}.
	 * @param ctx the parse tree
	 */
	void exitAugassign(LcdPythonParser.AugassignContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#del_stmt}.
	 * @param ctx the parse tree
	 */
	void enterDel_stmt(LcdPythonParser.Del_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#del_stmt}.
	 * @param ctx the parse tree
	 */
	void exitDel_stmt(LcdPythonParser.Del_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#pass_stmt}.
	 * @param ctx the parse tree
	 */
	void enterPass_stmt(LcdPythonParser.Pass_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#pass_stmt}.
	 * @param ctx the parse tree
	 */
	void exitPass_stmt(LcdPythonParser.Pass_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#flow_stmt}.
	 * @param ctx the parse tree
	 */
	void enterFlow_stmt(LcdPythonParser.Flow_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#flow_stmt}.
	 * @param ctx the parse tree
	 */
	void exitFlow_stmt(LcdPythonParser.Flow_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#break_stmt}.
	 * @param ctx the parse tree
	 */
	void enterBreak_stmt(LcdPythonParser.Break_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#break_stmt}.
	 * @param ctx the parse tree
	 */
	void exitBreak_stmt(LcdPythonParser.Break_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#continue_stmt}.
	 * @param ctx the parse tree
	 */
	void enterContinue_stmt(LcdPythonParser.Continue_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#continue_stmt}.
	 * @param ctx the parse tree
	 */
	void exitContinue_stmt(LcdPythonParser.Continue_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#return_stmt}.
	 * @param ctx the parse tree
	 */
	void enterReturn_stmt(LcdPythonParser.Return_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#return_stmt}.
	 * @param ctx the parse tree
	 */
	void exitReturn_stmt(LcdPythonParser.Return_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#yield_stmt}.
	 * @param ctx the parse tree
	 */
	void enterYield_stmt(LcdPythonParser.Yield_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#yield_stmt}.
	 * @param ctx the parse tree
	 */
	void exitYield_stmt(LcdPythonParser.Yield_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#raise_stmt}.
	 * @param ctx the parse tree
	 */
	void enterRaise_stmt(LcdPythonParser.Raise_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#raise_stmt}.
	 * @param ctx the parse tree
	 */
	void exitRaise_stmt(LcdPythonParser.Raise_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#import_stmt}.
	 * @param ctx the parse tree
	 */
	void enterImport_stmt(LcdPythonParser.Import_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#import_stmt}.
	 * @param ctx the parse tree
	 */
	void exitImport_stmt(LcdPythonParser.Import_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#import_name}.
	 * @param ctx the parse tree
	 */
	void enterImport_name(LcdPythonParser.Import_nameContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#import_name}.
	 * @param ctx the parse tree
	 */
	void exitImport_name(LcdPythonParser.Import_nameContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#import_from}.
	 * @param ctx the parse tree
	 */
	void enterImport_from(LcdPythonParser.Import_fromContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#import_from}.
	 * @param ctx the parse tree
	 */
	void exitImport_from(LcdPythonParser.Import_fromContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#import_as_name}.
	 * @param ctx the parse tree
	 */
	void enterImport_as_name(LcdPythonParser.Import_as_nameContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#import_as_name}.
	 * @param ctx the parse tree
	 */
	void exitImport_as_name(LcdPythonParser.Import_as_nameContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#dotted_as_name}.
	 * @param ctx the parse tree
	 */
	void enterDotted_as_name(LcdPythonParser.Dotted_as_nameContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#dotted_as_name}.
	 * @param ctx the parse tree
	 */
	void exitDotted_as_name(LcdPythonParser.Dotted_as_nameContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#import_as_names}.
	 * @param ctx the parse tree
	 */
	void enterImport_as_names(LcdPythonParser.Import_as_namesContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#import_as_names}.
	 * @param ctx the parse tree
	 */
	void exitImport_as_names(LcdPythonParser.Import_as_namesContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#dotted_as_names}.
	 * @param ctx the parse tree
	 */
	void enterDotted_as_names(LcdPythonParser.Dotted_as_namesContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#dotted_as_names}.
	 * @param ctx the parse tree
	 */
	void exitDotted_as_names(LcdPythonParser.Dotted_as_namesContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#dotted_name}.
	 * @param ctx the parse tree
	 */
	void enterDotted_name(LcdPythonParser.Dotted_nameContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#dotted_name}.
	 * @param ctx the parse tree
	 */
	void exitDotted_name(LcdPythonParser.Dotted_nameContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#global_stmt}.
	 * @param ctx the parse tree
	 */
	void enterGlobal_stmt(LcdPythonParser.Global_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#global_stmt}.
	 * @param ctx the parse tree
	 */
	void exitGlobal_stmt(LcdPythonParser.Global_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#nonlocal_stmt}.
	 * @param ctx the parse tree
	 */
	void enterNonlocal_stmt(LcdPythonParser.Nonlocal_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#nonlocal_stmt}.
	 * @param ctx the parse tree
	 */
	void exitNonlocal_stmt(LcdPythonParser.Nonlocal_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#assert_stmt}.
	 * @param ctx the parse tree
	 */
	void enterAssert_stmt(LcdPythonParser.Assert_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#assert_stmt}.
	 * @param ctx the parse tree
	 */
	void exitAssert_stmt(LcdPythonParser.Assert_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#compound_stmt}.
	 * @param ctx the parse tree
	 */
	void enterCompound_stmt(LcdPythonParser.Compound_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#compound_stmt}.
	 * @param ctx the parse tree
	 */
	void exitCompound_stmt(LcdPythonParser.Compound_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#async_stmt}.
	 * @param ctx the parse tree
	 */
	void enterAsync_stmt(LcdPythonParser.Async_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#async_stmt}.
	 * @param ctx the parse tree
	 */
	void exitAsync_stmt(LcdPythonParser.Async_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#if_stmt}.
	 * @param ctx the parse tree
	 */
	void enterIf_stmt(LcdPythonParser.If_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#if_stmt}.
	 * @param ctx the parse tree
	 */
	void exitIf_stmt(LcdPythonParser.If_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#while_stmt}.
	 * @param ctx the parse tree
	 */
	void enterWhile_stmt(LcdPythonParser.While_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#while_stmt}.
	 * @param ctx the parse tree
	 */
	void exitWhile_stmt(LcdPythonParser.While_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#for_stmt}.
	 * @param ctx the parse tree
	 */
	void enterFor_stmt(LcdPythonParser.For_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#for_stmt}.
	 * @param ctx the parse tree
	 */
	void exitFor_stmt(LcdPythonParser.For_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#try_stmt}.
	 * @param ctx the parse tree
	 */
	void enterTry_stmt(LcdPythonParser.Try_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#try_stmt}.
	 * @param ctx the parse tree
	 */
	void exitTry_stmt(LcdPythonParser.Try_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#with_stmt}.
	 * @param ctx the parse tree
	 */
	void enterWith_stmt(LcdPythonParser.With_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#with_stmt}.
	 * @param ctx the parse tree
	 */
	void exitWith_stmt(LcdPythonParser.With_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#with_item}.
	 * @param ctx the parse tree
	 */
	void enterWith_item(LcdPythonParser.With_itemContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#with_item}.
	 * @param ctx the parse tree
	 */
	void exitWith_item(LcdPythonParser.With_itemContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#except_clause}.
	 * @param ctx the parse tree
	 */
	void enterExcept_clause(LcdPythonParser.Except_clauseContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#except_clause}.
	 * @param ctx the parse tree
	 */
	void exitExcept_clause(LcdPythonParser.Except_clauseContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#suite}.
	 * @param ctx the parse tree
	 */
	void enterSuite(LcdPythonParser.SuiteContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#suite}.
	 * @param ctx the parse tree
	 */
	void exitSuite(LcdPythonParser.SuiteContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#test}.
	 * @param ctx the parse tree
	 */
	void enterTest(LcdPythonParser.TestContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#test}.
	 * @param ctx the parse tree
	 */
	void exitTest(LcdPythonParser.TestContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#test_nocond}.
	 * @param ctx the parse tree
	 */
	void enterTest_nocond(LcdPythonParser.Test_nocondContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#test_nocond}.
	 * @param ctx the parse tree
	 */
	void exitTest_nocond(LcdPythonParser.Test_nocondContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#lambdef}.
	 * @param ctx the parse tree
	 */
	void enterLambdef(LcdPythonParser.LambdefContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#lambdef}.
	 * @param ctx the parse tree
	 */
	void exitLambdef(LcdPythonParser.LambdefContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#lambdef_nocond}.
	 * @param ctx the parse tree
	 */
	void enterLambdef_nocond(LcdPythonParser.Lambdef_nocondContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#lambdef_nocond}.
	 * @param ctx the parse tree
	 */
	void exitLambdef_nocond(LcdPythonParser.Lambdef_nocondContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#or_test}.
	 * @param ctx the parse tree
	 */
	void enterOr_test(LcdPythonParser.Or_testContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#or_test}.
	 * @param ctx the parse tree
	 */
	void exitOr_test(LcdPythonParser.Or_testContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#and_test}.
	 * @param ctx the parse tree
	 */
	void enterAnd_test(LcdPythonParser.And_testContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#and_test}.
	 * @param ctx the parse tree
	 */
	void exitAnd_test(LcdPythonParser.And_testContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#not_test}.
	 * @param ctx the parse tree
	 */
	void enterNot_test(LcdPythonParser.Not_testContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#not_test}.
	 * @param ctx the parse tree
	 */
	void exitNot_test(LcdPythonParser.Not_testContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#comparison}.
	 * @param ctx the parse tree
	 */
	void enterComparison(LcdPythonParser.ComparisonContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#comparison}.
	 * @param ctx the parse tree
	 */
	void exitComparison(LcdPythonParser.ComparisonContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#comp_op}.
	 * @param ctx the parse tree
	 */
	void enterComp_op(LcdPythonParser.Comp_opContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#comp_op}.
	 * @param ctx the parse tree
	 */
	void exitComp_op(LcdPythonParser.Comp_opContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#star_expr}.
	 * @param ctx the parse tree
	 */
	void enterStar_expr(LcdPythonParser.Star_exprContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#star_expr}.
	 * @param ctx the parse tree
	 */
	void exitStar_expr(LcdPythonParser.Star_exprContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterExpr(LcdPythonParser.ExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitExpr(LcdPythonParser.ExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#xor_expr}.
	 * @param ctx the parse tree
	 */
	void enterXor_expr(LcdPythonParser.Xor_exprContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#xor_expr}.
	 * @param ctx the parse tree
	 */
	void exitXor_expr(LcdPythonParser.Xor_exprContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#and_expr}.
	 * @param ctx the parse tree
	 */
	void enterAnd_expr(LcdPythonParser.And_exprContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#and_expr}.
	 * @param ctx the parse tree
	 */
	void exitAnd_expr(LcdPythonParser.And_exprContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#shift_expr}.
	 * @param ctx the parse tree
	 */
	void enterShift_expr(LcdPythonParser.Shift_exprContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#shift_expr}.
	 * @param ctx the parse tree
	 */
	void exitShift_expr(LcdPythonParser.Shift_exprContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#arith_expr}.
	 * @param ctx the parse tree
	 */
	void enterArith_expr(LcdPythonParser.Arith_exprContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#arith_expr}.
	 * @param ctx the parse tree
	 */
	void exitArith_expr(LcdPythonParser.Arith_exprContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#term}.
	 * @param ctx the parse tree
	 */
	void enterTerm(LcdPythonParser.TermContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#term}.
	 * @param ctx the parse tree
	 */
	void exitTerm(LcdPythonParser.TermContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#factor}.
	 * @param ctx the parse tree
	 */
	void enterFactor(LcdPythonParser.FactorContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#factor}.
	 * @param ctx the parse tree
	 */
	void exitFactor(LcdPythonParser.FactorContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#power}.
	 * @param ctx the parse tree
	 */
	void enterPower(LcdPythonParser.PowerContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#power}.
	 * @param ctx the parse tree
	 */
	void exitPower(LcdPythonParser.PowerContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#atom_expr}.
	 * @param ctx the parse tree
	 */
	void enterAtom_expr(LcdPythonParser.Atom_exprContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#atom_expr}.
	 * @param ctx the parse tree
	 */
	void exitAtom_expr(LcdPythonParser.Atom_exprContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#atom}.
	 * @param ctx the parse tree
	 */
	void enterAtom(LcdPythonParser.AtomContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#atom}.
	 * @param ctx the parse tree
	 */
	void exitAtom(LcdPythonParser.AtomContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#testlist_comp}.
	 * @param ctx the parse tree
	 */
	void enterTestlist_comp(LcdPythonParser.Testlist_compContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#testlist_comp}.
	 * @param ctx the parse tree
	 */
	void exitTestlist_comp(LcdPythonParser.Testlist_compContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#trailer}.
	 * @param ctx the parse tree
	 */
	void enterTrailer(LcdPythonParser.TrailerContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#trailer}.
	 * @param ctx the parse tree
	 */
	void exitTrailer(LcdPythonParser.TrailerContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#subscriptlist}.
	 * @param ctx the parse tree
	 */
	void enterSubscriptlist(LcdPythonParser.SubscriptlistContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#subscriptlist}.
	 * @param ctx the parse tree
	 */
	void exitSubscriptlist(LcdPythonParser.SubscriptlistContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#subscript}.
	 * @param ctx the parse tree
	 */
	void enterSubscript(LcdPythonParser.SubscriptContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#subscript}.
	 * @param ctx the parse tree
	 */
	void exitSubscript(LcdPythonParser.SubscriptContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#sliceop}.
	 * @param ctx the parse tree
	 */
	void enterSliceop(LcdPythonParser.SliceopContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#sliceop}.
	 * @param ctx the parse tree
	 */
	void exitSliceop(LcdPythonParser.SliceopContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#exprlist}.
	 * @param ctx the parse tree
	 */
	void enterExprlist(LcdPythonParser.ExprlistContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#exprlist}.
	 * @param ctx the parse tree
	 */
	void exitExprlist(LcdPythonParser.ExprlistContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#testlist}.
	 * @param ctx the parse tree
	 */
	void enterTestlist(LcdPythonParser.TestlistContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#testlist}.
	 * @param ctx the parse tree
	 */
	void exitTestlist(LcdPythonParser.TestlistContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#dictorsetmaker}.
	 * @param ctx the parse tree
	 */
	void enterDictorsetmaker(LcdPythonParser.DictorsetmakerContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#dictorsetmaker}.
	 * @param ctx the parse tree
	 */
	void exitDictorsetmaker(LcdPythonParser.DictorsetmakerContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#classdef}.
	 * @param ctx the parse tree
	 */
	void enterClassdef(LcdPythonParser.ClassdefContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#classdef}.
	 * @param ctx the parse tree
	 */
	void exitClassdef(LcdPythonParser.ClassdefContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#arglist}.
	 * @param ctx the parse tree
	 */
	void enterArglist(LcdPythonParser.ArglistContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#arglist}.
	 * @param ctx the parse tree
	 */
	void exitArglist(LcdPythonParser.ArglistContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#argument}.
	 * @param ctx the parse tree
	 */
	void enterArgument(LcdPythonParser.ArgumentContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#argument}.
	 * @param ctx the parse tree
	 */
	void exitArgument(LcdPythonParser.ArgumentContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#comp_iter}.
	 * @param ctx the parse tree
	 */
	void enterComp_iter(LcdPythonParser.Comp_iterContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#comp_iter}.
	 * @param ctx the parse tree
	 */
	void exitComp_iter(LcdPythonParser.Comp_iterContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#comp_for}.
	 * @param ctx the parse tree
	 */
	void enterComp_for(LcdPythonParser.Comp_forContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#comp_for}.
	 * @param ctx the parse tree
	 */
	void exitComp_for(LcdPythonParser.Comp_forContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#comp_if}.
	 * @param ctx the parse tree
	 */
	void enterComp_if(LcdPythonParser.Comp_ifContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#comp_if}.
	 * @param ctx the parse tree
	 */
	void exitComp_if(LcdPythonParser.Comp_ifContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#encoding_decl}.
	 * @param ctx the parse tree
	 */
	void enterEncoding_decl(LcdPythonParser.Encoding_declContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#encoding_decl}.
	 * @param ctx the parse tree
	 */
	void exitEncoding_decl(LcdPythonParser.Encoding_declContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#yield_expr}.
	 * @param ctx the parse tree
	 */
	void enterYield_expr(LcdPythonParser.Yield_exprContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#yield_expr}.
	 * @param ctx the parse tree
	 */
	void exitYield_expr(LcdPythonParser.Yield_exprContext ctx);
	/**
	 * Enter a parse tree produced by {@link LcdPythonParser#yield_arg}.
	 * @param ctx the parse tree
	 */
	void enterYield_arg(LcdPythonParser.Yield_argContext ctx);
	/**
	 * Exit a parse tree produced by {@link LcdPythonParser#yield_arg}.
	 * @param ctx the parse tree
	 */
	void exitYield_arg(LcdPythonParser.Yield_argContext ctx);
}