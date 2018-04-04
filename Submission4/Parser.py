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

class Symbol_Table:
	parent = None
	declarations = {}
	func_dec = {}
	func_def = {}
	level = None
	return_type = None
	def __eq__(self, other): 
		return self.__dict__ == other.__dict__

global global_symbol_table
global_symbol_table = Symbol_Table()

global error_symbol_table
error_symbol_table = 0

global ternary_operators
ternary_operators = ['>', '<', '>=', '<=', '==', '!=', '&&', '||', '+', '-', '/', '*', '=', '!']

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
		settings.output_list += [p[0]]
	elif len(p) == 8:
		p[0] = [[], p[4], p[1], p[2]]
		settings.output_list += [p[0]]
	elif len(p) == 9:
		p[0] = [p[6], [], p[1], p[2]]
		settings.output_list += [p[0]]
	elif len(p) == 7:
		p[0] = [[], [], p[1], p[2]]
		settings.output_list += [p[0]]
	elif len(p) == 4:
		# print("gloabal_declarations_found")
		p[0] = p[1]
		settings.output_list += [p[0]]

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
		p[0] = [[p[1], [p[2]]]]
	else:
		p[0] = p[4]+[[p[1], [p[2]]]]

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
		p[0] = p[2]+[p[1]]

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
	
def p_assgn_expression_pointer(p):
	"""
	assgn : assgn_pointer EQUAL expression
		  | assgn_pointer EQUAL and
	"""
	p[0] = [p[2]]+p[1]+p[3]

def p_assgn_expression_name(p):
	"""
	assgn : NAME EQUAL and
		  | NAME EQUAL function_call
	"""
	p[0] = [p[2]]+[p[1]]+p[3]


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

# change func_name to NAME and assgn_pointer if ast should be drawn for function calls like ***func()
def p_function_call_expression(p):
	"""
	expression : NAME LPAREN parameters RPAREN
			   | NAME LPAREN RPAREN
	"""
	if len(p) == 4:
		p[0] = [[[], p[1]]]
	else:
		p[0] = [[p[3], p[1]]]

def p_function_call(p):
	"""
	function_call : func_name LPAREN parameters RPAREN
			      | func_name LPAREN RPAREN
	"""
	if len(p) == 4:
		p[0] = [[], p[1]]
	else:
		p[0] = [p[3], p[1]]

# remember the reverse order
def p_parameters_name(p):
	"""
	parameters : NAME COMMA parameters
			   | NAME
	"""
	if len(p) == 2:
		p[0] = [[p[1]]]
	else:
		p[0] = p[3]+[[p[1]]]

def p_parameters_expression(p):
	"""
	parameters : expression COMMA parameters
			   | expression
			   | and COMMA parameters
			   | and
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[3]+[p[1]] 

def p_function_call_line(p):
	"""
	line : NAME LPAREN parameters RPAREN SEMI_COLON
		 | NAME LPAREN RPAREN SEMI_COLON
		 | return_line
	"""
	if len(p) == 6:
		p[0] = [p[3]]+[p[1]]
	elif len(p) == 5:
		p[0] = [[], p[1]]
	else:
		p[0] = p[1]

def p_return_line(p):
	"""
	return_line : RETURN NAME SEMI_COLON
				| RETURN SEMI_COLON
	"""
	if len(p) == 4:
		p[0] = [[p[2]], p[1]]
	else:
		p[0] = [[], p[1]]

def p_return_line_assgn(p):
	"""
	return_line : RETURN expression SEMI_COLON
	"""
	p[0] = [p[2]]+[p[1]]

# def p_return_line(p):
# 	"""
# 	return_line : RETURN NAME SEMI_COLON
# 	"""
# 	if len(p) == 4:
# 		p[0] = [p[2], p[1]]
# 	else:
# 		p[0] = [p[1]]


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
		p[0] = [p[2]]+p[3]+p[1]

def p_error(p):
	if p:
		print("syntax error at {0}".format(p.value))
		settings.error = 1
	else:
		print("syntax error at EOF")
		settings.error = 1

