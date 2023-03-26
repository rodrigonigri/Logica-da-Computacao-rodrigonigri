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
    else:
        print("\033[99m {}\033[00m" .format(text))

reserved_words = ["println"]

class Node():
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self):
        pass

class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        if self.value == "-":
            return -1 * self.children[0].evaluate()
        
        elif self.value == "+":
            return self.children[0].evaluate()

class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        if self.value == "+":
            return self.children[0].evaluate() + self.children[1].evaluate()

        elif self.value == "-":
            return self.children[0].evaluate() - self.children[1].evaluate()

        elif self.value == "*":
            return self.children[0].evaluate() * self.children[1].evaluate()

        elif self.value == "/":
            return self.children[0].evaluate() // self.children[1].evaluate()
        

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self):
        return self.value
    

class NoOp(Node):
    def __init__(self):
        super().__init__(None, [])

    def evaluate(self):
        pass


class Block(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self):
        for child in self.children:
            child.evaluate()


class Identifier(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self):
        return SymbolTable.getter(self.value)
    

class Println(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self):
        print(self.children[0].evaluate())


class Assignment(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self):
        SymbolTable.setter(self.children[0].value, self.children[1].evaluate())


class SymbolTable(): # chama SymbleTabel.setter("x", 10) pra setar o valor de x ou SymbolTable.getter("x") pra pegar o valor de x
    table = {}
    def setter(key, value):
        SymbolTable.table[key] = value


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
                
                if char == " " or char in "+-*/()=" or char == "\n": # se for um espaço ou um operador então o token é formado
                    flag_token = False
                    if palavra in reserved_words: # se for uma palavra reservada
                        self.next = Token(palavra.upper(), palavra)
                    else: 
                        self.next = Token("ID", palavra)

                else:
                    palavra += char

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

                if char == " " or char in "+-*/()=" or char == "\n": 
                    flag_token = False
                    self.next = Token("INT", int(numero))
                else:
                    numero += char

        elif char in "+-*/()=" or char == "\n":
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
            
            elif char == "=":
                self.next = Token("EQUALS", "=")

            elif char == "\n":
                self.next = Token("NEWLINE", "\n")


            
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

            if token_agora.type == "EQUALS":
                Parser.tokenizer.selectNext()
                token_agora = Parser.tokenizer.next
                res = Assignment([temp, Parser.parseExpression()]) # possivel erro
                #Parser.tokenizer.selectNext()

                token_agora = Parser.tokenizer.next

                #print(res.children[1].children[0])
                if token_agora.type == "NEWLINE" or token_agora.type == "EOF":
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
                res = Parser.parseExpression()
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

        elif token_agora.type == "NEWLINE":
            Parser.tokenizer.selectNext()
            return NoOp()
        
        else:
            raise Exception("Erro de sintaxe")


    @staticmethod
    def parseFactor():
        token_agora = Parser.tokenizer.next

        if token_agora.type == "INT":
            #res = token_agora.value
            Parser.tokenizer.selectNext()
            res = IntVal(token_agora.value)

        elif token_agora.type == "MINUS":
            Parser.tokenizer.selectNext()
            res = UnOp("-", [Parser.parseFactor()])
            #res = (-1) * Parser.parseFactor()

        elif token_agora.type == "PLUS":
            Parser.tokenizer.selectNext()
            #token_agora = Parser.tokenizer.next
            res = UnOp("+", [Parser.parseFactor()])
            #res = Parser.parseFactor()

        elif token_agora.type == "ID":
            Parser.tokenizer.selectNext()
            res = Identifier(token_agora.value)


        elif token_agora.type == "OPEN":
            Parser.tokenizer.selectNext()
            #res = Parser.parseExpression()
            res = Parser.parseExpression()
            token_agora = Parser.tokenizer.next

            if token_agora.type != "CLOSE":  
                raise Exception("Erro de sintaxe: Não fechou o parênteses")
            Parser.tokenizer.selectNext()
        
        else:
            raise Exception("Erro de sintaxe factor")
        
        return res

            
                
    @staticmethod
    def parseTerm():
        res = Parser.parseFactor()
        token_agora = Parser.tokenizer.next
        

        while token_agora.type == "MULT" or token_agora.type == "DIV":
            if token_agora.type == "DIV":
                Parser.tokenizer.selectNext()
                #res //= Parser.parseFactor()
                res = BinOp("/", [res, Parser.parseFactor()])
            

            elif token_agora.type == "MULT":
                Parser.tokenizer.selectNext()
                #res *= Parser.parseFactor()
                res = BinOp("*", [res, Parser.parseFactor()])
            
            token_agora = Parser.tokenizer.next

        return res

    @staticmethod
    def parseExpression():
        res = Parser.parseTerm()
        token_agora = Parser.tokenizer.next
        

        while token_agora.type == "MINUS" or token_agora.type == "PLUS":
            if token_agora.type == "MINUS":
                Parser.tokenizer.selectNext()
                #res -= Parser.parseTerm()
                res = BinOp("-", [res, Parser.parseTerm()])
        

            elif token_agora.type == "PLUS":
                Parser.tokenizer.selectNext()
                #res += Parser.parseTerm()
                res = BinOp("+", [res, Parser.parseTerm()])
            
            token_agora = Parser.tokenizer.next

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


    parser.run(codigo)




