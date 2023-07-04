# Задание 1

import types

class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list

    def __iter__(self):
        self.cursor = 0
        self.help_cursor = -1
        self.result = []
        return self

    def __next__(self):
        if self.cursor == len(self.list_of_list):
            raise StopIteration
        el = self.list_of_list[self.cursor]
        self.help_cursor += 1
        if self.help_cursor != len(el):
            return el[self.help_cursor]
        self.cursor += 1
        self.help_cursor = 0
        if self.cursor == len(self.list_of_list):
            raise StopIteration
        return self.list_of_list[self.cursor][self.help_cursor]



def test_1():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


# задание 2


def flat_generator(list_of_lists):
    i = 0
    while i < len(list_of_lists):
        for letter in list_of_lists[i]:
            yield letter
        i += 1

def test_2():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


if __name__ == '__main__':
    test_1()
    test_2()

