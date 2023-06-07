import sys

def print_colored(text, color): # so pra debugar
    """Print text in color"""
    if color == "red":
        print("\033[91m {}\033[00m" .format(text))
    elif color == "green":
        print("\033[92m {}\033[00m" .format(text))
    elif color == "yellow":
        print("\033[93m {}\033[00m" .format(text))
    elif color == "blue":
        print("\033[94m {}\033[00m" .format(text))
    elif color == "magenta":
        print("\033[95m {}\033[00m" .format(text))
    elif color == "cyan":
        print("\033[96m {}\033[00m" .format(text))
    elif color == "white":
        print("\033[97m {}\033[00m" .format(text))
    elif color == "black":
        print("\033[98m {}\033[00m" .format(text))
    elif color == "grey":
        print("\033[99m {}\033[00m" .format(text))
    elif color == "lightgrey":
        print("\033[100m {}\033[00m" .format(text))
    elif color == "lightred":
        print("\033[101m {}\033[00m" .format(text))
    elif color == "lightgreen":
        print("\033[102m {}\033[00m" .format(text))
    elif color == "lightyellow":
        print("\033[103m {}\033[00m" .format(text))
    elif color == "lightblue":
        print("\033[104m {}\033[00m" .format(text))
    elif color == "lightmagenta":
        print("\033[105m {}\033[00m" .format(text))
    elif color == "lightcyan":
        print("\033[106m {}\033[00m" .format(text))
    elif color == "lightwhite":
        print("\033[107m {}\033[00m" .format(text))
    elif color == "boldred":
        print("\033[1m {}\033[00m" .format(text))
    else:
        print("\033[99m {}\033[00m" .format(text))

reserved_words = ["println", "if", "else", "while", "end", "readline", "Int", "String", "return", "function"]


class Node():
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self):
        pass

class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, table):
        if self.value == "-":
            return ("Int",-1 * self.children[0].evaluate(table)[1])
        
        elif self.value == "+":
            return ("Int",self.children[0].evaluate(table)[1])
        
        elif self.value == "!":
            return ("Int",not self.children[0].evaluate(table)[1])

class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, table):
        
        if self.value == ".":
            return ("String", str(self.children[0].evaluate(table)[1]) + str(self.children[1].evaluate(table)[1]))
        elif self.value == "==":
                    return ("Int", int(self.children[0].evaluate(table)[1] == self.children[1].evaluate(table)[1]))
        elif self.value == ">":
                    return ("Int", int(self.children[0].evaluate(table)[1] > self.children[1].evaluate(table)[1]))
                
        elif self.value == "<":
            return ("Int", int(self.children[0].evaluate(table)[1] < self.children[1].evaluate(table)[1]))
        
        else:
            if self.children[0].evaluate(table)[0] == "Int" and self.children[1].evaluate(table)[0] == "Int":
        
                if self.value == "+":
                    return ("Int", self.children[0].evaluate(table)[1] + self.children[1].evaluate(table)[1])

                elif self.value == "-":
                    return ("Int", self.children[0].evaluate(table)[1] - self.children[1].evaluate(table)[1])

                elif self.value == "*":
                    return ("Int", self.children[0].evaluate(table)[1] * self.children[1].evaluate(table)[1])

                elif self.value == "/":
                    return ("Int", self.children[0].evaluate(table)[1] // self.children[1].evaluate(table)[1])
                
                elif self.value == "||":
                    return ("Int", int(self.children[0].evaluate(table)[1] or self.children[1].evaluate(table)[1]))
                
                elif self.value == "&&":
                    return ("Int", int(self.children[0].evaluate(table)[1] and self.children[1].evaluate(table)[1]))
            
            else:
                raise Exception("Type error")
        
        
         

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, table):
        return ("Int",self.value)
    
    
class StrVal(Node):
    def __init__(self, value):
        super().__init__(value, [])
    
    def evaluate(self, table):
        return ("String",self.value)
    

class NoOp(Node):
    def __init__(self):
        super().__init__(None, [])

    def evaluate(self, table):
        pass


class Block(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, table):
        for child in self.children:
            #verify for return Node
            if child.value == "return":
                return child.evaluate(table)
            child.evaluate(table)


