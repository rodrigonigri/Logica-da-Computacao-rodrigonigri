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

                if char == " " or char in "+-":
                    flag_token = False
                    self.next = Token("INT", int(numero))
                else:
                    numero += char

        elif char in "+-":
            if char == "-":
                self.next = Token("MINUS", "-")
            
            elif char == "+":
                self.next = Token("PLUS", "+")
            
            self.position += 1
            
        elif char == " ": # se for um espaço
            self.position += 1
            self.selectNext()
        


class Parser():

    @staticmethod
    def parseExpression():
        token_agora = Parser.tokenizer.next
        res = token_agora.value

        if token_agora.type == "INT":
            Parser.tokenizer.selectNext()
            token_agora = Parser.tokenizer.next


            while token_agora.type == "MINUS" or token_agora.type == "PLUS":
                if token_agora.type == "MINUS":
                    Parser.tokenizer.selectNext()
                    token_agora = Parser.tokenizer.next
                    if token_agora.type == "INT":
                        res -= Parser.tokenizer.next.value

                    elif token_agora.type != "INT":
                        raise Exception("Erro de sintaxe")

                elif token_agora.type == "PLUS":
                    Parser.tokenizer.selectNext()
                    token_agora = Parser.tokenizer.next
                    if token_agora.type == "INT":
                        res += Parser.tokenizer.next.value

                    elif token_agora.type != "INT":
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

# get arguments from command line
args = sys.argv

print(parser.run(args[1]))

