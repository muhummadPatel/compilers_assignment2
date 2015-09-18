from llvmlite import ir
from ctypes import CFUNCTYPE, c_float
import llvmlite.binding as llvm

import sys
import os

import ir_ula

def create_execution_engine():
    """
    Create an ExecutionEngine suitable for JIT code generation on
    the host CPU.  The engine is reusable for an arbitrary number of
    modules.
    Source: http://llvmlite.pydata.org/en/latest/binding/examples.html#compiling-a-trivial-function
    """
    # Create a target machine representing the host
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    # And an execution engine with an empty backing module
    backing_mod = llvm.parse_assembly("")
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
    return engine


def compile_ir(engine, llvm_ir):
    """
    Compile the LLVM IR string with the given engine.
    The compiled module object is returned.
    Source: http://llvmlite.pydata.org/en/latest/binding/examples.html#compiling-a-trivial-function
    """
    # Create a LLVM module object from the IR
    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()
    # Now add the module and make sure it is ready for execution
    engine.add_module(mod)
    engine.finalize_object()
    return mod


def run_ir(llvm_ir):
    # All these initializations are required for code generation!
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()  # yes, even this one    
    
    engine = create_execution_engine()
    mod = compile_ir(engine, llvm_ir)
    
    # Run the code
    func_ptr = engine.get_function_address("main")
    cfunc = CFUNCTYPE(c_float)(func_ptr)
    res = cfunc()
    return res


    
def main():
    if len(sys.argv) == 2:
        infilename = sys.argv[1]
        if os.path.isfile(infilename):
            infile = open(infilename, "r")
            code = infile.read()
            
            ir_ula.gen_ir(code)
            
            outfilename = os.path.splitext(infilename)[0] + ".run"
            outfile = open(outfilename, "w")
            print(run_ir(str(ir_ula.module)), file=outfile)
            print(run_ir(str(ir_ula.module)))
            outfile.close()
        else:
            print("Invalid file.")
    else:
        print("Specify filename, e.g. error_ula.ply my_program.ula")

if __name__ == "__main__":
    main()
    
    

