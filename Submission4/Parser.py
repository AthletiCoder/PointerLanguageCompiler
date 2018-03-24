import sys
import copy
import ply.lex as lex
import ply.yacc as yacc
import settings
import trees
import blocks

class Tree:
	node = None
	lhs = None
	rhs = None
	depth = 0


tokens = (
		'VOID', 'TYPE', 'LPAREN', 'RPAREN', 'LFLOWER', 'RFLOWER', 'SEMI_COLON', 'COMMA', 'NAME', 'STAR', 'EQUAL', 'AND', 'INT', 'COMMENT', 'PLUS', 'MINUS', 'DIVIDE', 'IF', 'ELSE', 'WHILE', 'NOT_EQUAL', 'DOUBLE_EQUAL', 'GTHAN', 'LTHAN', 'GTHAN_EQUAL', 'LTHAN_EQUAL', 'COND_AND', 'COND_OR', 'NOT', 'FLOAT', 'RETURN'
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
t_NOT = r'!'

def t_COMMENT(t):
	r'(//)[^\n\r]*[\n\r]'
	# r'\/\*+((([^\*])+)|([\*]+(?!\/)))[*]+\/'
	return t

def t_NAME(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	if t.value == 'void':
		t.type = 'VOID'
	elif t.value == 'int' or t.value == 'float':
		t.type = 'TYPE'
	elif t.value == 'if':
		t.type = 'IF'
	elif t.value == 'else':
		t.type = 'ELSE'
	elif t.value == 'while':
		t.type = 'WHILE'
	elif t.value == 'and':
		t.type = 'COND_AND'
	elif t.value == 'or':
		t.type = 'COND_OR'
	elif t.value == 'return':
		t.type = 'RETURN'
	return t

def t_FLOAT(t):
	r'\d*\.\d+ | \d+\.\d*'
	try:
		t.value = float(t.value)
	except ValueError:
		print("Float value too large %f", t.value)
		t.value = 0
	return t

def t_INT(t):
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
		('left', 'COND_OR'),
		('left', 'COND_AND'),
		('right', 'NOT'),
		('left', 'NOT_EQUAL', 'DOUBLE_EQUAL'),
		('left', 'GTHAN', 'GTHAN_EQUAL'),
		('left', 'LTHAN', 'LTHAN_EQUAL'),
		('left', 'PLUS', 'MINUS'),
		('left', 'STAR', 'DIVIDE'),
		('right', 'UMINUS'),
		('right', 'STAR_POINTER', 'AND_POINTER'),
		('right', 'IF', 'ELSE')
)


# def p_program(p):
# 	'program : VOID MAIN LPAREN RPAREN LFLOWER code RFLOWER'
# 	p[0] = p[6]
# 	settings.output_list = p[0]

#Changed
settings.output_list = []
def p_program(p):
	"""
	program : VOID func_name LPAREN arguments RPAREN LFLOWER code RFLOWER program
			| TYPE func_name LPAREN arguments RPAREN LFLOWER code RFLOWER program
			| VOID func_name LPAREN arguments RPAREN SEMI_COLON program
			| TYPE func_name LPAREN arguments RPAREN SEMI_COLON program
			| VOID func_name LPAREN RPAREN LFLOWER code RFLOWER program
			| TYPE func_name LPAREN RPAREN LFLOWER code RFLOWER program
			| VOID func_name LPAREN RPAREN SEMI_COLON program
			| TYPE func_name LPAREN RPAREN SEMI_COLON program
			| dec SEMI_COLON program
			| epsilon
	"""
	if len(p) == 10:
		p[0] = [p[7], p[4], p[1], p[2]]
		settings.output_list += p[0]
	elif len(p) == 8:
		p[0] = [p[4], p[1], p[2]]
		settings.output_list += p[0]
	elif len(p) == 9:
		p[0] = [p[7], [], p[1], p[2]]
		settings.output_list += p[0]
	elif len(p) == 7:
		p[0] = [[], p[1], p[2]]
		settings.output_list += p[0]
	elif len(p) == 4:
		p[0] = p[1]
		
def p_func_name(p):
	"""
	func_name : NAME
			  | func_pointer
	"""
	p[0] = p[1]

def p_func_pointer(p):
	"""
	func_pointer : STAR NAME %prec STAR_POINTER
				 | STAR func_pointer %prec STAR_POINTER
	"""
	p[0] = p[1]+p[2]

# storing in the reverse order
def p_arguments(p):
	"""
	arguments : TYPE func_name COMMA arguments
			  | TYPE func_name
	"""
	if len(p) == 3:
		p[0] = [[p[1], p[2]]]
	else:
		p[0] = p[4]+[[p[1], p[2]]]

def p_epsilon(p):
	'epsilon : '

def p_code(p):
	"""
	code : line code
		 | line
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	elif len(p) == 3:
		p[0] = [p[1]]+p[2]
	# print("p_code")

def p_line_dec(p):
	"""
	line : dec SEMI_COLON
		 | COMMENT
	"""
	if len(p) == 3:
		p[0] = p[1]

def p_dec(p):
	"""
	dec : TYPE vars
	"""
	p[0] = [p[1]]+[p[2]]

def p_vars(p):
	"""
	vars : NAME COMMA vars
		 | func_pointer COMMA vars
		 | NAME
		 | func_pointer
	"""
	if len(p) == 4:
		p[0] = [p[1]]+p[3]
	else:
		p[0] = [p[1]]


def p_line(p):
	"""
	line : assgn SEMI_COLON
		 | if_else_section
		 | while_section
	"""
	if len(p) == 3:
		p[0] = p[1]
	elif p[1] is not None:
		p[0] = p[1]
	
def p_assgn_expression(p):
	"""
	assgn : assgn_pointer EQUAL expression
	"""
	temp = p[3]+["float*"]
	p[0] = [p[2]]+p[1]+temp

def p_assgn_pointer_nt(p):
	"""
	assgn_pointer : STAR assgn_pointer %prec STAR_POINTER
	"""
	p[0] = ["p"+p[1]]+p[2]

def p_assgn_pointer_t(p):
	"""
	assgn_pointer : STAR NAME %prec STAR_POINTER
	"""
	p[0] = ["p"+p[1]]+[p[2]]

def p_expression_basic_t(p):
	"""
	expression : INT
			   | FLOAT
	"""
	p[0] = [p[1]]

def p_expression_basic_nt(p):
	"""
	expression : assgn_pointer
			   | pointer_and_var
	"""
	p[0] = p[1]

def p_pointer_and_var(p):
	"""
	pointer_and_var : STAR and %prec STAR_POINTER
					| STAR pointer_and_var %prec STAR_POINTER
	"""
	p[0] = ["p"+p[1]]+p[2]

def p_and(p):
	"""
	and : AND NAME %prec AND_POINTER
	"""
	p[0] = ["a"+p[1]]+[p[2]]

def p_expression_advanced(p):
	"""
	expression : expression PLUS expression
			   | expression MINUS expression
			   | expression STAR expression
			   | expression DIVIDE expression
	"""
	p[0] = [p[2]]+p[3]+p[1]

def p_expression_group(p):
	'expression : LPAREN expression RPAREN'
	p[0] = p[2]

def p_expression_uminus(p):
	'expression : MINUS expression %prec UMINUS'
	p[0] = ["u"+p[1]]+p[2]

# change func_name to NAME and assgn pointer if ast should be drawn for function calls like ***func()
def p_function_call(p):
	"""
	expression : func_name LPAREN parameters RPAREN
			   | func_name LPAREN RPAREN
	"""
	if len(p) == 4:
		p[0] = [p[1]]
	else:
		p[0] = [p[3], p[1]]
# remember the reverse order
def p_parameters_name(p):
	"""
	parameters : NAME COMMA parameters
			   | NAME
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[3]+[p[1]]

def p_parameters_expression(p):
	"""
	parameters : expression COMMA parameters
			   | expression
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[3]+[p[1]] 


# def p_assgn_float_expression(p):
# 	"""
# 	assgn : assgn_pointer EQUAL float_expression
# 	"""
# 	temp = p[3]+["float*"]
# 	p[0] = [p[2]]+p[1]+temp
# 	# print("p_assgn")


#come back and check this after writing code for creating tuples at the latest
def p_function_call_line(p):
	"""
	line : NAME LPAREN parameters RPAREN SEMI_COLON
		 | NAME LPAREN RPAREN SEMI_COLON
		 | return_line
	"""
	if len(p) == 6:
		p[0] = [p[3]]+[p[1]]
	elif len(p) == 5:
		p[0] = [p[1]]
	else:
		p[0] = p[1]

def p_return_line(p):
	"""
	return_line : RETURN expression SEMI_COLON
				| RETURN SEMI_COLON
	"""
	if len(p) == 4:
		p[0] = [p[2], p[1]]
	else:
		p[0] = [p[1]]


def p_while_section(p):
	"""
	while_section : WHILE LPAREN complex_conditional RPAREN LFLOWER code RFLOWER
				  | WHILE LPAREN complex_conditional RPAREN line
	"""
	if len(p) == 6:
		p[0] = [[p[5]], p[3],"while"]
	elif len(p) == 8:
		p[0] = [p[6], p[3],"while"]

def p_if_else_section(p):
	"""
	if_else_section : if_section else_section
					| if_section
	"""
	if len(p) == 3:
		p[0] = p[1]+[p[2]]+["if"]
	else:
		p[0] = p[1]+["if"]

def p_if_section(p):
	"""
	if_section : IF LPAREN complex_conditional RPAREN LFLOWER code RFLOWER
		 	   | IF LPAREN complex_conditional RPAREN line
	"""
	if len(p)==6:
		p[0] = [p[3], [p[5]]]
	elif len(p)==8:
		p[0] = [p[3], p[6]]
def p_else_section(p):
	"""
	else_section : ELSE after_else
	"""
	p[0] = p[2] 

def p_after_else(p):
	"""
	after_else : LFLOWER code RFLOWER
			   | line
	"""
	if len(p) == 4:
		p[0] = p[2]
	else:
		p[0] = [p[1]]

def p_complex_conditional(p):
	"""
	complex_conditional : complex_conditional COND_AND complex_conditional
					    | complex_conditional COND_OR complex_conditional
					    | conditional
	"""
	if len(p) == 4:
		# p[0] = p[1]+p[3]+[p[2]]
		p[0] = [p[2]]+p[3]+p[1]
	else:
		p[0] = p[1]

def p_complex_group(p):
	"""
	complex_conditional : LPAREN complex_conditional RPAREN
						| NOT complex_conditional
	"""
	if len(p) == 4:
		p[0] = p[2]
	else:
		p[0] = [p[1]]+p[2]

def p_conditional(p):
	"""
	conditional : expression DOUBLE_EQUAL expression
				| expression NOT_EQUAL expression
				| expression GTHAN expression
				| expression LTHAN expression
				| expression GTHAN_EQUAL expression
				| expression LTHAN_EQUAL expression
	"""
	if len(p) == 4:
		# p[0] = p[1]+p[3]+[p[2]]
		p[0] = [p[2]]+p[3]+p[1]
	# else:
	# 	p[0] = p[1]

# def p_multi_assign(p):
# 	"""
# 	multi_assign : assgn
# 	"""
# 	if len(p) == 2:
# 		p[0] = p[1]



# def p_float_expression_advanced(p):
# 	"""
# 	float_expression : expression PLUS float_expression
# 					 | expression MINUS float_expression
# 					 | expression STAR float_expression
# 					 | expression DIVIDE float_expression
# 					 | float_expression PLUS expression
# 					 | float_expression MINUS expression
# 					 | float_expression STAR expression
# 					 | float_expression DIVIDE expression
# 					 | float_expression PLUS float_expression
# 					 | float_expression MINUS float_expression
# 					 | float_expression STAR float_expression
# 					 | float_expression DIVIDE float_expression
# 	"""
# 	p[0] = [p[2]]+p[3]+p[1]

# def p_float_expression_group(p):
# 	'float_expression : LPAREN float_expression RPAREN'
# 	p[0] = p[2]

# def p_float_expression_uminus(p):
# 	'float_expression : MINUS float_expression %prec UMINUS'
# 	p[0] = ["u"+p[1]]+p[2]

# def p_float_exp_basic(p):
# 	"""
# 	float_expression : FLOAT
# 	"""
# 	p[0] = [p[1]]

# def p_pointer_term(p):
# 	"""
# 	pointer : STAR NAME %prec STAR_POINTER
# 	"""
# 	p[0] = ["p"+p[1]]+[p[2]]
# def p_pointer_nt(p):
# 	"""
# 	pointer : STAR pointer %prec STAR_POINTER
# 			| STAR and %prec STAR_POINTER
# 	"""
# 	p[0] = ["p"+p[1]]+p[2]

# def p_and(p):
# 	"""
# 	and : AND NAME %prec AND_POINTER
# 	"""
# 	p[0] = ["a"+p[1]]+[p[2]]

# def p_and_nt(p):
# 	"""
# 	and : AND and %prec AND_POINTER
# 		| AND pointer %prec AND_POINTER
# 	"""
# 	p[0] = ["a"+p[1]]+p[2]	

# def p_pointer_other_term(p):
# 	"""
# 	pointer_other : STAR NAME %prec STAR_POINTER
# 	"""
# 	p[0] = ["p"+p[1]]+[p[2]]
# def p_pointer_other_nt(p):
# 	"""
# 	pointer_other : STAR pointer %prec STAR_POINTER
# 	"""
# 	p[0] = ["p"+p[1]]+p[2]



def p_error(p):
	if p:
		print("syntax error at {0}".format(p.value))
		settings.error = 1
	else:
		print("syntax error at EOF")
		settings.error = 1

def process(data):
	lex.lex()
	yacc.yacc()
	yacc.parse(data)

if __name__ == "__main__":
	filename = sys.argv[-1]
	infile = open(filename, "r")
	lines = infile.read()
	settings.init_global()

	process(lines)
	
	if settings.error == 0:
		ast_filename = filename+".ast"
		print("Successfully parsed!")
		print("Checkout ast_output.txt for AST")
		print("Checkout cfg_output.txt for CFG")
		trees.process_output(settings.output_list, 0)
		blocks.trim(settings.output_list)
		settings.output_list.reverse()
		print(settings.output_to_file, file=open("ast_output.txt", "w"))
		blocks.create_blocks("assgn", 1, settings.output_list, None)
		blocks.construct_blocks(settings.blocks)
		settings.block_output += ('<bb %d>' %(settings.no_blocks+1))+'\n'
		settings.block_output += "End"
		print(settings.block_output, file=open("cfg_output.txt", "w"))
