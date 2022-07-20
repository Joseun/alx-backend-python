#!/usr/bin/env python3
""" Test module for utils module """
import unittest
from parameterized import parameterized
from typing import Mapping, Sequence
from unittest import mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """ Test class for access_nested_map method """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence,
                               expected):
        """ Test to access nested map"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping,
                                         path: Sequence):
        """ Test to access nested map with KeyError """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """ Test class for get_json method """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, url: str, payload: Mapping):
        """ Test to get json from requests """
        class Response(mock.Mock):
            """ Create a mock response for request with get_json method """

            def json(self):
                """ json method """
                return payload

        with mock.patch('requests.get') as mock_method:
            mock_method.return_value = Response()
            self.assertEqual(get_json(url), payload)
            mock_method.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    """ Test class for memoize method """
    def test_memoize(self):
        """ Test for memoize method """
        class TestClass():

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with mock.patch.object(TestClass, 'a_method',
                               return_value=42) as mock_method:
                test_object = TestClass()
                self.assertEqual(test_object.a_property, 42)
                self.assertEqual(test_object.a_property, 42)
                mock_method.assert_called_once()

if __name__ == '__main__':
    unittest.main()
