import JackTokenizer as JT
import CompilationEngine as CE
import sys
import os

if __name__ == "__main__":

    if len(sys.argv) != 2:
        raise Exception
    my_ce = CE.CompilationEngine()
    if os.path.isdir(sys.argv[1]):
        if sys.argv[1][-1] != '/':
            sys.argv[1] += '/'
        for root, dirs, files in os.walk(sys.argv[1]):
            files = sorted(files)
            for filename in files:
                if filename.split('.')[-1].strip() == 'jack':
                    my_tkzr = JT.JackTokenizer(
                        open(sys.argv[1] + filename, 'r'))
                    my_ce.run(my_tkzr, open(
                        sys.argv[1] + filename.split('.')[-2] + '.xml', 'w+'))

            break

    else:
        my_tkzr = JT.JackTokenizer(open(sys.argv[1], 'r'))
        my_ce.run(my_tkzr, open(sys.argv[1].split('.')[-2] + '.xml', 'w+'))
