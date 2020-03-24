""" ACM Class 2018 Compiler Homework """

import argparse
import fileinput

from .lexer import tokenize
from .parser import parse
from .semantic import semantic_check
from .IRbuilder import IRbuild

from .utils import print_tokens, print_ir
from .errors import error_collector, CompilerError
from .builtin import builtin

def main():
    arguemnts = get_arguments()
    process_file(arguemnts)
    
    error_collector.show()
    return not error_collector.ok()

def get_arguments():
    parser = argparse.ArgumentParser(
        description='Pymx is a Mx compiler created in Python', 
        usage='pymx [-h] [options] files...'
    )

    parser.add_argument('files', metavar='files', nargs="+")
    parser.add_argument('-c', dest='syntax_only', action='store_true')
    return parser.parse_args()

def process_file(args):
    file = args.files[0]
    code = read_file(file)

    token_list = tokenize(code, file)
    if not error_collector.ok():
        return None
    
    print_tokens(token_list)
    tree = parse(token_list)
    
    if not error_collector.ok():
        return None
    
    tree.builtin = builtin
    tree = semantic_check(tree)

    if not error_collector.ok() or args.syntax_only:
        return None

    ir = IRbuild(tree)
    print_ir(ir)

def read_file(file):
    try:
        with open(file) as mx_file:
            return mx_file.read()
    except IOError:
        error_collector.add(CompilerError(f'Can not open {file}'))
    return ''