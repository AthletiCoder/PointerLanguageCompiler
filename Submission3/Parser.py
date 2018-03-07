import sys
import ply.lex as lex
import ply.yacc as yacc
#Final
# think about negative numbers
#think about wrong variable names
var = 0
pointer = 0
assignments = 0
var_array = []
pointer_array = []
error = 0
assignment_set = []
global no_done
global one_time
global output

output_to_file = ""

no_done = 0
one_time = 0
class Tree:
	node = None
	lhs = None
	rhs = None
	depth = 0

output = []

tokens = (
		'MAIN', 'VOID', 'TYPE', 'LPAREN', 'RPAREN', 'LFLOWER', 'RFLOWER', 'SEMI_COLON', 'COMMA', 'NAME', 'STAR', 'EQUAL', 'AND', 'NUMBER', 'COMMENT', 'PLUS', 'MINUS', 'DIVIDE', 'IF', 'ELSE', 'WHILE', 'NOT_EQUAL', 'DOUBLE_EQUAL', 'GTHAN', 'LTHAN', 'GTHAN_EQUAL', 'LTHAN_EQUAL', 'COND_AND', 'COND_OR', 'ELSE_IF'
)

t_ignore = " \t\n"

t_PLUS = r'\+'
t_MINUS = r'-'
t_DIVIDE = r'/'

t_LPAREN = r'\('
t_RPAREN = r'\)'

t_LFLOWER = r'\{'
t_RFLOWER = r'\}'

t_SEMI_COLON = r'\;'
t_COMMA = r'\,'
t_STAR = r'\*'

t_DOUBLE_EQUAL = r'=='
t_NOT_EQUAL = r'!='
t_GTHAN_EQUAL = r'>='
t_LTHAN_EQUAL = r'<='
t_GTHAN = r'<'
t_LTHAN = r'>'

t_EQUAL = r'='
t_COND_AND = r'&&'
t_COND_OR = r'\|\|'
t_AND = r'&'
t_ELSE_IF = r'else\s+if' 

def t_COMMENT(t):
	r'(//)[^\n\r]*[\n\r]'
	return t

