import unittest
import requests
from ConfigReader import ConfigReader


# placeholder
class Tests(unittest.TestCase):
    def testWorkingSite(self) -> None:
        expected = 200
        actual = requests.get("https://www.google.com").status_code
        self.assertEqual(expected, actual)

    def testCatchAll(self) -> None:
        with self.assertRaises(requests.exceptions.RequestException) as cm:
            requests.get("https://www.fakewebsite.xyz", timeout=3)
        ex = cm.exception

    def testConfigBadFile(self) -> None:
        with self.assertRaises(Exception) as cm:
            cr: ConfigReader = ConfigReader()
            cr.load("config-test-bad.json")
        ex = cm.exception
        self.assertEqual(ex.args[0], "CONFIG FILE ERROR: INVALID URL\n")


if __name__ == "__main__":
    unittest.main()
