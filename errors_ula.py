import sys
import os

from parse_ula import parser

def is_identifier_expression (tupletree):
    return tupletree[0] == "IdentifierExpression"

def is_assignment_statement (tupletree):
    return tupletree[0] == "AssignStatement"

def get_identifier_data (tupletree):
    raw_str = tupletree[1][0]
    
    details = {}
    details["name"] = raw_str[raw_str.find(",")+1: raw_str.rfind(",")]
    details["lineno"] = raw_str[raw_str.rfind(",")+1:]
    
    return details

symbol_tbl = []
def print_tree(tupletree, depth=0):
    global symbol_tbl
    global infilename
    
    outfilename = os.path.splitext(infilename)[0] + ".err"
    outfile = open(outfilename, "w")
    
    if is_identifier_expression(tupletree):
        id_data = get_identifier_data(tupletree)
        if id_data["name"] not in symbol_tbl:
            print("semantic error on line %s" % id_data["lineno"])
            print("semantic error on line %s" % id_data["lineno"], file=outfile)
            outfile.close();
            exit()
            
    elif is_assignment_statement(tupletree):
        id_data = get_identifier_data(tupletree)
        if id_data["name"] in symbol_tbl:
            print("semantic error on line %s" % id_data["lineno"])
            print("semantic error on line %s" % id_data["lineno"], file=outfile)
            outfile.close();
            exit()
        else:
            symbol_tbl.append(id_data["name"])
    
    for item in tupletree[1]:
        if isinstance(item, tuple):
            print_tree( item, depth + 1)

infilename = ""
def main():
    global infilename
    
    if len(sys.argv) == 2:
        infilename = sys.argv[1]
        if os.path.isfile(infilename):
            infile = open(infilename, "r")
            
            outfilename = os.path.splitext(infilename)[0] + ".err"
            sys.stdout = open(outfilename, "w")
            syntree = parser.parse(infile.read())
            sys.stdout = sys.__stdout__
            
            print_tree(syntree)
        else:
            print("Invalid file.")
    else:
        print("Specify filename, e.g. error_ula.ply my_program.ula")

if __name__ == "__main__":
    main()
