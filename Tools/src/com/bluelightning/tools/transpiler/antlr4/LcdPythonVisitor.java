// Generated from LcdPython.g4 by ANTLR 4.7.2
package com.bluelightning.tools.transpiler.antlr4;
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link LcdPythonParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface LcdPythonVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#single_input}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSingle_input(LcdPythonParser.Single_inputContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#file_input}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFile_input(LcdPythonParser.File_inputContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#eval_input}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEval_input(LcdPythonParser.Eval_inputContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#decorator}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDecorator(LcdPythonParser.DecoratorContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#decorators}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDecorators(LcdPythonParser.DecoratorsContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#decorated}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDecorated(LcdPythonParser.DecoratedContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#async_funcdef}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAsync_funcdef(LcdPythonParser.Async_funcdefContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#funcdef}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFuncdef(LcdPythonParser.FuncdefContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#parameters}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParameters(LcdPythonParser.ParametersContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#typedargslist}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTypedargslist(LcdPythonParser.TypedargslistContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#tfpdef}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTfpdef(LcdPythonParser.TfpdefContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#varargslist}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVarargslist(LcdPythonParser.VarargslistContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#vfpdef}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVfpdef(LcdPythonParser.VfpdefContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStmt(LcdPythonParser.StmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#simple_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSimple_stmt(LcdPythonParser.Simple_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#small_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSmall_stmt(LcdPythonParser.Small_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#expr_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExpr_stmt(LcdPythonParser.Expr_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#annassign}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAnnassign(LcdPythonParser.AnnassignContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#testlist_star_expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTestlist_star_expr(LcdPythonParser.Testlist_star_exprContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#augassign}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAugassign(LcdPythonParser.AugassignContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#del_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDel_stmt(LcdPythonParser.Del_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#pass_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPass_stmt(LcdPythonParser.Pass_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#flow_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFlow_stmt(LcdPythonParser.Flow_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#break_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBreak_stmt(LcdPythonParser.Break_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#continue_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitContinue_stmt(LcdPythonParser.Continue_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#return_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitReturn_stmt(LcdPythonParser.Return_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#yield_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitYield_stmt(LcdPythonParser.Yield_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#raise_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRaise_stmt(LcdPythonParser.Raise_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#import_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitImport_stmt(LcdPythonParser.Import_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#import_name}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitImport_name(LcdPythonParser.Import_nameContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#import_from}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitImport_from(LcdPythonParser.Import_fromContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#import_as_name}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitImport_as_name(LcdPythonParser.Import_as_nameContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#dotted_as_name}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDotted_as_name(LcdPythonParser.Dotted_as_nameContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#import_as_names}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitImport_as_names(LcdPythonParser.Import_as_namesContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#dotted_as_names}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDotted_as_names(LcdPythonParser.Dotted_as_namesContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#dotted_name}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDotted_name(LcdPythonParser.Dotted_nameContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#global_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGlobal_stmt(LcdPythonParser.Global_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#nonlocal_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNonlocal_stmt(LcdPythonParser.Nonlocal_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#assert_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAssert_stmt(LcdPythonParser.Assert_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#compound_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCompound_stmt(LcdPythonParser.Compound_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#async_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAsync_stmt(LcdPythonParser.Async_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#else_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitElse_stmt(LcdPythonParser.Else_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#elif_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitElif_stmt(LcdPythonParser.Elif_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#if_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIf_stmt(LcdPythonParser.If_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#while_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitWhile_stmt(LcdPythonParser.While_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#for_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFor_stmt(LcdPythonParser.For_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#try_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTry_stmt(LcdPythonParser.Try_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#with_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitWith_stmt(LcdPythonParser.With_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#with_item}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitWith_item(LcdPythonParser.With_itemContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#except_clause}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExcept_clause(LcdPythonParser.Except_clauseContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#suite}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSuite(LcdPythonParser.SuiteContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#test}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTest(LcdPythonParser.TestContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#test_nocond}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTest_nocond(LcdPythonParser.Test_nocondContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#lambdef}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLambdef(LcdPythonParser.LambdefContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#lambdef_nocond}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLambdef_nocond(LcdPythonParser.Lambdef_nocondContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#or_test}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitOr_test(LcdPythonParser.Or_testContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#and_test}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAnd_test(LcdPythonParser.And_testContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#not_test}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNot_test(LcdPythonParser.Not_testContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#comparison}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComparison(LcdPythonParser.ComparisonContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#comp_op}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComp_op(LcdPythonParser.Comp_opContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#star_expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStar_expr(LcdPythonParser.Star_exprContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExpr(LcdPythonParser.ExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#xor_expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXor_expr(LcdPythonParser.Xor_exprContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#and_expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAnd_expr(LcdPythonParser.And_exprContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#shift_expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitShift_expr(LcdPythonParser.Shift_exprContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#arith_expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArith_expr(LcdPythonParser.Arith_exprContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#term}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTerm(LcdPythonParser.TermContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#factor}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFactor(LcdPythonParser.FactorContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#power}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPower(LcdPythonParser.PowerContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#atom_expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAtom_expr(LcdPythonParser.Atom_exprContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#atom}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAtom(LcdPythonParser.AtomContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#testlist_comp}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTestlist_comp(LcdPythonParser.Testlist_compContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#trailer}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTrailer(LcdPythonParser.TrailerContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#subscriptlist}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSubscriptlist(LcdPythonParser.SubscriptlistContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#subscript}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSubscript(LcdPythonParser.SubscriptContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#sliceop}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSliceop(LcdPythonParser.SliceopContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#exprlist}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExprlist(LcdPythonParser.ExprlistContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#testlist}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTestlist(LcdPythonParser.TestlistContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#dictorsetmaker}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDictorsetmaker(LcdPythonParser.DictorsetmakerContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#classdef}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitClassdef(LcdPythonParser.ClassdefContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#arglist}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArglist(LcdPythonParser.ArglistContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#argument}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArgument(LcdPythonParser.ArgumentContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#comp_iter}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComp_iter(LcdPythonParser.Comp_iterContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#comp_for}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComp_for(LcdPythonParser.Comp_forContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#comp_if}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComp_if(LcdPythonParser.Comp_ifContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#encoding_decl}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEncoding_decl(LcdPythonParser.Encoding_declContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#yield_expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitYield_expr(LcdPythonParser.Yield_exprContext ctx);
	/**
	 * Visit a parse tree produced by {@link LcdPythonParser#yield_arg}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitYield_arg(LcdPythonParser.Yield_argContext ctx);
}