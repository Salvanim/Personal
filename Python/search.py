from collections import defaultdict

class Search:
    def __init__(self, array):
        self.index_map = defaultdict(list)
        self.max_index = -1  # Track the maximum index
        self.reversed_state = False
        self._repr_cache = ""  # Cache for __repr__
        self._modified = True  # Flag to track modifications

        for index, value in enumerate(array):
            self.index_map[value].append(index)
            self.max_index = max(self.max_index, index)
        self._modified = True

    def __getitem__(self, value):
        return self.index_map.get(value, [-1])

    def __setitem__(self, value, new_index):
        if new_index not in (index for indices in self.index_map.values() for index in indices):
            self.index_map[value].append(new_index)
            self.max_index = max(self.max_index, new_index)
            self._modified = True  # Mark as modified

    def __contains__(self, value):
        return value in self.index_map

    def __call__(self, value):
        return self[value]

    def __iter__(self):
        return iter(self.index_map.items())

    def __repr__(self):
        if self._modified:
            self._repr_cache = "\n".join(f"{key}: {indices}" for key, indices in self.index_map.items())
            self._modified = False  # Reset the flag
        return self._repr_cache

    def __len__(self):
        return len(self.index_map)

    def items(self):
        return self.index_map.items()

    def list(self):
        size = self.max_index + 1
        array = [None] * size
        for value, indices in self.index_map.items():
            for index in indices:
                array[index] = value
        return array

    def copy(self):
        new_copy = Search(self.list())
        if self.reversed_state:
            new_copy.reverse()
        return new_copy

    def __add__(self, other):
        output = Search(self.list() + other.list())
        output.reversed_state = self.reversed_state and other.reversed_state
        if output.reversed_state:
            output.reverse()
        return output

    def merge(self, other):
        offset = self.max_index + 1
        for value, indices in other.index_map.items():
            shifted_indices = [index + offset for index in indices]
            self.index_map[value].extend(shifted_indices)
        self.max_index += other.max_index + 1
        self._modified = True  # Mark as modified
        return self

    def reverse(self):
        reversed_map = defaultdict(list)
        for value, indices in self.index_map.items():
            for index in indices:
                reversed_map[index].append(value)
        self.index_map = reversed_map
        self.reversed_state = not self.reversed_state
        self.max_index = max(self.index_map.keys(), default=-1)
        self._modified = True  # Mark as modified
        return self
