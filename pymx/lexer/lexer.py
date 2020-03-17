import re

from .tokens import keyword, symbols, Token
from .tokens import number, const_contents
from .tokens import left_block_comment, right_block_comment, line_comment

from ..errors import ErrorManager, Position, Range

def tokenize(code, filename):
    tokens = []
    lines = code.splitlines()

    in_comment = False
    for line_num, line in enumerate(lines):
        with ErrorManager():
            line_tokens, in_comment = tokenize_line(line, line_num + 1, filename, in_comment)
            tokens += line_tokens
    
    return tokens

def tokenize_line(line, line_num, filename, in_comment):
    col = 0
    line_tokens = []
    while col < len(line):
        if line[col].isspace():
            col = col + 1
            continue
        
        kind, length = match_token(line, col)
        text = line[col : col + length]
        
        start = Position(filename, line_num, col + 1, line)
        end   = start + length
        range = Range(start, end)

        tk = Token(kind, text, text, range)        

        if kind in const_contents:
            tk.content = const_contents[kind](text)

        if kind == line_comment:
            return line_tokens, in_comment
        if in_comment:
            if kind == right_block_comment:
                in_comment = False
            col += 1
        elif kind == left_block_comment:
            in_comment = True
        else:
            line_tokens.append(tk)

        col += length

    return line_tokens, in_comment

def match_token(line, col):
    kind = None
    length = 0
    for rep in (keyword + symbols):
        res = re.match(rep, line[col:])
        if res and len(res.group(0)) > length:            
            kind = rep
            length = len(res.group(0))

    return kind, length
            