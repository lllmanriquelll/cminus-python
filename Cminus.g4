grammar Cminus;

program: declaration_list;
declaration_list: declaration_list declaration | declaration;
declaration: var_declaration | fun_declaration;
var_declaration:
    type_specifier ID SEMI
    | type_specifier ID LBRACK NUMBER RBRACK SEMI;
type_specifier: INT | VOID;
fun_declaration:
    type_specifier ID LPAREN params RPAREN compound_statement;
params: param_list | VOID;
param_list: param_list COMMA param | param;
param: type_specifier ID | type_specifier ID LBRACK RBRACK;
compound_statement: LBRACE local_declarations statement_list RBRACE;
local_declarations: var_declaration*;
statement_list: statement*;
statement:
    expression_statement
    | compound_statement
    | selection_statement
    | iteration_statement
    | return_statemet;
expression_statement: expression? SEMI;
selection_statement:
    IF LPAREN expression RPAREN statement
    | IF LPAREN expression RPAREN statement ELSE statement;
iteration_statement: WHILE LPAREN expression RPAREN statement;
return_statemet: RETURN expression? SEMI;
expression: var EQUAL expression | simple_expression;
var: ID | ID LBRACK expression RBRACK;
simple_expression:
    additive_expression relop additive_expression
    | additive_expression;
relop: LE | LT | GT | GE | EQUAL_EQUAL | NOT_EQUAL;
additive_expression: additive_expression addop term | term;
addop: ADD | SUB;
term: term mulop factor | factor;
mulop: MUL | DIV;
factor: LPAREN expression RPAREN | var | call | NUMBER;
call: ID LPAREN args RPAREN;
args: arg_list?;
arg_list: arg_list COMMA expression | expression;

INT : 'int' ;
VOID : 'void' ;
NUMBER: '0' | [1-9][0-9]*;
SEMI : ';' ;
LBRACK : '[' ;
RBRACK : ']' ;
LPAREN : '(' ;
RPAREN : ')' ;
COMMA : ',' ;
LBRACE : '{' ;
RBRACE : '}' ;
IF : 'if' ;
ELSE : 'else' ;
WHILE : 'while' ;
RETURN : 'return' ;
ID: [a-zA-Z]+;
EQUAL : '=' ;
LE : '<=' ;
LT : '<' ;
GT : '>' ;
GE : '>=' ;
EQUAL_EQUAL : '==' ;
NOT_EQUAL : '!=' ;
ADD : '+' ;
SUB : '-' ;
MUL : '*' ;
DIV : '/' ;
COMMENT: '/*' (.)*? '*/' -> skip;
WS: [ \t\r\n]+ -> skip;

