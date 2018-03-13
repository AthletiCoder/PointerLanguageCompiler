import sys
import copy
import ply.lex as lex
import ply.yacc as yacc
global error
error = 0

global output_list
global output_to_file
output_to_file = ""

class Tree:
	node = None
	lhs = None
	rhs = None
	depth = 0

output = []

tokens = (
		'MAIN', 'VOID', 'TYPE', 'LPAREN', 'RPAREN', 'LFLOWER', 'RFLOWER', 'SEMI_COLON', 'COMMA', 'NAME', 'STAR', 'EQUAL', 'AND', 'NUMBER', 'COMMENT', 'PLUS', 'MINUS', 'DIVIDE', 'IF', 'ELSE', 'WHILE', 'NOT_EQUAL', 'DOUBLE_EQUAL', 'GTHAN', 'LTHAN', 'GTHAN_EQUAL', 'LTHAN_EQUAL', 'COND_AND', 'COND_OR', 'NOT'
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


def p_program(p):
	'program : VOID MAIN LPAREN RPAREN LFLOWER code RFLOWER'
	global output_list
	p[0] = p[6]
	output_list = p[0]

def p_code(p):
	"""
	code : line code
		 | line
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	elif len(p) == 3:
		p[0] = [p[1]]+p[2]

def p_line_useless(p):
	"""
	line : dec SEMI_COLON
		 | COMMENT
	"""

def p_line(p):
	"""
	line : multi_assign SEMI_COLON
		 | if_else_section
		 | while_section
	"""
	if len(p) == 3:
		p[0] = p[1]
	elif p[1] is not None:
		p[0] = p[1]
	# print(p[0])

def p_while_section(p):
	"""
	while_section : WHILE LPAREN complex_conditional RPAREN LFLOWER code RFLOWER
				  | WHILE LPAREN complex_conditional RPAREN line
	"""
	if len(p) == 6:
		# p[0] = ['while', p[3], p[5]]
		p[0] = [[p[5]], p[3],"while"]
	elif len(p) == 8:
		# p[0] = ['while', p[3], p[6]]
		p[0] = [p[6], p[3],"while"]

def p_if_else_section(p):
	"""
	if_else_section : if_section else_section
					| if_section
	"""
	if len(p) == 3:
		p[0] = p[1]+[p[2]]+["if"]
		# print("else")
	else:
		p[0] = p[1]+["if"]
		# print("if")

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

def p_multi_assign(p):
	"""
	multi_assign : assgn
	"""
	if len(p) == 2:
		p[0] = p[1]
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

def p_assgn(p):
	"""
	assgn : pointer EQUAL expression
		  | name EQUAL not_number_expression
	"""
	# p[0] = p[1]+p[3]+[p[2]]
	p[0] = [p[2]]+p[1]+p[3]
	# print(p[0])

def p_name(p):
	"""
	name : NAME
	"""
	p[0] = [p[1]]

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

	# p[0] = p[1]+p[3]+[p[2]]
	p[0] = [p[2]]+p[3]+p[1]

def p_not_number_expression_basic_term(p):
	"""
	not_number_expression : NAME
	"""
	p[0] = [p[1]]

def p_not_number_expression_basic_nt(p):
	"""
	not_number_expression : and
						  | pointer
	"""
	p[0] = p[1]
def p_not_number_expression_group(p):
	"""
	not_number_expression : LPAREN not_number_expression RPAREN
	"""
	p[0] = p[2]
def p_not_number_expression_uminus(p):
	'not_number_expression : MINUS not_number_expression %prec UMINUS'
	# p[0] = p[2]+["u"+p[1]]
	p[0] = ["u"+p[1]]+p[2]

def p_number_expression(p):
	"""
	number_expression : number_expression PLUS number_expression
					  | number_expression MINUS number_expression
					  | number_expression STAR number_expression
					  | number_expression DIVIDE number_expression
	"""
	# p[0] = p[1]+p[3]+[p[2]]
	p[0] = [p[2]]+p[3]+p[1]

def p_number_expression_group(p):
	"""
	number_expression : LPAREN number_expression RPAREN
	"""
	p[0] = p[2]

def p_number_expression_uminus(p):
	"""
	number_expression : MINUS number_expression %prec UMINUS
	"""
	p[0] = ["u"+p[1]]+p[2]

def p_number_expression_basic(p):
	"""
	number_expression : NUMBER
	"""
	p[0] = [p[1]]


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

def p_expression_basic_term(p):
	"""
	expression : NUMBER
			   | NAME
	"""
	p[0] = [p[1]]

def p_expression_basic_nt(p):
	"""
	expression : pointer
			   | and
	"""
	p[0] = p[1]

def p_pointer_term(p):
	"""
	pointer : STAR NAME %prec STAR_POINTER
	"""
	p[0] = ["p"+p[1]]+[p[2]]
def p_pointer_nt(p):
	"""
	pointer : STAR pointer %prec STAR_POINTER
			| STAR and %prec STAR_POINTER
	"""
	p[0] = ["p"+p[1]]+p[2]

def p_and(p):
	"""
	and : AND NAME %prec AND_POINTER
	"""
	p[0] = ["a"+p[1]]+[p[2]]

def p_and_nt(p):
	"""
	and : AND and %prec AND_POINTER
		| AND pointer %prec AND_POINTER
	"""
	# p[0] = p[2] +["a"+p[1]]
	p[0] = ["a"+p[1]]+p[2]	

def p_pointer_other_term(p):
	"""
	pointer_other : STAR NAME %prec STAR_POINTER
	"""
	# p[0] = [p[2]]+["p"+p[1]]
	p[0] = ["p"+p[1]]+[p[2]]
def p_pointer_other_nt(p):
	"""
	pointer_other : STAR pointer %prec STAR_POINTER
	"""
	# p[0] = p[2]+["p"+p[1]]
	p[0] = ["p"+p[1]]+p[2]

def p_error(p):
	global error
	if p:
		print("syntax error at {0}".format(p.value))
		error = 1
	else:
		print("syntax error at EOF")
		error = 1


#function to creare various trees
def process_output(output, output_depth):
	global output_to_file
	for i in output:
		if i is not None:
			if len(i)==3 and i[-1] == "if":
				# if i[1] == "else":
				# 	temp = output_depth*"\t"
				# 	output_to_file += temp+"ELSE"+"\n"
				# 	output_to_file += temp+"("+"\n"
				# 	process_output(i[0]+[], output_depth+1)
				# # print(i, file=open("output2.txt", "w"))
				# # print(output_depth, file=open("output2.txt", "w"))
				# print("coming here")
				# my_tree = Tree()
				# add_to_tree(my_tree, i+[], output_depth)
				# print_parse_tree(my_tree)
				# output_to_file += '\n'
				temp = output_depth*"\t"
				output_to_file += temp+"IF"+"\n"
				output_to_file += temp+"("+"\n"
				my_tree = Tree()
				temp2 = i[0]+[]
				temp2.reverse()
				add_to_tree(my_tree, temp2, output_depth+1)
				print_parse_tree(my_tree)
				output_to_file += temp+'\t'+','+"\n"
				process_output(i[1]+[], output_depth+1)
				output_to_file += temp+")"+"\n"
			elif len(i)==4 and i[-1] == "if":
				# print(i[2], file=open("output2.txt", "w"))
				temp = output_depth*"\t"
				output_to_file += temp+"IF"+"\n"
				output_to_file += temp+"("+"\n"
				my_tree = Tree()
				temp2 = i[0]+[]
				temp2.reverse()
				add_to_tree(my_tree, temp2, output_depth+1)
				print_parse_tree(my_tree)
				output_to_file += temp+'\t'+','+"\n"
				process_output(i[1]+[], output_depth+1)
				# output_to_file += temp+")"+"\n"
				output_to_file += temp+'\t'+','+"\n"
				# print(i[2], file=open("output2.txt", "w"))
				# if len(i[2])==3 and i[2][-1] == "if":
					# print("correct")
				process_output(i[2]+[], output_depth+1)
				output_to_file += temp+")"+"\n"

			elif len(i)==3 and i[2] == "while":
				temp = output_depth*"\t"
				output_to_file += temp+"WHILE"+"\n"
				output_to_file += temp+"("+"\n"
				# process_output(i[1], output_depth+1)
				my_tree = Tree()
				temp2 = i[1]+[]
				temp2.reverse()
				add_to_tree(my_tree, temp2, output_depth+1)
				print_parse_tree(my_tree)
				# print(i[1], file=open("output2.txt", "w"))
				# output_to_file += '\n'
				output_to_file += temp+'\t'+','+"\n"
				process_output(i[0]+[], output_depth+1)
				output_to_file += temp+")"+"\n"
			elif len(i)>=3:
				# print(i, file=open("output2.txt", "w"))
				# print("coming here")
				my_tree = Tree()
				temp2 = i+[]
				temp2.reverse()
				add_to_tree(my_tree, temp2, output_depth)
				print_parse_tree(my_tree)
				output_to_file += '\n'

def add_to_tree(tree, output, depth):
	temp = output.pop()
	tree.node = temp
	tree.depth = depth
	if temp == '+' or temp == '-' or temp == '/' or temp == '*' or temp == '=' or temp == '==' or temp == '<=' or temp == '>=' or temp == '<' or temp == '>' or temp == '!=' or temp == '&&' or temp == '||':
		tree.lhs = Tree()
		tree.rhs = Tree()
		add_to_tree(tree.lhs, output, depth+1)
		add_to_tree(tree.rhs, output, depth+1)
	elif temp == 'p*' or temp == 'a&' or temp == 'u-' or temp == '!':
		tree.lhs = Tree()
		add_to_tree(tree.lhs, output, depth+1)

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
	elif tree.node == '!':
		output_to_file += tabs+"NOT"+"\n"
		output_to_file += tabs+"("+"\n"
	#start of conditionals
	elif tree.node == '||':
		output_to_file += tabs+"OR"+"\n"
		output_to_file += tabs+"("+"\n"
	elif tree.node == '&&':
		output_to_file += tabs+"AND"+"\n"
		output_to_file += tabs+"("+"\n"
	elif tree.node == '==':
		output_to_file += tabs+"EQ"+"\n"
		output_to_file += tabs+"("+"\n"
	elif tree.node == '<':
		output_to_file += tabs+"LT"+"\n"
		output_to_file += tabs+"("+"\n"
	elif tree.node == '>':
		output_to_file += tabs+"GT"+"\n"
		output_to_file += tabs+"("+"\n"
	elif tree.node == '<=':
		output_to_file += tabs+"LE"+"\n"
		output_to_file += tabs+"("+"\n"
	elif tree.node == '>=':
		output_to_file += tabs+"GE"+"\n"
		output_to_file += tabs+"("+"\n"
	elif tree.node == '!=':
		output_to_file += tabs+"NE"+"\n"
		output_to_file += tabs+"("+"\n"

	elif isinstance(tree.node, int):
		output_to_file += tabs+"CONST("+str(tree.node)+")"+"\n"
		t = 1
	else:
		output_to_file += tabs+"VAR("+tree.node+")"+"\n"
		t = 1
	if tree.node != '=':
		if tree.rhs is not None:
			print_parse_tree(tree.rhs)
			if t == 0:
				output_to_file += tabs+'\t'+','+"\n"
		if tree.lhs is not None:
			print_parse_tree(tree.lhs)
	else:
		if tree.lhs is not None:
			print_parse_tree(tree.lhs)
			if t == 0:
				output_to_file += tabs+'\t'+','+"\n"
		if tree.rhs is not None:
			print_parse_tree(tree.rhs)
	if t == 0:
		output_to_file += tabs+")"+"\n"
global no_blocks
no_blocks = 0
global blocks
blocks = {}
global condition_symbols
condition_symbols = ["==", "<=", "<", ">=", ">", "!=", "&&", "||", "-", "+", "/", "*"]
def create_blocks(prev, current_block, input_list, goto):
	if len(input_list) > 0:
		i = input_list.pop()
		global no_blocks
		if len(i)==3 and i[-1] == "if":
			no_blocks = no_blocks+1
			temp2 = i[1]+[]
			temp2.reverse()
			if prev == "while" and len(input_list) == 0:
				create_blocks("while", current_block+1, temp2, goto)
			elif prev == "while" or prev == "ifwhile":
				create_blocks("ifwhile", current_block+1, temp2, goto)				
			else:
				create_blocks("assgn", current_block+1, temp2, None)
			my_tree = Tree()
			temp2 = i[0] + []
			temp2.reverse()
			add_to_tree(my_tree, temp2, 0)
			blocks[current_block] = []
			dfs_list = [my_tree]
			left = None
			right = None
			block_line_if = ["if", current_block+1]
			if len(input_list) == 0 and prev == "while":
				block_line_else = ["else", goto]
			else:
				block_line_else = ["else", no_blocks+1]
			blocks[current_block].append(block_line_else)
			blocks[current_block].append(block_line_if)
			while len(dfs_list) > 0:
				temp = dfs_list.pop()
				if temp.node in condition_symbols:
					# print("coming")
					if temp.rhs.node in condition_symbols or temp.rhs.node == "u-" or temp.rhs.node == "!":
						dfs_list.append(temp.rhs)
						right = False
					else:
						right = True
					if temp.lhs.node in condition_symbols or temp.lhs.node == "u-" or temp.rhs.node == "!":
						dfs_list.append(temp.lhs)
						left = False
					else:
						left = True
					block_line = []
					if right:
						block_line.append(temp.rhs.node)
					else:
						block_line.append("t*")
					block_line.append(temp.node)
					if left:
						block_line.append(temp.lhs.node)
					else:
						block_line.append("t*")
					blocks[current_block].append(block_line)
				elif temp.node == "u-":
					if temp.lhs.node in condition_symbols:
						block_line = []
						block_line.append("-")
						block_line.append("t*")
						blocks[current_block].append(block_line)
						dfs_list.append(temp.lhs)
					else:
						block_line = []
						block_line.append("-")
						block_line.append(temp.lhs.node)
						blocks[current_block].append(block_line)
				elif temp.node == "!":
					if temp.lhs.node in condition_symbols or temp.lhs.node == "!":
						block_line = []
						block_line.append("!")
						block_line.append("t*")
						blocks[current_block].append(block_line)
						dfs_list.append(temp.lhs)
			if len(input_list) > 0:
				if prev == "while":
					create_blocks("while", no_blocks+1, input_list, goto)
				elif prev == "ifwhile":
					create_blocks("ifwhile", no_blocks+1, input_list, goto)
				else:
					create_blocks("assgn", no_blocks+1, input_list, None)
		elif len(i) == 3 and i[2] == "while":
			no_blocks = no_blocks+1
			temp2 = i[0]+[]
			temp2.reverse()
			create_blocks("while", current_block+1, temp2, current_block)
			my_tree = Tree()
			temp2 = i[1] + []
			temp2.reverse()
			add_to_tree(my_tree, temp2, 0)
			blocks[current_block] = []
			dfs_list = [my_tree]
			left = None
			right = None
			block_line_if = ["if", current_block+1]
			if len(input_list) == 0 and prev == "while":
				block_line_else = ["else", goto]
			else:
				block_line_else = ["else", no_blocks+1]
			blocks[current_block].append(block_line_else)
			blocks[current_block].append(block_line_if)
			while len(dfs_list) > 0:
				temp = dfs_list.pop()
				if temp.node in condition_symbols:
					# print("coming")
					if temp.rhs.node in condition_symbols or temp.rhs.node == "u-" or temp.rhs.node == "!":
						dfs_list.append(temp.rhs)
						right = False
					else:
						right = True
					if temp.lhs.node in condition_symbols or temp.lhs.node == "u-" or temp.rhs.node == "!":
						dfs_list.append(temp.lhs)
						left = False
					else:
						left = True
					block_line = []
					if right:
						block_line.append(temp.rhs.node)
					else:
						block_line.append("t*")
					block_line.append(temp.node)
					if left:
						block_line.append(temp.lhs.node)
					else:
						block_line.append("t*")
					blocks[current_block].append(block_line)
				elif temp.node == "u-":
					if temp.lhs.node in condition_symbols:
						block_line = []
						block_line.append("-")
						block_line.append("t*")
						blocks[current_block].append(block_line)
						dfs_list.append(temp.lhs)
					else:
						block_line = []
						block_line.append("-")
						block_line.append(temp.lhs.node)
						blocks[current_block].append(block_line)
				elif temp.node == "!":
					if temp.lhs.node in condition_symbols or temp.lhs.node == "!":
						block_line = []
						block_line.append("!")
						block_line.append("t*")
						blocks[current_block].append(block_line)
						dfs_list.append(temp.lhs)
			if len(input_list) > 0:
				if prev == "while":
					create_blocks("while", no_blocks+1, input_list, goto)
				elif prev == "ifwhile":
					create_blocks("ifwhile", no_blocks+1, input_list, goto)
				else:
					create_blocks("assgn", no_blocks+1, input_list, None)
		elif len(i) == 4 and i[-1] == "if":
			no_blocks = no_blocks+1

			t1 = copy.deepcopy(i[1]) # if block
			t2 = copy.deepcopy(i[2]) # else block
			# print(t1)
			# thing = isinstance(t1, (list,))
			# print(thing)
			if_blocks = no_of_blocks(t1)

			else_blocks = no_of_blocks(t2)

			temp2 = i[1]+[]
			temp2.reverse()

			# create_blocks("while", current_block+1, temp2, current_block+1+if_blocks+else_blocks)
			if prev == "while" and len(input_list) == 0:
				create_blocks("while", current_block+1, temp2, goto)
			elif prev == "while" or prev == "ifwhile":
				create_blocks("ifelse", current_block+1, temp2, current_block+1+if_blocks+else_blocks)				
			else:
				create_blocks("while", current_block+1, temp2, current_block+1+if_blocks+else_blocks)
			block_line_else = ["else", no_blocks+1]
			temp2 = i[2]+[]
			temp2.reverse()
			if prev == "while" and len(input_list) == 0:
				create_blocks("while", no_blocks+1, temp2, goto)
			elif prev == "while" or prev == "ifwhile":
				create_blocks("ifwhile", no_blocks+1, temp2, goto)				
			else:
				create_blocks("assgn", no_blocks+1, temp2, None)

			

			my_tree = Tree()
			temp2 = i[0] + []
			temp2.reverse()
			add_to_tree(my_tree, temp2, 0)
			blocks[current_block] = []
			dfs_list = [my_tree]
			left = None
			right = None
			block_line_if = ["if", current_block+1]
			blocks[current_block].append(block_line_else)
			blocks[current_block].append(block_line_if)
			while len(dfs_list) > 0:
				temp = dfs_list.pop()
				if temp.node in condition_symbols:
					# print("coming")	
					if temp.rhs.node in condition_symbols or temp.rhs.node == "u-" or temp.rhs.node == "!":
						dfs_list.append(temp.rhs)
						right = False
					else:
						right = True
					if temp.lhs.node in condition_symbols or temp.lhs.node == "u-" or temp.rhs.node == "!":
						dfs_list.append(temp.lhs)
						left = False
					else:
						left = True
					block_line = []
					if right:
						block_line.append(temp.rhs.node)
					else:
						block_line.append("t*")
					block_line.append(temp.node)
					if left:
						block_line.append(temp.lhs.node)
					else:
						block_line.append("t*")
					blocks[current_block].append(block_line)
				elif temp.node == "u-":
					if temp.lhs.node in condition_symbols:
						block_line = []
						block_line.append("-")
						block_line.append("t*")
						blocks[current_block].append(block_line)
						dfs_list.append(temp.lhs)
					else:
						block_line = []
						block_line.append("-")
						block_line.append(temp.lhs.node)
						blocks[current_block].append(block_line)
				elif temp.node == "!":
					if temp.lhs.node in condition_symbols or temp.lhs.node == "!":
						block_line = []
						block_line.append("!")
						block_line.append("t*")
						blocks[current_block].append(block_line)
						dfs_list.append(temp.lhs)
			if len(input_list) > 0:
				# i2 = input_list.pop()
				if prev == "while":
					create_blocks("while", no_blocks+1, input_list, goto)
				elif prev == "ifwhile":
					create_blocks("ifwhile", no_blocks+1, input_list, goto)
				else:
					create_blocks("assgn", no_blocks+1, input_list, None)
		else:
			if current_block not in blocks:
				no_blocks = no_blocks+1
				blocks[current_block] = []
			while len(i) > 3:
				if i[-2] == 'u-':
					last = i.pop()
					_ = i.pop()
					blocks[current_block] = [['-', last]] + blocks[current_block]
					i.append("t*")
				else:
					last = i.pop()
					last_but_one = i.pop()
					symbol = i.pop()
					blocks[current_block] = [[last, symbol, last_but_one]] + blocks[current_block]
					i.append("t*")
			blocks[current_block] = [[i[1], "=", i[2]]] + blocks[current_block]
			if len(input_list) == 0:
				if prev == "while" or prev == "ifelse":
					# print(goto)
					blocks[current_block] = [["goto", goto]] + blocks[current_block]	
				else:
					blocks[current_block] = [["goto", current_block+1]] + blocks[current_block]
			elif input_list[-1][-1] == "while":
				blocks[current_block] = [["goto", current_block+1]] + blocks[current_block]
				if prev == "while" or prev == "ifwhile":
					create_blocks(prev, current_block+1, input_list, goto)
				else:
					create_blocks("assgn", current_block+1, input_list, None)
			elif input_list[-1][-1] == "if":
				blocks[current_block] = [["goto", current_block+1]] + blocks[current_block]
				if prev == "while":
					create_blocks("while", current_block+1, input_list, goto)
				elif prev == "ifwhile":
					create_blocks("ifwhile", current_block+1, input_list, goto)	
				else:
					create_blocks("assgn", current_block+1, input_list, None)
			else:
				if prev == "while":
					create_blocks("while", current_block, input_list, goto)
				if prev == "ifwhile":
					create_blocks("ifwhile", current_block, input_list, goto)
				else:
					create_blocks("assgn", current_block, input_list, None)
def trim(input_list):
	i = 0
	while i < len(input_list):
		if input_list[i] is not None:
			# print(input_list[i])
			if isinstance(input_list[i], (list,)):
				trim(input_list[i])
			elif input_list[i] == 'a&':
				count = 0
				while input_list[i] == 'a&':
					i = i+1
					count = count+1
				text = count*"&"
				input_list[i] = text+input_list[i]
			elif input_list[i] == 'p*':
				count = 0
				while input_list[i] == 'p*':
					i = i+1
					count = count+1
				text = count*"*"
				input_list[i] = text+input_list[i]
		i = i+1
	# input_list = [x for x in input_list if x != 'a&']
	# input_list = [x for x in input_list if x != 'p*']
	while(True):
		if 'a&' in input_list:
			input_list.remove('a&')
		else:
			break
	while(True):
		if 'p*' in input_list:
			input_list.remove('p*')
		else:
			break
	while(True):
		if None in input_list:
			input_list.remove(None)
		else:
			break
global block_output
block_output = ""
def construct_blocks(l):
	blocks = list(l.values())
	ternary_operators = ['>', '<', '>=', '<=', '==', '!=', '&&', '||', '+', '-', '/', '*']
	block_index = 0
	global block_output
	index = 0
	for block in blocks:
		block_output += ('<bb %d>' %(block_index+1))+'\n'
		block.reverse()
		for line in block:
			if(line[1] in ternary_operators and len(line) == 3):
				if line[0] == 't*' and line[2] == 't*':
					# print(1)
					block_output += ('t%d = t%d %s t%d' %(index, index-2, line[1], index-1))+'\n'
				elif line[0] == 't*':
					# print(2)
					block_output += ('t%d = t%d %s %s' %(index, index-1, line[1], line[2]))+'\n'
				elif line[2] == 't*':
					# print(3)
					block_output += ('t%s = %s %s t%d' %(index, line[0], line[1], index-1))+'\n'
				else:
					# print(4)
					block_output += ('t%d = %s %s %s' %(index, line[0], line[1], line[2]))+'\n'
				index += 1
			elif(line[0] == '-' and len(line) == 2):
				if line[1] == 't*':
					block_output += ('t%d = -t%d' %(index, index-1))+'\n'
				else:
					block_output += ('t%d = -%s' %(index, line[1]))+'\n'
				index += 1
			elif(line[0] == '!' and len(line) == 2):
				if line[1] == 't*':
					block_output += ('t%d = !t%d' %(index, index-1))+'\n'
				else:
					block_output += ('t%d = !%s' %(index, line[1]))+'\n'
				index += 1
			elif(line[1] == '='):
				if line[2] != 't*':
					block_output += ('%s = %s' %(line[0], line[2]))+'\n'
				else:
					block_output += ('%s = t%d' %(line[0], index-1))+'\n'
			elif(line[0] == 'if' and len(line) == 2):
				block_output += ('if(t%d) goto <bb %s>' %(index-1, line[1]))+'\n'
			elif(line[0] == 'else' and len(line) == 2):
				block_output += ('else goto <bb %d>' %(line[1]))+'\n'
			elif(line[0] == 'goto' and len(line) == 2):
				block_output += ('goto <bb %s>' %(line[1]))+'\n'
		block_output += '\n'
		block_index += 1
		block_output += ("")


def no_of_blocks(input_list):
	input_list.reverse()
	if len(input_list) > 0:
		temp = input_list.pop()
		if temp[-1] == "while":
			input_list.reverse()
			return no_of_blocks(input_list)+1+no_of_blocks(temp[0])
		elif temp[-1] == "if":
			if len(temp) == 3:
				input_list.reverse()
				return no_of_blocks(input_list)+1+no_of_blocks(temp[0])
			else:
				input_list.reverse()
				return no_of_blocks(input_list)+1+no_of_blocks(temp[1])+no_of_blocks(temp[2])
		else:
			while len(input_list) > 0:
				if input_list[-1][-1] == "while" or input_list[-1][-1] == "if":
					break
				else:
					input_list.pop()
			input_list.reverse()
			return 1+no_of_blocks(input_list)
	else:
		return 0

def process(data):
	lex.lex()
	yacc.yacc()
	yacc.parse(data)

if __name__ == "__main__":
	filename = sys.argv[-1]
	infile = open(filename, "r")
	lines = infile.read()

	process(lines)
	
	# global block_output
	if error == 0:
		ast_filename = filename+".ast"
		# print(filename)
		print("Successfully parsed!")
		print("Checkout ast_output.txt for AST")
		print("Checkout cfg_output.txt for CFG")

		# print(output_list, file=open("output2.txt", "w"))
		process_output(output_list, 0)
		trim(output_list)
		# print(output_list, file=open("output3.txt", "w"))
		output_list.reverse()
		print(output_to_file, file=open("ast_output.txt", "w"))
		create_blocks("assgn", 1, output_list, None)
		construct_blocks(blocks)
		block_output += ('<bb %d>' %(no_blocks+1))+'\n'
		block_output += "End"
		print(block_output, file=open("cfg_output.txt", "w"))
