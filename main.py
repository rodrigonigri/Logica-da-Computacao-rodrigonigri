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

reserved_words = ["println", "if", "else", "while", "end", "readline", "Int", "String"]

class AssemblyHandler():
    def write(text):
        filename = args[1].split(".")[0]
        with open(f"{filename}.asm", "r") as file:
            whole_file = file.read()
        with open(f"{filename}.asm", "w") as file:
            file.write(whole_file)
            file.write(text + "\n")
            

class Node():
    i = 0
    
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self):
        pass
    
    def new_id(self):
        Node.i += 1
        return Node.i

class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
        self.id = self.new_id()

    def evaluate(self):
        if self.value == "-":
            return ("Int",-1 * self.children[0].evaluate()[1])
        
        elif self.value == "+":
            return ("Int",self.children[0].evaluate()[1])
        
        elif self.value == "!":
            return ("Int",not self.children[0].evaluate()[1])

class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
        self.id = self.new_id()

    def evaluate(self):
        operator = ""
        
        self.children[0].evaluate()
        AssemblyHandler.write("PUSH EBX")
        self.children[1].evaluate()
        AssemblyHandler.write("POP EAX")
        
        if self.value in "+-*/":
            if self.value == "+":
                operator = "ADD"

            elif self.value == "-":
                operator = "SUB"

            elif self.value == "*":
                operator = "IMUL"

            elif self.value == "/":
                operator = "IDIV"
            
            elif self.value == "||":
                operator = "OR"
                
            elif self.value == "&&":    
                operator = "AND"
            
            AssemblyHandler.write(f"{operator} EAX, EBX")
            AssemblyHandler.write("MOV EBX, EAX")
            
        elif self.value in ['>','<','==']:
            if self.value == "==":
                operator = "binop_je"
            elif self.value == ">":
                operator = "binop_jg"
            elif self.value == "<":
                operator = "binop_jl"
            
            AssemblyHandler.write(f"CMP EAX, EBX")
            AssemblyHandler.write(f"CALL {operator}")
            
        '''
        if self.value == ".":
            return ("String", str(self.children[0].evaluate()[1]) + str(self.children[1].evaluate()[1]))
        elif self.value == "==":
            operator = "CMP"
            return ("Int", int(self.children[0].evaluate()[1] == self.children[1].evaluate()[1]))
        elif self.value == ">":
            operator
            return ("Int", int(self.children[0].evaluate()[1] > self.children[1].evaluate()[1]))
        elif self.value == "<":
            return ("Int", int(self.children[0].evaluate()[1] < self.children[1].evaluate()[1]))
        
        else:
            if self.children[0].evaluate()[0] == "Int" and self.children[1].evaluate()[0] == "Int":
                
                if self.value == "+":
                    operator = "ADD"
                    return ("Int", self.children[0].evaluate()[1] + self.children[1].evaluate()[1])

                elif self.value == "-":
                    operator = "SUB"
                    return ("Int", self.children[0].evaluate()[1] - self.children[1].evaluate()[1])

                elif self.value == "*":
                    operator = "MUL"
                    return ("Int", self.children[0].evaluate()[1] * self.children[1].evaluate()[1])

                elif self.value == "/":
                    operator = "DIV"
                    return ("Int", self.children[0].evaluate()[1] // self.children[1].evaluate()[1])
                
                
                
                elif self.value == "||":
                    operator = "OR"
                    return ("Int", int(self.children[0].evaluate()[1] or self.children[1].evaluate()[1]))
                elif self.value == "&&":
                    operator = "AND"
                    return ("Int", int(self.children[0].evaluate()[1] and self.children[1].evaluate()[1]))
                
                
                AssemblyHandler.write(f"{operator} EAX, EBX;")
                AssemblyHandler.write("MOV EBX, EAX;")
            
            else:
                raise Exception("Type error")
                '''

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value, [])
        self.id = self.new_id()

    def evaluate(self):
        AssemblyHandler.write(f"MOV EBX, {str(self.value)}")
    
    
class StrVal(Node):
    def __init__(self, value):
        super().__init__(value, [])
        self.id = self.new_id()
    
    def evaluate(self):
        return ("String",self.value)
    

class NoOp(Node):
    def __init__(self):
        super().__init__(None, [])
        self.id = self.new_id()

    def evaluate(self):
        pass


class Block(Node):
    def __init__(self, children):
        super().__init__(None, children)
        self.id = self.new_id()

    def evaluate(self):
        for child in self.children:
            child.evaluate()


class Identifier(Node):
    def __init__(self, value):
        super().__init__(value, [])
        self.id = self.new_id()

    def evaluate(self):
        AssemblyHandler.write(f"MOV EBX, [EBP{SymbolTable.getter(self.value)[2]}]")
    

class Println(Node):
    def __init__(self, children):
        super().__init__(None, children)
        self.id = self.new_id()

    def evaluate(self):
        #print(self.children[0].evaluate()[1])
        self.children[0].evaluate()
        AssemblyHandler.write("PUSH EBX")
        AssemblyHandler.write("CALL print")
        AssemblyHandler.write("POP EBX")
        


