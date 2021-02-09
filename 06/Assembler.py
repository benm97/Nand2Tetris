import sys
import os
import Parser as p
import Code as c
import SymbolTable as s


def to_bin(number):
    binary = "{0:b}".format(number)
    to_return = '0' * (15 - len(binary))
    for bit in binary:
        to_return += bit
    return to_return[:15]


def parse_file(path, file_name,is_absolute):
    my_file_path=path +file_name
    if is_absolute:
        my_file_path=path + '/' + file_name
    file = open(my_file_path, 'r')
    # Parse Symbols
    symbol_parser = p.Parser(file)
    my_table = s.SymbolTable()
    while symbol_parser.has_more_commands():
        symbol_parser.advance()
        if symbol_parser.command_type() == p.L_COMMAND:
            my_table.table[symbol_parser.symbol()] = symbol_parser.counter

    # Second Parse
    my_hack_path=path  + file_name.split('.')[0] + '.hack'
    if is_absolute:
        my_hack_path=path  +'/'+ file_name.split('.')[0] + '.hack'
    hack_file = open(my_hack_path,'w+')  # TODO if exists

    file.seek(0)
    my_parser = p.Parser(file)
    my_code = c.Code()
    memory_counter = 16
    while my_parser.has_more_commands():
        my_parser.advance()
        if my_parser.command_type() == p.A_COMMAND:
            symbol = my_parser.symbol()

            if not symbol.isdigit():
                if symbol not in my_table.table:
                    my_table.table[symbol] = memory_counter
                    memory_counter += 1
                symbol = my_table.table[symbol]
            hack_file.write('0' + to_bin(int(symbol)) + "\n")
        elif my_parser.command_type() == p.C_COMMAND:
            if '<<' in my_parser.current_command or '>>' in my_parser.current_command:
                hack_file.write(
                    '101' + my_code.comp(my_parser.comp()) + my_code.dest(
                        my_parser.dest()) + my_code.jump(my_parser.jump()) + "\n")

            else:
                hack_file.write(
                    '111' + my_code.comp(my_parser.comp()) + my_code.dest(
                        my_parser.dest()) + my_code.jump(my_parser.jump()) + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception
    is_absolute=False
    if '/' in sys.argv[1]:
        is_absolute=True

    if os.path.isdir(sys.argv[1]):
        for (dirpath, dirnames, filenames) in os.walk(sys.argv[1]):
            for filename in filenames:
                if filename.split('.')[-1].strip()=='asm':
                    parse_file(sys.argv[1], filename,is_absolute)
            break
    else:

        splitted_path = sys.argv[1].split('/')
        path = '/'.join(splitted_path[:-1])
        parse_file(path, splitted_path[-1],is_absolute)
