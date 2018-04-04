import settings
import trees
import copy
import Parser

def create_blocks(prev, current_block, input_list, goto):
	if len(input_list) > 0:
		i = input_list.pop()
		if len(i) == 2 and (i[0] == "int" or i[0] == "float"):
			do_nothing = 1
			create_blocks("assgn", current_block, input_list, goto)
		elif len(i)==3 and i[-1] == "if":
			settings.no_blocks = settings.no_blocks+1
			temp2 = i[1]+[]
			temp2.reverse()
			if prev == "while" and len(input_list) == 0:
				create_blocks("while", current_block+1, temp2, goto)
			elif prev == "while" or prev == "ifwhile":
				create_blocks("ifwhile", current_block+1, temp2, goto)				
			else:
				create_blocks("assgn", current_block+1, temp2, None)
			my_tree = Parser.Tree()
			temp2 = i[0] + []
			temp2.reverse()
			trees.add_to_tree(my_tree, temp2, 0)
			settings.blocks[current_block] = []
			dfs_list = [my_tree]
			left = None
			right = None
			block_line_if = ["if", current_block+1]
			if len(input_list) == 0 and prev == "while":
				block_line_else = ["else", goto]
			else:
				block_line_else = ["else", settings.no_blocks+1]
			settings.blocks[current_block].append(block_line_else)
			settings.blocks[current_block].append(block_line_if)
			while len(dfs_list) > 0:
				temp = dfs_list.pop()
				if temp.node in settings.condition_symbols:
					if temp.rhs.node in settings.condition_symbols or temp.rhs.node == "u-" or temp.rhs.node == "!":
						dfs_list.append(temp.rhs)
						right = False
					else:
						right = True
					if temp.lhs.node in settings.condition_symbols or temp.lhs.node == "u-" or temp.rhs.node == "!":
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
					settings.blocks[current_block].append(block_line)
				elif temp.node == "u-":
					if temp.lhs.node in settings.condition_symbols:
						block_line = []
						block_line.append("-")
						block_line.append("t*")
						settings.blocks[current_block].append(block_line)
						dfs_list.append(temp.lhs)
					else:
						block_line = []
						block_line.append("-")
						block_line.append(temp.lhs.node)
						settings.blocks[current_block].append(block_line)
				elif temp.node == "!":
					if temp.lhs.node in settings.condition_symbols or temp.lhs.node == "!":
						block_line = []
						block_line.append("!")
						block_line.append("t*")
						settings.blocks[current_block].append(block_line)
						dfs_list.append(temp.lhs)
			if len(input_list) > 0:
				if prev == "while":
					create_blocks("while", settings.no_blocks+1, input_list, goto)
				elif prev == "ifwhile":
					create_blocks("ifwhile", settings.no_blocks+1, input_list, goto)
				else:
					create_blocks("assgn", settings.no_blocks+1, input_list, None)
		elif len(i) == 3 and i[2] == "while":
			settings.no_blocks = settings.no_blocks+1
			temp2 = i[0]+[]
			temp2.reverse()
			create_blocks("while", current_block+1, temp2, current_block)
			settings.blocks[current_block] = []
			block_line_if = ["if", current_block+1]
			if len(input_list) == 0 and prev == "while":
				block_line_else = ["else", goto]
			else:
				block_line_else = ["else", settings.no_blocks+1]
			settings.blocks[current_block].append(block_line_else)
			settings.blocks[current_block].append(block_line_if)
			my_tree = Parser.Tree()
			temp2 = i[1] + []
			temp2.reverse()
			trees.add_to_tree(my_tree, temp2, 0)
			dfs_list = [my_tree]
			left = None
			right = None
			while len(dfs_list) > 0:
				temp = dfs_list.pop()
				if temp.node in settings.condition_symbols:
					if temp.rhs.node in settings.condition_symbols or temp.rhs.node == "u-" or temp.rhs.node == "!":
						dfs_list.append(temp.rhs)
						right = False
					else:
						right = True
					if temp.lhs.node in settings.condition_symbols or temp.lhs.node == "u-" or temp.rhs.node == "!":
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
					settings.blocks[current_block].append(block_line)
				elif temp.node == "u-":
					if temp.lhs.node in settings.condition_symbols:
						block_line = []
						block_line.append("-")
						block_line.append("t*")
						settings.blocks[current_block].append(block_line)
						dfs_list.append(temp.lhs)
					else:
						block_line = []
						block_line.append("-")
						block_line.append(temp.lhs.node)
						settings.blocks[current_block].append(block_line)
				elif temp.node == "!":
					if temp.lhs.node in settings.condition_symbols or temp.lhs.node == "!":
						block_line = []
						block_line.append("!")
						block_line.append("t*")
						settings.blocks[current_block].append(block_line)
						dfs_list.append(temp.lhs)
			if len(input_list) > 0:
				if prev == "while":
					create_blocks("while", settings.no_blocks+1, input_list, goto)
				elif prev == "ifwhile":
					create_blocks("ifwhile", settings.no_blocks+1, input_list, goto)
				else:
					create_blocks("assgn", settings.no_blocks+1, input_list, None)
		elif len(i) == 4 and i[-1] == "if":
			settings.no_blocks = settings.no_blocks+1

			t1 = copy.deepcopy(i[1]) # if block
			t2 = copy.deepcopy(i[2]) # else block
			if_blocks = no_of_blocks(t1)

			else_blocks = no_of_blocks(t2)

			temp2 = i[1]+[]
			temp2.reverse()

			if prev == "while" and len(input_list) == 0:
				create_blocks("while", current_block+1, temp2, goto)
			elif prev == "while" or prev == "ifwhile":
				create_blocks("ifelse", current_block+1, temp2, current_block+1+if_blocks+else_blocks)				
			else:
				create_blocks("while", current_block+1, temp2, current_block+1+if_blocks+else_blocks)
			block_line_else = ["else", settings.no_blocks+1]
			temp2 = i[2]+[]
			temp2.reverse()
			if prev == "while" and len(input_list) == 0:
				create_blocks("while", settings.no_blocks+1, temp2, goto)
			elif prev == "while" or prev == "ifwhile":
				create_blocks("ifwhile", settings.no_blocks+1, temp2, goto)				
			else:
				create_blocks("assgn", settings.no_blocks+1, temp2, None)

			

			my_tree = Parser.Tree()
			temp2 = i[0] + []
			temp2.reverse()
			trees.add_to_tree(my_tree, temp2, 0)
			settings.blocks[current_block] = []
			dfs_list = [my_tree]
			left = None
			right = None
			block_line_if = ["if", current_block+1]
			settings.blocks[current_block].append(block_line_else)
			settings.blocks[current_block].append(block_line_if)
			while len(dfs_list) > 0:
				temp = dfs_list.pop()
				if temp.node in settings.condition_symbols:
					# print("coming")	
					if temp.rhs.node in settings.condition_symbols or temp.rhs.node == "u-" or temp.rhs.node == "!":
						dfs_list.append(temp.rhs)
						right = False
					else:
						right = True
					if temp.lhs.node in settings.condition_symbols or temp.lhs.node == "u-" or temp.rhs.node == "!":
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
					settings.blocks[current_block].append(block_line)
				elif temp.node == "u-":
					if temp.lhs.node in settings.condition_symbols:
						block_line = []
						block_line.append("-")
						block_line.append("t*")
						settings.blocks[current_block].append(block_line)
						dfs_list.append(temp.lhs)
					else:
						block_line = []
						block_line.append("-")
						block_line.append(temp.lhs.node)
						settings.blocks[current_block].append(block_line)
				elif temp.node == "!":
					if temp.lhs.node in settings.condition_symbols or temp.lhs.node == "!":
						block_line = []
						block_line.append("!")
						block_line.append("t*")
						settings.blocks[current_block].append(block_line)
						dfs_list.append(temp.lhs)
			if len(input_list) > 0:
				if prev == "while":
					create_blocks("while", settings.no_blocks+1, input_list, goto)
				elif prev == "ifwhile":
					create_blocks("ifwhile", settings.no_blocks+1, input_list, goto)
				else:
					create_blocks("assgn", settings.no_blocks+1, input_list, None)
		elif i[0] == "=" or (i[-1] != "return" and len(i) == 2):
			if current_block not in settings.blocks:
				settings.no_blocks = settings.no_blocks+1
				settings.blocks[current_block] = []
			if len(i) > 2:
				while len(i) > 3:
					if i[-2] == 'u-':
						last = i.pop()
						_ = i.pop()
						settings.blocks[current_block] = [['-', last]] + settings.blocks[current_block]
						i.append("t*")
					else:
						last = i.pop()
						last_but_one = i.pop()
						symbol = i.pop()
						settings.blocks[current_block] = [[last, symbol, last_but_one]] + settings.blocks[current_block]
						i.append("t*")
				settings.blocks[current_block] = [[i[1], "=", i[2]]] + settings.blocks[current_block]
			else:
				# print("coming")
				settings.blocks[current_block] = [[i]] + settings.blocks[current_block]
			if len(input_list) == 0:
				if prev == "while" or prev == "ifelse":
					settings.blocks[current_block] = [["goto", goto]] + settings.blocks[current_block]	
				else:
					settings.blocks[current_block] = [["goto", current_block+1]] + settings.blocks[current_block]
			elif input_list[-1][-1] == "while":
				settings.blocks[current_block] = [["goto", current_block+1]] + settings.blocks[current_block]
				if prev == "while" or prev == "ifwhile":
					create_blocks(prev, current_block+1, input_list, goto)
				else:
					create_blocks("assgn", current_block+1, input_list, None)
			elif input_list[-1][-1] == "if":
				settings.blocks[current_block] = [["goto", current_block+1]] + settings.blocks[current_block]
				if prev == "while":
					create_blocks("while", current_block+1, input_list, goto)
				elif prev == "ifwhile":
					create_blocks("ifwhile", current_block+1, input_list, goto)	
				else:
					create_blocks("assgn", current_block+1, input_list, None)
			elif input_list[-1][0] == "=" or (input_list[-1][-1] != "return" and len(input_list[-1]) == 2):
				if prev == "while":
					create_blocks("while", current_block, input_list, goto)
				if prev == "ifwhile":
					create_blocks("ifwhile", current_block, input_list, goto)
				else:
					create_blocks("assgn", current_block, input_list, None)
			elif input_list[-1][-1] == "return":
				settings.blocks[current_block] = [["goto", current_block+1]] + settings.blocks[current_block]
				create_blocks("assgn", current_block+1, input_list, None)
		elif i[-1] == "return" and len(i[0]) > 0:
			settings.no_blocks = settings.no_blocks+1
			my_tree = Parser.Tree()
			temp2 = i[0] + []
			temp2.reverse()
			trees.add_to_tree(my_tree, temp2, 0)
			settings.blocks[current_block] = []
			dfs_list = [my_tree]
			left = None
			right = None
			# block_line_if = ["if", current_block+1]
			# if len(input_list) == 0 and prev == "while":
			# 	block_line_else = ["else", goto]
			# else:
			# 	block_line_else = ["else", settings.no_blocks+1]
			# settings.blocks[current_block].append(block_line_else)
			# settings.blocks[current_block].append(block_line_if)
			settings.blocks[current_block] = [["goto", current_block+1]] + settings.blocks[current_block]
			block_line_return = ["return", "t*"]
			settings.blocks[current_block].append(block_line_return)

			while len(dfs_list) > 0:
				temp = dfs_list.pop()
				if temp.node in settings.condition_symbols:
					if temp.rhs.node in settings.condition_symbols or temp.rhs.node == "u-" or temp.rhs.node == "!":
						dfs_list.append(temp.rhs)
						right = False
					else:
						right = True
					if temp.lhs.node in settings.condition_symbols or temp.lhs.node == "u-" or temp.rhs.node == "!":
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
					settings.blocks[current_block].append(block_line)
				elif temp.node == "u-":
					if temp.lhs.node in settings.condition_symbols:
						block_line = []
						block_line.append("-")
						block_line.append("t*")
						settings.blocks[current_block].append(block_line)
						dfs_list.append(temp.lhs)
					else:
						block_line = []
						block_line.append("-")
						block_line.append(temp.lhs.node)
						settings.blocks[current_block].append(block_line)
				elif temp.node == "!":
					if temp.lhs.node in settings.condition_symbols or temp.lhs.node == "!":
						block_line = []
						block_line.append("!")
						block_line.append("t*")
						settings.blocks[current_block].append(block_line)
						dfs_list.append(temp.lhs)
				else:
					settings.blocks[current_block].append(["t*", "=", temp.node])
					break
		elif i[-1] == "return" and len(i[0]) == 0:
			#check
			# settings.no_blocks = settings.no_blocks+1
			settings.blocks[current_block] = []
			settings.blocks[current_block] = [["goto", current_block+1]] + settings.blocks[current_block]
			block_line_return = ["return_nothing"]
			settings.blocks[current_block].append(block_line_return)




