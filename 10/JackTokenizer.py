import re

SYMBOL = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&',
          '|', '>', '<', '=', '~']

KEYWORD = ['class', 'constructor', 'function', 'method', 'field', 'static',
           'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
           'this', 'let', 'do', 'if', 'else', 'while', 'return']
SYM = 'symbol'
KEY = "keyword"
ID = "identifier"
INT = 'integerConstant'
STR = 'stringConstant'


class JackTokenizer:
    def __init__(self, file):
        self.content = []
        self.read(file)
        self.index = -1
        self.current_token = ""

    def read(self, file):
        text = ""
        in_comment=False
        for line in file:

            line = line.strip()
            if line == '' :
                continue

            in_quote = False
            in_simple_comment=False
            newline = ''
            for char in range(len(line)):
                if char!=len(line)-1 and not in_quote and not in_comment and line[char]=='/'and line[char+1]=='/' :
                    in_simple_comment=True
                if char!=len(line)-1 and not in_quote and line[char]=='/'and line[char+1]=='*' and not in_simple_comment:
                    in_comment=True

                if char!=len(line)-1 and  not in_quote and line[char]=='*'and line[char+1]=='/'and not in_simple_comment:
                    in_comment=False
                if line[char] == '"' and not in_comment and not in_simple_comment:
                    in_quote = not in_quote
                if line[char] in SYMBOL and not in_quote:
                    newline += ' ' + line[char] + ' '
                elif (line[char] == ' ' or line[char]=='\t') and in_quote:
                    newline += '$'
                elif line[char] == '/' and in_quote:
                    newline += '@'
                else:
                    newline += line[char]
            line = newline
            #print(line+'***************'+str(in_simple_comment)+'*************'+str(in_quote))
            # line = self.replace_in_str(list(line))
            m = re.search("/\s*/.*", line)
            if m and in_simple_comment:
                line = line[:m.start()]
            text += line+' '
        print(text)
        text = re.sub('/\s*\\*.*?\\*\s*/', ' ', text)
        self.content = text.split()
        for token in range(len(self.content)):
            self.content[token] = self.content[token].replace('$', ' ')
            self.content[token] = self.content[token].replace('@', '/')
            #print(self.content[token])


    # def replace_in_str(self, line):
    #     in_quote = False
    #     for char in range(len(line)):
    #         if line[char] == '"':
    #             in_quote = not in_quote
    #         if line[char] == ' ' and in_quote:
    #             line[char] = '$'
    #         if line[char] == '/' and in_quote:
    #             line[char] = '@'
    #     return ''.join(line)

    def has_more_tokens(self):
        return self.index < len(self.content) - 1

    def advance(self):
        if self.has_more_tokens():
            self.index += 1
            self.current_token = self.content[self.index]

    def token_type(self):
        if self.current_token in SYMBOL:
            return SYM
        if self.current_token in KEYWORD:
            return KEY
        if re.match("[a-zA-Z_]\w*", self.current_token):
            return ID
        if re.match("\d{1,5}", self.current_token) and int(
                self.current_token) <= 32767:
            return INT
        if re.match('"[^\n]*"', self.current_token):
            return STR

    def keyword(self):
        if self.token_type() == KEY:
            return self.current_token

    def symbol(self):
        if self.token_type() == SYM:
            if self.current_token == '<':
                return '&lt;'
            if self.current_token == '>':
                return '&gt;'
            if self.current_token == '&':
                return '&amp;'
            return self.current_token

    def identifier(self):
        if self.token_type() == ID:
            return self.current_token

    def int_val(self):
        if self.token_type() == INT:
            return self.current_token

    def string_val(self):
        if self.token_type() == STR:
            return self.current_token.strip()[1:-1]

    def get_token(self):

        if self.token_type() == KEY:
            return self.keyword()
        if self.token_type() == SYM:
            return self.symbol()
        if self.token_type() == ID:
            return self.identifier()
        if self.token_type() == INT:
            return self.int_val()
        if self.token_type() == STR:
            return self.string_val()
