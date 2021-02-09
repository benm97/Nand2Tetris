class VMWriter:
    def __init__(self, file):
        self.file = file

    def write_push(self, segment, index):
        self.file.write('push ' + segment + ' ' + str(index) + '\n')

    def write_pop(self, segment, index):
        self.file.write('pop ' + segment + ' ' + str(index) + '\n')

    def write_arithmetic(self, command):
        self.file.write(command + '\n')

    def write_label(self, symbol):
        self.file.write('label ' + symbol + '\n')

    def write_goto(self, symbol):
        self.file.write('goto ' + symbol + '\n')

    def write_if(self, symbol):
        self.file.write('if-goto ' + symbol + '\n')

    def write_call(self, name, n_args):
        self.file.write('call ' + name + ' ' + str(n_args) + '\n')

    def write_function(self, name, n_locals):
        self.file.write('function ' + name + ' ' + str(n_locals) + '\n')

    def write_return(self):
        self.file.write('return\n')

