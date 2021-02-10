# Course: CS261 - Data Structures
# Student Name: Jeremy Vernon
# Assignment: 3
# Description: Singly Linked List


class SLLException(Exception):
    """
    Custom exception class to be used by Singly Linked List
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class SLNode:
    """
    Singly Linked List Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        self.next = None
        self.value = value


class LinkedList:
    def __init__(self, start_list=None):
        """
        Initializes a new linked list with front and back sentinels
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.head = SLNode(None)
        self.tail = SLNode(None)
        self.head.next = self.tail

        # populate SLL with initial values (if provided)
        # before using this feature, implement add_back() method
        if start_list is not None:
            for value in start_list:
                self.add_back(value)

    def __str__(self) -> str:
        """
        Return content of singly linked list in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'SLL ['
        if self.head.next != self.tail:
            cur = self.head.next.next
            out = out + str(self.head.next.value)
            while cur != self.tail:
                out = out + ' -> ' + str(cur.value)
                cur = cur.next
        out = out + ']'
        return out

    def length(self) -> int:
        """
        Return the length of the linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        length = 0
        cur = self.head
        while cur.next != self.tail:
            cur = cur.next
            length += 1
        return length

    def is_empty(self) -> bool:
        """
        Return True is list is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.head.next == self.tail

    # ------------------------------------------------------------------ #

    def add_front(self, value: object) -> None:
        """
        Adds an element to the beginning of the list
        """
        front_node = SLNode(value)
        front_node.next = self.head.next
        self.head.next = front_node

    def add_back(self, value: object) -> None:
        """
        Adds an element to the end of the list
        """
        # traverses the list to find last node
        def find_last(current=self.head):
            if current.next == self.tail:
                return current
            current = current.next
            return find_last(current)

        # inserts the new node
        last_node = find_last()
        end_node = SLNode(value)
        last_node.next = end_node
        end_node.next = self.tail

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Inserts an element at the given index location
        """
        # helper function sets current index and current node values
        # then recursively searches for the node at the given index position
        def get_at_index(target_index=index, curr_index=0, current=self.head):
            if target_index == curr_index:
                return current
            current = current.next
            curr_index += 1
            return get_at_index(index, curr_index, current)

        # checks for valid index location, then inserts at index
        if index > self.length() or index < 0:
            raise SLLException
        insert_after = get_at_index()
        insert_node = SLNode(value)
        insert_node.next = insert_after.next
        insert_after.next = insert_node

    def remove_front(self) -> None:
        """
        Removes front element
        """
        if self.length() == 0:
            raise SLLException
        front_node = self.head.next
        self.head.next = front_node.next

    def remove_back(self) -> None:
        """
        Removes back element
        """
        # traverses the list to find last node
        def remove_back_helper(previous=self.head):
            if previous.next.next == self.tail:
                return previous
            previous = previous.next
            return remove_back_helper(previous)

        # removes last element
        if self.length() == 0:
            raise SLLException
        previous = remove_back_helper()
        previous.next = self.tail

    def remove_at_index(self, index: int) -> None:
        """
        Removes element at the given index
        """
        # helper function sets current index and current node values
        # then recursively searches for the node at the given index position
        def remove_at_index_helper(target_index=index, curr_index=0, previous=self.head):
            if target_index == curr_index:
                return previous
            previous = previous.next
            curr_index += 1
            return remove_at_index_helper(index, curr_index, previous)

        if index > (self.length() - 1) or index < 0:
            raise SLLException
        previous_node = remove_at_index_helper()
        previous_node.next = previous_node.next.next

    def get_front(self) -> object:
        """
        Gets the value of the first element
        """
        if self.length() == 0:
            raise SLLException
        return self.head.next.value

    def get_back(self) -> object:
        """
        Gets the value of the last element
        """
        # traverses the list to find last node
        def get_back_helper(current=self.head):
            if current.next == self.tail:
                return current
            current = current.next
            return get_back_helper(current)

        # checks that the list is not empty
        if self.length() == 0:
            raise SLLException
        # gets the value of the last eleement
        last_node = get_back_helper()
        return last_node.value

    def remove(self, value: object) -> bool:
        """
        Removes the first element that matches the given value
        Returns True if removed and False if not found
        """
        # traverses the list to find if there is a matching element
        def remove_helper(previous=self.head):
            if previous.next.value == value:
                return previous
            if previous.next != self.tail:
                previous = previous.next
                return remove_helper(previous)
            return False

        # if element was found, removes the element
        previous = remove_helper()
        if previous:
            previous.next = previous.next.next
            return True
        return False

    def count(self, value: object) -> int:
        """
        Counts the number of instances of a value in the list
        """
        # traverses the list to find if there is a matching element
        def find_value(previous=self.head, count=0):
            if previous.next.value == value:
                count += 1
            if previous.next != self.tail:
                previous = previous.next
                return find_value(previous, count)
            return count

        count = find_value()
        return count

    def slice(self, start_index: int, size: int) -> object:
        """
        Creates a new LinkedList that contains the elements between the start_index and size
        """
        # helper function sets current index and current node values
        # then recursively searches for the node at the given index position
        # adds found node to the new list, then continues size times
        def slice_helper(target_index=start_index, curr_index=0, size=size, current=self.head.next):
            if target_index == curr_index:
                new_list.add_back(current.value)
                size -= 1
                target_index += 1
            if size == 0:
                return
            current = current.next
            curr_index += 1
            return slice_helper(target_index, curr_index, size, current)

        # checks for valid parameters
        if (start_index + size) > self.length() \
                or start_index < 0 \
                or size < 0:
            raise SLLException
        # creates a new list, and then adds elements to the new list
        new_list = LinkedList()
        if size > 0:
            slice_helper()
        return new_list


if __name__ == '__main__':
    print('\n add_front example 1')
    list = LinkedList()
    print(list)
    list.add_front('A')
    list.add_front('B')
    list.add_front('C')
    print(list)

    print('\n add_back example 1')
    list = LinkedList()
    print(list)
    list.add_back('C')
    list.add_back('B')
    list.add_back('A')
    print(list)

    print('\n insert_at_index example 1')
    list = LinkedList()
    test_cases = [(0, 'A'), (0, 'B'), (1, 'C'), (3, 'D'), (-1, 'E'), (5, 'F'), (4, 'G')]
    for index, value in test_cases:
        print('Insert of', value, 'at', index, ': ', end='')
        try:
            list.insert_at_index(index, value)
            print(list)
        except Exception as e:
            print(type(e))

    print('\n remove_front example 1')
    list = LinkedList([1, 2])
    print(list)
    for i in range(3):
        try:
            list.remove_front()
            print('Successful removal', list)
        except Exception as e:
            print(type(e))

    print('\n remove_back example 1')
    list = LinkedList()
    try:
        list.remove_back()
    except Exception as e:
        print(type(e))
    list.add_front('Z')
    list.remove_back()
    print(list)
    list.add_front('Y')
    list.add_back('Z')
    list.add_front('X')
    print(list)
    list.remove_back()
    print(list)

    print('\n remove_at_index example 1')
    list = LinkedList([1, 2, 3, 4, 5, 6])
    print(list)
    for index in [0, 0, 0, 2, 2, -2]:
        print('Removed at index:', index, ': ', end='')
        try:
            list.remove_at_index(index)
            print(list)
        except Exception as e:
            print(type(e))
    print(list)

    print('\n get_front example 1')
    list = LinkedList(['A', 'B'])
    print(list.get_front())
    print(list.get_front())
    list.remove_front()
    print(list.get_front())
    list.remove_back()
    try:
        print(list.get_front())
    except Exception as e:
        print(type(e))

    print('\n get_back example 1')
    list = LinkedList([1, 2, 3])
    list.add_back(4)
    print(list.get_back())
    list.remove_back()
    print(list)
    print(list.get_back())

    print('\n remove example 1')
    list = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(list)
    for value in [7, 3, 3, 3, 3]:
        print(list.remove(value), list.length(), list)

    print('\n count example 1')
    list = LinkedList([1, 2, 3, 1, 2, 2])
    print(list, list.count(1), list.count(2), list.count(3), list.count(4))

    print('\n slice example 1')
    list = LinkedList([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ll_slice = list.slice(1, 3)
    print(list, ll_slice, sep="\n")
    ll_slice.remove_at_index(0)
    print(list, ll_slice, sep="\n")

    print('\n slice example 2')
    list = LinkedList([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", list)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1)]
    for index, size in slices:
        print("Slice", index, "/", size, end="")
        try:
            print(" --- OK: ", list.slice(index, size))
        except:
            print(" --- exception occurred.")

    print('\n slice example 3')
    list = LinkedList([-44833, -72604, 71651, 54351, 36147, -82785, 70524, -2173, -81096, 71506])
    print("SOURCE:", list)
    slices = [(2, -1), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (0, 0)]
    for index, size in slices:
        print("Slice", index, "/", size, end="")
        try:
            print(" --- OK: ", list.slice(index, size))
        except:
            print(" --- exception occurred.")
