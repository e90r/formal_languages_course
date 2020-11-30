grammar db_language;

/*
 * parser rules
 */

script : (stmt NEWLINE)* EOF ;

stmt : CONNECT '"' PATH '"' 
     | STRING ':' pattern
     | SELECT obj FROM graph
     ;

graph : GRAMMAR
      | '[' pattern ']'
      | '"' NAME '"'
      | SET_START_FINAL vertices vertices graph
      | '(' graph '&' graph ')'
      ;

vertices : '{' set '}'
         | INT ':' INT
         | '_'
         ;

set : (INT ',')* INT ;

obj : edges
    | COUNT edges
    ;

edges : EDGES
      | FILTER cond ':' edges
      ;

cond : '(' STRING ',' STRING ',' STRING ')' ARROW '(' bool_expr ')' ;

bool_expr : STRING HAS_LBL STRING
          | IS_START STRING
          | IS_FINAL STRING
          | '(' bool_expr ')'
          | '!' bool_expr
          | bool_expr '&' bool_expr
          | bool_expr '|' bool_expr
          ;

pattern : TERM '(' STRING ')'
        | NONTERM '(' STRING ')'
        | EPS
        | '(' pattern ')'
        | pattern '*'
        | pattern '+'
        | pattern '?'
        | pattern '.' pattern
        | pattern '|' pattern
        ;

/*
 * lexer rules
 */

fragment LOWERCASE : [a-z] ;
fragment UPPERCASE : [A-Z] ;
fragment DIGIT : [0-9] ;

NEWLINE : '\r'? '\n' ;
PATH : (LOWERCASE | UPPERCASE | DIGIT | '_' | '/')+ ;
STRING : (LOWERCASE | UPPERCASE) (LOWERCASE | UPPERCASE | DIGIT | '_')+;
NAME : (LOWERCASE | UPPERCASE | DIGIT | '_' | '.')+ ;
INT : '0' | [1-9] DIGIT* ;
CONNECT : 'connect' ;
SELECT : 'select' ;
FROM : 'from' ;
GRAMMAR : 'grammar' ;
SET_START_FINAL : 'setStartAndFinal' ;
COUNT : 'count' ;
EDGES : 'edges' ;
FILTER : 'filter' ;
ARROW : '->' ;
HAS_LBL : 'hasLbl' ;
IS_START : 'isStart' ;
IS_FINAL : 'isFinal' ;
TERM : 'term' ;
NONTERM : 'var';
EPS : 'e';
WHITESPACE : ' ' -> skip ;