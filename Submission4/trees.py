import settings
import Parser
import copy

#function to creare various trees
global temp_gen
temp_gen = 0
def process_output(input_list, output_depth):
	global temp_gen
	while len(input_list) > 0:
		i = input_list.pop()
		if i is not None:
			if i[0] == "int" or i[0] == "float":
				do_nothing = 1
			elif len(i)==3 and i[-1] == "if":
				temp = output_depth*"\t"
				settings.output_to_file += temp+"IF"+"\n"
				settings.output_to_file += temp+"("+"\n"
				my_tree = Parser.Tree()
				temp2 = i[0]+[]
				temp2.reverse()
				add_to_tree(my_tree, temp2, output_depth+1)
				print_parse_tree(my_tree)
				settings.output_to_file += temp+'\t'+','+"\n"
				process_output(i[1]+[], output_depth+1)
				settings.output_to_file += temp+")"+"\n"
			elif len(i)==4 and i[-1] == "if":
				temp = output_depth*"\t"
				settings.output_to_file += temp+"IF"+"\n"
				settings.output_to_file += temp+"("+"\n"
				my_tree = Parser.Tree()
				temp2 = i[0]+[]
				temp2.reverse()
				add_to_tree(my_tree, temp2, output_depth+1)
				print_parse_tree(my_tree)
				settings.output_to_file += temp+'\t'+','+"\n"
				process_output(i[1]+[], output_depth+1)
				settings.output_to_file += temp+'\t'+','+"\n"
				process_output(i[2]+[], output_depth+1)
				settings.output_to_file += temp+")"+"\n"

			elif len(i)==3 and i[2] == "while":
				temp = output_depth*"\t"
				settings.output_to_file += temp+"WHILE"+"\n"
				settings.output_to_file += temp+"("+"\n"
				my_tree = Parser.Tree()
				temp2 = i[1]+[]
				temp2.reverse()
				add_to_tree(my_tree, temp2, output_depth+1)
				print_parse_tree(my_tree)
				settings.output_to_file += temp+'\t'+','+"\n"
				process_output(i[0]+[], output_depth+1)
				settings.output_to_file += temp+")"+"\n"
			elif len(i[0]) > 0 and (i[-2] == "int" or i[-2] == "void" or i[-2] == "float"):
				func_name = list(i[-1])
				level = 0
				name = ""
				for j in func_name:
					if j == "*":
						level += 1
					else:
						name = name+j
				# print(name)
				settings.output_to_file += "FUNCTION "+name+"\n"
				settings.output_to_file += "PARAMS ("
				while len(i[1])>0:
					# print(i[1])
					argument = i[1].pop()
					# print(argument[1])
					argument_name = list(argument[1][0])
					arg_level = 0
					for j in argument_name:
						if j == "*":
							arg_level += 1
						else:
							break
					settings.output_to_file += argument[0]+" "+arg_level*"*t"+str(temp_gen)
					temp_gen += 1
					if len(i[1])>0:
						settings.output_to_file += ", "
				settings.output_to_file += ")\n"
				settings.output_to_file += "RETURNS "+level*"*"+i[-2]+"\n"
				process_output(i[0], 1)
			elif i[-1] == "return":
				settings.output_to_file += "RETURN\n(\n"
				my_tree = Parser.Tree()
				temp2 = i[0]+[]
				temp2.reverse()
				add_to_tree(my_tree, temp2, 1)
				print_parse_tree(my_tree)
				settings.output_to_file += ")\n"
			elif len(i) == 2:
				temp = output_depth*"\t"
				settings.output_to_file += temp+"CALL "+i[-1]+"(\n"
				while len(i[0]) > 0:
					my_tree = Parser.Tree()
					temp2 = i[0].pop()
					temp2.reverse()
					add_to_tree(my_tree, temp2, output_depth+1)
					print_parse_tree(my_tree)
					if len(i[0]) > 0:
						settings.output_to_file += temp+"\t,\n"
				settings.output_to_file += temp+")\n"
			elif i[0] == "=":
				my_tree = Parser.Tree()
				temp2 = i+[]
				temp2.reverse()
				add_to_tree(my_tree, temp2, output_depth)
				print_parse_tree(my_tree)
				settings.output_to_file += '\n'

