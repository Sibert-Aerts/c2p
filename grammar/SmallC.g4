grammar SmallC;

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
