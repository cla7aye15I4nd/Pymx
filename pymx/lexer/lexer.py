import re

from .tokens import keyword, symbols, Token
from .tokens import number, string, true, false, null
from .tokens import left_block_comment, right_block_comment, line_comment

from ..errors import error_manager, Position, Range

class Tagged:
    def __init__(self, c, p):        
        self.c = c
        self.p = p
        self.r = Range(p, p)

def tokenize(code, filename):
    tokens = []
    lines = code.splitlines()

    in_comment = False
    for line_num, line in enumerate(lines):
        with error_manager:
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

        contents = {
            number : lambda text : int(text),
            string : lambda text : re.escape(text[1 : -1]),
            true   : lambda text : True,
            false  : lambda text : False
        }

        if kind in contents:
            tk.content = contents[kind](text)

        if kind == line_comment:
            return line_tokens
        if in_comment:
            if kind == right_block_comment:
                in_comment = False
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
            