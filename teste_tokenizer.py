reserved_words = ["println", "if", "else", "while", "end", "readln"]

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
                
                if char == " " or char in "+-*/()=<>|&!" or char == "\n": # se for um espaço ou um operador então o token é formado
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

                if char == " " or char in "+-*/()=<>|&!" or char == "\n": 
                    flag_token = False
                    self.next = Token("INT", int(numero))
                else:
                    numero += char

        elif char in "+-*/()=<>|&!" or char == "\n":
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
                
            
            self.position += 1
            
        elif char == " ": # se for um espaço
            self.position += 1
            self.selectNext()
            
            
word = """
println(readline())
"""
            
prepro = PrePro(word)
code_filtered = prepro.filter(word)

tokenizer = Tokenizer(code_filtered)
tokenizer.selectNext()
print(f'{tokenizer.next.type}: {tokenizer.next.value}')
while (tokenizer.next.type!='EOF'):
    tokenizer.selectNext()
    print(f'{tokenizer.next.type}: {tokenizer.next.value}')