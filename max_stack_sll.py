# Course: CS261 - Data Structures
# Student Name: Jeremy Vernon
# Assignment: 3
# Description: Max Stack


from sll import *

class SimpleLinkedListIterator:
    # init function
    def __init__(self, head):
        self.head = head
        self.current = head

    # iter function
    def __iter__(self):
        return self

    # advances iterator
    def __next__(self):
        if self.current.next is None:
            raise StopIteration
        cur = self.current
        self.current = self.current.next
        return cur

class StackException(Exception):
    """
    Custom exception to be used by MaxStack Class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MaxStack:
    def __init__(self):
        """
        Init new MaxStack based on Singly Linked Lists
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.sll_val = LinkedList()
        self.sll_max = LinkedList()

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "MAX STACK: " + str(self.sll_val.length()) + " elements. "
        out += str(self.sll_val)
        return out

    def is_empty(self) -> bool:
        """
        Return True is Maxstack is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.sll_val.is_empty()

    def size(self) -> int:
        """
        Return number of elements currently in the MaxStack
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.sll_val.length()

    # ------------------------------------------------------------------ #

    def push(self, value: object) -> None:
        """
        Adds value to the top of the stack
        """
        self.sll_val.add_front(value)

    def pop(self) -> object:
        """
        Pops the element at the top of the stack and returns that element
        """
        # checks if stack is empty
        if self.is_empty():
            raise StackException
        # removes top element and returns the value of that element
        popped = self.sll_val.head.next.value
        self.sll_val.remove_front()
        return popped

    def top(self) -> object:
        """
        Gets the value at the top of the stack
        """
        # checks if stack is empty
        if self.is_empty():
            raise StackException
        # returns the value of the top element
        return self.sll_val.head.next.value

    def get_max(self) -> object:
        """
        Gets max element
        TODO: refactor formula to search all elements in O(1)
        """
        # checks if stack is empty
        if self.is_empty():
            raise StackException
        # iterates to find the max
        maximum = self.sll_val.head.next
        for i in SimpleLinkedListIterator(self.sll_val.head.next):
            if i.value > maximum.value:
                maximum = i
        return maximum.value

        # # checks if stack is empty
        # if self.is_empty():
        #     raise StackException
        # # checks if there is only one element in the stack
        # if self.size() > 1:
        #     # compares new top of stack with last element
        #     second_to_top = self.sll_val.head.next.next.value
        #     if self.top() > second_to_top:
        #         return self.top()
        #     return second_to_top
        # return self.top()


# BASIC TESTING
if __name__ == "__main__":

     print('\n push example 1')
     s = MaxStack()
     print(s)
     for value in [1, 2, 3, 4, 5]:
         s.push(value)
     print(s)
    
    
     print('\n pop example 1')
     s = MaxStack()
     try:
         print(s.pop())
     except Exception as e:
         print("Exception:", type(e))
     for value in [1, 2, 3, 4, 5]:
         s.push(value)
     for i in range(6):
         try:
             print(s.pop())
         except Exception as e:
             print("Exception:", type(e))
    
    
     print('\n top example 1')
     s = MaxStack()
     try:
         s.top()
     except Exception as e:
         print("No elements in stack", type(e))
     s.push(10)
     s.push(20)
     print(s)
     print(s.top())
     print(s.top())
     print(s)
    
     print('\n get_max example 1')
     s = MaxStack()
     for value in [1, -20, 15, 21, 21, 40, 50]:
         print(s, ' ', end='')
         try:
             print(s.get_max())
         except Exception as e:
             print(type(e))
         s.push(value)
     while not s.is_empty():
         print(s.size(), end='')
         print(' Pop value:', s.pop(), ' get_max after: ', end='')
         try:
             print(s.get_max())
         except Exception as e:
             print(type(e))