def add_to_tree(tree, output, depth):
	temp = output.pop()
	tree.node = temp
	tree.depth = depth
	if temp == '+' or temp == '-' or temp == '/' or temp == '*' or temp == '=' or temp == '==' or temp == '<=' or temp == '>=' or temp == '<' or temp == '>' or temp == '!=' or temp == '&&' or temp == '||':
		tree.lhs = Parser.Tree()
		tree.rhs = Parser.Tree()
		add_to_tree(tree.lhs, output, depth+1)
		add_to_tree(tree.rhs, output, depth+1)
	elif temp == 'p*' or temp == 'a&' or temp == 'u-' or temp == '!':
		tree.lhs = Parser.Tree()
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
	tabs = tree.depth*"\t"
	tabs2 = tabs+"\t"
	
	if tree.node == '=':
		settings.output_to_file += tabs+"ASGN"+"\n"
		settings.output_to_file += tabs+"("+"\n"
	elif tree.node == '+':
		comma = 1
		settings.output_to_file += tabs+"PLUS"+"\n"
		settings.output_to_file += tabs+"("+"\n"
	elif tree.node == '-':
		comma = 1
		settings.output_to_file += tabs+"MINUS"+"\n"
		settings.output_to_file += tabs+"("+"\n"
	elif tree.node == '/':
		comma = 1
		settings.output_to_file += tabs+"DIV"+"\n"
		settings.output_to_file += tabs+"("+"\n"
	elif tree.node == '*':
		comma = 1
		settings.output_to_file += tabs+"MUL"+"\n"
		settings.output_to_file += tabs+"("+"\n"
	elif tree.node == 'p*':
		settings.output_to_file += tabs+"DEREF"+"\n"
		settings.output_to_file += tabs+"("+"\n"
	elif tree.node == 'a&':
		settings.output_to_file += tabs+"ADDR"+"\n"
		settings.output_to_file += tabs+"("+"\n"
	elif tree.node == 'u-':
		settings.output_to_file += tabs+"UMINUS"+"\n"
		settings.output_to_file += tabs+"("+"\n"
	elif tree.node == '!':
		settings.output_to_file += tabs+"NOT"+"\n"
		settings.output_to_file += tabs+"("+"\n"
	elif tree.node == '||':
		settings.output_to_file += tabs+"OR"+"\n"
		settings.output_to_file += tabs+"("+"\n"
	elif tree.node == '&&':
		settings.output_to_file += tabs+"AND"+"\n"
		settings.output_to_file += tabs+"("+"\n"
	elif tree.node == '==':
		settings.output_to_file += tabs+"EQ"+"\n"
		settings.output_to_file += tabs+"("+"\n"
	elif tree.node == '<':
		settings.output_to_file += tabs+"LT"+"\n"
		settings.output_to_file += tabs+"("+"\n"
	elif tree.node == '>':
		settings.output_to_file += tabs+"GT"+"\n"
		settings.output_to_file += tabs+"("+"\n"
	elif tree.node == '<=':
		settings.output_to_file += tabs+"LE"+"\n"
		settings.output_to_file += tabs+"("+"\n"
	elif tree.node == '>=':
		settings.output_to_file += tabs+"GE"+"\n"
		settings.output_to_file += tabs+"("+"\n"
	elif tree.node == '!=':
		settings.output_to_file += tabs+"NE"+"\n"
		settings.output_to_file += tabs+"("+"\n"

	elif isinstance(tree.node, int) or isinstance(tree.node, float):
		settings.output_to_file += tabs+"CONST("+str(tree.node)+")"+"\n"
		t = 1
	elif isinstance(tree.node, (list,)):
		# print(tree.node)
		# settings.output_to_file += tabs+"CALL "+tree.node[-1]+"(\n"
		# while len(tree.node[0]) > 0:
		# 	# print(tree.node[0])
		# 	argument = tree.node[0].pop()
		# 	# print(argument)
		# 	process_output(argument, tree.depth+1)
		# 	if len(tree.node[0]) > 0:
		# 		settings.output_to_file += tabs2+",\n"
		print(tree.node)
		process_output([tree.node], tree.depth)
		t = 1
	else:
		settings.output_to_file += tabs+"VAR("+tree.node+")"+"\n"
		t = 1
	if tree.node != '=':
		if tree.rhs is not None:
			print_parse_tree(tree.rhs)
			if t == 0:
				settings.output_to_file += tabs+'\t'+','+"\n"
		if tree.lhs is not None:
			print(tree.lhs.node)
			print_parse_tree(tree.lhs)

	else:
		if tree.lhs is not None:
			print_parse_tree(tree.lhs)
			if t == 0:
				settings.output_to_file += tabs+'\t'+','+"\n"
		if tree.rhs is not None:
			print_parse_tree(tree.rhs)
	if t == 0:
		settings.output_to_file += tabs+")"+"\n"
