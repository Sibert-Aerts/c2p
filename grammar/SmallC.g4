grammar SmallC;

int a[10];

externalDeclaration: functionDefinition | declaration;
functionDefinition: typeSpecifier Identifier '(' parameterDeclarationList ')' compoundStatement;
typeSpecifier: 'char' | 'int' | 'float';
parameterDeclarationList: parameterDeclaration (',' parameterDeclaration)*
parameterDeclaration: typeSpecifier Identifier;
compoundStatement: '{' (variableDeclaration | statement)* '}';
variableDeclaration: typeSpecifier variableInitList;
vairableInitList: variableInit (',' variableInit)*;
variableInit: Identifier ('=' expression)?;
statement : compoundStatement | condStatement | whileStatement | breakStatement | continueStatement | returnStatement;
condStatement: 'if' '(' expression ')' statement ('else' statement)?;
whileStatement: 'while' '(' expression ')' statement;
breakStatement: 'break' ';';
continueStatement: 'continue' ';';
returnStatement: 'return' expression ';';

expression: identifier '=' expression | condition;
condition: disjunction | disjunction '?' expression ':' condition;
disjunction: conjunction | disjunction '||' conjunction;
conjunction: comparison | conjunction '&&' comparison;
comparison: relation | relation '==' relation;
relation: sum | sum ('<' | '>') sum;
sum: sum '+' term | sum '-' term | term;
term: term '*' factor | term '/' factor | term '%' factor | factor;
factor: '!' factor | '-' factor | primary;
primary: constant | identifier | '(' expression ')';
constant: FloatingConstant | IntegerConstant | CharacterConstant | StringConstant;

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
