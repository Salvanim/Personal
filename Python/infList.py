class infList(list):
    def __init__(self, *content):
        if len(content) == 1 and isinstance(content[0], list):
            self.content = content[0]
        else:
            self.content = list(content)
        self.fillValue = None

    def __getitem__(self, index):
        while len(self.content) <= index:
            self.content.append(self.fillValue)
        return self.content[index]

    def __setitem__(self, index, value):
        while len(self.content) <= index:
            self.content.append(self.fillValue)
        self.content[index] = value

    def __matmul__(self, value):
        self.fillValue = value

    def __str__(self):
        return str(self.content)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter(self.content)

    def __eq__(self, other):
        isiterable = True
        try:
            iter(other)
        except TypeError as te:
           isiterable = False

        if isinstance(other, infList):
            return tuple(self.content) == tuple(other.content)
        elif isiterable:
            return tuple(self.content) == tuple(other)
        else:
            return False

    def __ne__(self,other):
        return not(self==other)

    def __hash__(self):
        return hash(tuple(self.content))
