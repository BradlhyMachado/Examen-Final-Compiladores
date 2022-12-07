from lexer import get_tokens
from parser import ll1

ruta = "Tests/test3.txt"
root, _ = ll1(ruta)

class symbol_table_node:
  def __init__(self, identifier, typ, category, father = 'main', line = None):        
    self.identifier = identifier
    self.type = typ # tipo de dato
    self.category = category # funcion o variable
    self.line = line
    self.father = father # a q función pertenece

symbol_table = []
variables = []
funciones = []
types = []
estadoVar = True
estadoTip = True

def add_symbol(identifier, typ, category, current_function):
  node_symbol = symbol_table_node(identifier, typ, category, current_function)
  symbol_table.append(node_symbol)

def find_symbol(node):
  find=False
  for symbol in symbol_table:
    if symbol.identifier==node.lexeme and symbol.father == current_function:
      find=True
      break
  return find

def remove_symbol(father):
  for symbol in symbol_table:
    if symbol.father==father and symbol.father != symbol.identifier:
      symbol_table.remove(symbol)
      remove_symbol(father)

def table_symbol():
  print("\n------------ Tabla de Símbolos ------------")
  print("ID \t Tipo \t Categoría \t Padre")
  for symbol in symbol_table:
    print(symbol.identifier,"\t" , symbol.type,"\t" , symbol.category,"\t" , symbol.father)
  print("-------------------------------------------\n")


#========================================== Tipos ==========================================

def underTreeTour(node):
  global types
  if((node.symbol.symbol == 'numero') or (node.symbol.symbol == 'palabra')):
    types.append(node.symbol.symbol)

  for child in node.children:
    underTreeTour(child)

def type(root, idLexeme, typeVar):
  typ = None
  if(typeVar == 'cadena'):
    typ = 'palabra'
  elif(typeVar == 'numerico'):
    typ = 'numero'
  pila = root.children

  while len(pila) > 0:
    ultimo = pila.pop()

    if(ultimo.symbol.symbol == 'DE'):
      types.append(typ)
      underTreeTour(ultimo)

      if(all(i == types[0] for i in types)):
        print(types)
      else:
        line = None
        for i in ultimo.father.children:
          if i.symbol.symbol == 'id':
            line = i.line
        print(types)
        print("ERROR SEMÁNTICO 03: Línea", line, "Expresión en variable <", idLexeme,"> no coincide con el tipo de dato declarado '", typeVar, "'.")
        return False
  types.clear()
    
'''def find_types(node, idLexeme, typeVar):
  global estadoTip
  if(node.symbol.symbol == 'DECLA'):
    for i in node.children:
      if (i.lexeme == idLexeme):
        result = type(node, idLexeme, typeVar)

        if(result == False):
          estadoTip = False

  for child in node.children:
    if estadoTip:
      find_types(child, idLexeme, typeVar)'''

def find_func_id(node):
  fath = node
  while(fath.symbol.symbol != 'FUNC'):
    fath = fath.father
  return fath.children[1].lexeme

def find_types(node, symbol_table):
  global estadoTip
  ## Se busca la parte del arbol donde haya un nodo DECLA ya que en sus hijos se hará asignaciones de tipos
  if(node.symbol.symbol == 'DECLA'):
    for i in node.children:
      ## Consultamos la información de la "Tabla de información del Scope"
      for symbol in symbol_table:
        ## Llamamos a una función auxiliar para que nos debuelva a que función pertenece el nodo en el que estamos en la iteración.
        currentFuncID = find_func_id(node)
        ## Se consulta si el ID y el nombre de la función actual coinciden
        if (i.lexeme == symbol.identifier and symbol.father == currentFuncID):
          ## Type constata el tipo de datos de la degregación del arbol por determinado ID
          result = type(node, symbol.identifier, symbol.type)
          if(result == False):
            estadoTip = False

  for child in node.children:
    if estadoTip:
      find_types(child, symbol_table)


#========================================== Variables y Funciones ==========================================

def find_var_declaration(node):
  global current_function, estadoVar
  ## Esta parte es para detectar la creación de una función
  #current_function = 'Programa'
  
  if node.symbol.symbol == 'funcion':
    piv = node.father.children[1]
    current_function = piv.lexeme # obtenmos el nombre de la función

  ## Esta parte es para detectar la finalización de una función
  if node.symbol.symbol == 'der_llave' and node.father.children[0].symbol.symbol == 'funcion':
    #print("Función terminada '", node.lexeme, "' en línea", node.line )
    remove_symbol(current_function)  # eliminar todos los simbolos de current_function
    current_function = 'Principal'
    
  ## Esta parte es para ver cuando hay un nombre de función o variable
  if node.symbol.symbol == 'id':
    ev_categoria = node.father.children[0]
    
    if(ev_categoria.symbol.symbol == 'id' and ev_categoria.lexeme not in variables):
      print("ERROR SEMÁNTICO 01: Línea", node.line, "Variable <",node.lexeme,"> no fué declarada.")
      estadoVar = False

    if(ev_categoria.symbol.symbol == 'TYPE'):
      category = 'Variable'
      if(find_symbol(node)):
        print("ERROR SEMÁNTICO 02: Línea", node.line, "Variable <",node.lexeme,"> ya fue declarada anteriormente.")
        estadoVar = False
      else:
        #print("Variable <",node.lexeme, "> declarada en línea:",node.line)
        variables.append(node.lexeme)
        add_symbol( node.lexeme, ev_categoria.children[0].lexeme, category, current_function)
        #===========================================
        #find_types(root, node.lexeme, ev_categoria.children[0].lexeme)
        find_types(root, symbol_table)
        #===========================================
        #table_symbol()
    
    if(ev_categoria.symbol.symbol == 'funcion'):
      category = 'Función'
      if(node.lexeme in funciones):
        print("ERROR SEMÁNTICO 02: Línea", node.line, "Función <",node.lexeme,"> ya fue declarada anteriormente.")
        estadoVar = False
      else:
        #print("Función <",node.lexeme, "> declarada en línea:",node.line)
        funciones.append(node.lexeme)
        add_symbol( node.lexeme, None, category, current_function)
      
  for child in node.children:
    if estadoVar:
      find_var_declaration(child)

find_var_declaration(root)

#table_symbol()