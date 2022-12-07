import ply.lex as lex

reserved = {
  'funcion': 'funcion', 
  'imprimir': 'imprimir',
  'leer':'leer',
  'si':'si',
  'sino':'sino',
  'mientras':'mientras',
  'fun':'fun'
}

tokens = [
  # Tipos declarado
  'numerico',
  'cadena',
  
  # Tipos dato
  'numero',
  'palabra',

  # Operadores Aritmeticas
  'suma',
  'resta',
  'division',
  'multiplicacion',
  
  # Operadores lógicos
  'y',
  'o',
  'igual',
  'mayor_que',
  'menor_que',
  'mayor_igual',
  'menor_igual',
  'igualdad',
  'diferente',

  #Signos
  'iz_paren',
  'der_paren',
  'iz_llave',
  'der_llave',
  'pt_coma',
  'coma',
  'hash',

  # Otros
  'id'
] + list(reserved.values())

 # Regular expression rules for simple tokens
t_suma    = r'\+'
t_resta   = r'-'
t_multiplicacion   = r'\*'
t_division  = r'/'
t_y     = r'&&'
t_o      = r'\|{2}'
t_igual  = r'\='
t_iz_paren  = r'\('
t_der_paren  = r'\)'
t_iz_llave    = r'\{'
t_der_llave    = r'\}'
t_pt_coma = r'\;'
t_coma = r'\,'
t_hash = r'\#'
t_mayor_que = r'\>'
t_menor_que = r'\<'
t_mayor_igual = r'\>\='
t_menor_igual = r'\<\='
t_igualdad = r'\=\='
t_diferente = r'\!='

# A regular expression rule with some action code
def t_numero(t):
  r'([0-9]*[.])?[0-9]+'
  #t.value = int(t.value)
  return t

def t_palabra(t):
  r'\"(\w+ \ *\w*\d* \ *)\"'
  #t.value = int(t.value)
  return t

def t_numerico(t):
  r'numerico'
  return t

def t_cadena(t):
  r'cadena'
  return t

# A regular expression rule with some action code
def t_id(t):
  r'[a-zA-Z]+ ( [a-zA-Z0-9]* )'    
  t.type = reserved.get(t.value,'id')    # Check for reserved words
  return t

# Define a rule so we can track line numbers
def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

#Comments more one line (#.Comment mult.#)
def t_comments(t):
  r'\#\.(.|\n)*?\.\#'
  t.lexer.lineno += t.value.count('\n')
  #print("Comentario de multiple linea")

#Comments one line (##Comment)
def t_comments_ONELine(t):
  r'\#\#(.)*\n'
  t.lexer.lineno += 1
  #print("Comentario de una linea")

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
 
# Error handling rule
def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)

# Admission Test
def prueba(data):
  resultado_analisis = []
  
  analizador = lex.lex()
  analizador.input(data)
  
  resultado_analisis.clear()
  while True:
    tok = analizador.token()
    if not tok:
      break
    resultado_analisis.append([str(tok.type), str(tok.value), str(tok.lineno)])
  resultado_analisis.append(['$', None, None])
  return resultado_analisis

# Instantiate the lexical analyzer
analizador = lex.lex()

def get_tokens(ruta):
  archivo = open(ruta, "r")
  data = archivo.read() # It is entered to read the data obtained from the txt file
  
  return (prueba(data))