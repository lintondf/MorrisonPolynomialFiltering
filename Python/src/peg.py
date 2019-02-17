from __future__ import unicode_literals
import string
import sys

# We only use unicode in our parser, except for __repr__, which must return str.
if sys.version_info.major == 2:
    repr_str = lambda s: s.encode("utf-8")
    str = unicode
else:
    repr_str = lambda s: s

peg_grammar_src = r"""
#                        Parsing Expression Grammars
# Based on:        A Recognition-Based Syntactic Foundation
#                              - Bryan Ford
#
# Modified slightly to use equals sign, simpler character escapes and fixed
# "-" at end of character class. Added a fixed number of repeats (e.g. {3})
# and starting a definition with a semicolon ensures any matched strings
# are ignored.
#
# A skipper is added. <expr1> expr2 will parse expr2 as usual, but skips any
# occurrences of expr1 at any point in expr2. At most one skipper can be active,
# in nested skippers only the deepest one is active.

# Hierarchical syntax
grammar    = spacing definition+ eof
definition = semicolon? identifier equals expression
expression = sequence (slash sequence)*
sequence   = prefix*
prefix     = (and / not)? suffix
suffix     = primary (question / star / plus / repeat)?
repeat     = open_brace integer close_brace
primary    = identifier !equals
           / open_paren expression close_paren
           / open_angled_bracket expression close_angled_bracket expression
           / literal / class / dot

# Lexical syntax
integer     = [0-9]+
identifier  = ident_start ident_cont* spacing
ident_start = [a-zA-Z_]
ident_cont  = ident_start / [0-9]
literal     = ['] (!['] char)* ['] spacing
            / ["] (!["] char)* ["] spacing
class       = "[" (!"]" range)* "]" spacing
range       = char "-" !"]" char / char
char        = "\\" [nrt'"\[\]\\]
            / "\\x" [0-9a-fA-F]{2}
            / "\\u" [0-9a-fA-F]{4}
            / "\\U" [0-9a-fA-F]{8}
            / !"\\" .
semicolon   = ";" spacing
equals      = "=" spacing
slash       = "/" spacing
and         = "&" spacing
not         = "!" spacing
question    = "?" spacing
star        = "*" spacing
plus        = "+" spacing
open_paren  = "(" spacing
close_paren = ")" spacing
open_brace  = "{" spacing
close_brace = "}" spacing
open_angled_bracket  = "<" spacing
close_angled_bracket = ">" spacing
dot         = "." spacing
; spacing   = (space / comment)*
comment     = "#" (!eol .)* eol
space       = " " / "\t" / eol
eol         = "\r\n" / "\n" / "\r"
eof         = !.
"""

class Val(object):
    """Val represents a value resulting from a grammar expression.

    If v is a Val object, str(v) returns the string as found in the source,
    v.v is the value, v.name is the name if the value resulted from a non-
    terminal, and v.ignore indicates that it's value is to be ignored for
    str().

    As a shorthand, you can index v directly, rather than having to write
    v.v[i] to index lists of results."""

    def __init__(self, v, name=None, ignore=False):
        self.name = name
        self.v = v
        self.ignore = ignore

    def __str__(self):
        if self.ignore: return ""
        if type(self.v) is str: return self.v
        return "".join(str(v) for v in self.v)

    if sys.version_info.major == 2:
        __unicode__ = __str__
        del __str__

    def __repr__(self):
        return repr_str("{}({!r})".format(type(self).__name__, self.v))

    def __getitem__(self, idx): return self.v[idx]
    def __len__(self): return len(self.v)


class Failure(object):
    def __init__(self, i, expected):
        self.i = i
        self.expected = expected

    def __str__(self):
        if hasattr(self, "name"):
            return "error at {}, expected {} ({})".format(self.i + 1, self.expected, self.name)
        return "error at {}, expected {}".format(self.i + 1, self.expected)

def isfail(obj): return isinstance(obj, Failure)

class AnyCharVal(Val): pass
class StringVal(Val): pass
class CharClassVal(Val): pass
class OptionalVal(Val): pass
class ZeroOrMoreVal(Val): pass
class OneOrMoreVal(Val): pass
class SequenceVal(Val): pass
class ChoiceVal(Val):
    def __init__(self, v, choice, name=None, ignore=False):
        super(ChoiceVal, self).__init__(v, name, ignore)
        self.choice = choice

class Expr(object):
    def __init__(self, data):
        self.data = data

    def parse(self, s):
        m, i = self.match(s)
        return m

    def __repr__(self):
        return repr_str("{}({!r})".format(type(self).__name__, self.data))

class AnyChar(Expr):
    def __init__(self): pass
    def __repr__(self): return repr_str("AnyChar()")
    def match(self, s, i=0):
        if i >= len(s): return Failure(i, self), i
        return AnyCharVal(s[i]), i + 1

class CharClass(Expr):
    def match(self, s, i=0):
        if i >= len(s) or s[i] not in self.data: return Failure(i, self), i
        return CharClassVal(s[i]), i + 1

class String(Expr):
    def match(self, s, i=0):
        ss = s[i:i+len(self.data)]
        if ss != self.data: return Failure(i, self), i
        return StringVal(ss), i + len(self.data)

