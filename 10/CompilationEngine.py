import JackTokenizer as JT

CLASS = 'class'
KEYWORD = 'keyword'
IDENTIFIER = 'identifier'
SYMBOL = 'symbol'
INT = "integerConstant"
STR_CST = "stringConstant"
METHOD = 'method'
FIELD = 'field'
FUNCTION = 'function'
CONSTRUCTOR = 'constructor'
STATIC = 'static'
STATEMENT_START = {'if', 'let', 'while', 'do', 'return'}
KEYWORD_CONSTANT = {"true", "false", "null", "this"}
OP = {'+', '-', '*', '/', '&gt;', '|', '&lt;', '&amp;', '='}
UN_OP = {'-', '~'}


class CompilationEngine:
    def __init__(self):

        self.output = None
        self.tkzr = None

    def run(self, tkzr, output):
        self.tkzr = tkzr
        self.output = output
        self.tkzr.advance()
        if self.tkzr.keyword() == CLASS:
            self.write_start(CLASS)
            self.compile_class()
            self.write_end(CLASS)

    def write(self, tag, value):
        self.output.write('<' + tag + '> ' + value + ' </' + tag + '>\n')

    def write_start(self, tag):
        self.output.write('<' + tag + '>\n')

    def write_end(self, tag):
        self.output.write('</' + tag + '>\n')

    def compile_class(self):
        self.write(KEYWORD, CLASS)
        self.tkzr.advance()
        if self.tkzr.token_type() == IDENTIFIER:
            self.write(IDENTIFIER, self.tkzr.identifier())
        self.tkzr.advance()
        if self.tkzr.symbol() == '{':
            self.write(SYMBOL, '{')
        self.tkzr.advance()
        while self.tkzr.keyword() == FIELD or self.tkzr.keyword() == STATIC:
            self.write_start('classVarDec')
            self.class_var_dec()
            self.write_end('classVarDec')
        while self.tkzr.keyword() == METHOD or self.tkzr.keyword() == CONSTRUCTOR or self.tkzr.keyword() == FUNCTION:
            self.write_start('subroutineDec')
            self.subroutine_dec()
            self.write_end('subroutineDec')
        if self.tkzr.symbol() == '}':
            self.write(SYMBOL, '}')

    def class_var_dec(self):
        self.write(KEYWORD, self.tkzr.keyword())
        self.tkzr.advance()
        if self.tkzr.keyword() == 'int' or self.tkzr.keyword() == 'char' or self.tkzr.keyword() == 'boolean':
            self.write(KEYWORD, self.tkzr.keyword())
        elif self.tkzr.token_type() == IDENTIFIER:
            self.write(IDENTIFIER, self.tkzr.identifier())
        self.tkzr.advance()
        if self.tkzr.token_type() == IDENTIFIER:
            self.write(IDENTIFIER, self.tkzr.identifier())
        self.tkzr.advance()
        while self.tkzr.symbol() == ',':
            self.write(SYMBOL, ',')
            self.tkzr.advance()
            if self.tkzr.token_type() == IDENTIFIER:
                self.write(IDENTIFIER, self.tkzr.identifier())
            self.tkzr.advance()
        if self.tkzr.symbol() == ';':
            self.write(SYMBOL, ';')
        self.tkzr.advance()

    def subroutine_dec(self):
        self.write(KEYWORD, self.tkzr.keyword())
        self.tkzr.advance()
        if self.tkzr.keyword() == 'int' or self.tkzr.keyword() == 'char' or self.tkzr.keyword() == 'boolean' or self.tkzr.keyword() == 'void':
            self.write(KEYWORD, self.tkzr.keyword())
        elif self.tkzr.token_type() == IDENTIFIER:
            self.write(IDENTIFIER, self.tkzr.identifier())
        self.tkzr.advance()
        if self.tkzr.token_type() == IDENTIFIER:
            self.write(IDENTIFIER, self.tkzr.identifier())
        self.tkzr.advance()
        if self.tkzr.symbol() == '(':
            self.write(SYMBOL, '(')
        self.tkzr.advance()

        self.write_start('parameterList')
        self.parameter_list()
        self.write_end('parameterList')
        if self.tkzr.symbol() == ')':
            self.write(SYMBOL, ')')
        self.tkzr.advance()
        self.write_start('subroutineBody')
        self.subroutine_body()
        self.write_end('subroutineBody')

    def parameter_list(self):
        if self.tkzr.keyword() == 'int' or self.tkzr.keyword() == 'char' or self.tkzr.keyword() == 'boolean':
            self.write(KEYWORD, self.tkzr.keyword())
            self.tkzr.advance()
        elif self.tkzr.token_type() == IDENTIFIER:
            self.write(IDENTIFIER, self.tkzr.identifier())
            self.tkzr.advance()

        if self.tkzr.token_type() == IDENTIFIER:
            self.write(IDENTIFIER, self.tkzr.identifier())
            self.tkzr.advance()
        while self.tkzr.symbol() == ',':
            self.write(SYMBOL, ',')
            self.tkzr.advance()
            if self.tkzr.keyword() == 'int' or self.tkzr.keyword() == 'char'\
                    or self.tkzr.keyword() == 'boolean':
                self.write(KEYWORD, self.tkzr.keyword())
                self.tkzr.advance()
            elif self.tkzr.token_type() == IDENTIFIER:
                self.write(IDENTIFIER, self.tkzr.identifier())
                self.tkzr.advance()
            if self.tkzr.token_type() == IDENTIFIER:
                self.write(IDENTIFIER, self.tkzr.identifier())
            self.tkzr.advance()

    def subroutine_body(self):

        if self.tkzr.symbol() == '{':
            self.write(SYMBOL, '{')
        self.tkzr.advance()
        while self.tkzr.keyword() == 'var':
            self.write_start('varDec')
            self.var_dec()
            self.write_end('varDec')

        self.write_start('statements')
        self.statements()
        self.write_end('statements')
        if self.tkzr.symbol() == '}':
            self.write(SYMBOL, '}')
        self.tkzr.advance()

    def var_dec(self):
        self.write(KEYWORD, self.tkzr.keyword())
        self.tkzr.advance()
        if self.tkzr.keyword() == 'int' or self.tkzr.keyword() == 'char' or self.tkzr.keyword() == 'boolean':
            self.write(KEYWORD, self.tkzr.keyword())
        elif self.tkzr.token_type() == IDENTIFIER:
            self.write(IDENTIFIER, self.tkzr.identifier())
        self.tkzr.advance()
        if self.tkzr.token_type() == IDENTIFIER:
            self.write(IDENTIFIER, self.tkzr.identifier())
        self.tkzr.advance()
        while self.tkzr.symbol() == ',':
            self.write(SYMBOL, ',')
            self.tkzr.advance()
            if self.tkzr.token_type() == IDENTIFIER:
                self.write(IDENTIFIER, self.tkzr.identifier())
            self.tkzr.advance()
        if self.tkzr.symbol() == ';':
            self.write(SYMBOL, ';')
        self.tkzr.advance()

    def statements(self):
        while self.tkzr.keyword() in STATEMENT_START:
            if self.tkzr.keyword() == "let":
                self.write_start('letStatement')
                self.let_statement()
                self.write_end('letStatement')
            elif self.tkzr.keyword() == "while":
                self.write_start('whileStatement')
                self.while_statement()
                self.write_end('whileStatement')
            elif self.tkzr.keyword() == "if":
                self.write_start('ifStatement')
                self.if_statement()
                self.write_end('ifStatement')
            elif self.tkzr.keyword() == "do":
                self.write_start('doStatement')
                self.do_statement()
                self.write_end('doStatement')
            elif self.tkzr.keyword() == "return":
                self.write_start('returnStatement')
                self.return_statement()
                self.write_end('returnStatement')

    def let_statement(self):
        self.write(KEYWORD, "let")
        self.tkzr.advance()
        if self.tkzr.token_type() == IDENTIFIER:
            self.write(IDENTIFIER, self.tkzr.identifier())
        self.tkzr.advance()
        if self.tkzr.symbol() == "[":
            self.write(SYMBOL, "[")
            self.tkzr.advance()
            self.write_start('expression')
            self.expression()
            self.write_end('expression')
            if self.tkzr.symbol() == "]":
                self.write(SYMBOL, "]")
                self.tkzr.advance()
        if self.tkzr.symbol() == "=":
            self.write(SYMBOL, "=")
        self.tkzr.advance()
        self.write_start('expression')
        self.expression()
        self.write_end('expression')
        if self.tkzr.symbol() == ";":
            self.write(SYMBOL, ";")
        self.tkzr.advance()

    def while_statement(self):
        self.write(KEYWORD, "while")
        self.tkzr.advance()
        if self.tkzr.symbol() == "(":
            self.write(SYMBOL, "(")
            self.tkzr.advance()
        self.write_start('expression')
        self.expression()
        self.write_end('expression')

        if self.tkzr.symbol() == ")":
            self.write(SYMBOL, ")")
        self.tkzr.advance()

        if self.tkzr.symbol() == "{":
            self.write(SYMBOL, "{")
            self.tkzr.advance()

        self.write_start('statements')
        self.statements()
        self.write_end('statements')
        if self.tkzr.symbol() == "}":
            self.write(SYMBOL, "}")
        self.tkzr.advance()

    def if_statement(self):
        self.write(KEYWORD, "if")
        self.tkzr.advance()
        if self.tkzr.symbol() == "(":
            self.write(SYMBOL, "(")
            self.tkzr.advance()
        self.write_start('expression')
        self.expression()
        self.write_end('expression')
        if self.tkzr.symbol() == ")":
            self.write(SYMBOL, ")")
        self.tkzr.advance()

        if self.tkzr.symbol() == "{":
            self.write(SYMBOL, "{")
            self.tkzr.advance()

        self.write_start('statements')
        self.statements()
        self.write_end('statements')
        if self.tkzr.symbol() == "}":
            self.write(SYMBOL, "}")
        self.tkzr.advance()

        if self.tkzr.keyword() == "else":
            self.write(KEYWORD, "else")
            self.tkzr.advance()
            if self.tkzr.symbol() == "{":
                self.write(SYMBOL, "{")
                self.tkzr.advance()

            self.write_start('statements')
            self.statements()
            self.write_end('statements')
            if self.tkzr.symbol() == "}":
                self.write(SYMBOL, "}")
            self.tkzr.advance()

    def do_statement(self):
        self.write(KEYWORD, "do")
        self.tkzr.advance()
        if self.tkzr.token_type() == IDENTIFIER:
            # self.write_start('subroutineCall')
            self.subroutine_call()
            # self.write_end('subroutineCall')
        if self.tkzr.symbol() == ";":
            self.write(SYMBOL, ";")
        self.tkzr.advance()

    def return_statement(self):
        self.write(KEYWORD, "return")
        self.tkzr.advance()
        if self.tkzr.symbol() != ";":
            self.write_start('expression')
            self.expression()
            self.write_end('expression')

        if self.tkzr.symbol() == ";":
            self.write(SYMBOL, ";")
        self.tkzr.advance()

    def expression(self):

        self.write_start('term')
        self.compile_term()
        self.write_end('term')

        while self.tkzr.symbol() in OP:
            self.write(SYMBOL, self.tkzr.symbol())
            self.tkzr.advance()
            self.write_start('term')
            self.compile_term()
            self.write_end('term')

    def compile_term(self):
        if self.tkzr.token_type() == "integerConstant":
            self.write(INT, self.tkzr.int_val())
            self.tkzr.advance()
        elif self.tkzr.token_type() == "stringConstant":
            self.write(STR_CST, self.tkzr.string_val())
            self.tkzr.advance()
        elif self.tkzr.keyword() in KEYWORD_CONSTANT:
            self.write(KEYWORD, self.tkzr.keyword())
            self.tkzr.advance()
        elif self.tkzr.symbol() == "(":
            self.write(SYMBOL, "(")
            self.tkzr.advance()
            self.write_start('expression')
            self.expression()
            self.write_end('expression')
            if self.tkzr.symbol() == ")":
                self.write(SYMBOL, ")")
            self.tkzr.advance()
        elif self.tkzr.symbol() in UN_OP:
            self.write(SYMBOL, self.tkzr.symbol())
            self.tkzr.advance()
            self.write_start('term')
            self.compile_term()
            self.write_end('term')
        elif self.tkzr.token_type() == IDENTIFIER:
            if self.tkzr.content[self.tkzr.index + 1] == "[":
                self.write(IDENTIFIER, self.tkzr.identifier())
                self.tkzr.advance()
                if self.tkzr.symbol() == "[":
                    self.write(SYMBOL, "[")
                    self.tkzr.advance()
                    self.write_start('expression')
                    self.expression()
                    self.write_end('expression')
                    if self.tkzr.symbol() == "]":
                        self.write(SYMBOL, "]")
                        self.tkzr.advance()

            elif self.tkzr.content[self.tkzr.index + 1] == "(" or \
                    self.tkzr.content[self.tkzr.index + 1] == ".":
                # self.write_start('subroutineCall')
                self.subroutine_call()
                # self.write_end('subroutineCall')
            else:
                self.write(IDENTIFIER, self.tkzr.identifier())
                self.tkzr.advance()

    def subroutine_call(self):
        self.write(IDENTIFIER, self.tkzr.identifier())
        self.tkzr.advance()
        if self.tkzr.symbol() == "(":
            self.write(SYMBOL, "(")
            self.tkzr.advance()
            self.write_start('expressionList')
            self.expression_list()
            self.write_end('expressionList')
            if self.tkzr.symbol() == ")":
                self.write(SYMBOL, ")")
        elif self.tkzr.symbol() == ".":
            self.write(SYMBOL, ".")
            self.tkzr.advance()
            if self.tkzr.token_type() == IDENTIFIER:
                self.write(IDENTIFIER, self.tkzr.identifier())
                self.tkzr.advance()
                if self.tkzr.symbol() == "(":
                    self.write(SYMBOL, "(")
                self.tkzr.advance()
                self.write_start('expressionList')
                self.expression_list()
                self.write_end('expressionList')
                if self.tkzr.symbol() == ")":
                    self.write(SYMBOL, ")")
        self.tkzr.advance()

    def expression_list(self):
        if self.tkzr.get_token() != ')':
            self.write_start('expression')
            self.expression()
            self.write_end('expression')
            while self.tkzr.symbol() == ',':
                self.write(SYMBOL, ',')
                self.tkzr.advance()
                self.write_start('expression')
                self.expression()
                self.write_end('expression')
