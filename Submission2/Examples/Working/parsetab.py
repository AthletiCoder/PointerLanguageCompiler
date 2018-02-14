
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftPLUSMINUSleftSTARDIVIDErightUMINUSrightSTAR_POINTERAND_POINTERMAIN VOID TYPE LPAREN RPAREN LFLOWER RFLOWER SEMI_COLON COMMA NAME STAR EQUAL AND NUMBER COMMENT PLUS MINUS DIVIDEprogram : VOID MAIN LPAREN RPAREN LFLOWER code RFLOWER\n\tcode : line code\n\t\t | line\n\t\n\tline : dec SEMI_COLON\n\t\t | assgn COMMA\n\t\t | assgn SEMI_COLON\n\t\t | COMMENT\n\t\n\tdec : TYPE vars\n\t\n\tvars : NAME COMMA vars\n\t\t | pointer_other COMMA vars\n\t\t | NAME\n\t\t | pointer_other\n\t\n\tassgn : pointer EQUAL expression\n\t\t  | name EQUAL not_number_expression\n\t\n\tname : NAME\n\t\n\tnot_number_expression : not_number_expression PLUS number_expression\n\t\t\t\t\t\t  |\tnot_number_expression MINUS number_expression\n\t\t\t\t\t\t  | not_number_expression STAR number_expression\n\t\t\t\t\t\t  | not_number_expression DIVIDE number_expression\n\t\t\t\t\t\t  | number_expression PLUS not_number_expression\n\t\t\t\t\t\t  | number_expression MINUS not_number_expression\n\t\t\t\t\t\t  | number_expression STAR not_number_expression\n\t\t\t\t\t\t  | number_expression DIVIDE not_number_expression\n\t\t\t\t\t\t  | not_number_expression PLUS not_number_expression\n\t\t\t\t\t\t  | not_number_expression MINUS not_number_expression\n\t\t\t\t\t\t  | not_number_expression STAR not_number_expression\n\t\t\t\t\t\t  | not_number_expression DIVIDE not_number_expression\n\t\n\tnot_number_expression : NAME\n\t\t\t\t\t\t  | and\n\t\t\t\t\t\t  | pointer\n\t\n\tnot_number_expression : LPAREN not_number_expression RPAREN\n\tnot_number_expression : MINUS not_number_expression %prec UMINUS\n\tnumber_expression : number_expression PLUS number_expression\n\t\t\t\t\t  | number_expression MINUS number_expression\n\t\t\t\t\t  | number_expression STAR number_expression\n\t\t\t\t\t  | number_expression DIVIDE number_expression\n\t\n\tnumber_expression : LPAREN number_expression RPAREN\n\t\n\tnumber_expression : MINUS number_expression %prec UMINUS\n\t\n\tnumber_expression : NUMBER\n\t\n\texpression : expression PLUS expression\n\t\t\t   | expression MINUS expression\n\t\t\t   | expression STAR expression\n\t\t\t   | expression DIVIDE expression\n\texpression : LPAREN expression RPARENexpression : MINUS expression %prec UMINUS\n\texpression : NUMBER\n\t\t\t   | NAME\n\t\t\t   | pointer\n\t\t\t   | and\n\t\n\tpointer : STAR pointer %prec STAR_POINTER\n\t\t\t| STAR and %prec STAR_POINTER\n\t\t\t| STAR NAME %prec STAR_POINTER\n\t\n\tand : AND and %prec AND_POINTER\n\t\t| AND NAME %prec AND_POINTER\n\t\t| AND pointer %prec AND_POINTER\n\t\n\tpointer_other : STAR pointer %prec STAR_POINTER\n\t\t\t\t  | STAR NAME %prec STAR_POINTER\n\t'
    
