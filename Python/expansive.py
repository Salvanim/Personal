from collections.abc import Iterable, Iterator
from typing import Any, SupportsIndex


class ExpA(list):
    def __init__(self, *content, fillValue=None):
        self.content = list(content)
        self.fill = fillValue

    def __getitem__(self,index):
        while len(self.content) <= index:
            self.content.append(self.fill)
        return self.content[index]
    
    def __setitem__(self, index, value):
        while len(self.content) <= index:
            self.content.append(self.fill)
        self.content[index] = value
    
    def __str__(self):
        return str(self.content)
    
    def __repr__(self):
        return [self.content, self.fill]

    def __matmul__(self, value):
        self.fill = value
        return self
    
    def append(self, value):
        self[len(self)] = value
        return self
    
    def __contains__(self, key: object) -> bool:
        return self.content.__contains__(key)

    def __delitem__(self, key: SupportsIndex | slice) -> None:
        return self.content.__delitem__(key)
    
    def __eq__(self, value: object) -> bool:
        return self.content.__eq__(value)
    
    def __reduce__(self) -> str | tuple[Any, ...]:
        return self.content.__reduce__()

    def __iter__(self) -> Iterator:
        return self.content.__iter__()
    
    def __call__(self, *args: Any) -> Any:
        for arg in args:
            self.append(arg)
        return self
    
    def __len__(self):
        return len(self.content)
    
    def __dir__(self) -> Iterable[str]:
        return self.content.__dir__()
    
    def isItterable(self, Object : object):
        try:
            iter(Object)
        except:
            return False
        return True

    def __add__(self, value):
        if self.isItterable(value):
          for val in value:
            self.append(val)
        else:
            self.append(value)
        return self
    
    def index(self, value):
        return self.content.index(value)

a = ExpA(1,2,3,4,5,6,7,fillValue="A")
a[100]
print(a.index("A"))