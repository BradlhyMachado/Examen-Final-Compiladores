from lexer import get_tokens
#import sys
import pandas as pd
import graphviz
#import math

counter = 0
cont = 0
tree = ''
syntax_table = pd.read_csv("syntax_table_final.csv", index_col=0)
  
    
def generateTree(node, element_tree, info = False):
    global tree
    tree = "digraph G { \n"    
    for nod in element_tree:
        if nod.symbol.is_terminal: 
            if nod.symbol.symbol == 'ɛ':
                tree += str(nod.symbol.id) + ' [label=< <b>' + nod.symbol.symbol + '</b> > ]; \n'      
            else:             
                lexeme = nod.lexeme
                lexeme = "&#38;" if lexeme == '&' else nod.lexeme           
                tree += str(nod.symbol.id) + ' [label=< <b>' + nod.symbol.symbol + '</b> > ]; \n' 
        else:
            tree += str(nod.symbol.id) + ' [ label=" ' + nod.symbol.symbol + ' " ]; \n'                    
    generateTreeRec(node)        
    tree += "}"

    #print(tree)
    tree = graphviz.Source(tree)
    tree.render(filename="Arboles_obtenidos/Tree", format='png')


def generateTreeRec(node):
    global tree
    tmp = []
    for child in node.children:
        tree += str(node.symbol.id) + ' -> ' + str(child.symbol.id) + '; \n'
        tmp.append(str(child.symbol.id))
        generateTreeRec(child)
    if len(node.children) > 0:
        tree += "{ \n"
        tree += "    rank = same; \n"
        tree += "    edge[ style=invis]; \n"
        tree += " -> ".join(tmp) + "; \n"
        tree += "    rankdir = LR; \n"
        tree += "} \n" 


def searchInTree(element_tree, id):
    for nod in element_tree:
        if nod.symbol.id == id:
            return nod


def print_stack(stack):
    print("\nSTACK:")
    for element in stack:
        #print(element.symbol + ':' + str(element.is_terminal), end=' ')
        print(element.symbol, end=' ')
    print()

def print_input(input):
    print("\nINPUT:")
    for element in input:        
        print(element[0], end=' ')
    print()

def update_stack(root, element_tree, syntax_table, stack, current_token):
    production = syntax_table.loc[ stack[0].symbol, current_token ]

    '''print("\nACTION:")
    print(production)
    print()'''

    if(pd.isna(production)):
        return False

    productions = production.split(" ")
    productions.pop(0) # eliminamos el lado izquierdo de la produccion
    productions.pop(0) # eliminamos la flecha

    # elimnamos el primer elemento de la pila e insertamos la nueva produccion
    father = stack.pop(0)
    node_father = searchInTree(element_tree, father.id)

    if productions[0] == "''": # vacio
        new_symbol = node_stack( 'ɛ', True )
        nod_tree    = node_parser( new_symbol, None, [], node_father )
        node_father.children.insert(0, nod_tree )
        element_tree.append(nod_tree)
        return True
    
    #print(father.id, father.symbol, father.is_terminal)
    for prod in reversed(productions):
        # insertamos en la pila
        new_symbol = node_stack( prod, False if prod.isupper() else True )
        stack.insert(0, new_symbol)        
        nod_tree    = node_parser( new_symbol, None, [], node_father )
        node_father.children.insert(0, nod_tree )
        element_tree.append(nod_tree)
    return True

class node_stack:
    def __init__(self, symbol, terminal):
        global counter
        self.id = counter
        self.symbol = symbol
        self.is_terminal = terminal
        counter += 1

class node_parser:
    def __init__(self, symbol, lexeme = None,  children = [], father = None, line = None):  
        self.symbol = symbol
        self.lexeme = lexeme        
        self.line = line
        self.children = children
        self.father = father

        self.type = None # es para guardar el tipo de dato, lo usaremos en el analizador semantico
        self.visited = False # para saber si el nodo fue visitado, lo usaremos en el analizador semantico


# insert the first elements in STACK
symbol_1 = node_stack( '$', True )
symbol_2 = node_stack( 'PROGRA', False )
stack = []
stack.insert(0, symbol_1)
stack.insert(0, symbol_2)

# inserter raiz del arbol
root = node_parser( symbol_2 )
element_tree = []
element_tree.append(root)

#print(syntax_table)
#print_stack(stack)
#print(tokens)

def parser(tokens):
    global cont
    result = False
    while True:
        '''cont = cont + 1
        print("--------- ITERATION ", cont, " ---------")
        print_stack(stack)
        print_input(tokens)'''

        if stack[0].symbol == tokens[0][0] == '$':  # if terminla are $
            result = True
            '''print("\nTODO BIEN :D\n")'''
            break

        if stack[0].is_terminal:            
            '''print("\nterminales ... \n")'''
            if stack[0].symbol == tokens[0][0]:
                #print("Terminales iguales :", tokens[0][0])
                # antes de eliminar, asigno el lexeme y no linea
                nod = searchInTree(element_tree, stack[0].id)
                nod.lexeme = tokens[0][1]
                nod.line = tokens[0][2]
                stack.pop(0)
                tokens.pop(0)
            else:
                #print("Terminales diferentes")
                result = False 
                print("ERROR SINTÁCTICO 01: Línea ", tokens[0][2]) 
                break  
        else:            
            if not update_stack(root, element_tree, syntax_table, stack, tokens[0][0]):
                result = False 
                print("ERROR SINTÁCTICO 02: Línea ", tokens[0][2]) 
                break 
    return root, element_tree


def ll1(ruta):
    tokens = get_tokens(ruta)
    root_tree, element_tree = parser(tokens)
    
    generateTree(root_tree, element_tree)

    return root_tree, element_tree