class AndPredicate(Expr):
    def match(self, s, i=0):
        m, _ = self.data.match(s, i)
        return (Failure(i, self) if isfail(m) else None), i

class NotPredicate(Expr):
    def match(self, s, i=0):
        m, _ = self.data.match(s, i)
        return (Failure(i, self) if not isfail(m) else None), i

class Optional(Expr):
    def match(self, s, i=0):
        m, i = self.data.match(s, i)
        return OptionalVal([] if isfail(m) else [m]), i

class ZeroOrMore(Expr):
    def match(self, s, i=0):
        l = []
        while True:
            m, i = self.data.match(s, i)
            if isfail(m): return ZeroOrMoreVal(l), i
            if m is not None: l.append(m)

class OneOrMore(Expr):
    def match(self, s, i=0):
        l = []
        m, i = self.data.match(s, i)
        if isfail(m): return m, i
        while True:
            if m is not None: l.append(m)
            m, i = self.data.match(s, i)
            if isfail(m): return OneOrMoreVal(l), i

class Sequence(Expr):
    def match(self, s, i=0):
        orig_i = i
        l = []
        for expr in self.data:
            m, i = expr.match(s, i)
            if isfail(m): return m, orig_i
            if m is not None:
                l.append(m)
        if len(l) > 1:
            return SequenceVal(l), i
        return l[0] if l else None, i

class Choice(Expr):
    def match(self, s, i=0):
        furthest_fail = None
        for choice, expr in enumerate(self.data):
            m, i = expr.match(s, i)
            if not isfail(m):
                return ChoiceVal(m, choice), i
            if furthest_fail is None or m.i >= furthest_fail.i:
                furthest_fail = m
        return furthest_fail, i

class Nonterminal(Expr):
    def __init__(self, name, expr, ignore=False):
        self.name = name
        self.expr = expr
        self.ignore = ignore

    def match(self, s, i=0):
        m, i = self.expr.match(s, i)
        if m is not None:
            if not hasattr(m, "name"):
                m.name = self.name
            if not isfail(m):
                m.ignore = self.ignore
        return m, i

    def __repr__(self):
        return repr_str("Nonterminal({!r}, {!r})".format(self.name, self.expr))


def compile_grammar(grammar):
    m = peg_grammar.parse(grammar)
    if isfail(m): raise RuntimeError(str(m))

    definitions = m[1]
    identifiers = [str(d[1]) for d in definitions]
    if len(identifiers) > len(set(identifiers)):
        raise RuntimeError("duplicate definition")

    nts = {ident: Nonterminal(ident, None) for ident in identifiers}  # Forward declaration.
    for d in definitions:
        identifier, expr = str(d[1]), d[3]
        nts[identifier].expr = compile_expr(expr, nts)
        if d[0]: nts[identifier].ignore = True

    return nts[identifiers[0]]

def compile_expr(expr, nts):
    if not len(expr[1]):
        return compile_seq(expr[0], nts)
    return Choice([compile_seq(expr[0], nts)] + [compile_seq(s[1], nts) for s in expr[1]])

def compile_seq(seq, nts):
    if len(seq) == 0: return String("")
    if len(seq) == 1: return compile_prefix(seq[0], nts)
    return Sequence([compile_prefix(p, nts) for p in seq])

def compile_prefix(prefix, nts):
    predicate = {"&": AndPredicate,
                 "!": NotPredicate,
                  "": lambda s: s}[str(prefix[0])]
    return predicate(compile_suffix(prefix[1], nts))

def compile_suffix(suffix, nts):
    op = str(suffix[1])
    quantifier = {"?": Optional,
                  "*": ZeroOrMore,
                  "+": OneOrMore,
                  "{": lambda p: Sequence([p] * int(op[1:-1])),
                   "": lambda p: p}[op[:1]]
    return quantifier(compile_primary(suffix[0], nts))

def compile_primary(r, nts):
    if r.choice == 0:
        return nts[str(r)]
    elif r.choice == 1:
        return compile_expr(r[1], nts)
    elif r.choice == 2:
        return String("".join(char_to_str(ch) for ch in r[1]))
    elif r.choice == 3:
        return CharClass("".join(map(compile_char_range, r[1])))
    return AnyChar()

def compile_char_range(char_range):
    if char_range.choice == 0:
        start = ord(char_to_str(char_range[0]))
        stop = ord(char_to_str(char_range[2])) + 1
        return "".join(chr(c) for c in range(start, stop))
    elif char_range.choice == 1:
        return char_to_str(char_range.v)

def char_to_str(ch):
    if ch.choice == 0:  # Backslash.
        ch = str(ch[1])
        return {"n": "\n", "r": "\r", "t": "\t"}.get(ch, ch)
    elif ch.choice == 4:  # Literal.
        return str(ch)
    return chr(int(str(ch[1]), 16))  # Unicode escape.


