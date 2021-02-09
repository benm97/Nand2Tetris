SEGMENT = {'local', 'argument', 'this', 'that'}
CONSTANT = 'constant'
STATIC = 'static'
TEMP = 'temp'
POINTER = 'pointer'

UNARY = {'neg', 'not'}
POPCODE = "@SP\nM=M-1\n@SP\nA=M\nD=M\n"
PUSHCODE = "@SP\nA=M\nM=D\n@SP\nM=M+1\n"
JUMPCODE1 = "@R14\nD=M\n@R13\nD=M-D\n@TRUE"
JUMPCODE2 = "D=0\n@NEXT"
JUMPCODE3 = "\n0;JMP\n(TRUE"
JUMPCODE4 = ")\nD=-1\n(NEXT"
JUMPCODE5 = ")\n" + PUSHCODE
import Parser as p


class CodeWriter:

    def __init__(self):
        self.file = None
        self.filename = ""
        self.counter = 0

    def set_file(self, file):
        self.file = file

    def set_filename(self, filename):
        self.filename = filename

    def format_segment(self, str):
        if str == "local":
            return "LCL"
        elif str == "argument":
            return "ARG"
        elif str == "this":
            return "THIS"
        elif str == "that":
            return "THAT"

    def push(self, segment, index):
        if segment in SEGMENT:
            self.file.write("@" + self.format_segment(segment) +
                            "\nD=M\n@" + index + "\nA=D+A\nD=M\n")
        elif segment == CONSTANT:
            self.file.write("@" + index + "\nD=A\n")
        elif segment == STATIC:
            self.file.write("@" + self.filename + "." + index + "\nD=M\n")
        elif segment == TEMP:
            self.file.write("@5\nD=A\n@" + index + "\nA=D+A\nD=M\n")
        elif segment == POINTER:
            if index == '0':
                self.file.write("@THIS\n")
            else:
                self.file.write("@THAT\n")
            self.file.write("D=M\n")
        self.file.write(PUSHCODE)

    def pop(self, segment, index):
        if segment in SEGMENT:
            self.file.write("@" + self.format_segment(segment) +
                            "\nD=M\n@" + index +
                            "\nA=D+A\nD=A\n@R13\nM=D\n"
                            + POPCODE + "@R13\nA=M\nM=D\n")
        elif segment == STATIC:
            self.file.write(
                POPCODE + "@" + self.filename + "." + index + "\nM=D\n")
        elif segment == TEMP:
            self.file.write(
                "@5\nD=A\n@" + index + "\nA=D+A\nD=A\n@R13\nM=D\n"
                + POPCODE + "@R13\nA=M\nM=D\n")
        elif segment == POINTER:
            self.file.write(POPCODE)
            if index == '0':
                self.file.write("@THIS\nM=D\n")
            else:
                self.file.write("@THAT\nM=D\n")

    def WritePushPop(self, command, segment, index):
        if command == p.C_PUSH:
            self.push(segment, index)
        elif command == p.C_POP:
            self.pop(segment, index)

    def write_arithmetic(self, command):
        self.file.write(POPCODE + "@R14\nM=D\n")
        if command not in UNARY:
            self.file.write(POPCODE + "@R13\nM=D\n")

        if command == p.ARITH_COMMANDS[0]:  # add
            self.file.write("@R14\nD=M\n@R13\nD=D+M\n" + PUSHCODE)
        elif command == p.ARITH_COMMANDS[1]:  # sub
            self.file.write("@R14\nD=M\n@R13\nD=M-D\n" + PUSHCODE)
        elif command == p.ARITH_COMMANDS[2]:  # neg
            self.file.write("@R14\nD=-M\n" + PUSHCODE)
        elif command == p.ARITH_COMMANDS[3]:  # eq
            self.file.write(
                JUMPCODE1 + str(self.counter) + "\nD;JEQ\n" + JUMPCODE2 + str(
                    self.counter) + JUMPCODE3 + str(
                    self.counter) + JUMPCODE4 + str(self.counter) + JUMPCODE5)
        elif command == p.ARITH_COMMANDS[4]:  # gt
            self.file.write(
                '@R14\nD=D-M\n@R15\nM=D\n@R13\nM=M>>\n@R14\nM=M>>\n'
                + JUMPCODE1 + str(
                    self.counter) + "\nD;JGT\n" + JUMPCODE2 + str(
                    self.counter) + JUMPCODE3 + str(
                    self.counter) + JUMPCODE4 + str(self.counter) + JUMPCODE5)
            self.counter += 1
            self.file.write('D=1\n' + PUSHCODE + '@R15\nD=M\n' + PUSHCODE
                            + POPCODE + "@R14\nM=D\n"
                            + POPCODE + "@R13\nM=D\n"
                            + JUMPCODE1 + str(
                self.counter) + "\nD;JEQ\n" + JUMPCODE2 + str(
                self.counter) + JUMPCODE3 + str(
                self.counter) + JUMPCODE4 + str(
                self.counter) + JUMPCODE5  # equal
                            + POPCODE + "@R14\nM=D\n"
                            + POPCODE + "@R13\nM=D\n"
                            + "@R14\nD=M\n@R13\nD=D|M\n" + PUSHCODE)  # or

        elif command == p.ARITH_COMMANDS[5]:  # lt
            self.file.write(
                '@R14\nD=M-D\n@R15\nM=D\n@R13\nM=M>>\n@R14\nM=M>>\n'
                + JUMPCODE1 + str(
                    self.counter) + "\nD;JLT\n" + JUMPCODE2 + str(
                    self.counter) + JUMPCODE3 + str(
                    self.counter) + JUMPCODE4 + str(self.counter) + JUMPCODE5)
            self.counter += 1
            self.file.write('D=1\n' + PUSHCODE + '@R15\nD=M\n' + PUSHCODE
                            + POPCODE + "@R14\nM=D\n"
                            + POPCODE + "@R13\nM=D\n"
                            + JUMPCODE1 + str(
                self.counter) + "\nD;JEQ\n" + JUMPCODE2 + str(
                self.counter) + JUMPCODE3 + str(
                self.counter) + JUMPCODE4 + str(
                self.counter) + JUMPCODE5  # equal
                            + POPCODE + "@R14\nM=D\n"
                            + POPCODE + "@R13\nM=D\n"
                            + "@R14\nD=M\n@R13\nD=D|M\n" + PUSHCODE)  # or

        elif command == p.ARITH_COMMANDS[6]:  # and
            self.file.write("@R14\nD=M\n@R13\nD=D&M\n" + PUSHCODE)
        elif command == p.ARITH_COMMANDS[7]:  # or
            self.file.write("@R14\nD=M\n@R13\nD=D|M\n" + PUSHCODE)
        elif command == p.ARITH_COMMANDS[8]:  # not
            self.file.write("@R14\nD=!M\n" + PUSHCODE)

    def write_label(self, label):
        self.file.write('(' + label + ')\n')

    def write_goto(self, label):
        self.file.write('@' + label + '\n0;JMP\n')

    def write_if(self, label):
        self.file.write(POPCODE + '@' + label + '\nD;JNE\n')

    def write_call(self, function_name, num_args):
        self.file.write('@RETURN' + str(
            self.counter) + '\nD=A\n' + PUSHCODE)  # push return adress
        self.file.write('@LCL\nD=M\n' + PUSHCODE)  # push LCL
        self.file.write('@ARG\nD=M\n' + PUSHCODE)  # push ARG
        self.file.write('@THIS\nD=M\n' + PUSHCODE)  # push this
        self.file.write('@THAT\nD=M\n' + PUSHCODE)  # push that
        self.file.write(
            '@SP\nD=M\n@' + num_args + '\nD=D-A\n@5\nD=D-A\n@ARG\nM=D\n')  # ARG=SP-n-5
        self.file.write('@SP\nD=M\n@LCL\nM=D\n')  # LCL=SP
        self.file.write('@' + function_name + '\n0;JMP\n')  # goto f
        self.file.write(
            '(RETURN' + str(self.counter) + ')\n')  # (return address)

    def write_return(self):
        self.file.write('@LCL\nD=M\n@R14\nM=D\n')  # FRAME=LCL
        self.file.write('@5\nD=D-A\nA=D\nD=M\n@R15\nM=D\n')  # RET=*(FRAME-5)
        self.file.write(POPCODE + '@ARG\nA=M\nM=D\n')  # *ARG=POP
        self.file.write('@ARG\nD=M\nD=D+1\n@SP\nM=D\n')  # SP=ARG+1
        self.file.write(
            '@R14\nM=M-1\nA=M\nD=M\n@THAT\nM=D\n')  # THAT=*(FRAME-1)
        self.file.write(
            '@R14\nM=M-1\nA=M\nD=M\n@THIS\nM=D\n')  # THIS=*(FRAME-2)
        self.file.write('@R14\nM=M-1\nA=M\nD=M\n@ARG\nM=D\n')  # ARG=*(FRAME-3)
        self.file.write('@R14\nM=M-1\nA=M\nD=M\n@LCL\nM=D\n')  # LCL=*(FRAME-4)
        self.file.write('@R15\nA=M\n0;JMP\n')
    def write_function(self, function_name, locals_num):
        self.file.write('(' + function_name + ')\nD=0\n')
        for i in range(int(locals_num)):
            self.file.write(PUSHCODE)
