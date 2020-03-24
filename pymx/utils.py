def log(file):
    def decorator(func):
        def wrapper(*args, **kw):
            with open(file, 'w') as f:
                f.write(func(*args, **kw))
        return wrapper
    return decorator

@log('lexer.log')
def print_tokens(tokens):
    token_info = '{:<15} {}\n'.format('Type', 'Content')
    token_info += '------------------------------\n'
    for token in tokens:
        token_info += '{:<15} {}\n'.format(token.text, token.kind)
    token_info += '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
    return token_info

@log('sample.ll')
def print_ir(ir):
    return ir.__str__()