grammar SmallC;

// Program structure
program: '#include <stdio.h>'? (functionDefinition | declaration)*;
functionDefinition: declarationSpecifiers pointer Identifier '(' parameterDeclarationList ')' compoundStatement;
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
returnStatement: 'return' expression ';';
exprStatement: expression? ';';

// Declarations and types
declaration: declarationSpecifiers initDeclaratorList? ';';
declarationSpecifiers: ('void' | 'char' | 'int' | 'float' | 'const')+;
initDeclaratorList: initDeclarator (',' initDeclarator)*;
initDeclarator: declarator ('=' assignment)?;
declarator: pointer directDeclarator;
directDeclarator: Identifier | '(' declarator ')' | directDeclarator '[' assignment? ']';
// What about const pointers?
pointer: ('*' 'const'?)*;

// Expressions
expression: assignment | expression ',' assignment;
assignment: unary assignmentOperator expression | condition;
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
constant: FloatingConstant | IntegerConstant | CharacterConstant | StringConstant;
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
fragment EscapeSequence: '\\' ['"\\?abfnrtv];

FloatingConstant: Sign? Digit* '.' Digit* ([eE] Sign? Digit+)?;
IntegerConstant: Sign? Digit+;
CharacterConstant: '\'' (~['\\\n] | EscapeSequence) '\'';
StringConstant: '"' (EscapeSequence | ~["\\\n] | '\\\n')* '"';
Identifier: (Letter) (Letter | Digit)*;
