grammar Cminus;

 program: (declaration_list+=declaration)+ ;

  declaration: var_declaration
             | fun_declaration ;

  var_declaration: type_specifier ID SEMI
                 | type_specifier ID LSBRACKET NUMBER RSBRACKET SEMI ;

  type_specifier: INT
                | VOID ;

  fun_declaration: type_specifier ID LPAREN params RPAREN compound_decl ;

  params: param_list
        | VOID ;

  param_list: param_list COMMA param
            | param ;

  param: type_specifier ID
       | type_specifier ID LSBRACKET RSBRACKET ;

  compound_decl: LCBRACKET (l_decl+=local_declarations)* (stm_list+=statement_list)* RCBRACKET ;

  local_declarations: (var_decl+=var_declaration)+ ;

  statement_list: (stms+=statement)+ ;

  statement: expression_decl
           | compound_decl
           | selection_decl
           | iteration_decl
           | return_decl ;

  expression_decl: expression? SEMI ;

  selection_decl: IF LPAREN condition=expression RPAREN LCBRACKET bodyIF+=statement* RCBRACKET (ELSE LCBRACKET bodyElse+=statement* RCBRACKET)? ;

  iteration_decl: WHILE LPAREN expression RPAREN statement ;

  return_decl: RETURN SEMI
             | RETURN expression SEMI ;

  expression: var ASSIGN expression
            | simple_expression ;

  var: ID
     | ID LSBRACKET expression RSBRACKET ;

  simple_expression: left=additive_expression relational=(LETHAN| LT| GT| GETHAN| EQ| DF) right=additive_expression
                   | operation=additive_expression ;

  additive_expression: additive_expression op=('+'|'-') term
                     | term ;

  term: term op=('/'|'*') factor
      | factor ;

  factor: LPAREN expression RPAREN
        | var
        | call
        | NUMBER ;

  call: ID LPAREN (arg_list+=expression COMMA)* (arg_list+=expression) RPAREN
      | ID LPAREN RPAREN ;

      ELSE : 'else' ;
      IF : 'if' ;
      INT : 'int' ;
      RETURN : 'return' ;
      VOID : 'void' ;
      WHILE : 'while';
      LETHAN : '<=' ;
      GETHAN : '>=' ;
      ASSIGN : '=' ;
      EQ : '==' ;
      DF : '!=' ;
      LT : '<' ;
      GT : '>' ;
      PLUS : '+' ;
      MINUS : '-' ;
      TIMES : '*' ;
      OVER : '/' ;
      LPAREN : '(';
      RPAREN : ')';
      SEMI : ';' ;
      COMMA : ',' ;
      LCBRACKET : '{' ;
      RCBRACKET : '}' ;
      LSBRACKET : '[';
      RSBRACKET : ']' ;

      ID : [a-zA-Z]+ ;
      NUMBER : [0-9]+ ;

      BLOCK_COMMENT: '/*' .*? '*/' -> skip ;

      WS : [ \t\r\n\f]+ -> skip ;
