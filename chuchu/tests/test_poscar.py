import os
import sys
import unittest
import logging

import chuchu.vasp

logging.basicConfig(level = logging.DEBUG)


class TestPoscar(unittest.TestCase):

    """Test case docstring."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_name(self):
        self.assertTrue(True)
    def test_simple_poscar(self):
        poscar = chuchu.vasp.Poscar()
        self.assertTrue(poscar)
        file_name = os.path.dirname(__file__)+"/data/poscar_diamond_8_cubic"
        self.assertTrue(os.path.exists(file_name))
        poscar.load(file_name)
        for i in range(1,7):
            self.assertTrue(poscar.getAtomSymbol(i) == "C")
        self.assertTrue(poscar.getAtomSymbol(7) == "N")
        self.assertTrue(len(poscar.getAtomSymbols()) == 2)
        self.assertTrue(len(poscar.atoms) == 7)
        self.assertFalse(poscar.isCartesian())
        self.assertTrue(poscar.getNumberOfAtoms() == 7)
        contents = poscar.dump(fmt="asy")
        self.assertTrue(contents)
        fd = open("test_data.asy", "w+")
        poscar.dump(fd=fd, fmt="asy")
        self.assertTrue(os.path.exists("test_data.asy"))
        fd = open("test_data.vasp", "w+")
        poscar.dump(fd=fd, fmt="vasp")
        self.assertTrue(os.path.exists("test_data.vasp"))
        contents = poscar.dump()
        self.assertTrue(contents)



# vim: cc=80
