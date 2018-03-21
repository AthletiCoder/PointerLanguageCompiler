
def init_global():
	global error
	global no_blocks
	global blocks
	global condition_symbols
	global output_list
	global output_to_file
	global block_output

	no_blocks = 0
	error = 0
	blocks = {}
	condition_symbols = ["==", "<=", "<", ">=", ">", "!=", "&&", "||", "-", "+", "/", "*"]
	output_to_file = ""
	block_output = ""

