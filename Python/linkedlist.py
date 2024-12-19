class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = Node()

    def isItterable(self, object, exclude=[str]):
        try:
            object = iter(object)
        except:
            return False
        if type(object) in exclude:
            return False
        return True

    def append(self, data):
        new_node = Node(data)
        if not self.head.data:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def __getitem__(self, value):
        return self.head.data[value]

    def __setitem__(self, value, new):
        current = self.head
        while current:
            if current.data == value:
                current.data = new
                return

    def __len__(self):
        return len(self.head.data)

    def __contains__(self, value):
        current = self.head
        while current:
            if current.data == value:
                return True
        return False

    def __str__(self):
        output = ""
        current = self.head
        while current:
            output += str(current.data) + " -> "
            current = current.next
        output = output[0:len(output)-4]
        return output

    def delete(self, key):
        current = self.head
        if not current:
            return
        if current.data == key:
            self.head = current.next
            current = None
            return
        prev = None
        while current and current.data != key:
            prev = current
            current = current.next
        if current is None:
            return
        prev.next = current.next
        current = None

class Tree:
    def __init__(self, value=None):
        self.value = value
        self.children = LinkedList()

    def add_child(self, child_node):
        self.children.append(child_node)

    def __str__(self):
        return self._build_tree_str("", True)

    def _build_tree_str(self, prefix, is_last):
        result = prefix + ("└─ " if is_last else "├─ ") + str(self.value) + "\n"
        current = self.children.head
        while current:
            if isinstance(current.data, Tree):
                is_last_child = current.next is None
                child_prefix = prefix + ("   " if is_last else "│  ")
                result += current.data._build_tree_str(child_prefix, is_last_child)
            current = current.next
        return result

    def find_path(self, target_value):
        path = LinkedList()
        if self._find_path_helper(target_value, path):
            return path
        return None

    def _find_path_helper(self, target_value, path):
        path.append(self.value)
        if self.value == target_value:
            return True
        current = self.children.head
        while current:
            if isinstance(current.data, Tree) and current.data._find_path_helper(target_value, path):
                return True
            current = current.next
        current = path.head
        if current and current.data == self.value:
            path.head = path.head.next
        return False

# Example usage
root = Tree("Root")
child1 = Tree("Child 1")
child2 = Tree("Child 2")
root.add_child(child1)
root.add_child(child2)

grandchild1 = Tree("Grandchild 1.1")
grandchild2 = Tree("Grandchild 1.2")
child1.add_child(grandchild1)
child1.add_child(grandchild2)

grandchild3 = Tree("Grandchild 2.1")
child2.add_child(grandchild3)

greatgrandchild1 = Tree("Great Grandchild 1.1")
greatgrandchild2 = Tree("Great Grandchild 1.2")
grandchild1.add_child(greatgrandchild1)
grandchild1.add_child(greatgrandchild2)

greatgrandchild3 = Tree("Great Grandchild 2.1")
greatgrandchild4 = Tree("Great Grandchild 2.2")
grandchild2.add_child(greatgrandchild3)
grandchild2.add_child(greatgrandchild3)

# Print the tree
print(root)

path = root.find_path("Great Grandchild 1.1")
if path:
    print(f"Path to Great Grandchild 1.1:", path)
else:
    print("Target not found.")
