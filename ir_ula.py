from llvmlite import ir
from ctypes import CFUNCTYPE, c_float
import llvmlite.binding as llvm

import sys
import os

from parse_ula import parser

def compactify(element):
    if element == "AssignStatement":
        result = "="
    elif element == "AddExpression": 
        result = "+"
    elif element == "SubExpression":
        result = "-"
    elif element == "MulExpression":
        result = "*"
    elif element == "DivExpression":
        result = "/"
    elif element == "FloatExpression":
        result = ""
    elif element == "IdentifierExpression":
        result = "Load"
    elif element.startswith("FLOAT_LITERAL"):
        result = element[element.find(",")+1:]
    elif element.startswith("ID"):
        result = [element[element.find(",")+1: element.rfind(",")]]
    else:
        result = element
        
    return result
        

def sanitize_tree(tupletree, depth=0):
    lst = []
    compacted = compactify(tupletree[0])
    if not compacted == "":
        lst.append(compacted)
        
    for item in tupletree[1]:
        if isinstance(item, tuple):
            lst.append(sanitize_tree(item, depth + 1))
        else:
            compacted = compactify(item)
            if not compacted == "":
                lst.append(compacted)
            
    return lst


flttyp = ir.FloatType() # create float type
fnctyp = ir.FunctionType(flttyp, ()) # create function type to return a float
module = ir.Module(name="ula") # create module named "ula"
func = ir.Function(module, fnctyp, name="main") # create "main" function
block = func.append_basic_block(name="entry") # create block "entry" label
builder = ir.IRBuilder(block) # create irbuilder to generate code

last_var = "" # keeps track of the last var assigned
var_dict = {}  # var names associated with memory location

def code_gen(tree): # traverse tree recursively to generate code
    global last_var
    if tree[0] == "Program":
        for t in tree[1:]:
            code_gen(t)
    elif tree[0] == "=":
        last_var = tree[1][0]
        var_dict[last_var] = builder.alloca(ir.FloatType())
        builder.store(code_gen(tree[2]), var_dict[last_var])
    elif tree[0] == "+":
        return(builder.fadd(code_gen(tree[1]),code_gen(tree[2])))
    elif tree[0] == "-":
        return(builder.fsub(code_gen(tree[1]),code_gen(tree[2])))
    elif tree[0] == "*":
        return(builder.fmul(code_gen(tree[1]),code_gen(tree[2])))
    elif tree[0] == "/":
        return(builder.fdiv(code_gen(tree[1]),code_gen(tree[2])))
    elif tree[0].isnumeric():
        return(ir.Constant(ir.FloatType(), float(tree[0])))



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
            
            tree = sanitize_tree(syntree)
            tree = tree[1]
            
            print(tree)
            
            code_gen(tree) # call code_gen() to traverse tree & generate code
            builder.ret(builder.load(var_dict[last_var])) #specify return value
            print(module)
            print(var_dict)

        else:
            print("Invalid file.")
    else:
        print("Specify filename, e.g. error_ula.ply my_program.ula")

if __name__ == "__main__":
    main()