# function definition, function declaration, varibale declarations, variable assignments, while, if and if_else
global first
first = 0
def create_symbol_table(input_list, symbol_table, prev):
	global ternary_operators
	global first
	global global_symbol_table
	while len(input_list) > 0:
		global error_symbol_table
		temp = input_list.pop()
		# variable declarations
		if temp[0] == "int" or temp[0] == "float": 
			if prev == "dec_allowed":
				# print(first)
				for i in temp[1]:
					level = 0
					name = ""
					temp2 = list(i)
					for j in temp2:
						if j == "*":
							level += 1
						else:
							name = name+j
					if name not in symbol_table.declarations:
						# print(name)
						symbol_table.declarations[name] = [temp[0], level]
					else:
						error_symbol_table = 1
			else:
				error_symbol_table = 1

		# function definitions and declarations
		elif temp[-2] == "int" or temp[-2] == "float" or temp[-2] == "void":
			func_name = list(temp[-1])
			level = 0
			name = ""
			for i in func_name:
				if i == "*":
					level += 1
				else:
					name = name+i
			if len(temp[0]) == 0:
				if name in symbol_table.func_dec or name == "main":
					error_symbol_table = 1
				else:
					if temp[-2] == "void" and level != 0:
						error_symbol_table = 1
					else:
						arguments_list = []
						for i in temp[1]:
							var = list(i[1][0])
							arg_level = 0
							for j in var:
								if j == "*":
									arg_level += 1
								elif j == "&":
									arg_level = arg_level-1
							arguments_list.append([i[0], arg_level])
						symbol_table.func_dec[name] = [temp[-2], level, arguments_list]
			else:
				if name in symbol_table.func_dec:
					if symbol_table.func_dec[name][1] == level and symbol_table.func_dec[name][0] == temp[-2]:
						if temp[-2] != "void" and (temp[0][0][-1] != "return" or len(temp[0][0][0]) ==0):
							error_symbol_table = 1
						elif temp[-2] == "void" and temp[0][0][-1] == "return" and len(temp[0][0][0]) > 0:
							error_symbol_table = 1
						else:
							arguments_list = []
							for i in temp[1]:
								var = list(i[1][0])
								arg_level = 0
								for j in var:
									if j == "*":
										arg_level += 1
									elif j == "&":
										arg_level = arg_level-1
								arguments_list.append([i[0], arg_level])
							if arguments_list == symbol_table.func_dec[name][2]:
								# print("detecting func1")
								symbol_table.func_def[name] = Symbol_Table()
								symbol_table.func_def[name].parent = symbol_table
								symbol_table.func_def[name].level = level
								symbol_table.func_def[name].return_type = temp[-2]
								symbol_table.func_def[name].declarations = {}
								symbol_table.func_def[name].func_def = {}
								symbol_table.func_def[name].func_dec = {}
								create_symbol_table(temp[1], symbol_table.func_def[name], "dec_allowed")
								create_symbol_table(temp[0], symbol_table.func_def[name], "dec_allowed")
							else:
								error_symbol_table = 1	
					else:
						error_symbol_table = 1
				elif name == "main" and temp[-2] == "void":
					symbol_table.func_def[name] = Symbol_Table()
					symbol_table.func_def[name].parent = symbol_table
					symbol_table.func_def[name].level = level
					symbol_table.func_def[name].return_type = temp[-2]
					symbol_table.func_def[name].declarations = {}
					symbol_table.func_def[name].func_def = {}
					symbol_table.func_def[name].func_dec = {}
					create_symbol_table(temp[0], global_symbol_table.func_def["main"], "dec_allowed")
				else:
					error_symbol_table = 1

		# while
		elif temp[-1] == "while":
			condition_type = ""
			print(temp[1])
			valid, exp_type = exp_type_checking(temp[1], symbol_table)
			if valid:
				if exp_type[1] != 0:
					print("p1")
					error_symbol_table = 1
			else:
				print("p2")
				error_symbol_table = 1
			
			create_symbol_table(temp[0], symbol_table, "dec_not_allowed") 			

		# if
		elif temp[-1] == "if":
			condition_type = ""
			valid, exp_type = exp_type_checking(temp[0], symbol_table)
			if valid:
				if exp_type[1] != 0:
					error_symbol_table = 1
			else:
				error_symbol_table = 1
			create_symbol_table(temp[1], symbol_table, "dec_not_allowed")
			if len(temp) == 4:
				create_symbol_table(temp[2], symbol_table, "dec_not_allowed")

		# function calls without assignments
		elif len(temp) == 2 and temp[-1] != "return":
			valid, return_type = func_type_checking(temp, symbol_table)
			if not valid:
				error_symbol_table = 1

		# assignments
		elif temp[0] == "=":
			print(temp)
			condition_type = ""
			temp.reverse()
			nothing = temp.pop()
			lhs = temp.pop()
			valid_rhs, rhs_exp_type = exp_type_checking(temp, symbol_table)
			valid_lhs, lhs_exp_type = exp_type_checking([lhs], symbol_table)
			print(rhs_exp_type)
			print(lhs_exp_type)
			if valid_rhs and valid_lhs:
				if rhs_exp_type != lhs_exp_type:
					error_symbol_table = 1
			else:
				error_symbol_table = 1

		# returning expressions

		elif len(input_list) == 0:

		
			if temp[-1] == "return" and len(temp[0])>0:
				condition_type = ""
				valid, exp_type = exp_type_checking(temp[0], symbol_table)
				if valid:
					if exp_type != [symbol_table.return_type, symbol_table.level]:
						error_symbol_table = 1
				else:
					error_symbol_table = 1
					
			elif temp[-1] == "return":
				if symbol_table.return_type != "void":
					error_symbol_table = 1

		else:
			error_symbol_table = 1


