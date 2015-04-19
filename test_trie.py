import unittest
from unittest import TestCase
from Trie import Trie

__author__ = 'arubtsov'


class TestTrie(TestCase):

    def setUp(self):
        self.t = Trie()
        self.t.add_word('aaa', 1)
        self.t.add_word('asa', 2)
        self.t.add_word('sss', 3)

    def test_add_word(self):
        correct_dict = {'a': {'a': {'a': {'_end_': 1}}, 's': {'a': {'_end_': 2}}},
                        's': {'s': {'s': {'_end_': 3}}}}
        self.assertEquals(self.t.root, correct_dict)

    def test_get_word(self):
        self.assertFalse(self.t.get_word('a'))
        self.assertEqual(self.t.get_word('s'), 'sss')
        self.assertEqual(self.t.get_word('as'), 'asa')
        self.assertEqual(self.t.get_word('asa'), 'asa')

    def test_get_variants(self):
        self.assertEqual(self.t.get_variants('a'), ['aaa', 'asa'])
        self.assertEqual(self.t.get_variants('aaa'), ['aaa'])
        self.assertEqual(self.t.get_variants('aa'), ['aaa'])

    def test_get_content(self):
        self.assertEqual(self.t.get_content('aaa'), 1)
        self.assertEqual(self.t.get_content('asa'), 2)
        self.assertEqual(self.t.get_content('sss'), 3)
        self.assertFalse(self.t.get_content('worng'))

if __name__ == '__main__':
    unittest.main()