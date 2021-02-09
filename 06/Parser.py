import re

A_COMMAND = 'A'
C_COMMAND = 'C'
L_COMMAND = 'L'
NULL='null'

class Parser:
    def __init__(self, file):
        self.file = file
        self.counter = 0
        self.current_command = ""
        self.next_command = self.get_next()

    def command_type(self):
        if re.search("^@.+", self.current_command):
            return A_COMMAND
        elif re.search("^\(.+", self.current_command):
            return L_COMMAND
        return C_COMMAND

    def has_more_commands(self):
        return self.next_command != ""

    def advance(self):
        if self.has_more_commands():
            self.current_command = self.next_command
            if self.command_type() == A_COMMAND or self.command_type() == C_COMMAND:
                self.counter += 1
            self.next_command = self.get_next()

    def get_next(self):
        line = ""
        for line in self.file:
            line = line.strip()
            if line == '':
                continue
            if re.search("^//.*", line):
                line=""
                continue
            m=re.search("//.*",line)
            if m:
                line=line[:m.start()].strip()
            break

        return line
    def symbol(self):
        if self.command_type() == A_COMMAND:
            m=re.search("^@\s*.+",self.current_command)
            return m.group()[1:].strip()
        if self.command_type() == L_COMMAND:
            m=re.search("^\(\s*.+\)",self.current_command)
            return m.group()[1:-1].strip()
    def dest(self):
        command=self.current_command.split('=')
        if len(command)>1:
            return command[0].strip()
        else:
            return NULL
    def comp(self):
        command=self.current_command.split(';')
        if '=' in command[0]:
            my_command=command[0].split('=')
            return my_command[1].strip()
        else:
            return command[0].strip()
    def jump(self):
        command=self.current_command.split(';')
        if len(command)>1:
            return command[-1].strip()
        else:
            return NULL
