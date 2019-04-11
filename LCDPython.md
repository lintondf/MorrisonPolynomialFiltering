# LCD Python #
## Annotated Python Dialect for Multi-Target Transpilation ##

## Rules ##
1. All variables must be 'declared' in annotations, e.g. 
	
    '''@t : float'''
	1. Optional comments can be included after '|', e.g. 
	
	'''@t : float | time stamp'''
2. Python docstrings using double quotes '"""' are copied/transliterated to the generated target sources
3. Class and function docstrings must immediately follow the declaration with the exception of 'def __init__' docstrings which must follow any 'super' statement.
4. References to .shape elements are generally transpiled to unsigned values in target languages.  Cast them using int() when using as int values.
5. Python negative array references should not be used.
	1. Instead of A[-1] use A[A.shape[0]-1] 


# Installation @
## Windows 10 / Visual Studio 2017 ##

### javabridge ##

WORK ON THIS LATER; EXAMPLE EXCEPTIONS

run vcvars64.bat
insure cl.exe in PATH
set MSSdk=1
set DISTUTILS_USE_SDK=1
pip install javabridge