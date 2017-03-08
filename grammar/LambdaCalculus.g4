grammar LambdaCalculus;

term:  lam | app | var;
lam:   'lambda' ATOM '.' term;
app:   '(' term ')' term;
var:   ATOM;
ATOM:  ('a'..'z')+ ;
WS:    [ \n\t\r]+ -> skip;