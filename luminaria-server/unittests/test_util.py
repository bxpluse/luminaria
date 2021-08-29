import unittest

from common.util import type_transform, parse_word, gen_id, extract_domain


class TestStringMethods(unittest.TestCase):

    def test_parse_word(self):
        self.assertEqual(parse_word('test.'), 'test')
        self.assertEqual(parse_word('test!'), 'test')
        self.assertEqual(parse_word('test?'), 'test')
        self.assertEqual(parse_word('!?<>test:[]'), 'test')

    def test_gen_id(self):
        self.assertEqual(len(gen_id()), 8)
        self.assertEqual(len(gen_id(length=4)), 4)
        self.assertEqual(len(gen_id(length=12)), 12)

    def test_extract_domain(self):
        self.assertEqual(extract_domain('test.com'), 'test')
        self.assertEqual(extract_domain('www.test.com'), 'test')
        self.assertEqual(extract_domain('https://www.test.com'), 'test')
        self.assertEqual(extract_domain('https://www.test.com/'), 'test')
        self.assertEqual(extract_domain('https://www.test.com/a/b'), 'test')

    def test_type_transform(self):
        self.assertEqual(type_transform('1', 'int'), 1)
        self.assertEqual(type_transform('-1', 'int'), -1)

        self.assertEqual(type_transform('1.123456', 'float'), 1.123456)
        self.assertEqual(type_transform('-1.123456', 'float'), -1.123456)

        self.assertTrue(type_transform('True', 'bool'))
        self.assertTrue(type_transform('true', 'bool'))
        self.assertTrue(type_transform('1', 'bool'))
        self.assertTrue(type_transform('TrUe', 'bool'))

        self.assertFalse(type_transform('False', 'bool'))
        self.assertFalse(type_transform('false', 'bool'))
        self.assertFalse(type_transform('fAlSe', 'bool'))
        self.assertFalse(type_transform('0', 'bool'))
        self.assertFalse(type_transform('any other string', 'bool'))

        self.assertEqual(type_transform("[1, 3.14, None, 'test']", 'list'), [1, 3.14, None, 'test'])

        self.assertEqual(type_transform('test', None), 'test')
        self.assertEqual(type_transform('test', 'str'), 'test')
        self.assertEqual(type_transform('test', 'any other string'), 'test')


if __name__ == '__main__':
    unittest.main()
