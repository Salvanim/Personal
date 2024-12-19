class Node:
    def __init__(self, data=None):
        self.data = data  # Store data
        self.next = None  # Pointer to the next node
        self.first = type(self.data) == list, self.data[0] , self.data

class LinkedList:
    def __init__(self):
        self.head = Node()  # Initialize the list with an empty head

    # Method to add a new node at the end of the list
    def append(self, data):
        new_node = Node(data)  # Create a new node with the given data
        if not self.head.data:
            self.head = new_node  # If list is empty, new node is the head
            return
        last = self.head
        while last.next:  # Traverse to the last node
            last = last.next
        last.next = new_node  # Make the last node point to the new node

    def __getitem__(self, value):
        return self.head.data[value]

    def __len__(self):
        return len(self.head.data)

    def __str__(self):
        output = ""
        current = self.head
        while current:
            output += str(current.data) + " -> "
            current = current.next
        output += current.first
        return output

    # Method to delete a node by value
    def delete(self, key):
        current = self.head
        # If the list is empty
        if not current:
            print("The list is empty.")
            return
        # If the node to be deleted is the head
        if current.data == key:
            self.head = current.next
            current = None
            return
        # Find the node to delete
        prev = None
        while current and current.data != key:
            prev = current
            current = current.next
        if current is None:
            print(f"Node with value {key} not found.")
            return
        prev.next = current.next  # Unlink the node
        current = None

ll = LinkedList()
ll.append("1")
ll.append("2")
ll.append("3")
print(ll)