def func_type_checking(input_list, symbol_table):
	argument_list = []
	valid = True
	for i in input_list[0]:
		valid, arg = exp_type_checking(i, symbol_table)
		if not valid:
			return False, []
		else:
			argument_list.append(arg)

	name = input_list[-1]
	func_name = ""
	level = 0
	for k in name:
		if k == "*":
			level += 1
		else:
			func_name = func_name+k
	if func_name not in global_symbol_table.func_dec:
		return False, []
	if argument_list != global_symbol_table.func_dec[func_name][2]:
		return False, []
	return valid, [global_symbol_table.func_dec[func_name][0], global_symbol_table.func_dec[func_name][1]]
def exp_type_checking(input_list, symbol_table):
	global ternary_operators
	expression_type = ""
	level = 0
	valid = True
	for i in input_list:
		if isinstance(i, (list,)):
			valid, return_type = func_type_checking(i, symbol_table)
			if not valid:
				return valid, return_type
			else:
				if expression_type == "":
					expression_type = return_type[0]
					level = return_type[1]
				elif return_type[1] != 0:
					return False, return_type
				elif return_type[0] != expression_type:
					return False, return_type
		elif isinstance(i, int):
			if expression_type == "":
				expression_type = "int"
				level = 0
			elif expression_type != "int" or level != 0:
				return False, []

		elif isinstance(i, float):
			if expression_type == "":
				expression_type = "float"
				level = 0
			elif expression_type != "float" or level != 0:
				return False, []

		elif i not in ternary_operators:
			arg_level  = 0
			arg_name = ""
			var = list(i)
			for k in var:
				if k == "*":
					arg_level += 1
				elif k == "&":
					arg_level = arg_level-1
				else:
					arg_name = arg_name+k
			if arg_name in symbol_table.declarations:
				if expression_type == "":
					expression_type = symbol_table.declarations[arg_name][0]
					level = symbol_table.declarations[arg_name][1]-arg_level
				elif level != 0 or symbol_table.declarations[arg_name][1]-arg_level != 0:
					return False, []
				elif expression_type != symbol_table.declarations[arg_name][0]:
					return False, []


			elif arg_name in global_symbol_table.declarations:
				if expression_type == "":
					expression_type = global_symbol_table.declarations[arg_name][0]
					level = global_symbol_table.declarations[arg_name][1]-arg_level
				elif level != 0 or global_symbol_table.declarations[arg_name][1]-arg_level != 0:
					return False, []
				elif expression_type != global_symbol_table.declarations[arg_name][0]:
					return False, []
			else:
				return False, []
	return valid, [expression_type, level]


	