class Identifier(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, table):
        return table.getter(self.value)
    

class Println(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, table):
        print(self.children[0].evaluate(table)[1])


class Assignment(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, table):
        table.setter(self.children[0].value, self.children[1].evaluate(table))
        
        
class Readln(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, table):
        return ("Int",int(input()))
    
class If(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, table):
        if len(self.children) == 2:
            if self.children[0].evaluate(table)[1]:
                self.children[1].evaluate(table)
        else:
            if self.children[0].evaluate(table):
                self.children[1].evaluate(table)
            else:
                self.children[2].evaluate(table)
                
class While(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, table):
        while self.children[0].evaluate(table)[1]:
            self.children[1].evaluate(table)
            

class VarDec(Node):
    def __init__(self, value ,children):
        super().__init__(value, children)
        
        
    def evaluate(self, table):
        table.create(self.children[0].value, self.value)
        table.setter(self.children[0].value, self.children[1].evaluate(table))
        
        
        
        
class FuncDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
        
    def evaluate(self, table):
        func_table.create(self.children[0].value, self)


class FuncCall(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
        
    def evaluate(self, table):   
        
        # get from func_table
        func_node = func_table.getter(self.value)
        
        # verify if the number of arguments is the same
        if len(func_node.children) - 2 != len(self.children):
            raise Exception("Número de argumentos inválido")
        
        
        # create a new symbol table
        new_symbol_table = SymbolTable()
        # get arguments from func_table if there are more than 0 arguments (FuncDec.children[1:n-1])
        if len(func_node.children) > 2:
            for i in range(1, len(func_node.children) - 1): # percorre os filhos do FuncDec de 1 a n-1, que são os argumentos, e cria eles na nova symbol table
                
                new_symbol_table.create(func_node.children[i].children[0].value, func_node.children[i].value) #ou func_node.children[i].evaluate(new_symbol_table)
                new_symbol_table.setter(func_node.children[i].children[0].value, self.children[i-1].evaluate(new_symbol_table)) # ou table?
                
            #print_colored(new_symbol_table.table, "red")
            # run las child (FuncDec.children[n] which is a Block)
            # return value from function
            return func_node.children[-1].evaluate(new_symbol_table)
        else:
            # run las child (FuncDec.children[n] which is a Block)
            # return value from function
            return func_node.children[-1].evaluate(new_symbol_table)
      
    
class Return(Node):
    def __init__(self, children):
        super().__init__("return", children)
        
    def evaluate(self, table):
        return self.children[0].evaluate(table)



class SymbolTable(): # creates dinamically a symbol table for each function
    def __init__(self):
        self.table = {}
        
    def create(self, key, type):
        # verifica se a variável já foi declarada
        if key in self.table:
            raise Exception("Variável já declarada")
        if type == "Int":
            self.table[key] = ("Int", 0)
        elif type == "String":
            self.table[key] = ("String", "")
        
    def setter(self, key, value_tuple):
        #verifica se a variável já foi declarada
        if key not in self.table:
            raise Exception("Variável não declarada")
        #verifica se o tipo da variável é o mesmo do valor que está sendo atribuído
        if self.table[key][0] != value_tuple[0]:
            raise Exception("Tipos incompatíveis")
        #atribui o valor
        self.table[key] = value_tuple
        
    def getter(self, key):
        if key not in self.table:
            raise Exception("Variável não declarada")
        return self.table[key]


class FunctionTable():
    def __init__(self):
        self.table = {}
    
    def create(self, key, type):
        # verifica se a variável já foi declarada
        if key in self.table:
            raise Exception("Func já declarada")
        self.table[key] = type
        
    
    def setter(self, key, value_tuple):
        #verifica se a variável já foi declarada
        if key not in self.table:
            raise Exception("Func não declarada")
        #verifica se o tipo da variável é o mesmo do valor que está sendo atribuído
        if self.table[key] != value_tuple[0]:
            raise Exception("Tipos incompatíveis")
        #atribui o valor
        
        self.table[key] = value_tuple


    def getter(self, key):
        if key not in self.table:
            raise Exception("Func não declarada")
        return self.table[key]


class PrePro():
    def __init__(self, source):
        self.source = source

    @staticmethod
    def filter(source):
        '''percorre linha a linha removendo os comentários e espaços em branco'''
        source = source.split("\n")
        for i in range(len(source)):
            source[i] = source[i].split("#")[0]
            source[i] = source[i].strip()
        source = "\n".join(source)

        return source


class Token():
    def __init__(self, type, value): # type is a string, value is a int
        self.type = type
        self.value = value 


class Tokenizer():
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None



    def selectNext(self):
        '''Percorre o código fonte e seleciona o próximo token'''
        flag_token = True
        

        try:
            char = self.source[self.position]
        except:
            self.next = Token("EOF", "")
            return
        
        
        if char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ": # se for uma letra
            flag_token = True
            palavra = ""
            palavra += char
            while flag_token: # vai percorrendo letra por letra até encontrar um espaço ou um operador
                self.position += 1
                try:
                    char = self.source[self.position]
                except:
                    self.next = Token("ID", palavra)
                    return
                
                if char == " " or char in "+-*/()=<>|&!:.," or char == "\n": # se for um espaço ou um operador então o token é formado
                    flag_token = False
                    if palavra in reserved_words: # se for uma palavra reservada
                        if palavra == "Int" or palavra == "String":
                            self.next = Token("TYPE", palavra)
                        else:
                            self.next = Token(palavra.upper(), palavra)
                    else: 
                        self.next = Token("ID", palavra)

                else:
                    palavra += char
                    
        ### STRING ###
        elif char == '"':
            flag_token = True
            palavra = ""
            while flag_token:
                self.position += 1
                try:
                    char = self.source[self.position]
                    if char == '"':
                        flag_token = False
                    else:
                        palavra += char
                except:
                    raise Exception("String não fechada")
                
            self.position += 1
            self.next = Token("STRING", palavra)
            
            
            

        elif char in "0123456789":
            flag_token = True
            numero = ""
            numero += char
            while flag_token: # vai percorrendo algarismo por algarismo até encontrar um espaço ou um operador
                self.position += 1
                try:
                    char = self.source[self.position]
                except:
                    self.next = Token("INT", int(numero))
                    return

                if char == " " or char in "+-*/()=<>|&!:.," or char == "\n": 
                    flag_token = False
                    self.next = Token("INT", int(numero))
                else:
                    numero += char

        elif char in "+-*/()=<>|&!:.," or char == "\n":
            if char == "-":
                self.next = Token("MINUS", "-")
            
            elif char == "+":
                self.next = Token("PLUS", "+")
            
            elif char == "*":
                self.next = Token("MULT", "*")

            elif char == "/":
                self.next = Token("DIV", "/")

            elif char == "(":
                self.next = Token("OPEN", "(")

            elif char == ")":
                self.next = Token("CLOSE", ")")
                
            elif char == ",":
                self.next = Token("COMMA", ",")
            
            
            elif char == "\n":
                self.next = Token("NEWLINE", "\n")
                
            elif char == "=":
                if self.source[self.position + 1] == "=":
                    self.next = Token("EQUAL", "==")
                    self.position += 1
                else:
                    self.next = Token("ASSIGN", "=")
                    
            elif char == ":":
                if self.source[self.position + 1] == ":":
                    self.next = Token("DECLARATOR", "::")
                    self.position += 1
                else:
                    raise Exception("Erro Lexico")
                    
            elif char == "<":
                self.next = Token("LESS", "<")
                
            elif char == ">":
                self.next = Token("GREATER", ">")
                
            elif char == "|":
                if self.source[self.position + 1] == "|":
                    self.next = Token("OR", "||")
                    self.position += 1
                else:
                    raise Exception("Erro Lexico")
                
            elif char == "&":
                if self.source[self.position + 1] == "&":
                    self.next = Token("AND", "&&")
                    self.position += 1
                else:
                    raise Exception("Erro Lexico")
                
            elif char == "!":
                self.next = Token("NOT", "!")
                
            elif char == ".":
                self.next = Token("CONCAT", ".")
                
            
            self.position += 1
            
        elif char == " ": # se for um espaço
            self.position += 1
            self.selectNext()
            
            
        #print_colored(str(self.next.type) + " " + str(self.next.value), "red")
        

class Parser():

    @staticmethod
    def parseBlock():
        children = []
        while Parser.tokenizer.next.type != "EOF":
            children.append(Parser.parseStatement())
        return Block(children)
    

    @staticmethod
    def parseStatement():
        
        token_agora = Parser.tokenizer.next
        
        if token_agora.type == "ID":


            temp = Identifier(token_agora.value) # possivel erro
            Parser.tokenizer.selectNext()
            token_agora = Parser.tokenizer.next
            
            if token_agora.type == "DECLARATOR":
                Parser.tokenizer.selectNext()
                token_agora = Parser.tokenizer.next
                
                if token_agora.type == "TYPE":
                    varType = Parser.tokenizer.next.value
                    Parser.tokenizer.selectNext()
                    token_agora = Parser.tokenizer.next
                    
                    if token_agora.type == "ASSIGN":
                        Parser.tokenizer.selectNext()
                        token_agora = Parser.tokenizer.next
                        res = VarDec(varType, [temp, Parser.parseRelExpression()])
                        token_agora = Parser.tokenizer.next
                    else:
                        if varType == "Int":
                            res = VarDec(varType, [temp, IntVal(0)])
                        elif varType == "String":
                            res = VarDec(varType, [temp, StrVal("")])
                            
                    if token_agora.type == "NEWLINE" or token_agora.type == "EOF":
                        Parser.tokenizer.selectNext()
                        token_agora = Parser.tokenizer.next
                        
                        return res
                        
                        
                else:
                    raise Exception("Erro de sintaxe na declaração de variável")
            
            if token_agora.type == "ASSIGN":

                Parser.tokenizer.selectNext()
                token_agora = Parser.tokenizer.next
                
                res = Assignment([temp, Parser.parseRelExpression()]) # possivel erro
                #Parser.tokenizer.selectNext()

                token_agora = Parser.tokenizer.next
                

                if token_agora.type == "NEWLINE" or token_agora.type == "EOF":
                    
                    Parser.tokenizer.selectNext()
                    token_agora = Parser.tokenizer.next
                    
                    return res
                else:
                    raise Exception("Erro de sintaxe na declaração de variável")
                
            if token_agora.type == "OPEN":
                Parser.tokenizer.selectNext()
                token_agora = Parser.tokenizer.next
                
                lista_args = []
                while token_agora.type != "CLOSE":
                    lista_args.append(Parser.parseRelExpression())
                    token_agora = Parser.tokenizer.next
                
                    
                
                    if token_agora.type == "COMMA":
                        Parser.tokenizer.selectNext()
                        token_agora = Parser.tokenizer.next
                    else:
                        break
                res = FuncCall(temp.value, lista_args)
                
                if token_agora.type != "CLOSE":
                    raise Exception("Erro de sintaxe: Não fechou o parênteses")
                
                Parser.tokenizer.selectNext() ### possivel erro
                token_agora = Parser.tokenizer.next ### possivel erro
                
                if token_agora.type == "NEWLINE" or token_agora.type == "EOF":
                        Parser.tokenizer.selectNext()
                        token_agora = Parser.tokenizer.next
                        
                        return res
            
            else:
                raise Exception("Erro de sintaxe na declaração de variável")

        elif token_agora.type == "RETURN":
            Parser.tokenizer.selectNext()
            res = Return([Parser.parseRelExpression()]) # Return(children)
            token_agora = Parser.tokenizer.next
            
            if token_agora.type == "NEWLINE" or token_agora.type == "EOF":
                
                Parser.tokenizer.selectNext()
                token_agora = Parser.tokenizer.next
                
                return res
            else:
                raise Exception("Erro de sintaxe")
            
        elif token_agora.type == "FUNCTION":
            # FuncDec.value = tipo de retorno
            # FuncDec.children = [Identifier, VarDec, VarDec, VarDec, ..., Block]
            Parser.tokenizer.selectNext()
            token_agora = Parser.tokenizer.next
            
            if token_agora.type == "ID":
                func_ident = Identifier(token_agora.value)
                Parser.tokenizer.selectNext()
                token_agora = Parser.tokenizer.next
                
                
                if token_agora.type == "OPEN":
                    Parser.tokenizer.selectNext()
                    token_agora = Parser.tokenizer.next
                    
                    lista_args = []
                    lista_args.append(func_ident)
                    while token_agora.type != "CLOSE":
                        # ID :: TYPE, ID :: TYPE, ID :: TYPE...
                        if token_agora.type == "ID":
                            param_ident = Identifier(token_agora.value)
                            Parser.tokenizer.selectNext()
                            token_agora = Parser.tokenizer.next
                            
                            if token_agora.type == "DECLARATOR":
                                Parser.tokenizer.selectNext()
                                token_agora = Parser.tokenizer.next
                                
                                if token_agora.type == "TYPE":
                                    varType = Parser.tokenizer.next.value
                                    Parser.tokenizer.selectNext()
                                    token_agora = Parser.tokenizer.next
                                    if varType == "Int":
                                        lista_args.append(VarDec(varType, [param_ident, IntVal(0)]))
                                    elif varType == "String":
                                        lista_args.append(VarDec(varType, [param_ident, StrVal("")]))
                                    
                                    if token_agora.type == "COMMA":
                                        Parser.tokenizer.selectNext()
                                        token_agora = Parser.tokenizer.next
                                        
                                    elif token_agora.type == "CLOSE":
                                        break
                                        
                                    else:
                                        raise Exception("Erro de sintaxe")                                    
                                else:
                                    raise Exception("Erro de sintaxe")
                            else:
                                raise Exception("Erro de sintaxe")
                        else:
                            raise Exception("Erro de sintaxe")
                        
                    if token_agora.type == "CLOSE":
                        Parser.tokenizer.selectNext()
                        token_agora = Parser.tokenizer.next
                        
                        if token_agora.type == "DECLARATOR":
                            Parser.tokenizer.selectNext()
                            token_agora = Parser.tokenizer.next
                            
                            if token_agora.type == "TYPE":
                                func_tipo = Parser.tokenizer.next.value
                                Parser.tokenizer.selectNext()
                                token_agora = Parser.tokenizer.next
                                
                                if token_agora.type == "NEWLINE":
                                    Parser.tokenizer.selectNext()
                                    token_agora = Parser.tokenizer.next
                                    
                                    lista_func_children = []
                                    while token_agora.type != "END":
                                        # guarda os statements em uma variavel e depois passa pra children como Block
                                        lista_func_children.append(Parser.parseStatement())
                                        token_agora = Parser.tokenizer.next
                                        
                                    lista_args.append(Block(lista_func_children))
                                    
                                    if token_agora.type == "END":
                                        Parser.tokenizer.selectNext()
                                        token_agora = Parser.tokenizer.next
                                        
                                        if token_agora.type == "NEWLINE":
                                            Parser.tokenizer.selectNext()
                                            token_agora = Parser.tokenizer.next
                                            
                                            return FuncDec(func_tipo, lista_args)
                                        
                                        else:
                                            raise Exception("Erro de sintaxe")
                                    else:
                                        raise Exception("Erro de sintaxe")
                                else:
                                    raise Exception("Erro de sintaxe")
                            else:
                                raise Exception("Erro de sintaxe")
                        else:
                            raise Exception("Erro de sintaxe")
                    else:
                        raise Exception("Erro de sintaxe")
                else:
                    raise Exception("Erro de sintaxe")
            else:
                raise Exception("Erro de sintaxe")
            
        
        elif token_agora.type == "PRINTLN":
            
            Parser.tokenizer.selectNext()
            token_agora = Parser.tokenizer.next
            
            
            if token_agora.type == "OPEN":
                Parser.tokenizer.selectNext()
                token_agora = Parser.tokenizer.next
                
                
                res = Parser.parseRelExpression()
                current_token = Parser.tokenizer.next
                
                if current_token.type == "CLOSE":
                    Parser.tokenizer.selectNext()
                    token_agora = Parser.tokenizer.next
                    res = Println([res])
                    #Parser.tokenizer.selectNext()
                    #token_agora = Parser.tokenizer.next
                    
                    if token_agora.type == "NEWLINE":
        
                        return res
                    else:
                        raise Exception("Erro de sintaxe")

                else:
                    raise Exception("Erro de sintaxe")
            else:
                raise Exception("Erro de sintaxe")
            
        elif token_agora.type == "WHILE":
            Parser.tokenizer.selectNext()
            condition = Parser.parseRelExpression()
            if Parser.tokenizer.next.type == "NEWLINE":
                lista_while_children = []
                while Parser.tokenizer.next.type != "END":
                    lista_while_children.append(Parser.parseStatement())

                res = While([condition, Block(lista_while_children)])
                if Parser.tokenizer.next.type == "END":
                    
                    Parser.tokenizer.selectNext()
                    token_agora = Parser.tokenizer.next
                    if Parser.tokenizer.next.type == "NEWLINE":
                        
                        Parser.tokenizer.selectNext()
                        token_agora = Parser.tokenizer.next
                        return res
                    else:
                        raise Exception("Erro de sintaxe")
                return res
            
        elif token_agora.type == "IF":
            Parser.tokenizer.selectNext()
            condition = Parser.parseRelExpression()
            if Parser.tokenizer.next.type == "NEWLINE":
                lista_if_children = []
                parser.tokenizer.selectNext()
                while Parser.tokenizer.next.type != "END" and Parser.tokenizer.next.type != "ELSE":
                    lista_if_children.append(Parser.parseStatement())
                res = If([condition, Block(lista_if_children)])
                if Parser.tokenizer.next.type == "END":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "NEWLINE":
                        Parser.tokenizer.selectNext()
                    else:
                        raise Exception("Erro de sintaxe")
                
                elif Parser.tokenizer.next.type == "ELSE":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "NEWLINE":
                        Parser.tokenizer.selectNext()
                        
                        lista_else_children = []
                        while Parser.tokenizer.next.type != "END":
                            lista_else_children.append(Parser.parseStatement())
                            
                        token_agora = Parser.tokenizer.next
                        res = If([res, Block(lista_if_children), Block(lista_else_children)])
                        
                        if Parser.tokenizer.next.type == "END":
                            Parser.tokenizer.selectNext()
                            token_agora = Parser.tokenizer.next
                            if Parser.tokenizer.next.type == "NEWLINE":
                                Parser.tokenizer.selectNext()
                                token_agora = Parser.tokenizer.next
                            else:
                                raise Exception("Erro de sintaxe")
                        else:
                            raise Exception("Erro de sintaxe")
                    else:
                        raise Exception("Erro de sintaxe")
                else:
                    raise Exception("Erro de sintaxe") 
            else:
                raise Exception("Erro de sintaxe")
            
        
        
            
                
            return res
        elif token_agora.type == "NEWLINE":
            
            Parser.tokenizer.selectNext()
            token_agora = Parser.tokenizer.next
            
            return NoOp()
        
        else:
            raise Exception("Erro de sintaxe")

    @staticmethod
    def parseRelExpression():
        res = Parser.parseExpression()
        token_agora = Parser.tokenizer.next
        
        
        while token_agora.type == "LESS" or token_agora.type == "GREATER" or token_agora.type == "EQUAL":
            if token_agora.type == "LESS":
                Parser.tokenizer.selectNext()
                res = BinOp("<", [res, Parser.parseExpression()])
                
            elif token_agora.type == "GREATER":
                Parser.tokenizer.selectNext()
                res = BinOp(">", [res, Parser.parseExpression()])

            elif token_agora.type == "EQUAL":
                Parser.tokenizer.selectNext()
                res = BinOp("==", [res, Parser.parseExpression()])

            token_agora = Parser.tokenizer.next
            
            
        return res

    @staticmethod
    def parseExpression():
        res = Parser.parseTerm()
        token_agora = Parser.tokenizer.next
        
        

        while token_agora.type == "MINUS" or token_agora.type == "PLUS" or token_agora.type == "OR" or token_agora.type == "CONCAT":
            if token_agora.type == "MINUS":
                Parser.tokenizer.selectNext()
                res = BinOp("-", [res, Parser.parseTerm()])

            elif token_agora.type == "PLUS":
                Parser.tokenizer.selectNext()
                res = BinOp("+", [res, Parser.parseTerm()])
                
            elif token_agora.type == "OR":
                Parser.tokenizer.selectNext()
                res = BinOp("||", [res, Parser.parseTerm()])
                
            elif token_agora.type == "CONCAT":
                Parser.tokenizer.selectNext()
                res = BinOp(".", [res, Parser.parseTerm()])
            
            token_agora = Parser.tokenizer.next
            

        return res

            
                
    @staticmethod
    def parseTerm():
        res = Parser.parseFactor()
        token_agora = Parser.tokenizer.next
        
        

        while token_agora.type == "MULT" or token_agora.type == "DIV" or token_agora.type == "AND":
            if token_agora.type == "DIV":
                Parser.tokenizer.selectNext()
                res = BinOp("/", [res, Parser.parseFactor()])
            

            elif token_agora.type == "MULT":
                Parser.tokenizer.selectNext()
                res = BinOp("*", [res, Parser.parseFactor()])
                
            elif token_agora.type == "AND":
                Parser.tokenizer.selectNext()
                res = BinOp("&&", [res, Parser.parseFactor()])
            
            token_agora = Parser.tokenizer.next
            

        return res

    
    
    @staticmethod
    def parseFactor():
        token_agora = Parser.tokenizer.next
        

        if token_agora.type == "INT":

            Parser.tokenizer.selectNext()
            res = IntVal(token_agora.value)
            
        elif token_agora.type == "STRING":
            
            Parser.tokenizer.selectNext()
            res = StrVal(token_agora.value)

        elif token_agora.type == "MINUS":

            Parser.tokenizer.selectNext()
            res = UnOp("-", [Parser.parseFactor()])

        elif token_agora.type == "PLUS":
            Parser.tokenizer.selectNext()
            res = UnOp("+", [Parser.parseFactor()])
            
        elif token_agora.type == "NOT":
            Parser.tokenizer.selectNext()
            res = UnOp("!", [Parser.parseFactor()])

        elif token_agora.type == "ID":
            Parser.tokenizer.selectNext()
            
            res = Identifier(token_agora.value)
            
            if Parser.tokenizer.next.type == "OPEN":
                Parser.tokenizer.selectNext()
                token_agora = Parser.tokenizer.next
                
                lista_args = []
                while token_agora.type != "CLOSE":
                    lista_args.append(Parser.parseRelExpression())
                    token_agora = Parser.tokenizer.next
                    
                    if token_agora.type == "COMMA":
                        Parser.tokenizer.selectNext()
                        token_agora = Parser.tokenizer.next
                    else:
                        break
                    
                
                res = FuncCall(res.value, lista_args)
                
                if token_agora.type != "CLOSE":
                    raise Exception("Erro de sintaxe: Não fechou o parênteses")
                
                Parser.tokenizer.selectNext() ### possivel erro
                token_agora = Parser.tokenizer.next ### possivel erro


        elif token_agora.type == "OPEN":

            Parser.tokenizer.selectNext()
            
            res = Parser.parseRelExpression()
            token_agora = Parser.tokenizer.next

            
            


            if token_agora.type != "CLOSE":
                raise Exception("Erro de sintaxe: Não fechou o parênteses")
            
            Parser.tokenizer.selectNext()
            token_agora = Parser.tokenizer.next
            
            
        elif token_agora.type == "READLINE":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "OPEN":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "CLOSE":

                    Parser.tokenizer.selectNext()
                    res = Readln(None) ### não sei se é assim que se faz
                    
                else:
                    raise Exception("Erro de sintaxe: Não fechou o parênteses")

        
        else:
            raise Exception("Erro de sintaxe factor")
        
        return res
        

    @staticmethod
    def run(codigo):
        Parser.symbol_table = SymbolTable()
        Parser.function_table = FunctionTable()
        codigo = PrePro.filter(codigo)
        Parser.tokenizer = Tokenizer(codigo)
        Parser.tokenizer.selectNext()
        resultado = Parser.parseBlock()

        evaluate = resultado.evaluate(Parser.symbol_table)


        if Parser.tokenizer.next.type == "EOF":
            return evaluate
        
        else:
            raise Exception("Erro de sintaxe")
        

parser = Parser()

func_table = FunctionTable()
# get arguments from command line
args = sys.argv

with open(args[1], "r") as f:
    codigo = f.read()
    parser.run(codigo)

