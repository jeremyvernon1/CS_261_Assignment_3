# Course: CS261 - Data Structures
# Student Name: Jeremy Vernon
# Assignment: 3
# Description: Circular Doubly Linked Lists


class SimpleLinkedListIterator:
    def __init__(self, sentinel):
        self.sentinel = sentinel
        self.current = sentinel.next

    def __iter__(self):
        return self

    def __next__(self):
        cur = self.current
        if cur is self.sentinel:
            raise StopIteration
        self.current = self.current.next
        return cur

class CDLLException(Exception):
    """
    Custom exception class to be used by Circular Doubly Linked List
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DLNode:
    """
    Doubly Linked List Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        self.next = None
        self.prev = None
        self.value = value


class CircularList:
    def __init__(self, start_list=None):
        """
        Initializes a new linked list with sentinel
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.sentinel = DLNode(None)
        self.sentinel.next = self.sentinel
        self.sentinel.prev = self.sentinel

        # populate CDLL with initial values (if provided)
        # before using this feature, implement add_back() method
        if start_list is not None:
            for value in start_list:
                self.add_back(value)

    def __str__(self) -> str:
        """
        Return content of singly linked list in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'CDLL ['
        if self.sentinel.next != self.sentinel:
            cur = self.sentinel.next.next
            out = out + str(self.sentinel.next.value)
            while cur != self.sentinel:
                out = out + ' <-> ' + str(cur.value)
                cur = cur.next
        out = out + ']'
        return out

    def length(self) -> int:
        """
        Return the length of the linked list

        This can also be used as troubleshooting method. This method works
        by independently measuring length during forward and backward
        traverse of the list and return the length if results agree or error
        code of -1 or -2 if thr measurements are different.

        Return values:
        >= 0 - length of the list
        -1 - list likely has an infinite loop (forward or backward)
        -2 - list has some other kind of problem

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """

        # length of the list measured traversing forward
        count_forward = 0
        cur = self.sentinel.next
        while cur != self.sentinel and count_forward < 101_000:
            count_forward += 1
            cur = cur.next

        # length of the list measured traversing backwards
        count_backward = 0
        cur = self.sentinel.prev
        while cur != self.sentinel and count_backward < 101_000:
            count_backward += 1
            cur = cur.prev

        # if any of the result is > 100,000 -> list has a loop
        if count_forward > 100_000 or count_backward > 100_000:
            return -1

        # if counters have different values -> there is some other problem
        return count_forward if count_forward == count_backward else -2

    def is_empty(self) -> bool:
        """
        Return True is list is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.sentinel.next == self.sentinel

    # ------------------------------------------------------------------ #

    def add_front(self, value: object) -> None:
        """
        Adds element to the front after the sentinel
        """
        new_element = DLNode(value)
        prev_first = self.sentinel.next
        new_element.next = prev_first
        new_element.prev = prev_first.prev
        prev_first.prev = new_element
        self.sentinel.next = new_element

    def add_back(self, value: object) -> None:
        """
        Adds element to the back "before" the sentinel
        """
        new_element = DLNode(value)
        prev_last = self.sentinel.prev
        self.sentinel.prev = new_element
        prev_last.next = new_element
        new_element.prev = prev_last
        new_element.next = self.sentinel

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Inserts element at the given index
        """
        # checks for valid index
        if index < 0 or index > self.length():
            raise CDLLException
        # inserts new element at index
        # beginning of linked list
        elif self.length() == 0 or index == 0:
            self.add_front(value)
        # end of linked list
        elif index == self.length():
            self.add_back(value)
        # middle of linked list
        else:
            iteration = 0
            for i in SimpleLinkedListIterator(self.sentinel):
                if iteration == index:
                    insert_before = i
                    insert_after = i.prev
                    new_element = DLNode(value)
                    insert_after.next = new_element
                    insert_before.prev = new_element
                    new_element.prev = insert_after
                    new_element.next = insert_before
                    return
                iteration += 1

    def remove_front(self) -> None:
        """
        Removes first element
        """
        if self.length() < 1:
            raise CDLLException
        else:
            new_front = self.sentinel.next.next
            # cleans up connections
            old_front = self.sentinel.next
            old_front.prev = None
            old_front.next = None
            # establishes new connections
            self.sentinel.next = new_front
            new_front.prev = self.sentinel

    def remove_back(self) -> None:
        """
        Removes last element
        """
        if self.length() < 1:
            raise CDLLException
        else:
            new_last = self.sentinel.prev.prev
            # cleans up connections
            prev_last = self.sentinel.prev
            prev_last.prev = None
            prev_last.next = None
            # establishes new connections
            self.sentinel.prev = new_last
            new_last.next = self.sentinel

    def remove_at_index(self, index: int) -> None:
        """
        Removes element at the given index position
        """
        # checks for valid index
        if index < 0 or index > (self.length() - 1):
            raise CDLLException
        # removes element at index
        elif index == 0:
            self.remove_front()
        elif index == (self.length() - 1):
            self.remove_back()
        else:
            iteration = 0
            for i in SimpleLinkedListIterator(self.sentinel):
                if iteration == index:
                    remove_after = i.prev
                    remove_before = i.next
                    # establishes new connections
                    remove_after.next = remove_before
                    remove_before.prev = remove_after
                iteration += 1

    def get_front(self) -> object:
        """
        Gets the front element
        """
        if self.length() < 1:
            raise CDLLException
        else:
            return self.sentinel.next.value

    def get_back(self) -> object:
        """
        Gets the last element
        """
        if self.length() < 1:
            raise CDLLException
        else:
            return self.sentinel.prev.value

    def remove(self, value: object) -> bool:
        """
        Traverses the list to find the matching value,
        if found, removes that element
        """
        for i in SimpleLinkedListIterator(self.sentinel):
            if i.value == value:
                remove_element = i
                remove_after = i.prev
                remove_before = i.next
                # cleans up connections
                remove_element.next = None
                remove_element.prev = None
                # establishes new connections
                remove_after.next = remove_before
                remove_before.prev = remove_after
                return True
        return False

    def count(self, value: object) -> int:
        """
        Counts the number of elements that match the given value
        """
        value_count = 0
        for i in SimpleLinkedListIterator(self.sentinel):
            if i.value == value:
                value_count += 1
        return value_count

    def swap_pairs(self, index1: int, index2: int) -> None:
        """
        Swaps two noedes given their indices.
        """
        # checks for valid index posistions
        length = (self.length() - 1)
        if \
            index1 < 0 or\
            index1 > length or\
            index2 < 0 or\
            index2 > length:
            raise CDLLException
        # if both index1 and index 2 are the same
        if index1 == index2:
            return
        # finds elements at the given index positions
        index_pos = -1
        swap1 = None
        swap2 = None
        for i in SimpleLinkedListIterator(self.sentinel):
            index_pos += 1
            if index_pos == index1:
                swap1 = i
            elif index_pos == index2:
                swap2 = i
            if swap1 and swap2:
                break

        # if index2 is one more than index1
        if index2 == (index1 + 1):
            swap1.prev.next = swap2
            swap2.next.prev = swap1
            swap1.next = swap2.next
            swap2.next = swap1
            swap2.prev = swap1.prev
            swap1.prev = swap2
        # if index1 is one more than index2
        elif index1 == (index2 + 1):
            swap2.prev.next = swap1
            swap1.next.prev = swap2
            swap2.next = swap1.next
            swap1.next = swap2
            swap1.prev = swap2.prev
            swap2.prev = swap1
        else:
            # saves prev and next before changing
            swap1_prev = swap1.prev
            swap1_next = swap1.next
            swap2_prev = swap2.prev
            swap2_next = swap2.next
            # move second element to the prev pos of first element
            swap2.prev = swap1_prev
            swap1.prev.next = swap2
            swap2.next = swap1_next
            swap1.next.prev = swap2
            # move first element to the prev pos of the second element
            swap1.prev = swap2_prev
            swap2_prev.next = swap1
            swap1.next = swap2_next
            swap2_next.prev = swap1

    def reverse(self) -> None:
        """
        Reverses a doubly linked list
        """
        # initialize
        curr = self.sentinel.prev
        first_element = self.sentinel.next
        last_element = self.sentinel.prev

        # reverse iterates through the list swapping, prev and next values
        while curr is not self.sentinel:
            prev = curr.prev
            curr.prev = curr.next
            curr.next = prev
            curr = curr.next

        # reverses prev and next values for the sentinel
        self.sentinel.next = last_element
        self.sentinel.prev = first_element

    def sort(self) -> None:
        """
        Sorts CDLL using bubble sort
        """
        # initializes loop
        compare_a = self.sentinel.next
        while True:
            compare_b = compare_a.next
            while compare_b is not self.sentinel:
                # checks if nodes should be swapped
                if compare_a.value > compare_b.value:

                    # bookmarks the pos
                    compare_a_resume = compare_b

                    # swaps the nodes
                    # if nodes are adjacent
                    if compare_b.prev == compare_a:
                        compare_a.prev.next = compare_b
                        compare_b.next.prev = compare_a
                        compare_a.next = compare_b.next
                        compare_b.next = compare_a
                        compare_b.prev = compare_a.prev
                        compare_a.prev = compare_b
                    # if nodes are not adjacent
                    else:
                        # saves prev and next before changing
                        compare_a_prev = compare_a.prev
                        compare_a_next = compare_a.next
                        compare_b_prev = compare_b.prev
                        compare_b_next = compare_b.next
                        # move second element to the prev pos of first element
                        compare_b.prev = compare_a_prev
                        compare_a.prev.next = compare_b
                        compare_b.next = compare_a_next
                        compare_a.next.prev = compare_b
                        # move first element to the prev pos of the second element
                        compare_a.prev = compare_b_prev
                        compare_b_prev.next = compare_a
                        compare_a.next = compare_b_next
                        compare_b_next.prev = compare_a

                    # resumes search from bookmarked pos
                    compare_a = compare_a_resume
                # advances compare_b
                compare_b = compare_b.next
            # advances compare_a
            compare_a = compare_a.next

            # provides end condition
            if compare_a is self.sentinel:
                break

    def rotate(self, steps: int) -> None:
        """
        TODO: Write this implementation
        """
        pass
        # curr = self.sentinel
        # for i in SimpleLinkedListIterator(self.sentinel):
        #     curr.next = curr.prev
        #     curr.prev = curr.prev.prev
        #     curr = curr.next

    def remove_duplicates(self) -> None:
        """
        TODO: Write this implementation
        """
        pass

    def odd_even(self) -> None:
        """
        TODO: Write this implementation
        """
        pass

    def add_integer(self, num: int) -> None:
        """
        TODO: Write this implementation
        """
        pass

