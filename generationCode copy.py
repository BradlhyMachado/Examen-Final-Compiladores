import copy
from parser import ll1

ruta = "Tests/test4.txt"
root, _ = ll1(ruta)

listDecla = []
code = ''
decla = ''
asig = ''
cond = ''
invFun = ''
fun = ''

contCond = 0

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
    del pila, my_list
    return(finales[::-1])


def getEvaluationOp(expresiones):
    signos = ['suma', 'resta', 'multiplicacion', 'division', 'mayor_que', 'menor_que']
    numeros = []
    operaciones = []
    evaluar = []
    aux = 0
    id = ()
    
    for i in range(len(expresiones)):
        if str(expresiones[i][0]) == 'fun':
            #cgen_invFunc(expresiones)
            break
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

    del signos, operaciones
    #print(evaluar)
    return(evaluar, id)

##============================================================================================##

def cgen_decla(node):
    global decla, listDecla
    if node.symbol.symbol == 'DECLA':
        expresiones = getExpresiones(node)

        if str(expresiones[0][0]) == "numerico":
            decla += "\tvar_"
            decla += str(expresiones[1][1]) + (":")
            decla += "  .word  0:1\n"

    for child in node.children:
        cgen_decla(child)

##============================================================================================##

def cgen_asig(node, padre, param):
    global asig

    if ((node.symbol.symbol == 'DECLA') and (node.father.father.symbol.symbol in padre)):
        expresiones = getExpresiones(node)
        evaluar, idVar = getEvaluationOp(expresiones)

        primeroOpe = 0
        estadoOpe = 0
        estadoOpe = False
        estadoAux = False
        contParam = 0
        
        while len(evaluar) > 0:
            exp = evaluar.pop(0)
            # Para sumar más de 2 operandos
            if estadoAux == True:
                asig += "\n"
                asig += "\tsw $a0 0($sp)\n"
                asig += "\tadd $sp $sp -4\n"

            # Expresion 1 (e1) tipo numero ("1" + 1)
            if str(exp[0]) == 'numero':
                asig += "\n"
                asig += "\tli $a0, "
                asig += exp[1] + ("\n")
                primeroOpe += 1
                estadoOpe = True
                estadoAux = False
                if (primeroOpe == 1) and (len(evaluar) > 0):
                    asig += "\n"
                    asig += "\tsw $a0 0($sp)\n"
                    asig += "\tadd $sp $sp -4\n"
                    continue
           
            # Expresion 1 (e1) tipo id ("a" + 1)
            if (str(exp[0]) == 'id') and (exp not in param):
                asig += "\n"
                asig += "\tla $t0, var_"
                asig += exp[1] + ("\n")
                asig += "\tlw $a0, 0($t0)\n"
                primeroOpe += 1
                estadoOpe = True
                estadoAux = False
                if primeroOpe == 1 and (len(evaluar) >= 1):
                    asig += "\n"
                    asig += "\tsw $a0 0($sp)\n"
                    asig += "\tadd $sp $sp -4\n"
                    continue
            
            if (str(exp[0]) == 'id') and (exp in param):
                contParam += 1
                asig += "\n"
                asig += "\tlw $a0, " + str(contParam*8) + "($sp)"
                asig += "\n"
                primeroOpe += 1
                estadoOpe = True
                estadoAux = False
                if (primeroOpe == 1) and (len(evaluar) > 0):
                    asig += "\n"
                    asig += "\tsw $a0 0($sp)\n"
                    asig += "\tadd $sp $sp -4\n"
                    continue

            if str(exp[0]) == 'suma':
                asig += "\n"
                asig += "\tlw $t1 4($sp)\n"
                asig += "\tadd $a0 $t1 $a0\n"
                asig += "\tadd $sp $sp 4\n"
                estadoAux = True

            elif str(exp[0]) == 'resta':
                asig += "\n"
                asig += "\tlw $t1 4($sp)\n"
                asig += "\tsub $a0 $t1 $a0\n"
                asig += "\tadd $sp $sp 4\n"
                estadoAux = True
        
        if (str(idVar[0]) == 'id') and (estadoOpe == True) :
            asig += "\n"
            asig += "\tla $t0, var_"
            asig +=  idVar[1] + ("\n")
            asig += "\tsw $a0, 0($t0)\n"

    for child in node.children:
        cgen_asig(child, padre, param)

##============================================================================================##

