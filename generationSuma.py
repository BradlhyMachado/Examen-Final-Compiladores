import copy
from parser import ll1

ruta = "Tests/test3.txt"
root, _ = ll1(ruta)

listDecla = []
code = ''
decla = ''
asig = ''

##============================================================================================##

def getExpresiones(node):
    my_list = [node]
    pila = copy.deepcopy(my_list)
    finales = []
    while len(pila) > 0:
        if len(pila[0].children) > 0:
            piv = pila[0].children
            pila.pop(0)

            while len(piv) > 0:
                pila.insert(0, piv[0])
                piv.pop(0)
        else:
            list = [pila[0].symbol.symbol, pila[0].lexeme]
            if str(list[1]) != 'None':
                finales.append(list)
            pila.pop(0)
            list = []
    del pila
    return(finales[::-1])


def getEvaluation(expresiones):
    signos = ['suma', 'resta', 'multiplicacion', 'division']
    numeros = []
    operaciones = []
    evaluar = []
    aux = 0
    id = ()

    for i in range(len(expresiones)):
        if (i == 0) or (i == 1):
            if str(expresiones[i][0]) == 'id':
                id = ((expresiones[i][0], expresiones[i][1]))
                continue
        else:
            if str(expresiones[i][0]) == 'id':
                numeros.append((expresiones[i][0], expresiones[i][1]))
            if str(expresiones[i][0]) == 'numero':
                numeros.append((expresiones[i][0], expresiones[i][1]))
            if str(expresiones[i][0]) in signos:
                operaciones.append((expresiones[i][0], expresiones[i][1]))
    
    for num in numeros:
        evaluar.append(num)
        aux += 1
        if aux >= 2:
            while len(operaciones)>0:
                op = operaciones.pop(0)
                evaluar.append(op)
                break
    del signos
    del operaciones
    print(evaluar)
    return(evaluar, id)


def cgen_decla(node):
    global decla
    global listDecla
    if node.symbol.symbol == 'DECLA':
        listDecla = getExpresiones(node)
        expresiones = listDecla.copy()

        if str(expresiones[0][0]) == "numerico":
            decla += "\tvar_"
            decla += str(expresiones[1][1]) + (":")
            decla += "  .word  0:1\n"

    for child in node.children:
        cgen_decla(child)


def cgen_asig(node):
    global asig
    global listDecla

    if node.symbol.symbol == 'DECLA':
        listDecla = getExpresiones(node)
        expresiones = listDecla.copy()
        evaluar, idVar = getEvaluation(expresiones)

        primero = 0

        while len(evaluar) > 0:
            exp = evaluar.pop(0)
            
            if str(exp[0]) == 'numero':
                asig += "\n"
                asig += "\tli $a0, "
                asig += exp[1] + ("\n")
                primero += 1

                if primero == 1:
                    asig += "\n"
                    asig += "\tsw $a0 0($sp)\n"
                    asig += "\tadd $sp $sp -4\n"
                    continue

            if str(exp[0]) == 'suma':
                asig += "\n"
                asig += "\tlw $t0 4($sp)\n"
                asig += "\tadd $a0 $t0 $a0\n"
                asig += "\tadd $sp $sp 4\n"
            
        if str(idVar[0]) == 'id':
            asig += "\n"
            asig += "\tla $t1, var_"
            asig +=  idVar[1] + ("\n")
            asig += "\tsw $a0, 0($t1)\n"

    for child in node.children:
        cgen_asig(child)


def cgen_all():
    global code
    global decla
    global asig

    code += ".data\n"
    
    cgen_decla(root)
    code += decla
    del decla

    code += ".text\n"
    code += "main:\n"
    
    cgen_asig(root)
    code += asig
    del asig
    
    code += "\n"
    code += "\tjr $ra"


def write_file(codeFile):
    codeFile.write(code)
    codeFile.close()

# Main
if __name__ == "__main__":
    codeFile = open("Codigos_obtenidos/generatedCode.s", "w")
    cgen_all()
    write_file(codeFile)