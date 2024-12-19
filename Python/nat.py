class Node:
    def __init__(self, data):
        self.data = data  # Store data
        self.next = None  # Pointer to the next node

class LinkedList:
    def __init__(self):
        self.head = None  # Initialize the list with an empty head

    # Method to add a new node at the end of the list
    def append(self, data):
        new_node = Node(data)  # Create a new node with the given data
        if not self.head:
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

    # Method to print the linked list
    def print_list(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")  # End of the list

    def __str__(self):
        output = ""
        current = self.head
        while current:
            output += str(current.data) + " -> "
            current = current.next
        output += "None"
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

def check(num, list = []):
    list.append(num)
    if num == 1:
        return list
    elif num % 2 == 0:
        return check(num/2, list)
    elif num % 2 == 1:
        return check((num*3)+1, list)

for n in range((2*(10**20)),(9*(10**999)),1):
    cl = check(n)
    c = cl[len(cl)-1]
    print(c == 1)
