/**
 * 
 */
package com.bluelightning.tools.transpiler;

import java.util.HashMap;

/**
 * @author lintondf
 *
 */
public class ReservedWords {
	
	HashMap<String, String> words = new HashMap<>();
	
	public ReservedWords() {}
	
	String rewrite( String symbol ) {
		String r = words.get(symbol);
		if (r != null)
			return r;
		return symbol;
	}

}
/** Go
break        default      func         interface    select
case         defer        go           map          struct
chan         else         goto         package      switch
const        fallthrough  if           range        type
continue     for          import       return       var
 */
/** Java
abstract	assert	boolean	break	byte	case
catch	char	class	const	continue	default
double	do	else	enum	extends	false
final	finally	float	for	goto	if
implements	import	instanceof	int	interface	long
native	new	null	package	private	protected
public	return	short	static	strictfp	super
switch	synchronized	this	throw	throws	transient
true	try	void	volatile	while
 */
/** C++
 * asm	else	new	this
auto	enum	operator	throw
bool	explicit	private	true
break	export	protected	try
case	extern	public	typedef
catch	false	register	typeid
char	float	reinterpret_cast	typename
class	for	return	union
const	friend	short	unsigned
const_cast	goto	signed	using
continue	if	sizeof	virtual
default	inline	static	void
delete	int	static_cast	volatile
do	long	struct	wchar_t
double	mutable	switch	while
dynamic_cast	namespace	template
And	bitor	not_eq	xor
and_eq	compl	or	xor_eq
bitand	not	or_eq
 */
/** Rust
  "as",
  "use",
  "extern crate",
  "break",
  "const",
  "continue",
  "crate",
  "else",
  "if",
  "if let",
  "enum",
  "extern",
  "false",
  "fn",
  "for",
  "if",
  "impl",
  "in",
  "for",
  "let",
  "loop",
  "match",
  "mod",
  "move",
  "mut",
  "pub",
  "impl",
  "ref",
  "return",
  "Self",
  "self",
  "static",
  "struct",
  "super",
  "trait",
  "true",
  "type",
  "unsafe",
  "use",
  "where",
  "while",
  "abstract",
  "alignof",
  "become",
  "box",
  "do",
  "final",
  "macro",
  "offsetof",
  "override",
  "priv",
  "proc",
  "pure",
  "sizeof",
  "typeof",
  "unsized",
  "virtual",
  "yield"
*/
/** Octave

__FILE__	__LINE__	break
case	catch	classdef
continue	do	else
elseif	end	end_try_catch
end_unwind_protect	endclassdef	endenumeration
endevents	endfor	endfunction
endif	endmethods	endparfor
endproperties	endswitch	endwhile
enumeration	events	for
function	global	if
methods	otherwise	parfor
persistent	properties	return
switch	try	until
unwind_protect	unwind_protect_cleanup	while
 */
/** Julia
"begin","while","if","for","try","return","break","continue","function","macro",
            "quote","let","local","global","const","do","struct","module","baremodule",
            "using","import","export"
 */
