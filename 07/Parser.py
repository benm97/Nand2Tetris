import re

ARITH_COMMANDS = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']
C_ARITHMETIC = 'A'
C_PUSH = 'B'
C_POP = 'C'
PUSH = 'push'
POP = 'pop'


class Parser:
    def __init__(self):
        self.file = None
        self.counter = 0
        self.current_command = ""
        self.next_command = ""

    def set_file(self, file):
        self.file = file
        self.next_command = self.get_next()

    def has_more_commands(self):
        return self.next_command != ""

    def advance(self):
        if self.has_more_commands():
            self.current_command = self.next_command
            self.next_command = self.get_next()

    def get_next(self):
        line = ""
        for line in self.file:
            line = line.strip()
            if line == '':
                continue
            if re.search("^//.*", line):
                line = ""
                continue
            m = re.search("//.*", line)
            if m:
                line = line[:m.start()].strip()
            break
        print(line.strip())
        return line.strip()

    def command_type(self):
        if self.current_command in ARITH_COMMANDS:
            return C_ARITHMETIC
        if PUSH in self.current_command:
            return C_PUSH
        if POP in self.current_command:
            return C_POP

    def arg1(self):  # TODO return ex8
        if self.command_type() == C_ARITHMETIC:
            return self.current_command
        splitted = self.current_command.split()
        return splitted[1]

    def arg2(self):  # TODO ex8
        splitted = self.current_command.split()
        return splitted[2]
