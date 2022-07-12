import unittest
from cgi import test

import toml
from uidom import __version__


class TestVersion(unittest.TestCase):
    
    def setUp(self) -> None:
        self.version = toml.load("pyproject.toml")['tool']['poetry']['version']

    def test_version(self):
        self.assertEqual(__version__, self.version)

if __name__ == '__main__':
    unittest.main()
