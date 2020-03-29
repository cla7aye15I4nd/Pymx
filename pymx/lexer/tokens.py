import re

class Token:
    def __init__(self, kind, text="", content="", range=None):
        """Base class for token
            kind (str) - Kind of token
            text (str) - Text in code.
            content (Any) - instance token
            r (Range) - Range of token covers.
        """
        self.kind = kind        
        self.text = text if text else kind
        self.content = content        
        self.range = range

    def __eq__(self, other):
        if type(other) is str:
            return self.text == other
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

keyword = []
symbols = []

def add_token(rep, kinds=[]):
    kinds.append(rep)
    return rep

## Add Keywords
add_token('bool'    , keyword)
add_token('int'     , keyword)
add_token('string'  , keyword)
add_token('void'    , keyword)
add_token('if'      , keyword)
add_token('else'    , keyword)
add_token('for'     , keyword)
add_token('while'   , keyword)
add_token('break'   , keyword)
add_token('continue', keyword)
add_token('return'  , keyword)
add_token('new'     , keyword)
add_token('class'   , keyword)
add_token('this'    , keyword)

null = add_token('null'    , keyword)
true = add_token('true'    , keyword)
false = add_token('false'   , keyword)

## Add Symbol
add_token(r'!'      , symbols)
add_token(r'~'      , symbols)
add_token(r'--'     , symbols)
add_token(r'\+\+'   , symbols)
add_token(r'\+'     , symbols)
add_token(r'-'      , symbols)
add_token(r'\*'     , symbols)
add_token(r'/'      , symbols)
add_token(r'%'      , symbols)
add_token(r'<'      , symbols)
add_token(r'>'      , symbols)
add_token(r'<='     , symbols)
add_token(r'>='     , symbols)
add_token(r'!='     , symbols)
add_token(r'=='     , symbols)
add_token(r'&&'     , symbols)
add_token(r'\|\|'   , symbols)
add_token(r'<<'     , symbols)
add_token(r'>>'     , symbols)
add_token(r'\|'     , symbols)
add_token(r'\^'     , symbols)
add_token(r'&'      , symbols)
add_token(r'='      , symbols)
add_token(r'\.'     , symbols)
add_token(r';'      , symbols)
add_token(r','      , symbols)
add_token(r'\)'     , symbols)
add_token(r'\('     , symbols)
add_token(r'\]'     , symbols)
add_token(r'\['     , symbols)
add_token(r'\{'     , symbols)
add_token(r'\}'     , symbols)

line_comment = add_token('//.*', symbols)
left_block_comment = add_token(r'/\*', symbols)
right_block_comment = add_token(r'\*/', symbols)

number = add_token('[0-9]*', symbols)
string = add_token('"(?:[^"\\\\]|\\\\.)*"', symbols)
identifier = add_token('[a-zA-Z][_a-zA-Z0-9]*', symbols)

const_contents = {
    number : lambda text : int(text),
    string : lambda text : bytes(text[1 : -1], encoding = "utf8").decode('unicode-escape'),
    true   : lambda text : True,
    false  : lambda text : False,
    null   : lambda text : None
}