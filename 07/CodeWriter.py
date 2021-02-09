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