def trim(input_list):
	i = 0
	while i < len(input_list):
		if input_list[i] is not None:
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
	for i in range(len(input_list)):
		if isinstance(input_list[i], str):
			if input_list[i][-2:] == 'a&':
				if len(input_list[i]) > 2:
					input_list[i+1] = (len(input_list[i])-2)*"*"+"&"+input_list[i+1]
					input_list[i] = 'a&'
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


global block_index
block_index = 0
def construct_blocks(l):
	global block_index
	blocks = []
	for key, value in sorted(l.items()):
		blocks.append(value)
	ternary_operators = ['>', '<', '>=', '<=', '==', '!=', '&&', '||', '+', '-', '/', '*']
	index = 0
	for block in blocks:
		settings.block_output += ('<bb %d>' %(block_index+1))+'\n'
		block.reverse()
		return_block = False
		for line in block:
			# function call
			if len(line) == 3:
				if isinstance(line[0], (list,)):
						arguments = ""
						for arg in line[0][0]:
							arguments = arg[0] + ", " + arguments
						arguments = arguments[:-2]
						arguments = ('%s(%s)' %(line[0][1], arguments))
						line[0] = arguments
				if isinstance(line[2], (list,)):
						# line[0] = [[<arguments>], <name>]
						arguments = ""
						for arg in line[2][0]:
							arguments = arg[0] + ", " + arguments
						arguments = arguments[:-2]
						arguments = ('%s(%s)' %(line[2][1], arguments))
						line[2] = arguments
			if(isinstance(line[0], (list,)) and len(line) == 1):
				# line[0] = [[<arguments>], <name>]
				arguments = ""
				for arg in line[0][0]:
					arguments = arg[0] + ", " + arguments
				arguments = arguments[:-2]
				settings.block_output += ('%s(%s)' %(line[0][1], arguments)) + '\n'

			# return statement
			elif line[0] == 'return' and line[1] == "t*":
				return_block = True

			elif line[0] == 'return_nothing':
				settings.block_output += "return\n"
			elif(line[1] in ternary_operators and len(line) == 3):
				if line[0] == 't*' and line[2] == 't*':
					settings.block_output += ('t%d = t%d %s t%d' %(index, index-2, line[1], index-1))+'\n'
				elif line[0] == 't*':
					settings.block_output += ('t%d = t%d %s %s' %(index, index-1, line[1], line[2]))+'\n'
				elif line[2] == 't*':
					settings.block_output += ('t%s = %s %s t%d' %(index, line[0], line[1], index-1))+'\n'
				else:
					settings.block_output += ('t%d = %s %s %s' %(index, line[0], line[1], line[2]))+'\n'
				index += 1
			elif(line[0] == '-' and len(line) == 2):
				if line[1] == 't*':
					settings.block_output += ('t%d = -t%d' %(index, index-1))+'\n'
				else:
					settings.block_output += ('t%d = -%s' %(index, line[1]))+'\n'
				index += 1
			elif(line[0] == '!' and len(line) == 2):
				if line[1] == 't*':
					settings.block_output += ('t%d = !t%d' %(index, index-1))+'\n'
				else:
					settings.block_output += ('t%d = !%s' %(index, line[1]))+'\n'
				index += 1
			elif(line[1] == '='):
				if line[2] != 't*' and line[0] != 't*':
					settings.block_output += ('%s = %s' %(line[0], line[2]))+'\n'
				elif line[0] == 't*':
					settings.block_output += ('t%d = %s' %(index, line[2]))+'\n'
					index += 1
				else:
					settings.block_output += ('%s = t%d' %(line[0], index-1))+'\n'
			elif(line[0] == 'if' and len(line) == 2):
				settings.block_output += ('if(t%d) goto <bb %s>' %(index-1, line[1]))+'\n'
			elif(line[0] == 'else' and len(line) == 2):
				settings.block_output += ('else goto <bb %d>' %(line[1]))+'\n'
			elif(line[0] == 'goto' and len(line) == 2):
				if return_block:
					settings.block_output += "return t"+str(index-1)+"\n"
					return_block = False 
				settings.block_output += ('goto <bb %s>' %(line[1]))+'\n'
		
		settings.block_output += '\n'
		block_index += 1
		settings.block_output += ("")


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