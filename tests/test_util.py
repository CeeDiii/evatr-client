import unittest
from unittest.mock import patch
from urllib.parse import urlencode
from evatr_client.util import ResultType, get_error_description, get_result_description
from evatr_client.status_codes import status_codes

class TestClient(unittest.TestCase):

    def test_get_result_description_should_return_string(self):
        expected = ResultType.MATCH
        actual = 'A'
        self.assertEqual(get_result_description(expected), actual)

    def test_get_result_description_should_return_none(self):
        expected = 'E' # Value not in enum
        actual = None
        self.assertEqual(get_result_description(expected), actual)


    def test_get_error_description_should_return_string(self):
        expected = get_error_description(200)
        actual = status_codes['200']
        self.assertEqual(expected, actual)
        

    def test_get_error_description_should_return_string(self):
        expected = get_error_description(404) # Value currently not in status_codes
        actual = 'Beschreibung für diesen Code wurde nicht gefunden.'
        self.assertEqual(expected, actual)
