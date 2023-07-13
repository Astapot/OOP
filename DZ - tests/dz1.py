from old_dz import find_russia
from old_dz import find_unique_id
from old_dz import find_max_stats
from unittest import TestCase
import pytest

class TestDZ(TestCase):
    def test_find_russia1(self):
        geo_logs = [
            {'v1': ['Балалайка', 'Россия']},
            {'v2': ['Маугли', 'Индия']},
            {'v3': ['Россия', 'Иваново']},
            {'v4': ['Караганда', 'Караганда']},
            {'v5': ['Рим', 'Рим']},
            {'v6': ['Лиссабон', 'Португалия']},
            {'v7': ['Бульбатрульба', 'Трульбабульба']},
            {'v8': ['Вашингтон', 'Америка']},
            {'v9': ['Нью-Йорк', 'Россия']},
            {'v10': ['Воронеж', 'Россия']}
        ]
        expected_res = [
            {'v1': ['Балалайка', 'Россия']},
            {'v3': ['Россия', 'Иваново']},
            {'v9': ['Нью-Йорк', 'Россия']},
            {'v10': ['Воронеж', 'Россия']}
        ]
        res = find_russia(geo_logs)
        self.assertEqual(expected_res, res, 'Wrong Function')

    def test_find_ids1(self):
        ids = {'user1': [111, 123, 321, 1, 11],
               'user2': [11, 11, 111, 111, 1111],
               'user3': [1, 1, 1, 1]}
        expected_res = [1, 11, 111, 123, 321, 1111]
        res = find_unique_id(ids)
        self.assertCountEqual(expected_res, res, 'Wrong Function')


@pytest.mark.parametrize(
    'stats, expected', [
        ({'facebook': 55, 'yandex': 120, 'vk': 115, 'google': 99, 'email': 42, 'ok': 98}, 'yandex'),
        ({'cs': 99, 'dota': 110, 'pubg': 15, 'hmm': 399, 'RE4': 100, 'chess': 1}, 'hmm'),
        ({'a': 1, 'b': 2, 'c': 3, 'e': 5, 'g': 7, 'd': 4}, 'g')
    ]
)
def test_with_params(stats, expected):
    result = find_max_stats(stats)
    assert result == expected