if __name__ == '__main__':

    print('\n# add_front example 1')
    lst = CircularList()
    print(lst)
    lst.add_front('A')
    lst.add_front('B')
    lst.add_front('C')
    print(lst)

    print('\n# add_back example 1')
    lst = CircularList()
    print(lst)
    lst.add_back('C')
    lst.add_back('B')
    lst.add_back('A')
    print(lst)

    print('\n# insert_at_index example 1')
    lst = CircularList()
    test_cases = [(0, 'A'), (0, 'B'), (1, 'C'), (3, 'D'), (-1, 'E'), (5, 'F')]
    for index, value in test_cases:
        print('Insert of', value, 'at', index, ': ', end='')
        try:
            lst.insert_at_index(index, value)
            print(lst)
        except Exception as e:
            print(type(e))

    print('\n# remove_front example 1')
    lst = CircularList([1, 2])
    print(lst)
    for i in range(3):
        try:
            lst.remove_front()
            print('Successful removal', lst)
        except Exception as e:
            print(type(e))

    print('\n# remove_back example 1')
    lst = CircularList()
    try:
        lst.remove_back()
    except Exception as e:
        print(type(e))
    lst.add_front('Z')
    lst.remove_back()
    print(lst)
    lst.add_front('Y')
    lst.add_back('Z')
    lst.add_front('X')
    print(lst)
    lst.remove_back()
    print(lst)

    print('\n# remove_at_index example 1')
    lst = CircularList([1, 2, 3, 4, 5, 6])
    print(lst)
    for index in [0, 0, 0, 2, 2, -2]:
        print('Removed at index:', index, ': ', end='')
        try:
            lst.remove_at_index(index)
            print(lst)
        except Exception as e:
            print(type(e))
    print(lst)

    print('\n# remove_at_index example 2')
    lst = CircularList([-32343, 64131, -54873, -77700])
    print(lst)
    try:
        lst.remove_at_index(2)
        print(lst)
    except Exception as e:
        print(type(e))

    print('\n# get_front example 1')
    lst = CircularList(['A', 'B'])
    print(lst.get_front())
    print(lst.get_front())
    lst.remove_front()
    print(lst.get_front())
    lst.remove_back()
    try:
        print(lst.get_front())
    except Exception as e:
        print(type(e))

    print('\n# get_back example 1')
    lst = CircularList([1, 2, 3])
    lst.add_back(4)
    print(lst.get_back())
    lst.remove_back()
    print(lst)
    print(lst.get_back())

    print('\n# remove example 1')
    lst = CircularList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(lst)
    for value in [7, 3, 3, 3, 3]:
        print(lst.remove(value), lst.length(), lst)

    print('\n# count example 1')
    lst = CircularList([1, 2, 3, 1, 2, 2])
    print(lst, lst.count(1), lst.count(2), lst.count(3), lst.count(4))

    print('\n# swap_pairs example 1')
    lst = CircularList([0, 1, 2, 3, 4, 5, 6])
    test_cases = ((0, 6), (0, 7), (-1, 6), (1, 5)
                   ,(4, 2), (3, 3), (1, 2), (2, 1))

    for i, j in test_cases:
        print('Swap nodes ', i, j, ' ', end='')
        try:
            lst.swap_pairs(i, j)
            print(lst)
        except Exception as e:
            print(type(e))

    print('\n# reverse example 1')
    test_cases = (
        [1, 2, 3, 3, 4, 5],
        [1, 2, 3, 4, 5],
        ['A', 'B', 'C', 'D']
    )
    for case in test_cases:
        lst = CircularList(case)
        lst.reverse()
        print(lst)

    print('\n# reverse example 2')
    lst = CircularList()
    print(lst)
    lst.reverse()
    print(lst)
    lst.add_back(2)
    lst.add_back(3)
    lst.add_front(1)
    lst.reverse()
    print(lst)

    print('\n# reverse example 3')


    class Student:
        def __init__(self, name, age):
            self.name, self.age = name, age

        def __eq__(self, other):
            return self.age == other.age

        def __str__(self):
            return str(self.name) + ' ' + str(self.age)


    s1, s2 = Student('John', 20), Student('Andy', 20)
    lst = CircularList([s1, s2])
    print(lst)
    lst.reverse()
    print(lst)
    print(s1 == s2)

    print('\n# reverse example 4')
    lst = CircularList([1, 'A'])
    lst.reverse()
    print(lst)

    print('\n# sort example 1')
    test_cases = (
        [1, 10, 2, 20, 3, 30, 4, 40, 5],
        ['zebra2', 'apple', 'tomato', 'apple', 'zebra1'],
        [(1, 1), (20, 1), (1, 20), (2, 20)]
    )
    for case in test_cases:
        lst = CircularList(case)
        print(lst)
        lst.sort()
        print(lst)

    print('\n# rotate example 1')
    source = [_ for _ in range(-20, 20, 7)]
    for steps in [1, 2, 0, -1, -2, 28, -100]:
        lst = CircularList(source)
        lst.rotate(steps)
        print(lst, steps)

    print('\n# rotate example 2')
    lst = CircularList([10, 20, 30, 40])
    for j in range(-1, 2, 2):
        for _ in range(3):
            lst.rotate(j)
            print(lst)

    print('\n# rotate example 3')
    lst = CircularList()
    lst.rotate(10)
    print(lst)

    print('\n# remove_duplicates example 1')
    test_cases = (
        [1, 2, 3, 4, 5], [1, 1, 1, 1, 1],
        [], [1], [1, 1], [1, 1, 1, 2, 2, 2],
        [0, 1, 1, 2, 3, 3, 4, 5, 5, 6],
        list("abccd"),
        list("005BCDDEEFI")
    )

    for case in test_cases:
        lst = CircularList(case)
        print('INPUT :', lst)
        lst.remove_duplicates()
        print('OUTPUT:', lst)

    print('\n# odd_even example 1')
    test_cases = (
        [1, 2, 3, 4, 5], list('ABCDE'),
        [], [100], [100, 200], [100, 200, 300],
        [100, 200, 300, 400],
        [10, 'A', 20, 'B', 30, 'C', 40, 'D', 50, 'E']
    )

    for case in test_cases:
        lst = CircularList(case)
        print('INPUT :', lst)
        lst.odd_even()
        print('OUTPUT:', lst)

    print('\n# add_integer example 1')
    test_cases = (
      ([1, 2, 3], 10456),
      ([], 25),
      ([2, 0, 9, 0, 7], 108),
       ([9, 9, 9], 9_999_999),
    )
    for list_content, integer in test_cases:
       lst = CircularList(list_content)
    print('INPUT :', lst, 'INTEGER', integer)
    lst.add_integer(integer)
    print('OUTPUT:', lst)
