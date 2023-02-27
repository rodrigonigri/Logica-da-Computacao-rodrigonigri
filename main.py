import sys

# get arguments from command line
args = sys.argv


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

class Token():
    def _init_(self, type, value): # type is a string, value is a int
        self.type = type
        self.value = value 


class Tokenizer():
    def _init_(self, source):
        self.source = source
        self.position = 0
        self.next = None

    def selectNext(self):
        operacoes = "+-"
        numeros = "0123456789"


        if self.position >= len(self.source):
            return Token("EOF", None)
        
        else:

            char = self.source[self.position]

            self.position += 1
            if char in operacoes:
                if char == "+":
                    self.next = Token("PLUS", "+")
                elif char == "-":
                    self.next = Token("MINUS", "-")
            
            elif char in numeros:
            
                number = ""
                while char in numeros:
                    number += char
                    char = self.source[self.position]
                    self.position += 1

                self.next = Token("INT", int(number))
                self.position -= 1

            elif char == " ":
                self.position += 1
                self.selectNext()

class Parser():
    tokenizer = None
    @staticmethod
    def parseExpression():
        token_agora = Parser.tokenizer.next
        if token_agora.type == "INT":
            res = token_agora.value
            Parser.tokenizer.selectNext()
            token_agora = Parser.tokenizer.next

            while token_agora.type == "PLUS" or token_agora.type == "MINUS":
                if token_agora.type == "MINUS":
                    Parser.tokenizer.selectNext()
                    token_agora = Parser.tokenizer.next
                    if token_agora.type == "INT":
                        res -= token_agora.value
                    else:
                        raise Exception("Erro de sintaxe")

                elif token_agora.type == "PLUS":
                    Parser.tokenizer.selectNext()
                    token_agora = Parser.tokenizer.next
                    if token_agora.type == "INT":
                        res += token_agora.value
                    else:
                        raise Exception("Erro de sintaxe")
                
                Parser.tokenizer.selectNext()
                token_agora = Parser.tokenizer.next
            
            return res
        
        else:
            raise Exception("Erro de sintaxe")
    @staticmethod
    def run(codigo):
        Parser.tokenizer = Tokenizer(codigo)
        Parser.tokenizer.selectNext()
        resultado = Parser.parseExpression()

        if Parser.tokenizer.next.type == "EOF":
            return resultado
        else:
            raise Exception("Erro de sintaxe")
        

parser = Parser()
print(parser.run(sys.argv[1]))