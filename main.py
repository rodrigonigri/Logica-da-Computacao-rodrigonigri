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


class PrePro():
    def __init__(self, source):
        self.source = source

    @staticmethod
    def filter(source):
        return source.split("#")[0]


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

        if char in "0123456789":
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

                if char == " " or char in "+-*/()":
                    flag_token = False
                    self.next = Token("INT", int(numero))
                else:
                    numero += char

        elif char in "+-*/()":
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

            
            self.position += 1
            
        elif char == " ": # se for um espaço
            self.position += 1
            self.selectNext()
        


class Parser():

    @staticmethod
    def parseFactor():
        token_agora = Parser.tokenizer.next

        if token_agora.type == "INT":
            #res = token_agora.value
            res = IntVal(token_agora.value)
            Parser.tokenizer.selectNext()

        elif token_agora.type == "MINUS":
            Parser.tokenizer.selectNext()
            res = UnOp("-", [Parser.parseFactor()])
            #res = (-1) * Parser.parseFactor()

        elif token_agora.type == "PLUS":
            Parser.tokenizer.selectNext()
            token_agora = Parser.tokenizer.next
            res = UnOp("+", [Parser.parseFactor()])
            #res = Parser.parseFactor()

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
        resultado = Parser.parseExpression()

        evaluate = resultado.evaluate()


        if Parser.tokenizer.next.type == "EOF":
            return evaluate
        
        else:
            raise Exception("Erro de sintaxe")
        

parser = Parser()

# get arguments from command line
args = sys.argv

print(parser.run(args[1]))

