import os
import unittest
import logging

import chuchu.vasp

logging.basicConfig(level=logging.DEBUG)


class TestIncar(unittest.TestCase):

    """Test case docstring."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_name(self):
        self.assertTrue(True)

    def test_simple_poscar(self):
        incar = chuchu.vasp.Incar()
        self.assertTrue(incar)
        file_name = os.path.dirname(__file__)+"/data/INCAR.example"
        self.assertTrue(os.path.exists(file_name))
        incar.load(file_name)

        contents = incar.dump()
        self.assertTrue(contents)
        fd = open("test_data.incar", "w+")
        incar.dump(fd=fd, fmt="vasp")
        self.assertTrue(os.path.exists("test_data.incar"))


# vim: cc=80