_lr_action_items = {'$end':([1,17,],[0,-1,]),'EQUAL':([10,12,14,22,24,25,36,37,38,],[-15,27,30,-50,-51,-52,-55,-53,-54,]),'COMMA':([13,19,21,22,24,25,32,33,36,37,38,39,40,43,44,45,46,48,51,52,53,61,72,74,75,76,77,78,79,80,83,84,85,86,87,88,89,91,93,95,97,98,104,105,106,107,108,],[28,34,35,-50,-51,-52,-56,-57,-55,-53,-54,-13,-46,-47,-48,-49,-14,-39,-28,-30,-29,-45,-32,-42,-40,-41,-43,-44,-26,-18,-24,-16,-25,-17,-27,-19,-22,-20,-23,-21,-31,-37,-38,-35,-33,-36,-34,]),'VOID':([0,],[2,]),'DIVIDE':([22,24,25,36,37,38,39,40,43,44,45,46,47,48,51,52,53,60,61,70,71,72,73,74,75,76,77,78,79,80,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,103,104,105,106,107,108,],[-50,-51,-52,-55,-53,-54,59,-46,-47,-48,-49,65,68,-39,-28,-30,-29,59,-45,65,68,-32,-38,-42,59,59,-43,-44,-26,-18,65,101,65,101,-27,-19,-22,-35,65,68,-23,-36,65,68,-31,-37,101,-38,-35,101,-36,101,]),'COMMENT':([6,11,15,28,29,31,],[15,15,-7,-5,-6,-4,]),'MAIN':([2,],[3,]),'RFLOWER':([7,11,15,26,28,29,31,],[17,-3,-7,-2,-5,-6,-4,]),'STAR':([6,8,9,11,15,18,22,23,24,25,27,28,29,30,31,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,],[9,18,9,9,-7,9,-50,9,-51,-52,9,-5,-6,9,-4,18,18,-55,-53,-54,56,-46,9,9,-47,-48,-49,62,66,-39,9,9,-28,-30,-29,9,9,9,9,56,-45,9,9,9,9,9,9,9,9,62,66,-32,-38,-42,56,56,-43,-44,-26,-18,9,9,62,99,62,99,-27,-19,-22,-35,62,66,-23,-36,62,66,-31,-37,9,9,9,9,99,-38,-35,99,-36,99,]),'NUMBER':([27,30,41,42,49,50,56,57,58,59,62,63,64,65,66,67,68,69,81,82,99,100,101,102,],[40,48,40,40,48,48,40,40,40,40,48,48,48,48,48,48,48,48,48,48,48,48,48,48,]),'TYPE':([6,11,15,28,29,31,],[8,8,-7,-5,-6,-4,]),'RPAREN':([4,22,24,25,36,37,38,40,43,44,45,48,51,52,53,60,61,70,71,72,73,74,75,76,77,78,79,80,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,103,104,105,106,107,108,],[5,-50,-51,-52,-55,-53,-54,-46,-47,-48,-49,-39,-28,-30,-29,78,-45,97,98,-32,-38,-42,-40,-41,-43,-44,-26,-18,-24,-16,-25,-17,-27,-19,-22,-35,-20,-33,-23,-36,-21,-34,-31,-37,98,-38,-35,-33,-36,-34,]),'LFLOWER':([5,],[6,]),'AND':([9,23,27,30,41,42,49,50,56,57,58,59,62,63,64,65,66,67,68,69,81,82,99,100,101,102,],[23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,]),'SEMI_COLON':([13,16,19,20,21,22,24,25,32,33,36,37,38,39,40,43,44,45,46,48,51,52,53,54,55,61,72,74,75,76,77,78,79,80,83,84,85,86,87,88,89,91,93,95,97,98,104,105,106,107,108,],[29,31,-11,-8,-12,-50,-51,-52,-56,-57,-55,-53,-54,-13,-46,-47,-48,-49,-14,-39,-28,-30,-29,-9,-10,-45,-32,-42,-40,-41,-43,-44,-26,-18,-24,-16,-25,-17,-27,-19,-22,-20,-23,-21,-31,-37,-38,-35,-33,-36,-34,]),'MINUS':([22,24,25,27,30,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,],[-50,-51,-52,42,50,-55,-53,-54,58,-46,42,42,-47,-48,-49,64,69,-39,50,50,-28,-30,-29,42,42,42,42,58,-45,82,82,82,82,50,50,50,50,64,69,-32,-38,-42,-40,-41,-43,-44,-26,-18,82,82,-24,-16,-25,-17,-27,-19,-22,-35,-20,-33,-23,-36,-21,-34,-31,-37,82,82,82,82,102,-38,-35,-33,-36,-34,]),'NAME':([6,8,9,11,15,18,23,27,28,29,30,31,34,35,41,42,49,50,56,57,58,59,62,63,64,65,66,67,68,69,81,82,99,100,101,102,],[10,19,25,10,-7,33,38,43,-5,-6,51,-4,19,19,43,43,51,51,43,43,43,43,51,51,51,51,51,51,51,51,51,51,51,51,51,51,]),'PLUS':([22,24,25,36,37,38,39,40,43,44,45,46,47,48,51,52,53,60,61,70,71,72,73,74,75,76,77,78,79,80,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,103,104,105,106,107,108,],[-50,-51,-52,-55,-53,-54,57,-46,-47,-48,-49,63,67,-39,-28,-30,-29,57,-45,63,67,-32,-38,-42,-40,-41,-43,-44,-26,-18,-24,-16,-25,-17,-27,-19,-22,-35,-20,-33,-23,-36,-21,-34,-31,-37,100,-38,-35,-33,-36,-34,]),'LPAREN':([3,27,30,41,42,49,50,56,57,58,59,62,63,64,65,66,67,68,69,81,82,99,100,101,102,],[4,41,49,41,41,49,49,41,41,41,41,81,81,81,81,49,49,49,49,81,81,81,81,81,81,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'not_number_expression':([30,49,50,62,63,64,65,66,67,68,69,81,82,99,100,101,102,],[46,70,72,79,83,85,87,89,91,93,95,70,72,89,91,93,95,]),'expression':([27,41,42,56,57,58,59,],[39,60,61,74,75,76,77,]),'name':([6,11,],[14,14,]),'number_expression':([30,49,50,62,63,64,65,66,67,68,69,81,82,99,100,101,102,],[47,71,73,80,84,86,88,90,92,94,96,103,104,105,106,107,108,]),'vars':([8,34,35,],[20,54,55,]),'code':([6,11,],[7,26,]),'pointer_other':([8,34,35,],[21,21,21,]),'program':([0,],[1,]),'dec':([6,11,],[16,16,]),'line':([6,11,],[11,11,]),'pointer':([6,9,11,18,23,27,30,41,42,49,50,56,57,58,59,62,63,64,65,66,67,68,69,81,82,99,100,101,102,],[12,22,12,32,36,44,52,44,44,52,52,44,44,44,44,52,52,52,52,52,52,52,52,52,52,52,52,52,52,]),'assgn':([6,11,],[13,13,]),'and':([9,23,27,30,41,42,49,50,56,57,58,59,62,63,64,65,66,67,68,69,81,82,99,100,101,102,],[24,37,45,53,45,45,53,53,45,45,45,45,53,53,53,53,53,53,53,53,53,53,53,53,53,53,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> VOID MAIN LPAREN RPAREN LFLOWER code RFLOWER','program',7,'p_program','A2_temp2.py',93),
  ('code -> line code','code',2,'p_code','A2_temp2.py',97),
  ('code -> line','code',1,'p_code','A2_temp2.py',98),
  ('line -> dec SEMI_COLON','line',2,'p_line','A2_temp2.py',103),
  ('line -> assgn COMMA','line',2,'p_line','A2_temp2.py',104),
  ('line -> assgn SEMI_COLON','line',2,'p_line','A2_temp2.py',105),
  ('line -> COMMENT','line',1,'p_line','A2_temp2.py',106),
  ('dec -> TYPE vars','dec',2,'p_dec','A2_temp2.py',111),
  ('vars -> NAME COMMA vars','vars',3,'p_vars','A2_temp2.py',116),
  ('vars -> pointer_other COMMA vars','vars',3,'p_vars','A2_temp2.py',117),
  ('vars -> NAME','vars',1,'p_vars','A2_temp2.py',118),
  ('vars -> pointer_other','vars',1,'p_vars','A2_temp2.py',119),
  ('assgn -> pointer EQUAL expression','assgn',3,'p_assgn','A2_temp2.py',134),
  ('assgn -> name EQUAL not_number_expression','assgn',3,'p_assgn','A2_temp2.py',135),
  ('name -> NAME','name',1,'p_name','A2_temp2.py',159),
  ('not_number_expression -> not_number_expression PLUS number_expression','not_number_expression',3,'p_not_number_expression','A2_temp2.py',169),
  ('not_number_expression -> not_number_expression MINUS number_expression','not_number_expression',3,'p_not_number_expression','A2_temp2.py',170),
  ('not_number_expression -> not_number_expression STAR number_expression','not_number_expression',3,'p_not_number_expression','A2_temp2.py',171),
  ('not_number_expression -> not_number_expression DIVIDE number_expression','not_number_expression',3,'p_not_number_expression','A2_temp2.py',172),
  ('not_number_expression -> number_expression PLUS not_number_expression','not_number_expression',3,'p_not_number_expression','A2_temp2.py',173),
  ('not_number_expression -> number_expression MINUS not_number_expression','not_number_expression',3,'p_not_number_expression','A2_temp2.py',174),
  ('not_number_expression -> number_expression STAR not_number_expression','not_number_expression',3,'p_not_number_expression','A2_temp2.py',175),
  ('not_number_expression -> number_expression DIVIDE not_number_expression','not_number_expression',3,'p_not_number_expression','A2_temp2.py',176),
  ('not_number_expression -> not_number_expression PLUS not_number_expression','not_number_expression',3,'p_not_number_expression','A2_temp2.py',177),
  ('not_number_expression -> not_number_expression MINUS not_number_expression','not_number_expression',3,'p_not_number_expression','A2_temp2.py',178),
  ('not_number_expression -> not_number_expression STAR not_number_expression','not_number_expression',3,'p_not_number_expression','A2_temp2.py',179),
  ('not_number_expression -> not_number_expression DIVIDE not_number_expression','not_number_expression',3,'p_not_number_expression','A2_temp2.py',180),
  ('not_number_expression -> NAME','not_number_expression',1,'p_not_number_expression_basic','A2_temp2.py',189),
  ('not_number_expression -> and','not_number_expression',1,'p_not_number_expression_basic','A2_temp2.py',190),
  ('not_number_expression -> pointer','not_number_expression',1,'p_not_number_expression_basic','A2_temp2.py',191),
  ('not_number_expression -> LPAREN not_number_expression RPAREN','not_number_expression',3,'p_not_number_expression_group','A2_temp2.py',201),
  ('not_number_expression -> MINUS not_number_expression','not_number_expression',2,'p_not_number_expression_uminus','A2_temp2.py',207),
  ('number_expression -> number_expression PLUS number_expression','number_expression',3,'p_number_expression','A2_temp2.py',216),
  ('number_expression -> number_expression MINUS number_expression','number_expression',3,'p_number_expression','A2_temp2.py',217),
  ('number_expression -> number_expression STAR number_expression','number_expression',3,'p_number_expression','A2_temp2.py',218),
  ('number_expression -> number_expression DIVIDE number_expression','number_expression',3,'p_number_expression','A2_temp2.py',219),
  ('number_expression -> LPAREN number_expression RPAREN','number_expression',3,'p_number_expression_group','A2_temp2.py',228),
  ('number_expression -> MINUS number_expression','number_expression',2,'p_number_expression_uminus','A2_temp2.py',233),
  ('number_expression -> NUMBER','number_expression',1,'p_number_expression_basic','A2_temp2.py',242),
  ('expression -> expression PLUS expression','expression',3,'p_expression_advanced','A2_temp2.py',251),
  ('expression -> expression MINUS expression','expression',3,'p_expression_advanced','A2_temp2.py',252),
  ('expression -> expression STAR expression','expression',3,'p_expression_advanced','A2_temp2.py',253),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression_advanced','A2_temp2.py',254),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','A2_temp2.py',261),
  ('expression -> MINUS expression','expression',2,'p_expression_uminus','A2_temp2.py',266),
  ('expression -> NUMBER','expression',1,'p_expression_basic','A2_temp2.py',273),
  ('expression -> NAME','expression',1,'p_expression_basic','A2_temp2.py',274),
  ('expression -> pointer','expression',1,'p_expression_basic','A2_temp2.py',275),
  ('expression -> and','expression',1,'p_expression_basic','A2_temp2.py',276),
  ('pointer -> STAR pointer','pointer',2,'p_pointer','A2_temp2.py',285),
  ('pointer -> STAR and','pointer',2,'p_pointer','A2_temp2.py',286),
  ('pointer -> STAR NAME','pointer',2,'p_pointer','A2_temp2.py',287),
  ('and -> AND and','and',2,'p_and','A2_temp2.py',303),
  ('and -> AND NAME','and',2,'p_and','A2_temp2.py',304),
  ('and -> AND pointer','and',2,'p_and','A2_temp2.py',305),
  ('pointer_other -> STAR pointer','pointer_other',2,'p_pointer_other','A2_temp2.py',321),
  ('pointer_other -> STAR NAME','pointer_other',2,'p_pointer_other','A2_temp2.py',322),
]