def t_NAME(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	if t.value == 'void':
		t.type = 'VOID'
	elif t.value == 'int':
		t.type = 'TYPE'
	elif t.value == 'if':
		t.type = 'IF'
	elif t.value == 'else':
		t.type = 'ELSE'
	elif t.value == 'while':
		t.type = 'WHILE'
	elif t.value == 'main':
		t.type = 'MAIN'
	elif t.value == 'and':
		t.type = 'COND_AND'
	elif t.value == 'or':
		t.type = 'COND_OR'
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

precedence = (
		('left', 'PLUS', 'MINUS'),
		('left', 'STAR', 'DIVIDE'),
		('right', 'UMINUS'),
		('right', 'STAR_POINTER', 'AND_POINTER'),
		('right', 'IF', 'ELSE')
)


def p_program(p):
	'program : VOID MAIN LPAREN RPAREN LFLOWER code RFLOWER'

def p_code(p):
	"""
	code : line code
		 | line
	"""

def p_while_section(p):
	"""
	while_section : WHILE util
	"""

def p_if_else_section(p):
	"""
	if_else_section : if_section elif_section else_section
					| if_section else_section
					| if_section
	"""
	if p[1] == None:
		print("if")
	elif p[2] == None:
		print("else")
	elif p[3] == None:
		print("elif")

def p_util(p):
	"""
	util : LPAREN complex_conditional RPAREN LFLOWER code RFLOWER
		 | LPAREN complex_conditional RPAREN line
	"""

def p_if_section(p):
	"""
	if_section : IF util
	"""
	print("if section")

def p_elif_section(p):
	"""
	elif_section : ELSE_IF util elif_section
				 | ELSE_IF util
	"""
	print("else if section")

def p_else_section(p):
	"""
	else_section : ELSE LFLOWER code RFLOWER
				 | ELSE line
	"""
	print("else section")

def p_complex_conditional(p):
	"""
	complex_conditional : conditional COND_AND complex_conditional
					    | conditional COND_OR complex_conditional
					    | conditional
	"""

def p_conditional(p):
	"""
	conditional : expression DOUBLE_EQUAL conditional
				| expression NOT_EQUAL conditional
				| expression GTHAN conditional
				| expression LTHAN conditional
				| expression GTHAN_EQUAL conditional
				| expression LTHAN_EQUAL conditional
				| expression
	"""

def p_line(p):
	"""
	line : dec SEMI_COLON
		 | assgn COMMA
		 | assgn SEMI_COLON
		 | COMMENT
		 | if_else_section
		 | while_section
	"""

def p_dec(p):
	"""
	dec : TYPE vars
	"""

def p_vars(p):
	"""
	vars : NAME COMMA vars
		 | pointer_other COMMA vars
		 | NAME
		 | pointer_other
	"""
	global pointer
	global var
	global pointer_array
	global var_array
	if p[1] is None:
		pointer = pointer+1
	else:
		var = var+1

def p_assgn(p):
	"""
	assgn : pointer EQUAL expression
		  | name EQUAL not_number_expression
	"""
	global assignments
	global no_done
	if one_time == 1 and no_done < len(output):
		if p[1] is not None:
			output[no_done].append(p[1])
		if p[3] is not None:
			output[no_done].append(p[3])
		output[no_done].append(p[2])
		no_done = no_done+1
	else:
		assignments = assignments+1

def p_name(p):
	"""
	name : NAME
	"""
	if one_time == 1 and no_done < len(output):
		output[no_done].append(p[1])

def p_not_number_expression(p):
	"""
	not_number_expression : not_number_expression PLUS number_expression
						  |	not_number_expression MINUS number_expression
						  | not_number_expression STAR number_expression
						  | not_number_expression DIVIDE number_expression
						  | number_expression PLUS not_number_expression
						  | number_expression MINUS not_number_expression
						  | number_expression STAR not_number_expression
						  | number_expression DIVIDE not_number_expression
						  | not_number_expression PLUS not_number_expression
						  | not_number_expression MINUS not_number_expression
						  | not_number_expression STAR not_number_expression
						  | not_number_expression DIVIDE not_number_expression
	"""
	if one_time == 1 and no_done < len(output):
		output[no_done].append(p[2])

def p_not_number_expression_basic(p):
	"""
	not_number_expression : NAME
						  | and
						  | pointer
	"""
	global output
	if one_time == 1 and no_done < len(output):
		if p[1] is not None:
			output[no_done].append(p[1])

def p_not_number_expression_group(p):
	"""
	not_number_expression : LPAREN not_number_expression RPAREN
	"""

def p_not_number_expression_uminus(p):
	'not_number_expression : MINUS not_number_expression %prec UMINUS'
	global output
	if one_time == 1 and no_done < len(output):
		output[no_done].append("u"+p[1])


def p_number_expression(p):
	"""
	number_expression : number_expression PLUS number_expression
					  | number_expression MINUS number_expression
					  | number_expression STAR number_expression
					  | number_expression DIVIDE number_expression
	"""
	global output
	if one_time == 1 and no_done < len(output):
		output[no_done].append(p[2])

def p_number_expression_group(p):
	"""
	number_expression : LPAREN number_expression RPAREN
	"""
	
def p_number_expression_uminus(p):
	"""
	number_expression : MINUS number_expression %prec UMINUS
	"""
	global output
	if one_time == 1 and no_done < len(output):
		output[no_done].append("u"+p[1])

def p_number_expression_basic(p):
	"""
	number_expression : NUMBER
	"""
	if one_time == 1 and no_done < len(output):
		if p[1] is not None:
			output[no_done].append(p[1])

def p_expression_advanced(p):
	"""
	expression : expression PLUS expression
			   | expression MINUS expression
			   | expression STAR expression
			   | expression DIVIDE expression
	"""
	global output
	if one_time == 1 and no_done < len(output):
		output[no_done].append(p[2])

def p_expression_group(p):
	'expression : LPAREN expression RPAREN'

def p_expression_uminus(p):
	'expression : MINUS expression %prec UMINUS'
	global output
	if one_time == 1 and no_done < len(output):
		# print("u"+p[1])
		output[no_done].append("u"+p[1])

def p_expression_basic(p):
	"""
	expression : NUMBER
			   | NAME
			   | pointer
			   | and
	"""
	global output
	if one_time == 1 and no_done < len(output):
		if p[1] is not None:
			output[no_done].append(p[1])
def p_pointer(p):
	"""
	pointer : STAR pointer %prec STAR_POINTER
			| STAR and %prec STAR_POINTER
			| STAR NAME %prec STAR_POINTER
	"""
	global output
	if one_time == 1 and no_done < len(output):
		if p[2] is not None:
			output[no_done].append(p[2])
			output[no_done].append("p"+p[1])
		else:
			output[no_done].append("p"+p[1])

def p_and(p):
	"""
	and : AND and %prec AND_POINTER
		| AND NAME %prec AND_POINTER
		| AND pointer %prec AND_POINTER
	"""
	global output
	if one_time == 1 and no_done < len(output):
		if p[2] is not None:
			output[no_done].append(p[2])
			output[no_done].append("a"+p[1])
		else:
			output[no_done].append("a"+p[1])


def p_pointer_other(p):
	"""
	pointer_other : STAR pointer %prec STAR_POINTER
				  | STAR NAME %prec STAR_POINTER
	"""
	
def p_error(p):
	global error
	if p:
		print("syntax error at {0}".format(p.value))
		error = 1
	else:
		print("syntax error at EOF")
		error = 1

def add_to_tree(tree, output, depth):
	temp = output.pop()
	tree.node = temp
	tree.depth = depth
	if temp == '+' or temp == '-' or temp == '/' or temp == '*' or temp == '=':
		tree.rhs = Tree()
		tree.lhs = Tree()
		add_to_tree(tree.rhs, output, depth+1)
		add_to_tree(tree.lhs, output, depth+1)
	elif temp == 'p*' or temp == 'a&' or temp == 'u-':
		tree.rhs = Tree()
		add_to_tree(tree.rhs, output, depth+1)

def print_tree(tree):
	if tree.lhs is not None:
		print_tree(tree.lhs)
	print(tree.node)
	if tree.rhs is not None:
		print_tree(tree.rhs)

def print_parse_tree(tree):
	t = 0
	comma = 0

	global output_to_file

	tabs = tree.depth*"\t"
	tabs2 = tabs+"\t"
	
	if tree.node == '=':
		output_to_file += tabs+"ASGN"+"\n"
		output_to_file += tabs+"("+"\n"
	elif tree.node == '+':
		comma = 1
		output_to_file += tabs+"PLUS"+"\n"
		output_to_file += tabs+"("+"\n"
	elif tree.node == '-':
		comma = 1
		output_to_file += tabs+"MINUS"+"\n"
		output_to_file += tabs+"("+"\n"
	elif tree.node == '/':
		comma = 1
		output_to_file += tabs+"DIV"+"\n"
		output_to_file += tabs+"("+"\n"
	elif tree.node == '*':
		comma = 1
		output_to_file += tabs+"MUL"+"\n"
		output_to_file += tabs+"("+"\n"
	elif tree.node == 'p*':
		output_to_file += tabs+"DEREF"+"\n"
		output_to_file += tabs+"("+"\n"
	elif tree.node == 'a&':
		output_to_file += tabs+"ADDR"+"\n"
		output_to_file += tabs+"("+"\n"
	elif tree.node == 'u-':
		output_to_file += tabs+"UMINUS"+"\n"
		output_to_file += tabs+"("+"\n"
	elif isinstance(tree.node, int):
		output_to_file += tabs+"CONST("+str(tree.node)+")"+"\n"
		t = 1
	else:
		output_to_file += tabs+"VAR("+tree.node+")"+"\n"
		t = 1

	if tree.lhs is not None:
		print_parse_tree(tree.lhs)
		if t == 0:
			output_to_file += tabs+'\t'+','+"\n"
	if tree.rhs is not None:
		print_parse_tree(tree.rhs)

	if t == 0:
		output_to_file += tabs+")"+"\n"

def process(data):
	lex.lex()
	yacc.yacc()
	yacc.parse(data)

if __name__ == "__main__":
	filename = sys.argv[-1]
	infile = open(filename, "r")
	lines = infile.read()

	process(lines)
	one_time = 1

	for i in range(assignments):
		output.append([])

	if error == 0:
		print("Successfully parsed!")
		print("Checkout output.txt")
	process(lines)
	k = 0
	for i in output:
		my_tree = Tree()
		add_to_tree(my_tree, i, 0)
		print_parse_tree(my_tree)
		if k < len(output)-1:
			output_to_file += '\n'
		k += 1

	print(output_to_file, file=open("output.txt", "w"))


