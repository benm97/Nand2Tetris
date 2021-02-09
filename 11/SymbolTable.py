SUBROUTINE_TYPES = ('var', 'argument')


class SymbolTable:

    def __init__(self):
        self.class_table = dict()
        self.subroutine_table = None
        self.counts = {'static': 0, 'field': 0, 'argument': 0, 'var': 0}
    def start_subroutine(self):
        self.counts['var'] = 0
        self.counts['argument'] = 0
        self.subroutine_table = dict()

    def define(self, name, type, kind):

        data = (type, kind, self.counts[kind])
        if kind in SUBROUTINE_TYPES:
            self.subroutine_table[name] = data
        else:
            self.class_table[name] = data
        #print(name,kind,type,self.counts[kind])
        self.counts[kind] += 1
    def var_count(self, kind):
        return self.counts[kind]

    def kind_of(self, name):

        if name in self.subroutine_table:
            return self.subroutine_table[name][1]
        elif name in self.class_table:
            return self.class_table[name][1]

    def type_of(self, name):
        if name in self.subroutine_table:
            return self.subroutine_table[name][0]
        elif name in self.class_table:
            return self.class_table[name][0]

    def index_of(self, name):
        if name in self.subroutine_table:
            return self.subroutine_table[name][2]
        elif name in self.class_table:
            return self.class_table[name][2]
