import SymbolTable as ST

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

        self.writer = None
        self.sym_table = None
        self.tkzr = None
        self.class_name = None

    def run(self, tkzr, writer):
        self.tkzr = tkzr
        self.writer = writer
        self.class_name = None
        self.sym_table = ST.SymbolTable()
        self.tkzr.advance()
        if self.tkzr.keyword() == CLASS:
            self.compile_class()

    def compile_class(self):
        self.tkzr.advance()
        if self.tkzr.token_type() == IDENTIFIER:
            self.class_name = self.tkzr.identifier()
        self.tkzr.advance()
        if self.tkzr.symbol() != '{':
            raise Exception('no bracket')
        self.tkzr.advance()
        while self.tkzr.keyword() == FIELD or self.tkzr.keyword() == STATIC:
            self.class_var_dec()
        while self.tkzr.keyword() == METHOD or self.tkzr.keyword() == CONSTRUCTOR or self.tkzr.keyword() == FUNCTION:
            self.sym_table.start_subroutine()

            self.subroutine_dec()
        if self.tkzr.symbol() != '}':
            raise Exception('no bracket')

    def class_var_dec(self):
        name = None
        type = None
        kind = self.tkzr.keyword()
        self.tkzr.advance()
        if self.tkzr.keyword() == 'int' or self.tkzr.keyword() == 'char' or self.tkzr.keyword() == 'boolean':
            type = self.tkzr.keyword()
        elif self.tkzr.token_type() == IDENTIFIER:
            type = self.tkzr.identifier()
        self.tkzr.advance()
        if self.tkzr.token_type() == IDENTIFIER:
            name = self.tkzr.identifier()
        self.sym_table.define(name, type, kind)
        self.tkzr.advance()
        while self.tkzr.symbol() == ',':
            self.tkzr.advance()
            if self.tkzr.token_type() == IDENTIFIER:
                name = self.tkzr.identifier()
            self.sym_table.define(name, type, kind)
            self.tkzr.advance()
        if self.tkzr.symbol() != ';':
            raise Exception('no comma')
        self.tkzr.advance()

    def subroutine_dec(self):
        name = None
        kind = self.tkzr.keyword()
        self.tkzr.advance()
        self.tkzr.advance()
        if self.tkzr.token_type() == IDENTIFIER:
            name = self.tkzr.identifier()
        n_local = 0
        in_declaration = False
        for i in range(self.tkzr.index, len(self.tkzr.content)):
            if self.tkzr.content[i] == 'var':
                n_local += 1
                in_declaration = True
            if self.tkzr.content[i] == ';':
                in_declaration = False
            if self.tkzr.content[i] == ',' and in_declaration:
                n_local += 1
            if self.tkzr.content[i] == METHOD or self.tkzr.content[
                i] == CONSTRUCTOR or self.tkzr.content[i] == FUNCTION:
                break
        self.writer.write_function(self.class_name + '.' + name, n_local)
        self.tkzr.advance()

        if self.tkzr.symbol() != '(':
            raise Exception('no parenthesis')
        self.tkzr.advance()
        if kind == 'method':
            self.sym_table.define('this', self.class_name, 'argument')
        self.parameter_list()
        if self.tkzr.symbol() != ')':
            raise Exception('no parenthesis')
        self.tkzr.advance()

        if kind == 'method':
            self.writer.write_push('argument', '0')
            self.writer.write_pop('pointer', '0')
        elif kind == 'constructor':
            self.writer.write_push('constant',
                                   str(self.sym_table.counts['field']))
            self.writer.write_call('Memory.alloc', 1)
            self.writer.write_pop('pointer', 0)
        self.subroutine_body()

    def parameter_list(self):
        name = None
        type = None
        if self.tkzr.keyword() == 'int' or self.tkzr.keyword() == 'char' or self.tkzr.keyword() == 'boolean':
            type = self.tkzr.keyword()
            self.tkzr.advance()
        elif self.tkzr.token_type() == IDENTIFIER:
            type = self.tkzr.identifier()
            self.tkzr.advance()

        if self.tkzr.token_type() == IDENTIFIER:
            name = self.tkzr.identifier()
            self.tkzr.advance()
        if name is not None and type is not None:
            self.sym_table.define(name, type, 'argument')
            name = None
            type = None
        while self.tkzr.symbol() == ',':

            self.tkzr.advance()
            if self.tkzr.keyword() == 'int' or self.tkzr.keyword() == 'char' \
                    or self.tkzr.keyword() == 'boolean':
                type = self.tkzr.keyword()
                self.tkzr.advance()
            elif self.tkzr.token_type() == IDENTIFIER:
                type = self.tkzr.identifier()
                self.tkzr.advance()
            if self.tkzr.token_type() == IDENTIFIER:
                name = self.tkzr.identifier()
            if name is not None and type is not None:
                self.sym_table.define(name, type, 'argument')
                name = None
                type = None
            self.tkzr.advance()

    def subroutine_body(self):

        if self.tkzr.symbol() != '{':
            raise Exception('no bracket')
        self.tkzr.advance()
        while self.tkzr.keyword() == 'var':
            self.var_dec()
        self.statements()
        if self.tkzr.symbol() != '}':
            raise Exception('no bracket ' + self.tkzr.get_token())
        self.tkzr.advance()

    def var_dec(self):
        type = None
        name = None
        self.tkzr.advance()
        if self.tkzr.keyword() == 'int' or self.tkzr.keyword() == 'char' or self.tkzr.keyword() == 'boolean':
            type = self.tkzr.keyword()
        elif self.tkzr.token_type() == IDENTIFIER:
            type = self.tkzr.identifier()
        self.tkzr.advance()
        if self.tkzr.token_type() == IDENTIFIER:
            name = self.tkzr.identifier()
        self.sym_table.define(name, type, 'var')
        self.tkzr.advance()
        while self.tkzr.symbol() == ',':
            self.tkzr.advance()
            if self.tkzr.token_type() == IDENTIFIER:
                name = self.tkzr.identifier()
            self.sym_table.define(name, type, 'var')
            self.tkzr.advance()
        if self.tkzr.symbol() != ';':
            raise Exception('no semicolon')
        self.tkzr.advance()

    def statements(self):
        while self.tkzr.keyword() in STATEMENT_START:

            if self.tkzr.keyword() == "let":
                self.let_statement()

            elif self.tkzr.keyword() == "while":
                self.while_statement()

            elif self.tkzr.keyword() == "if":
                self.if_statement()

            elif self.tkzr.keyword() == "do":
                self.do_statement()

            elif self.tkzr.keyword() == "return":
                self.return_statement()

    def let_statement(self):
        name = None
        is_array = False
        self.tkzr.advance()
        if self.tkzr.token_type() == IDENTIFIER:
            name = self.tkzr.identifier()
        kind = self.sym_table.kind_of(name)
        if kind == 'var':
            kind = 'local'
        elif kind == 'field':
            kind = 'this'
        self.tkzr.advance()
        if self.tkzr.symbol() == "[":
            is_array = True
            self.tkzr.advance()
            self.expression()
            if self.tkzr.symbol() == "]":
                self.tkzr.advance()
            self.writer.write_push(kind, self.sym_table.index_of(name))
            self.writer.write_arithmetic('add')
        if self.tkzr.symbol() != "=":
            raise Exception('= missing')
        self.tkzr.advance()
        self.expression()
        if not is_array:
            self.writer.write_pop(kind, self.sym_table.index_of(name))
        else:
            self.writer.write_pop('temp', '0')
            self.writer.write_pop('pointer', '1')
            self.writer.write_push('temp', '0')
            self.writer.write_pop('that', '0')
        if self.tkzr.symbol() != ";":
            raise Exception('no semicolon')
        self.tkzr.advance()

    def while_statement(self):
        l1 = 'L1$' + str(self.tkzr.index) + '$'
        l2 = 'L2$' + str(self.tkzr.index) + '$'
        self.writer.write_label(l1)
        self.tkzr.advance()
        if self.tkzr.symbol() != "(":
            raise Exception('no parenthesis')
        self.tkzr.advance()
        self.expression()
        self.writer.write_arithmetic('not')
        self.writer.write_if(l2)

        if self.tkzr.symbol() != ")":
            raise Exception('no parenthesis')
        self.tkzr.advance()
        if self.tkzr.symbol() != "{":
            raise Exception('no brackets')
        self.tkzr.advance()
        self.statements()
        self.writer.write_goto(l1)
        if self.tkzr.symbol() != "}":
            raise Exception('no brackets')
        self.writer.write_label(l2)
        self.tkzr.advance()

    def if_statement(self):
        l1 = 'L1$' + str(self.tkzr.index) + '$'
        l2 = 'L2$' + str(self.tkzr.index) + '$'
        self.tkzr.advance()
        if self.tkzr.symbol() != "(":
            raise Exception('no parenthesis')
        self.tkzr.advance()
        self.expression()
        self.writer.write_arithmetic('not')
        if self.tkzr.symbol() != ")":
            raise Exception('no parenthesis')
        self.writer.write_if(l1)
        self.tkzr.advance()

        if self.tkzr.symbol() != "{":
            raise Exception('no brackets')
        self.tkzr.advance()

        self.statements()
        if self.tkzr.symbol() != "}":
            raise Exception('no brackets')
        self.writer.write_goto(l2)

        self.writer.write_label(l1)
        self.tkzr.advance()
        if self.tkzr.keyword() == "else":
            self.tkzr.advance()
            if self.tkzr.symbol() != "{":
                raise Exception('no brackets')
            self.tkzr.advance()
            self.statements()
            if self.tkzr.symbol() != "}":
                raise Exception('no brackets')
            self.tkzr.advance()
        self.writer.write_label(l2)

        # print(self.tkzr.get_token())

    def do_statement(self):
        self.tkzr.advance()
        if self.tkzr.token_type() == IDENTIFIER:
            self.subroutine_call()
            self.writer.write_pop('temp', '0')
        if self.tkzr.symbol() != ";":
            raise Exception('no semicolon')
        self.tkzr.advance()

    def return_statement(self):
        self.tkzr.advance()
        if self.tkzr.symbol() != ";":
            self.expression()
        else:  # void
            self.writer.write_push('constant', '0')
        self.writer.write_return()
        if self.tkzr.symbol() != ";":
            raise Exception('no semicolon')
        # print(self.tkzr.get_token())
        self.tkzr.advance()

    def convert_operator(self, operator):
        if operator == '+':
            return 'add'
        if operator == '-':
            return 'sub'
        if operator == '&amp;':
            return 'and'
        if operator == '|':
            return 'or'
        if operator == '&lt;':
            return 'lt'
        if operator == '&gt;':
            return 'gt'
        if operator == '=':
            return 'eq'

    def convert_unary(self, operator):
        if operator == '~':
            return 'not'
        if operator == '-':
            return 'neg'
        raise Exception('wrong operator:' + operator)

    def expression(self):
        self.compile_term()
        while self.tkzr.symbol() in OP:
            operator = self.tkzr.symbol()
            self.tkzr.advance()
            self.compile_term()
            if operator == '*':
                self.writer.write_call('Math.multiply', 2)
            elif operator == '/':
                self.writer.write_call('Math.divide', 2)
            else:

                self.writer.write_arithmetic(self.convert_operator(operator))

    def compile_term(self):
        if self.tkzr.token_type() == "integerConstant":
            self.writer.write_push('constant', self.tkzr.int_val())
            self.tkzr.advance()
        elif self.tkzr.token_type() == "stringConstant":
            self.writer.write_push('constant', len(self.tkzr.string_val()))
            self.writer.write_call('String.new', 1)
            for letter in self.tkzr.string_val():
                self.writer.write_push('constant', str(ord(letter)))
                self.writer.write_call('String.appendChar', 2)
            self.tkzr.advance()
        elif self.tkzr.keyword() in KEYWORD_CONSTANT:
            if self.tkzr.keyword() == 'this':
                self.writer.write_push('pointer', '0')
            elif self.tkzr.keyword() == 'null' or self.tkzr.keyword() == 'false':
                self.writer.write_push('constant', '0')
            elif self.tkzr.keyword() == 'true':
                self.writer.write_push('constant', '0')
                self.writer.write_arithmetic('not')
            self.tkzr.advance()
        elif self.tkzr.symbol() == "(":
            self.tkzr.advance()
            self.expression()
            if self.tkzr.symbol() != ")":
                raise Exception('no parenthesis')
            self.tkzr.advance()
        elif self.tkzr.symbol() in UN_OP:
            operator = self.tkzr.symbol()
            self.tkzr.advance()
            self.compile_term()
            self.writer.write_arithmetic(self.convert_unary(operator))

        elif self.tkzr.token_type() == IDENTIFIER:
            if self.tkzr.content[self.tkzr.index + 1] == "[":
                name = self.tkzr.identifier()
                self.tkzr.advance()
                if self.tkzr.symbol() == "[":
                    self.tkzr.advance()
                    self.expression()
                    if self.tkzr.symbol() != "]":
                        raise Exception('no brackets')
                    kind = self.sym_table.kind_of(name)
                    if kind == 'var':
                        kind = 'local'
                    elif kind == 'field':
                        kind = 'this'
                    self.writer.write_push(kind, self.sym_table.index_of(name))
                    self.writer.write_arithmetic('add')
                    self.writer.write_pop('pointer', '1')
                    self.writer.write_push('that', '0')
                    self.tkzr.advance()

            elif self.tkzr.content[self.tkzr.index + 1] == "(" or \
                    self.tkzr.content[self.tkzr.index + 1] == ".":
                self.subroutine_call()
            else:
                kind = self.sym_table.kind_of(self.tkzr.identifier())
                if kind == 'var':
                    kind = 'local'
                elif kind == 'field':
                    kind = 'this'
                self.writer.write_push(kind, self.sym_table.index_of(
                    self.tkzr.identifier()))
                self.tkzr.advance()

    def get_args_num(self):
        args_num = 0
        if self.tkzr.content[self.tkzr.index + 1] != ')':
            args_num = 1
            parenthesis = 0
            for i in range(self.tkzr.index, len(self.tkzr.content)):

                if self.tkzr.content[i] == '(':
                    parenthesis += 1
                elif self.tkzr.content[i] == ')':
                    parenthesis -= 1
                    if parenthesis == 0:
                        break
                elif self.tkzr.content[i] == ',':
                    args_num += 1
        return args_num

    def subroutine_call(self):
        name = self.tkzr.identifier()
        function_name = None
        args_num=0
        self.tkzr.advance()
        if self.tkzr.symbol() == "(":  # method of the actual class
            args_num+=self.get_args_num()
            self.tkzr.advance()
            self.writer.write_push('pointer', '0')
            self.expression_list()
            if self.tkzr.symbol() != ")":
                raise Exception('no parenthesis')
            self.writer.write_call(self.class_name + '.' + name,
                                   str(args_num + 1))
        elif self.tkzr.symbol() == ".":
            self.tkzr.advance()
            class_name = self.sym_table.type_of(name)
            if class_name is None:
                class_name = name

            else:
                kind = self.sym_table.kind_of(name)
                if kind == 'var':
                    kind = 'local'
                elif kind == 'field':
                    kind = 'this'
                self.writer.write_push(kind, self.sym_table.index_of(name))
                args_num += 1
            if self.tkzr.token_type() == IDENTIFIER:
                function_name = self.tkzr.identifier()

                self.tkzr.advance()
                args_num+=self.get_args_num()
                if self.tkzr.symbol() != "(":
                    raise Exception('no parenthesis')
                self.tkzr.advance()
                self.expression_list()
                if self.tkzr.symbol() != ")":
                    raise Exception('no parenthesis')

            self.writer.write_call(class_name + '.' + function_name,
                                   str(args_num))
        self.tkzr.advance()

    def expression_list(self):
        if self.tkzr.get_token() != ')':

            self.expression()
            while self.tkzr.symbol() == ',':
                self.tkzr.advance()
                self.expression()
