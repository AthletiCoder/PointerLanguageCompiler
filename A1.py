import sys
import ply.lex as lex
import ply.yacc as yacc
#Final
var = 0
pointer = 0
assignments = 0
var_array = []
pointer_array = []
error = 0

tokens = (
        'MAIN', 'TYPE', 'LPAREN', 'RPAREN', 'LFLOWER', 'RFLOWER', 'SEMI_COLON', 'COMMA', 'NAME', 'STAR', 'EQUAL', 'AND', 'NUMBER', 'COMMENT'
)

# t_ignore = r'(//)[^\n\r]*[\n\r] | \t\n'
t_ignore = " \t\n"
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_LFLOWER = r'\{'
t_RFLOWER = r'\}'

t_SEMI_COLON = r'\;'
t_COMMA = r'\,'
t_STAR = r'\*'
t_EQUAL = r'='
t_AND = r'&'

# t_TYPE = r'int | void'
# t_MAIN = r'main'
# t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_COMMENT(t):
	r'(//)[^\n\r]*[\n\r]'
	return t

def t_NAME(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	if t.value == 'int' or t.value =='void':
		t.type = 'TYPE'
	elif t.value == 'main':
		t.type = 'MAIN'
	return t

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_error(t): 
	print("Syntax error at '%s'" % t.value[0])
	t.lexer.skip(1)

def p_program(p):
	'program : TYPE MAIN LPAREN RPAREN LFLOWER code RFLOWER'

def p_code(p):
	"""
	code : line code
		 | line
	"""

def p_line(p):
	"""
	line : dec SEMI_COLON
		 | assgn COMMA
		 | assgn SEMI_COLON
		 | COMMENT
	"""

def p_dec(p):
	"""
	dec : TYPE vars
	"""

def p_vars(p):
	"""
	vars : NAME COMMA vars
		 | STAR pointer COMMA vars
		 | NAME
		 | STAR pointer
	"""
	global pointer
	global var
	global pointer_array
	global var_array
	if p[1]	 == '*':
		pointer = pointer+1
		pointer_array.append(p[2])
	else:
		var = var+1
		var_array.append(p[1])
# def p_assn(p):
# 	"""
# 	assn : NAME EQUAL NAME
# 		 | STAR NAME EQUAL STAR NAME
# 		 | NAME EQUAL AND NAME
# 		 | STAR NAME EQUAL NAME
# 	"""
# 	# if p[1] == '*' and p[4] == '*':
# 	# 	assignments = assignments+1
# 	# elif ((p[1] in var_array) and (p[3] in var_array)):
# 	# 	assignments++
# 	# elif ((p[3] == '&') and (p[1] in pointer_array) and (p[4] in var_array)):
# 	# 	assignments++
# 	# else:
# 	# 	error = 1
# 	global assignments
# 	assignments = assignments+1
def p_pointer(p):
	"""
	pointer : STAR pointer
			| NAME
	"""
def p_assgn(p):
	"""
	assgn : STAR pointer EQUAL NUMBER
		  | NAME EQUAL NAME
		  | STAR pointer EQUAL STAR pointer
		  | NAME EQUAL AND NAME
		  | STAR pointer EQUAL NAME
	"""
	global assignments
	assignments = assignments+1

def p_error(p):
	if p:
		print("syntax error at {0}".format(p.value))
		error = 1
	else:
		print("syntax error at EOF")
		error = 1

def process(data):
	lex.lex()
	yacc.yacc()
	yacc.parse(data)

if __name__ == "__main__":
	# print("Enter the Equation")
	filename = sys.argv[-1]
	infile = open(filename, "r")
	lines = infile.read()
	# data = sys.stdin.readline()
	process(lines)
	if error==0:
		print(var)
		print(pointer)
		print(assignments)

