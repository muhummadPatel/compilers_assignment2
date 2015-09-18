from ply import yacc
from lex_ula import tokens
import os
import sys


start = "Start"


def p_start(p):
    """Start : Program"""
    p[0] = ("Start", [p[1]])


def p_program_statements(p):
    """Program : Statements"""
    p[0] = ("Program", p[1])


def p_statements(p):
    """Statements : Statements Statement
                    | Statement"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_statement(p):
    """Statement : ID '=' expression"""
    p[0] = ("AssignStatement", ["ID," + p[1] + "," + str(p.lineno(1)), p[3]])


def p_expression_plus(p):
    """expression : expression '@' term"""
    p[0] = ("AddExpression", [p[1], p[3]])


def p_expression_minus(p):
    """expression : expression '$' term"""
    p[0] = ("SubExpression", [p[1], p[3]])


def p_expression_term(p):
    """expression : term"""
    p[0] = p[1]


def p_term_multiply(p):
    """term : term '#' factor"""
    p[0] = ("MulExpression", [p[1], p[3]])


def p_term_divide(p):
    """term : term '&' factor"""
    p[0] = ("DivExpression", [p[1], p[3]])


def p_term_factor(p):
    """term : factor"""
    p[0] = p[1]


def p_factor_expression(p):
    """factor : '(' expression ')'"""
    p[0] = p[2]


def p_factor_float(p):
    """factor : FLOAT_LITERAL"""
    p[0] = ("FloatExpression", ["FLOAT_LITERAL," + p[1]])


def p_factor_id(p):
    """factor : ID"""
    p[0] = ("IdentifierExpression", ["ID," + p[1] + "," + str(p.lineno(1))])


def p_error(p):
    global infilename
    
    print("parse error on line %d" % p.lexer.lineno)
    
    outfilename = os.path.splitext(infilename)[0]+".err"
    with open(outfilename, "w") as outfile:
        print("parse error on line %d" % p.lexer.lineno, file=outfile)
            
    exit()


def print_tree(outfile, tupletree, depth=0):
    print("\t"*depth, tupletree[0], sep="", file=outfile)
    print("\t"*depth, tupletree[0])
    for item in tupletree[1]:
        if isinstance(item, tuple):
            print_tree(outfile, item, depth + 1)
        else:
            print("\t"*(depth+1), item, sep="", file=outfile)
            print("\t"*(depth+1), item)


parser = yacc.yacc()

infilename = ""
def main():
    global infilename
    
    if len(sys.argv) == 2:
        infilename = sys.argv[1]
        if os.path.isfile(infilename):
            infile = open(infilename, "r")
            syntree = parser.parse(infile.read())
            outfilename = os.path.splitext(infilename)[0]+".ast"
            with open(outfilename, "w") as outfile:
                print_tree(outfile, syntree)
        else:
            print("Not a valid file")
    else:
        print("Specify filename, e.g. parse_ula.ply my_program.ula")


if __name__ == "__main__":
    main()