class Assignment(Node):
    def __init__(self, children):
        super().__init__(None, children)
        self.id = self.new_id()

    def evaluate(self):
        
        #SymbolTable.setter(self.children[0].value, self.children[1].evaluate())
        self.children[1].evaluate()
        AssemblyHandler.write(f"MOV [EBP{SymbolTable.getter(self.children[0].value)[2]}], EBX")
        
class Readln(Node):
    def __init__(self, children):
        super().__init__(None, children)
        self.id = self.new_id()

    def evaluate(self):
        return ("Int",int(input()))
    
class If(Node):
    def __init__(self, children):
        super().__init__(None, children)
        self.id = self.new_id()

    def evaluate(self):
        if len(self.children) == 2: #if without else
            self.children[0].evaluate()
            AssemblyHandler.write(f"CMP EBX, 0")
            AssemblyHandler.write(f"JE ELSE_{self.id}")
            self.children[1].evaluate()
            
            
            #if self.children[0].evaluate()[1]:
            #    self.children[1].evaluate()
        else: #if with else
            self.children[0].evaluate()
            AssemblyHandler.write(f"CMP EBX, 0")
            AssemblyHandler.write(f"JE ELSE_{self.id}")
            self.children[1].evaluate()
            AssemblyHandler.write(f"JMP EXIT_{self.id}")
            AssemblyHandler.write(f"ELSE_{self.id}:")
            self.children[2].evaluate()
            AssemblyHandler.write(f"EXIT_{self.id}:")
            
            #if self.children[0].evaluate():
            #    self.children[1].evaluate()
            #else:
            #    self.children[2].evaluate()
                
class While(Node):
    def __init__(self, children):
        super().__init__(None, children)
        self.id = self.new_id()

    def evaluate(self):
        AssemblyHandler.write(f"LOOP_{self.id}:")
        self.children[0].evaluate()
        AssemblyHandler.write(f"CMP EBX, 0")
        AssemblyHandler.write(f"JE EXIT_{self.id}")
        self.children[1].evaluate()
        AssemblyHandler.write(f"JMP LOOP_{self.id}")
        AssemblyHandler.write(f"EXIT_{self.id}:")
        
        #while self.children[0].evaluate()[1]:
        #    self.children[1].evaluate()
            

class VarDec(Node):
    def __init__(self, value ,children):
        super().__init__(value, children)
        self.id = self.new_id()
        
    def evaluate(self):
        SymbolTable.create(self.children[0].value, self.value, (-4) * (len(SymbolTable.table) + 1))
        AssemblyHandler.write(f"PUSH DWORD 0")
        #SymbolTable.setter(self.children[0].value, self.children[1].evaluate())
        self.children[-1].evaluate()
        AssemblyHandler.write(f"MOV [EBP{SymbolTable.getter(self.children[0].value)[2]}], EBX")



class SymbolTable(): # chama SymbleTabel.setter("x", 10) pra setar o valor de x ou SymbolTable.getter("x") pra pegar o valor de x
    table = {}
    
    def create(key, type, shift):
        # verifica se a variável já foi declarada
        if key in SymbolTable.table:
            raise Exception("Variável já declarada")
        SymbolTable.table[key] = (type, None, shift)
        
    
    def setter(key, value_tuple):
        #verifica se a variável já foi declarada
        if key not in SymbolTable.table:
            raise Exception("Variável não declarada")
        #verifica se o tipo da variável é o mesmo do valor que está sendo atribuído
        if SymbolTable.table[key][0] != value_tuple[0]:
            raise Exception("Tipos incompatíveis")
        #atribui o valor
        SymbolTable.table[key] = value_tuple


    def getter(key):
        if key not in SymbolTable.table:
            raise Exception("Variável não declarada")
        return SymbolTable.table[key]


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
                
                if char == " " or char in "+-*/()=<>|&!:." or char == "\n": # se for um espaço ou um operador então o token é formado
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

                if char == " " or char in "+-*/()=<>|&!:." or char == "\n": 
                    flag_token = False
                    self.next = Token("INT", int(numero))
                else:
                    numero += char

        elif char in "+-*/()=<>|&!:." or char == "\n":
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
                

                #print(res.children[1].children[0])
                if token_agora.type == "NEWLINE" or token_agora.type == "EOF":
                    
                    Parser.tokenizer.selectNext()
                    token_agora = Parser.tokenizer.next
                    
                    return res
                else:
                    raise Exception("Erro de sintaxe na declaração de variável")
            else:
                raise Exception("Erro de sintaxe na declaração de variável")

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
        codigo = PrePro.filter(codigo)
        Parser.tokenizer = Tokenizer(codigo)
        Parser.tokenizer.selectNext()
        resultado = Parser.parseBlock()

        evaluate = resultado.evaluate()


        if Parser.tokenizer.next.type == "EOF":
            return evaluate
        
        else:
            raise Exception("Erro de sintaxe")
        

parser = Parser()

# get arguments from command line
args = sys.argv

with open(args[1], "r") as f:
    codigo = f.read()
    # create new file args[1].split(".")[0] + ".asm" file
    with open(args[1].split(".")[0] + ".asm", "w") as f:
        pass
    parser.run(codigo)
    

