from ply import lex
import os
import sys

tokens = ["ID", "FLOAT_LITERAL", "WHITESPACE", "COMMENT"]

literals = ["@", "$", "#", "&", "=", "(", ")"]

t_FLOAT_LITERAL = r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'

def t_WHITESPACE(t):
    r'\s*(\p{P})?\s'
    t.lexer.lineno += t.value.count("\n") # line number tracking for exception handling
    if __name__ == "__main__":
        return t

def t_COMMENT(t):
    r'/\*(.|[\r\n])*?\*/|(//.*)'
    # regex allows for /* */ and // comments but also allows extra *s in a multiline /* */ comment
    t.lexer.lineno += t.value.count("\n") # implement line number tracking
    if __name__ == "__main__":
        return t

def t_ID(t):
    r'[_a-zA-Z][_a-zA-Z0-9]*'
    return t

def t_error(t):
    global infilename
    
    print("lexical error on line %d" % t.lexer.lineno)
    
    if __name__ == "__main__":
        outfilename = os.path.splitext(infilename)[0]+".err"
        with open(outfilename, "w") as outfile:
            print("lexical error on line %d" % t.lexer.lineno, file=outfile)
            
    exit()
        
lexer = lex.lex()

infilename = ""
def main():
    global infilename
    
    if len(sys.argv) == 2:
        infilename = sys.argv[1]
        if os.path.isfile(infilename):
            infile = open(infilename, "r")
            lexer.input(infile.read())
            outfilename = os.path.splitext(infilename)[0]+".tkn"
            outfile = open(outfilename, "w")
    
            for token in lexer:
                if token.type in ["FLOAT_LITERAL", "ID"]:
                    print(token.type, token.value, sep=",", file=outfile)
                    print(token.type, token.value, sep=",")
                else:
                    print(token.type, file=outfile)
                    print(token.type)
    
            outfile.close()
        else:
            print("Not a valid file")
    else:
        print("Specify filename, e.g. lex_ula.ply my_program.ula")

if __name__ == "__main__":
    main()
