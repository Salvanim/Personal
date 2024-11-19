from collections import defaultdict

class search:
    def __init__(self, array):
        self.index_map = defaultdict(list)
        self.reversed_state = False  # Track if the map is reversed
        for index, value in enumerate(array):
            self.index_map[value].append(index)

    def __getitem__(self, value):
        return self.index_map.get(value, [-1])

    def __setitem__(self, value, new_index):
        if any(new_index in indices for indices in self.index_map.values()):
            for indices in self.index_map.values():
                for i in range(len(indices)):
                    if indices[i] >= new_index:
                        indices[i] += 1
        self.index_map[value].append(new_index)

    def __contains__(self, value):
        return value in self.index_map

    def __call__(self, value):
        return self[value]

    def __iter__(self):
        return iter(self.index_map.items())

    def __repr__(self):
        return "\n".join(f"{key}: {indices}" for key, indices in self.index_map.items())

    def __len__(self):
        return len(self.index_map)

    def items(self):
        return self.index_map.items()

    def list(self):
        if self.reversed_state:
            size = max(self.index_map.keys()) + 1
            array = [None] * size
            for index, values in self.index_map.items():
                for value in values:
                    array[index] = value
        else:
            size = max(index for indices in self.index_map.values() for index in indices) + 1
            array = [None] * size
            for value, indices in self.index_map.items():
                for index in indices:
                    array[index] = value
        return array

    def copy(self):
        new_copy = search(self.list())
        if self.reversed_state:
            new_copy.reverse()
        return new_copy

    def __add__(self, other):
        output = search(self.list() + other.list())
        output.reversed_state = self.reversed_state and other.reversed_state
        if output.reversed_state:
            output.reverse()
        return output

    def merge(self, other):
        current_max_index = max(index for indices in self.index_map.values() for index in indices) + 1
        for value, indices in other.index_map.items():
            shifted_indices = [index + current_max_index for index in indices]
            self.index_map[value].extend(shifted_indices)
        return self

    def reverse(self):
        reversed_map = defaultdict(list)
        for value, indices in self.index_map.items():
            for index in indices:
                reversed_map[index].append(value)
        self.index_map = reversed_map
        self.reversed_state = not self.reversed_state
        return self