def print_symbol_table():
	global global_symbol_table
	border_line = "-----------------------------------------------------------------"

	# function declarations
	print("Procedure table :-")
	print(border_line)
	print("Name\t\t|\tReturn Type\t|\tParameter List")
	for function in global_symbol_table.func_dec:
		base_type, level, arguments = global_symbol_table.func_dec[function]
		return_type = base_type+"*"*level
		argument_list = ""
		argument_index = 0
		for argument_type, type_level in arguments:
			argument_list += argument_type+type_level*"*"+" t"+str(argument_index)+", "
			argument_index += 1
		print(function+"\t\t|\t"+return_type+"\t\t|\t"+argument_list[:-2])
	print(border_line)

	# variable declarations
	print("Variable table :-")
	# global declarations
	print(border_line)
	print("Name\t\t|\tScope\t\t|\tBase Type\t|\tDerived Type")
	print(border_line)
	for var_name in global_symbol_table.declarations:
		base_type, derived_type = global_symbol_table.declarations[var_name]
		print(var_name+"\t\t|\tglobal\t|\t"+base_type+"\t\t\t|	"+derived_type*"*")

	# declarations in other function scopes
	for func_name, local_symbol_table in global_symbol_table.func_def.items():
		for var_name in local_symbol_table.declarations:
			base_type, derived_type = local_symbol_table.declarations[var_name]
			print(var_name+"\t\t|\tprocedure "+func_name+"\t|\t"+base_type+"\t\t\t|	"+derived_type*"*")
	print(border_line)
	print(border_line)	

def print_symbol_table_v2():
	global global_symbol_table

	# function declarations
	max_name_width = len("Name")
	max_return_type_width = len("Return Type")
	max_parameter_list_width = len("Parameter List")
	procedure_table = [["Name", "Return Type", "Parameter List"]]
	for function in global_symbol_table.func_dec:
		base_type, level, arguments = global_symbol_table.func_dec[function]
		return_type = base_type+"*"*level
		argument_list = ""
		argument_index = 0
		for argument_type, type_level in arguments:
			argument_list += argument_type+type_level*"*"+" t"+str(argument_index)+", "
			argument_index += 1
		procedure_table.append([function, return_type, argument_list[:-2]])

	for row in procedure_table:
		max_name_width = max(max_name_width, len(row[0]))
		max_return_type_width = max(max_return_type_width, len(row[1]))
		max_parameter_list_width = max(max_parameter_list_width, len(row[2]))

	max_name_width += 3
	max_return_type_width += 3
	max_parameter_list_width += 3
	border_line = "-"*(max_name_width+max_return_type_width+max_parameter_list_width+6)
	print("Procedure table :-")
	print(border_line)
	i = 0
	for row in procedure_table:
		if i == 1:
			print(border_line)
		print(row[0]+(max_name_width-len(row[0]))*" "+"|  "+row[1]+(max_return_type_width-len(row[1]))*" "+"|  "+row[2]+(max_parameter_list_width-len(row[2]))*" ")
		i += 1
	print(border_line)

	# variable declarations
	# global declarations
	variable_table = [["Name", "Scope", "Base Type", "Derived Type"]]
	for var_name in global_symbol_table.declarations:
		base_type, derived_type = global_symbol_table.declarations[var_name]
		variable_table.append([var_name, "global", base_type, derived_type*"*"])

	# declarations in other function scopes
	for func_name, local_symbol_table in global_symbol_table.func_def.items():
		for var_name in local_symbol_table.declarations:
			base_type, derived_type = local_symbol_table.declarations[var_name]
			variable_table.append([var_name, "procedure "+func_name, base_type, derived_type*"*"])
	max_name_width = len("Name")
	max_scope_width = len("Scope")
	max_base_type_width = len("Base Type")
	max_derived_type_width = len("Derived Type")
	for row in variable_table:
		max_name_width = max(max_name_width, len(row[0]))
		max_scope_width = max(max_scope_width, len(row[1]))
		max_base_type_width = max(max_base_type_width, len(row[2]))
		max_derived_type_width = max(max_derived_type_width, len(row[3]))

	max_name_width += 3
	max_scope_width += 3
	max_base_type_width += 3
	max_derived_type_width += 3
	border_line = "-"*(max_name_width+max_scope_width+max_base_type_width+max_derived_type_width+8)
	print("Variable table :-")
	print(border_line)
	i = 0
	for row in variable_table:
		if i == 1:
			print(border_line)
		print(row[0]+(max_name_width-len(row[0]))*" "+"|  "+row[1]+(max_scope_width-len(row[1]))*" "+"|  "+row[2]+(max_base_type_width-len(row[2]))*" "+"|  "+row[3]+(max_derived_type_width-len(row[3]))*" ")
		i += 1

	print(border_line)
	print(border_line)

