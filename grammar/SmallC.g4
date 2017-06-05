grammar SmallC;

// Program structure
program: '#include <stdio.h>'? (functionDeclaration | functionDefinition | declaration)*;
functionDeclaration: declarationSpecifiers pointer Identifier '(' parameterDeclarationList? ')' ';';
functionDefinition: declarationSpecifiers pointer Identifier '(' parameterDeclarationList? ')' compoundStatement;
parameterDeclarationList: parameterDeclaration (',' parameterDeclaration)*;
parameterDeclaration: declarationSpecifiers declarator;

// Statements
compoundStatement: '{' (declaration | statement)* '}';
statement: compoundStatement | condStatement | whileStatement | forStatement
    | breakStatement | continueStatement | returnStatement | exprStatement;
condStatement: 'if' '(' expression ')' statement ('else' statement)?;
whileStatement: 'while' '(' expression ')' statement;
forStatement: 'for' '(' (declaration | expression? ';') expression? ';' expression? ')' statement;
breakStatement: 'break' ';';
continueStatement: 'continue' ';';
returnStatement: 'return' expression? ';';
exprStatement: expression? ';';

// Declarations and types
declaration: declarationSpecifiers initDeclaratorList? ';';
declarationSpecifiers: ('void' | 'char' | 'int' | 'float' | 'const' | 'bool' )+;
initDeclaratorList: initDeclarator (',' initDeclarator)*;
initDeclarator: declarator ('=' assignment)?;
declarator: pointer directDeclarator;
directDeclarator: Identifier | '(' declarator ')' | directDeclarator '[' assignment? ']';
pointer: ('*' 'const'?)*;

// Expressions
expression: assignment | expression ',' assignment;
assignment: unary assignmentOperator assignment | condition;
condition: disjunction | disjunction '?' expression ':' condition;
disjunction: conjunction | disjunction '||' conjunction;
conjunction: comparison | conjunction '&&' comparison;
comparison: relation | relation ('==' | '!=') relation;
relation: plus | plus ('<' | '>' | '<=' | '>=') plus;
plus: plus '+' times | plus '-' times | times;
times: times '*' cast | times '/' cast | cast;
cast: unary | '(' declarationSpecifiers pointer ')' cast;
unary: postfix | ('++' | '--') unary | ('&' | '*' | '!' | '+' | '-') cast;
postfix: primary | postfix ('[' expression ']' | '(' expressionList? ')' | ('++' | '--'));
primary: constant | Identifier | '(' expression ')';
constant: FloatingConstant | IntegerConstant | CharacterConstant | StringConstant | BoolConstant;
assignmentOperator: '=' | '*=' | '/=' | '+=' | '-=';
expressionList: assignment (',' assignment)*;

// Trivia
Whitespace: [ \t]+ -> skip;
Newline: [\r\n]+ -> skip;
LineComment: '//' ~[\r\n]* -> skip;
BlockComment: '/*' .*? '*/' -> skip;

// Tokens
fragment Letter: [a-zA-Z_];
fragment Digit: [0-9];
fragment Sign: [-+];
fragment EscapeSequence: '\\' [\'"\\?abfnrtv];

FloatingConstant: Digit* '.' Digit* ([eE] Sign? Digit+)?;
IntegerConstant: Digit+;
CharacterConstant: '\'' (~[\'\\\n] | EscapeSequence) '\'';
StringConstant: '"' (EscapeSequence | ~["\\\n] | '\\\n')* '"';
BoolConstant: 'true' | 'false';
Identifier: (Letter) (Letter | Digit)*;