def getEvaluationLog(expresiones):
    logicos = ['igualdad', 'diferente', 'mayor_que', 'menor_que']
    numeros = []
    operaciones = []
    evaluar = []
    aux = 0

    for i in range(len(expresiones)):
        if str(expresiones[i][0]) == 'id':
            numeros.append((expresiones[i][0], expresiones[i][1]))
        if str(expresiones[i][0]) == 'numero':
            numeros.append((expresiones[i][0], expresiones[i][1]))
        if str(expresiones[i][0]) in logicos:
            operaciones.append((expresiones[i][0], expresiones[i][1]))

    for num in numeros:
        evaluar.append(num)
        aux += 1
        if aux >= 2:
            while len(operaciones)>0:
                op = operaciones.pop(0)
                evaluar.append(op)
                break

    del logicos, operaciones
    return(evaluar)


def cgen_cond(node, param):
    global cond, asig, contCond
    condAux = ''

    if node.symbol.symbol == 'EST':
        expresiones = getExpresiones(node)
        contCond += 1 

        while len(expresiones) > 0:
            exp = expresiones.pop(0)
            opeCab = []
            primeroOpe = 0
            estadoIf = False
            if exp[0] == 'si':
                exp = expresiones.pop(0)
                while exp[0] != 'der_paren':
                    exp = expresiones.pop(0)
                    opeCab.append(exp)
                eval = getEvaluationLog(opeCab)                 

                while(len(eval)>0):
                    ev = eval.pop(0)
                    #print(ev[0])
                    if ev[0] == 'id':
                        cond += "\n"
                        cond += "\tla $t0, var_"
                        cond += ev[1] + ("\n")
                        cond += "\tlw $a0, 0($t0)\n"
                        primeroOpe += 1
                        if (primeroOpe == 1) and (len(eval) > 0):
                            cond += "\n"
                            cond += "\tsw $a0 0($sp)\n"
                            cond += "\tadd $sp $sp -4\n"
                            continue

                    if ev[0] == 'numero':
                        cond += "\n"
                        cond += "\tli $a0, "
                        cond += ev[1] + ("\n")
                        primeroOpe += 1
                        if (primeroOpe == 1) and (len(eval) > 0):
                            cond += "\n"
                            cond += "\tsw $a0 0($sp)\n"
                            cond += "\tadd $sp $sp -4\n"
                            continue
                    
                    if ev[0] == 'igualdad':
                        cond += "\n"
                        cond += "\tlw $t1 4($sp)\n"
                        cond += "\tadd $sp $sp 4\n"
                        cond += "\tbeq $a0 $t1 label_true" + str(contCond) + "\n"
                        continue
                    
                    if ev[0] == 'diferente':
                        cond += "\n"
                        cond += "\tlw $t1 4($sp)\n"
                        cond += "\tadd $sp $sp 4\n"
                        cond += "\tbne $a0 $t1 label_true" + str(contCond) + "\n"
                        continue

                    if ev[0] == 'mayor_que':
                        cond += "\n"
                        cond += "\tlw $t1 4($sp)\n"
                        cond += "\tadd $sp $sp 4\n"
                        cond += "\tblt $a0 $t1, label_true" + str(contCond) + "\n"
                        continue
                    
                    if ev[0] == 'menor_que':
                        cond += "\n"
                        cond += "\tlw $t1 4($sp)\n"
                        cond += "\tadd $sp $sp 4\n"
                        cond += "\tble $a0 $t1, label_true" + str(contCond) + "\n"
                        continue

                exp = expresiones.pop(0)
                estadoIf = True

                if((exp[0] == 'iz_llave') and (estadoIf == True)):
                    condAux += "\n"
                    condAux += "label_true" + str(contCond) + ":\n"
                    #cgen_asig(node.children[7], ['EST'], param)
                    cgen_asig(node.children[7], ['EST'], param)
                    condAux += asig
                    asig = ''

            if exp[0] == 'sino':
                exp = expresiones.pop(0)
                while exp[0] != 'der_llave':
                    if((exp[0] == 'iz_llave')):
                        cond += "\n"
                        cond += "label_false" + str(contCond) + ":\n"
                        cgen_asig(node.children[9].children[2], ["EST'"], param)
                        cond += asig
                        asig = ''
                        cond += "\n"
                        cond += "\tb label_end" + str(contCond) + "\n"
                    exp = expresiones.pop(0)
                    
        cond += condAux
        cond += "\n"
        cond +="label_end" + str(contCond) + ":\n"

    for child in node.children:
        cgen_cond(child, param)

