# LCD Python #
## Annotated Python Dialect for Multi-Target Transpilation ##

## Rules ##
1. All variables must be 'declared' in annotations, e.g. 
	
    '''@t : float'''
	1. Optional comments can be included after '|', e.g. 
	
	'''@t : float | time stamp'''
2. Python docstrings using double quotes '"""' are copied/transliterated to the generated target sources
3. Class and function docstrings must immediately follow the declaration with the exception of 'def __init__' docstrings which must follow any 'super' statement.
4. References to .shape elements should be manually cast to integer