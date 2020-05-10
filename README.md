# Pymx

### A hapy compiler created in Python

---

Pymx is a compiler written in Python 3 for the M* language, M* is a toy language in course Compiler 2020 at ACM Class, Shanghai Jiao Tong University. The compiler is intended to support to generate rv32im code. 

### Usage

```
$ pymx -h
usage: run.py [-h] [-d] [-c] [-l IR_FILE] [-s ASM_FILE] files [files ...]

Pymx is a Mx compiler created in Python

positional arguments:
  files        Source file

optional arguments:
  -h, --help   show this help message and exit
  -d           Developer option
  -c           Syntax check only
  -l IR_FILE   Intermediate code file
  -s ASM_FILE  Target file
```

## Implementation Overview

### Stage

#### Lexer

Lexer is implemented in [`lexer`](pymx/lexer), It will generate a Token List. [`tokens.py`](pymx/lexer/tokens.py) defines token classes and keywords table, and [`lexer.py`](pymx/lexer/lexer.py) matches the source code greedily.

#### Parser

The Parser will parse the token list to AST and do the semantic check, [`tree`](pymx/tree) contains the definitions of the syntax tree. Parse instance is implemented in [`parser`](pymx/parser), it is a **recursive descent parser**. 

#### IR generation

Pymx traverses the syntax tree to generate linear intermediate code called TypeLess LL. The commands' format looks like LLVM IR but just keep partial instructions and without type system. TypeLess LL only care the size of each data. It is defined in [`inst.py`](pymx/fakecode/inst.py).  Most optimizations are carried out at this stage.

#### ASM generation

Pymx generate the RISCV target code from TypeLess LL code, [live analysis](pymx/codegen/riscv/allocator.py) and [register allocation](pymx/codegen/riscv/allocator.py) will be performed at this stage, and will do some simple peephole optimization. 

### Optimize

#### Mem2reg
#### Peephole
#### CFG simplify
#### DCE (Dead Code Eliminate)
#### GVN (Global Value numbering)

## Reference

- RISCV Specification - https://riscv.org/specifications/privileged-isa/
- RV32 ABI - https://github.com/riscv/riscv-elf-psabi-doc/blob/master/riscv-elf.md
- LLVM mem2reg - https://llvm.org/doxygen/PromoteMemoryToRegister_8cpp_source.html
- LLVM Language - https://llvm.org/docs/LangRef.html
- Visitor mode - https://abcdabcd987.com/notes-on-antlr4/
- Compilers: Principles, Techniques, and Tools (dragon book)

