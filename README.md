# Logica-da-Computacao-rodrigonigri

# Status dos Testes:

![git status](http://3.129.230.99/svg/rodrigonigri/Logica-da-Computacao-rodrigonigri/)


# Diagrama sintático
![diagrama sintatico factor](https://user-images.githubusercontent.com/62730936/224706673-f7c17077-195e-46d1-ae89-b824c2ae105f.png)

# EBNF:
```
EXPRESSION = TERM, {("+"|"-"), TERM};
TERM = FACTOR, {("*"|"/"), FACTOR};
FACTOR = ("+"|"-") FACTOR | "(" EXPRESSION ")" | NUMBER
NUMBER = DIGIT, {DIGIT};
DIGIT = 0|1|2|3|4|5|6|7|8|9;
```
