import sys
import os
import Parser as p
import CodeWriter as c

my_parser = p.Parser()
my_writer = c.CodeWriter()
0

def run_parsing():
    while my_parser.has_more_commands():
        my_parser.advance()
        my_writer.counter += 1

        if my_parser.command_type() == p.C_PUSH or \
                my_parser.command_type() == p.C_POP:
            my_writer.WritePushPop(my_parser.command_type(), my_parser.arg1(),
                                   my_parser.arg2())
        elif my_parser.command_type() == p.C_ARITHMETIC:
            my_writer.write_arithmetic(my_parser.arg1())

        elif my_parser.command_type() == p.C_LABEL:
            print(my_parser.functionStack)
            my_writer.write_label(
                my_parser.functionStack[-1] + '$' + my_parser.arg1())

        elif my_parser.command_type() == p.C_GOTO:
            my_writer.write_goto(
                my_parser.functionStack[-1] + '$' + my_parser.arg1())

        elif my_parser.command_type() == p.C_IF:
            my_writer.write_if(
                my_parser.functionStack[-1] + '$' + my_parser.arg1())

        elif my_parser.command_type() == p.C_CALL:
            my_writer.write_call(my_parser.arg1(), my_parser.arg2())
        elif my_parser.command_type() == p.C_RETURN:
            my_writer.write_return()
           # my_parser.functionStack.pop()
        elif my_parser.command_type() == p.C_FUNCTION:
            my_writer.write_function(my_parser.arg1(), my_parser.arg2())
            my_parser.functionStack.append(my_parser.arg1())



if __name__ == "__main__":
    print()
    if len(sys.argv) != 2:
        raise Exception

    if os.path.isdir(sys.argv[1]):
        if sys.argv[1][-1] != '/':
            sys.argv[1] += '/'
        dirname = (sys.argv[1]).split('/')[-2]
        my_writer.set_file(open(sys.argv[1] + dirname + ".asm", 'w+'))
        my_writer.file.write('@256\nD=A\n@SP\nM=D\n')
        my_writer.counter+=1
        my_writer.write_call('Sys.init','0')
        my_parser.functionStack.append('Sys.init')
        for root, dirs, files in os.walk(sys.argv[1]):
            files = sorted(files)
            for filename in files:
                if filename.split('.')[-1].strip() == 'vm':
                    my_parser.set_file(open(sys.argv[1] + filename, 'r'))
                    my_writer.set_filename(filename.split('.')[-2])
                    run_parsing()
            break

    else:
        path_we = '.'.join(sys.argv[1].split('.')[:-1])
        filename_we = path_we.split('/')[-1]  # pour liux remplacer par /
        my_writer.set_file(open(path_we + ".asm", 'w+'))
        my_writer.set_filename(filename_we)
        my_parser.set_file(open(sys.argv[1], 'r'))
        run_parsing()
