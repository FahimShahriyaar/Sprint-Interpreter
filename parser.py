import ply.yacc as yacc
from lexer import tokens
from nodes import *

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/')
)

def p_program(p):
    '''program : program statement
               | statement '''
    
    if len(p)==2:
        p[0]=[p[1]]
    elif len(p)==3:
       p[0]=p[1]+[p[2]]

def p_statement(p):
    '''statement : declaration
                 | assignment
                 | print
                 | read
                 | loop
                 | conditional'''

    p[0]=p[1]

def p_declaration(p):
    '''declaration : type ID
                   | type ID '=' expr'''

    if len(p)==3:
        p[0]=Declaration('data',p[1],p[2])
    else:
        p[0]=Declaration('data',p[1],p[2],p[4])

def p_assignment(p):
    '''assignment : ID '=' expr'''

    p[0]=Assignment(p[1],p[3])

def p_loop(p):
    '''loop : LOOP FROM INTEGER TO INTEGER BY INTEGER body'''

    p[0]=Loop(int(p[3]),int(p[5]),int(p[7]),p[8])


def p_conditional(p):
    '''conditional : WHEN expr body when_otherwise'''

    p[0]=Conditional(p[2],p[3],p[4])

def p_when_otherwise(p):
    '''when_otherwise : OTHERWISE conditional
                      | OTHERWISE body
                      |'''
    
    if len(p)==1:
        p[0]=None
    elif len(p)==3:
        p[0]=p[2]


def p_body(p):
    '''body : '[' program ']' '''

    p[0]=p[2]

def p_print(p):
    '''print : WRITE expr '''

    p[0]=Print(p[2])

def p_read(p):
    '''read : READ ID '''

    p[0]=Read(p[2])

def p_expression(p):
    '''expr : expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr
            | expr '<' expr
            | expr '>' expr
            | expr '<' '=' expr
            | expr '>' '=' expr
            | expr '=' '=' expr
            | expr '<' '>' expr
            | '(' expr ')'
            | expr_val'''
    
    if len(p)==2:
        p[0]=[p[1]]
    elif len(p)==4:
        if p[1]=='(' and p[3]==')':
            p[0]=[p[1]]+p[2]+[p[3]]
        else:
            p[0]=p[1]+[p[2]]+p[3]
    elif len(p)==5:
        p[0]=p[1]+[p[2]]+[p[3]]+p[4]

def p_type(p):
    '''type : WHOLE
            | DECIMAL
            | WORD
            | FLAG'''
    
    p[0]=p[1]

def p_expr_val(p):
    '''expr_val : INTEGER
               | FLOAT
               | STRING
               | BOOL
               | ID'''
    

    p[0]=Data(p.slice[1].type,str(p[1].strip('`')))


def p_error(p):
    print('Syntax error!')
    parser.error=1

# Build the parser
parser = yacc.yacc(debug=False,tabmodule=None)

def parse(data):
    parser.error = 0
    p = parser.parse(data)
    if parser.error:
        return None
    return p

