import sys
import random
import string

def random_string(length):
    return ''.join([random.choice(string.ascii_letters) for _ in range(length)])

def generate(var_count, operator):
    var = [random_string(var_count * 4) for _ in range(var_count)]
    text = 'int main() {\n' + '\n'.join(['  int {} = getInt();'.format(_) for _ in var]) + '\n'
    text += '  return '
    text += random.choice(var)
    for i in range(var_count * 2):
        text += random.choice(operator) + random.choice(var)
    text += ';\n}\n'
    with open('sum.mx', 'w') as f:
        f.write(text)

cnt = int(sys.argv[1]) if len(sys.argv) > 1 else 8
generate(cnt, ['&', '|', '^'])
