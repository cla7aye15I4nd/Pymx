""" ACM Class 2018 Compiler Homework """

import argparse

from .lexer import tokenize
from .parser import parse

from .utils import print_tokens
from .errors import error_collector, CompilerError

def main():
    arguemnts = get_arguments()

    objs = []
    for file in arguemnts.files:
        objs.append(process_file(file, arguemnts))
    
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

def process_file(file, args):
    code = read_file(file)

    token_list = tokenize(code, file)
    if not error_collector.ok():
        return None
    
    print_tokens(token_list)
    tree = parse(token_list)

def read_file(file):
    try:
        with open(file) as mx_file:
            return mx_file.read()
    except IOError:
        error_collector.add(CompilerError(f'Can not open {file}'))
    return ''