# def remove_dec(input_list):
# 	for i in input_list:
# 		if isinstance(i, (list,)) and len(i) > 0:
# 			if i[0] == "int" or i[0] == "float":
# 				input_list.remove(i)
# 			else:
# 				remove_dec(i)

def process(data):
	lex.lex()
	yacc.yacc()
	yacc.parse(data)

if __name__ == "__main__":
	# global error_symbol_table
	filename = sys.argv[-1]
	infile = open(filename, "r")
	lines = infile.read()
	settings.init_global()

	process(lines)
	if settings.error == 0:
		# print(settings.output_list)
		print(settings.output_list, file=open("temp", "w"))
		symbol_table_input = copy.deepcopy(settings.output_list)
		create_ast_input = copy.deepcopy(settings.output_list)
		create_block_input = copy.deepcopy(settings.output_list)
		blocks.trim(symbol_table_input)
		blocks.trim(create_block_input)
		
		# create_symbol_table(symbol_table_input, global_symbol_table, "dec_allowed")
		# # print(error_symbol_table)
		# if error_symbol_table == 0:
		# 	print_symbol_table_v2()

		# remove_dec(create_block_input)
		# print(create_block_input)
		while len(create_block_input) > 0:
			settings.blocks = {}
			settings.block_output = ""
			temp = create_block_input.pop()
			if len(temp[0]) > 0 and temp[0] != "int" and temp[0] != "float":
				func_name_with_stars = temp[-1]
				temp2 = list(func_name_with_stars)
				func_name = ""
				for i in temp2:
					if i != "*":
						func_name += i
				arguments = ""
				for i in temp[1]:
					arguments = i[0]+" "+i[1][0]+", " + arguments
				arguments = arguments[:-2]
				settings.block_output += "function "+func_name+"("+arguments+")\n"
				blocks.create_blocks("assgn", settings.no_blocks+1, temp[0], None)
				blocks.construct_blocks(settings.blocks)
				print(settings.block_output)


				# blocks.create_blocks("assgn", settings.no_blocks+1, temp[0], None)
				# settings.blocks = {}
				# settings.block_output += ('<bb %d>' %(settings.no_blocks+1))+'\n'
				# settings.block_output += "End"
		# print(settings.block_output, file=open("cfg_output.txt", "w"))


		# trees.process_output(create_ast_input, 0)
		# print(settings.output_to_file, file=open("ast_output.txt", "w"))

		# temp = create_block_input.pop()
		# if len(temp[0]) > 0:
		# 	blocks.create_blocks("assgn", settings.no_blocks+1, temp[0], None)
		# 	print(settings.blocks)
		# print(error_symbol_table)
		
		# print(error_symbol_table)
		# if error_symbol_table != 1:
			# print_symbol_table()
			# print_symbol_table_v2()




		# ast_filename = filename+".ast"
		# print("Successfully parsed!")
		# print("Checkout ast_output.txt for AST")
		# print("Checkout cfg_output.txt for CFG")
		# trees.process_output(settings.output_list, 0)
		# blocks.trim(settings.output_list)
		# settings.output_list.reverse()
		# print(settings.output_to_file, file=open("ast_output.txt", "w"))
		# blocks.create_blocks("assgn", 1, settings.output_list, None)
		# blocks.construct_blocks(settings.blocks)
		# settings.block_output += ('<bb %d>' %(settings.no_blocks+1))+'\n'
		# settings.block_output += "End"
		# print(settings.block_output, file=open("cfg_output.txt", "w"))
