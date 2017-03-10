grammar SmallC;

program: externalDeclaration*;
externalDeclaration: functionDefinition | declaration;
functionDefinition: typeSpecifier Identifier '(' parameterDeclarationList ')' compoundStatement;
parameterDeclarationList: parameterDeclaration (',' parameterDeclaration)*;
parameterDeclaration: typeSpecifier Identifier;
compoundStatement: '{' (variableDeclaration | statement)* '}';
variableDeclaration: typeSpecifier variableInitList;
variableInitList: variableInit (',' variableInit)*;
variableInit: Identifier ('=' assignment)?;
statement: compoundStatement | condStatement | whileStatement | breakStatement | continueStatement | returnStatement | exprStatement;
condStatement: 'if' '(' expression ')' statement ('else' statement)?;
whileStatement: 'while' '(' expression ')' statement;
breakStatement: 'break' ';';
continueStatement: 'continue' ';';
returnStatement: 'return' expression ';';
exprStatement: expression? ';';
typeSpecifier: 'void' | 'char' | 'int' | 'float';
typeQualifier: 'const';

declaration
    :   declarationSpecifiers initDeclaratorList? ';'
    ;

declarationSpecifiers: (typeSpecifier | typeQualifier)+;

initDeclaratorList
    :   initDeclarator
    |   initDeclaratorList ',' initDeclarator
    ;

initDeclarator
    :   declarator ('=' assignment)?
    ;

declarator
    :   pointer? directDeclarator
    ;

directDeclarator
    :   Identifier
    |   '(' declarator ')'
    |   directDeclarator '[' assignment? ']'
    ;

pointer
    :   '*' typeQualifier*
    |   '*' typeQualifier* pointer
    ;

expression: assignment | expression ',' assignment;
assignment: Identifier assignmentOperator expression | condition;
condition: disjunction | disjunction '?' expression ':' condition;
disjunction: conjunction | disjunction '||' conjunction;
conjunction: comparison | conjunction '&&' comparison;
comparison: relation | relation ('==' | '!=') relation;
relation: plus | plus ('<' | '>' | '<=' | '>=') plus;
plus: plus '+' times | plus '-' times | times;
times: times '*' cast | times '/' cast | times '%' cast | cast;
cast: unary | '(' typeSpecifier ')' cast;
unary: postfix | ('++' | '--') unary | ('&' | '*' | '!' | '+' | '-') cast;
postfix: primary | postfix ('[' expression ']' | '(' expressionList? ')' | ('.' | '->') Identifier | ('++' | '--'));
primary: constant | Identifier | '(' expression ')';
constant: FloatingConstant | IntegerConstant | CharacterConstant | StringConstant;
assignmentOperator: '=' | '*=' | '/=' | '%=' | '+=' | '-=';
expressionList: assignment (',' assignment)*;

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
