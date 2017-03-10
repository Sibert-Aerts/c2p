grammar SmallC;

externalDeclaration: functionDefinition | declaration;
functionDefinition: typeSpecifier Identifier '(' parameterDeclarationList ')' compoundStatement;
parameterDeclarationList: parameterDeclaration (',' parameterDeclaration)*;
parameterDeclaration: typeSpecifier Identifier;
compoundStatement: '{' (variableDeclaration | statement)* '}';
variableDeclaration: typeSpecifier variableInitList;
variableInit: variableInit (',' variableInit)*;
variableInit: Identifier ('=' expression)?;
statement: compoundStatement | condStatement | whileStatement | breakStatement | continueStatement | returnStatement | exprStatement;
condStatement: 'if' '(' expression ')' statement ('else' statement)?;
whileStatement: 'while' '(' expression ')' statement;
breakStatement: 'break' ';';
continueStatement: 'continue' ';';
returnStatement: 'return' expression ';';
exprStatement: expression? ';';
typeSpecifier: 'void' | 'char' | 'int' | 'float';

expression: Identifier assignmentOperator expression | condition;
condition: disjunction | disjunction '?' expression ':' condition;
disjunction: conjunction | disjunction '||' conjunction;
conjunction: comparison | conjunction '&&' comparison;
comparison: relation | relation ('==' | '!=') relation;
relation: sum | sum ('<' | '>' | '<=' | '>=') sum;
sum: sum '+' term | sum '-' term | term;
term: term '*' cast | term '/' cast | term '%' cast | cast;
cast: unary | '(' typeSpecifier ')' cast;
unary: postfix | ('++' | '--') unary | [&*!+-] cast;
postfix: primary | postfix ('[' expression ']' | '(' expressionList? ')' | ('.' | '->') Identifier | ('++' | '--'));
primary: constant | Identifier | '(' expression ')';
constant: FloatingConstant | IntegerConstant | CharacterConstant | StringConstant;
assignmentOperator: '=' | '*=' | '/=' | '%=' | '+=' | '-=';
expressionList: expression (',' expression)*;

Whitespace: [ \t]+ -> skip;
Newline: [\r\n]+ -> skip;
LineComment: '//' ~[\r\n]* -> skip;

fragment Letter: [a-zA-Z_];
fragment Digit: [0-9];
fragment Sign: [-+];

FloatingConstant: Sign? Digit* '.' Digit* ([eE] Sign? Digit+)?;
IntegerConstant: Sign? Digit+;
CharacterConstant: '\'' (~[\'\\\r\n] | EscapeSequence) '\'';
StringConstant: '"' (~[\"\\\r\n] | EscapeSequence | '\\\n')* '"';
EscapeSequence: '\\' [\'\"\\?abfnrtv];
Identifier: (Letter) (Letter | Digit)*;
