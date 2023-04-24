# Logica-da-Computacao-rodrigonigri

# Status dos Testes:

![git status](http://3.129.230.99/svg/rodrigonigri/Logica-da-Computacao-rodrigonigri/)


# Diagrama sintático
![diagrama sintatico if_while](https://user-images.githubusercontent.com/62730936/234004827-98afa55c-f486-4e13-a62d-3b6e7c98971e.png)


# EBNF:
```
BLOCK = {STATEMENT};
STATEMENT = (λ | ASSIGNMENT | PRINT), "\n";
ASSIGNMENT = IDENTIFIER, "=", EXPRESSION;
PRINT = "println", "(", EXPRESSION, ")";
EXPRESSION = TERM, { ("+"|"-"), TERM };
TERM = FACTOR, { ("*"|"/"), FACTOR };
FACTOR = (("+"|"-") FACTOR) | NUMBER | "(", EXPRESSION, ")" | IDENTIFIER;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" };
NUMBER = DIGIT, {DIGIT};
LETTER = (a | b | c | d | e | f | g | h | i | j | k | l | m | n | o | p | q | r | s | t | u | v | w | x | y | z | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | U | V | W | X | Y | Z )
DIGIT = ( 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 );
```