def bootstrap_grammar():
    # Equivalent to peg_grammar_src, but directly expressed using primitives. For correctness
    # this grammar was semi-automatically generated from peg_grammar_src after the first
    # version was hand-written.
    eof         = NotPredicate(AnyChar())
    eol         = Choice([String("\r\n"), String("\n"), String("\r")])
    space       = Choice([String(" "), String("\t"), eol])
    comment     = Sequence([String("#"), ZeroOrMore(Sequence([NotPredicate(eol), AnyChar()])), eol])
    spacing     = Nonterminal("spacing", ZeroOrMore(Choice([space, comment])), ignore=True)
    dot         = Sequence([String("."), spacing])
    close_brace = Sequence([String("}"), spacing])
    open_brace  = Sequence([String("{"), spacing])
    close_paren = Sequence([String(")"), spacing])
    open_paren  = Sequence([String("("), spacing])
    close_angled_bracket = Sequence([String(">"), spacing])
    open_angled_bracket  = Sequence([String("<"), spacing])
    plus        = Sequence([String("+"), spacing])
    star        = Sequence([String("*"), spacing])
    question    = Sequence([String("?"), spacing])
    not_        = Sequence([String("!"), spacing])
    and_        = Sequence([String("&"), spacing])
    slash       = Sequence([String("/"), spacing])
    equals      = Sequence([String("="), spacing])
    semicolon   = Sequence([String(";"), spacing])
    hexchar     = CharClass("0123456789abcdefABCDEF")
    char        = Choice([Sequence([String("\\"), CharClass("nrt'\"[]\\")]),
                          Sequence([String("\\x"), Sequence([hexchar] * 2)]),
                          Sequence([String("\\u"), Sequence([hexchar] * 4)]),
                          Sequence([String("\\U"), Sequence([hexchar] * 8)]),
                          Sequence([NotPredicate(String("\\")), AnyChar()])])
    range_      = Choice([Sequence([char, String("-"), NotPredicate(String("]")), char]), char])
    delim       = (lambda start, inner, stop:
                       Sequence([String(start),
                                 ZeroOrMore(Sequence([NotPredicate(String(stop)), inner])),
                                 String(stop), spacing]))
    class_      = delim("[", range_, "]")
    literal     = Choice([delim("'", char, "'"), delim('"', char, '"')])
    ident_start = CharClass(string.ascii_letters + "_")
    ident_cont  = Choice([ident_start, CharClass(string.digits)])
    identifier  = Sequence([ident_start, ZeroOrMore(ident_cont), spacing])
    integer     = OneOrMore(CharClass(string.digits))

    expression      = Nonterminal("expression", None) # Forward declaration, needed for recursion.
    primary         = Choice([Sequence([identifier, NotPredicate(equals)]),
                              Sequence([open_paren, expression, close_paren]),
                              Sequence([open_angled_bracket, expression, close_angled_bracket, expression]),
                              literal, class_, dot])
    repeat          = Sequence([open_brace, integer, close_brace])
    suffix          = Sequence([primary, Optional(Choice([question, star, plus, repeat]))])
    prefix          = Sequence([Optional(Choice([and_, not_])), suffix])
    sequence        = ZeroOrMore(prefix)
    expression.expr = Sequence([sequence, ZeroOrMore(Sequence([slash, sequence]))])
    definition      = Sequence([Optional(semicolon), identifier, equals, expression])
    grammar         = Sequence([spacing, OneOrMore(definition), eof])
    return grammar

peg_grammar = bootstrap_grammar()




if __name__ == "__main__":
    # Demo, simple calculator.
    grammar = compile_grammar(r"""
    line = expr eof
    expr = _ factor ([+-] _ factor)*
    factor = exponent (("//" / [*/%]) _ exponent)*
    exponent = primary ("**" _ primary)*
    number = &("."? [0-9]) [0-9]* ("." [0-9]*)? _  # The first part is to make sure this doesn't match ".".
    primary = "(" _ expr ")" _ / number / "-" _ primary
    ; _     = (" " / "\t" / "\r\n" / "\n" / "\r")*
    eof = !.
    """)

    def eval_expr(expr):
        r = eval_factor(expr[1])
        for f in expr[2]:
            if str(f[0]) == "+": r += eval_factor(f[2])
            else:                r -= eval_factor(f[2])
        return r

    def eval_factor(factor):
        r = eval_exponent(factor[0])
        for p in factor[1]:
            if str(p) == "*":    r *= eval_exponent(p[2])
            elif str(p) == "//": r //= eval_exponent(p[2])
            elif str(p) == "/":  r /= eval_exponent(p[2])
            else:                r %= eval_exponent(p[2])
        return r

    def eval_exponent(exponent):
        # Right-to-left associativity.
        exps = reversed([exponent[0]] + [e[2] for e in exponent[1]])
        r = eval_primary(next(exps))
        for e in exps:
            r = eval_primary(e) ** r
        return r


    def eval_primary(primary):
        if primary.choice == 0:   return eval_expr(primary[2])
        elif primary.choice == 1: return [int, float][len(primary[1]) > 0](str(primary))
        else:                     return -eval_primary(primary[2])

    def eval_str(s):
        m = grammar.parse(s)
        if isfail(m):
            raise RuntimeError(str(m))
        return eval_expr(m)


    print(eval_str("5*3+ 2 - 3 * (3)"))
