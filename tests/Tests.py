import sys
import os
import unittest
import requests

# https://www.delftstack.com/howto/python/python-import-from-parent-directory/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from URLListReader import URLListReader


class Tests(unittest.TestCase):
    def testWorkingSite(self) -> None:
        expected = 200
        actual = requests.get("https://www.google.com").status_code
        self.assertEqual(expected, actual)

    def testCatchAll(self) -> None:
        with self.assertRaises(requests.exceptions.RequestException) as cm:
            requests.get("https://www.fakewebsite.xyz", timeout=3)
        ex = cm.exception

    def testConfigBadSchema(self) -> None:
        with self.assertRaises(Exception) as cm:
            cr: URLListReader = URLListReader()
            cr.load("config-test-bad-schema.json")
        ex = cm.exception
        self.assertEqual(ex.args[0], "CONFIG FILE ERROR: INVALID SCHEMA\n")

    def testConfigBadUrl(self) -> None:
        with self.assertRaises(Exception) as cm:
            cr: URLListReader = URLListReader()
            cr.load("config-test-bad-url.json")
        ex = cm.exception
        self.assertEqual(ex.args[0], "CONFIG FILE ERROR: INVALID URL\n")


if __name__ == "__main__":
    unittest.main()
