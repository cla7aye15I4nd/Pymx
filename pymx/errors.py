import traceback

class ErrorCollector:
    def __init__(self):    
        self.issues = []

    def add(self, issue):
        self.issues.append(issue)        

    def ok(self):
        return not any(not issue.warning for issue in self.issues)

    def show(self):
        self.issues.sort()
        for issue in self.issues:
            print(issue)

    def clear(self):        
        self.issues = []

error_collector = ErrorCollector()

class Position:
    def __init__(self, file, line, col, full_line):
        self.file = file
        self.line = line
        self.col = col
        self.full_line = full_line

    def __add__(self, other):
        return Position(self.file, self.line, self.col + other, self.full_line)

class Range:
    def __init__(self, start, end=None):
        self.start = start
        self.end = end or start

    def __add__(self, other):
        return Range(self.start, other.end)

class CompilerError(Exception):
    def __init__(self, descrip, range=None, warning=False):
        self.descrip = descrip
        self.range = range
        self.warning = warning

    def __str__(self):  # pragma: no cover
        error_color = "\x1B[31m"
        warn_color = "\x1B[33m"
        reset_color = "\x1B[0m"
        bold_color = "\033[1m"

        color_code = warn_color if self.warning else error_color
        issue_type = "warning" if self.warning else "error"

        if self.range:
            indicator = warn_color
            indicator += " " * (self.range.start.col - 1)

            if (self.range.start.line == self.range.end.line and
                 self.range.start.file == self.range.end.file):

                if self.range.end.col == self.range.start.col:
                    indicator += "^"
                else:
                    indicator += "-" * (self.range.end.col -
                                        self.range.start.col + 1)

            else:
                indicator += "-" * (len(self.range.start.full_line) -
                                    self.range.start.col + 1)

            indicator += reset_color
            return (f"{bold_color}{self.range.start.file}:"
                    f"{self.range.start.line}:{self.range.start.col}: "
                    f"{color_code}{issue_type}:{reset_color} {self.descrip}\n"
                    f"  {self.range.start.full_line}\n"
                    f"  {indicator}")
        else:
            return (f"{bold_color}pymx: {color_code}{issue_type}:"
                    f"{reset_color} {self.descrip}")

    def __lt__(self, other):  # pragma: no cover        
        if not self.range:
            return bool(other.range)

        if self.range.start.file != other.range.start.file:
            return False

        this_tuple = self.range.start.line, self.range.start.col
        other_tuple = other.range.start.line, other.range.start.col
        return this_tuple < other_tuple

class CharacterMiss(CompilerError):
    def __init__(self, char, token):
        desc = 'May you forget the "{}" after "{}"'.format(char, token.text)
        super().__init__(desc, token.range)

class InvalidType(CompilerError):
    def __init__(self, token):
        desc = '"{}" is not valid type name'.format(token.text)
        super().__init__(desc, token.range)

class IdentifierError(CompilerError):
    def __init__(self, token):
        desc = '"{}" is not a valid identifier'.format(token.text)
        super().__init__(desc, token.range)

class ErrorManager:
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):        
        if exc_tb:
            if exc_type is CompilerError:
                error_collector.add(exc_value)
            elif exc_type.__bases__[0] is CompilerError:
                error_collector.add(exc_value)
            else:
                traceback.print_tb(exc_tb)
        return True
