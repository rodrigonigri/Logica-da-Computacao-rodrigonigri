# Logica-da-Computacao-rodrigonigri

# Status dos Testes:

![git status](http://3.129.230.99/svg/rodrigonigri/Logica-da-Computacao-rodrigonigri/)


# Diagrama sintático
![diagrama sintatico](https://user-images.githubusercontent.com/62730936/221664792-21d82679-7298-4d3f-b5c1-b5d99e921b8e.png)

# EBNF:
```
EXPRESSION = TERM, {("+"|"-"), TERM};
TERM = NUMBER, {("*"|"/"), NUMBER};
NUMBER = DIGIT, {DIGIT};
DIGIT = 0|1|2|3|4|5|6|7|8|9;
```