##============================================================================================##

def cgen_invFunc(node):
    global invFun
    param = []
    var = ''

    if (node.symbol.symbol == 'FUN') or (node.symbol.symbol == "FUN'"):
        if (node.symbol.symbol == 'FUN'):
            expresiones = getExpresiones(node.father.father.father.father)
            nameFun = expresiones[3][1]
            var += "\tla $t0, var_"
            var += str(expresiones[0][1]) + ("\n")
            var += "\tsw $a0, 0($t0)\n"
        elif (node.symbol.symbol == "FUN'"):
            expresiones = getExpresiones(node)
            nameFun = expresiones[1][1]

        invFun += "\tsw $fp 0($sp)\n"
        invFun += "\taddiu $sp $sp-4\n"
        
        while len(expresiones) > 0:
            exp = expresiones.pop(0)
            if exp[0] == 'iz_paren':
                exp = expresiones.pop(0)
                while exp[0] != 'der_paren':
                    if exp[0] == 'numero' or exp[0] == 'id':
                        param.append(exp)
                    exp = expresiones.pop(0)
        param = param[::-1]

        while len(param) > 0:
            par = param.pop(0)
            if str(par[0]) == 'numero':
                invFun += "\n"
                invFun += "\tli $a0, "
                invFun += par[1] + ("\n")
            elif str(par[0]) == 'id':
                invFun += "\n"
                invFun += "\tla $t0, var_"
                invFun += par[1] + ("\n")
                invFun += "\tlw $a0, 0($t0)\n"

            invFun += "\n"
            invFun += "\tsw $a0 0($sp)\n"
            invFun += "\taddiu $sp $sp-4\n"
        
        invFun += "\n"
        invFun += "\tjal "
        invFun += str(nameFun) + "\n"
        invFun += "\n"
        invFun += var
        ################ OJO ################
        invFun += "\n"
        invFun += "\tli $v0, 1\n"
        invFun += "\tsyscall\n"

        invFun += "\n"
        invFun += "\tli $v0, 10\n"
        invFun += "\tsyscall\n"
        invFun += "\n"
        #####################################
    for child in node.children:
        cgen_invFunc(child)


def cgen_func(node):
    global fun, asig, cond

    if (node.symbol.symbol == 'FUNC') and node.children[0].symbol.symbol != 'ɛ':
        param = []
        expresiones = getExpresiones(node)
        nameFun = expresiones[1][1]
        
        while len(expresiones) > 0:
            exp = expresiones.pop(0)
            if exp[0] == 'iz_paren':
                exp = expresiones.pop(0)
                while exp[0] != 'der_paren':
                    if exp[0] == 'numero' or exp[0] == 'id':
                        param.append(tuple(exp))
                    exp = expresiones.pop(0)
        param = param[::-1]
        print (param)

        fun += nameFun + (":\n")
        fun += "\tmove $fp $sp\n"
        fun += "\tsw $ra 0($sp)\n"
        fun += "\taddiu $sp $sp -4\n"

        cgen_asig(node.children[6], ['FUNC', 'SENT'], param)
        fun += asig
        asig = ''

        cgen_cond(node.children[6], param)
        fun += cond
        cond = ''
        


        fun += "\tlw $ra 4($sp)\n"
        fun += "\taddiu $sp $sp " + str((4 * len(param)) + 8) + "\n"
        fun += "\tlw $fp 0($sp)\n"

    for child in node.children:
        cgen_func(child) 

##============================================================================================##

def cgen_all():
    global code, decla, asig, invFun, fun

    code += ".data\n"
    
    cgen_decla(root)
    code += decla

    code += ".text\n"
    code += "main:\n"
    
    '''cgen_asig(root, ['FUNC', 'SENT'])
    code += asig
    asig = ''
    
    cgen_cond(root)
    code += cond'''

    cgen_invFunc(root)
    code += invFun
    invFun = ''

    cgen_func(root)
    code += fun
    fun = ''

    '''code += "\n"
    code += "\tli $v0, 1\n"
    code += "\tsyscall\n"'''

    code += "\n"
    code += "\tjr $ra"


def write_file(codeFile):
    codeFile.write(code)
    codeFile.close()

# Main
if __name__ == "__main__":
    file = ruta.split('/')[1]
    file = file.split('.')
    codeFile = open("Codigos_obtenidos/" + file[0] + "Code.s", "w")
    cgen_all()
    write_file(codeFile)