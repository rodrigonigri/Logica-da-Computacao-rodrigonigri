import sys
import re

# get arguments from command line
args = sys.argv


def print_colored(text, color):
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

def recebe_conta(conta):
    resultado = 0
    lista_temp = []
    lista_positivos = []
    lista_negativos = []

    # verifica se existe operador no final da string
    if conta[-1] in "+-":
        raise Exception ("Erro Sintático")

    # verfica se primeiro caractere é um número
    if conta[0] not in "0123456789 ":
        raise Exception ("Erro")

    # verifica se existe algum caractere inválido
    for i in conta:
        if i not in "0123456789+- ":
            raise Exception ("Erro Léxico")

    # verifica se existem operadores seguidos
    for i in range(len(conta)):
        if conta[i] in "+-":
            if conta[i+1] in "+-":
                raise Exception ("Erro Sintático")
        
    

    # verifica se existe espaço entre dois números
    if re.search(r"\d\s+\d", conta):
        raise Exception ("Erro Sintático")

    # manipula a string para separar os números e colocar em uma lista
    conta_split = conta.split("-")
    for i in conta_split:
        var_temp = i.split("+")
        lista_temp.append(var_temp)

    # soma os números positivos e negativos separando-os em duas listas diferentes
    for i in range(len(lista_temp)):
        if i == 0:
            for j in range(len(lista_temp[i])):
                lista_positivos.append(int(lista_temp[i][j]))
        else:
            for j in range(len(lista_temp[i])):
                if j == 0:
                    lista_negativos.append(int(lista_temp[i][j]))
                else:
                    lista_positivos.append(int(lista_temp[i][j]))
            

    resultado = sum(lista_positivos) - sum(lista_negativos)

    return resultado
        



print(recebe_conta(args[1]))
