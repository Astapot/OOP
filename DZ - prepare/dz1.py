from unittest import TestCase

# Задание 1

class Stack():
    def __init__(self, empty_list):
        self.list = empty_list

    def is_empty(self):
        if len(self.list) == 0:
            return True
        return False

    def push(self, el):
        self.list.append(el)

    def pop(self):
        return self.list.pop()

    def peek(self):
        return self.list[-1]

    def size(self):
        return len(self.list)

    # Задание 2

    def check_balance(self, test):
        open_array = ['(', '[', '{']
        check_close_dict = {'(': ')', '[': ']', '{': '}'}
        for bracket in test:
            if not self.is_empty():
                if bracket == check_close_dict[self.peek()]:
                    self.pop()
                    continue
            if bracket in open_array:
                self.push(bracket)
                continue
            return 'Несбалансированно'
        if self.is_empty():
            return 'Сбалансированно'
        return 'Несбалансированно'


class TestBrackets(TestCase):
    def test_brackets(self):
        brackets = '('
        expected_res = 'Несбалансированно'
        res = first.check_balance(brackets)
        self.assertEqual(expected_res, res, 'Неправильное дз')


first = Stack([])
# print(first)
print(first.check_balance('(((([{}]))))'))
print(first.check_balance('[([])((([[[]]])))]{()}'))
print(first.check_balance('{{[()]}}'))
print(first.check_balance('}{}'))
print(first.check_balance('{{[(])]}}'))
print(first.check_balance('[[{())}]'))