# -*- coding: utf-8 -*-
import sys
import re
import os
import numpy
import logging
import string

logger = logging.getLogger("vasp:poscar")


class Poscar(object):
    asy_template_path = os.path.dirname(__file__)+"/data/poscar-temp.asy"
    vasp_template_path = os.path.dirname(__file__)+"/data/poscar-temp.vasp"
    blender_template_path = os.path.dirname(__file__)\
        + "/data/poscar-temp.blender.py"

    def __init__(self):
        self.mode = False
        self.basis = []
        self.atoms = []
        self.logger = logging.getLogger("Poscar")
        self.comment = ""
        self.constant = 0
        self.atoms_header = []
        self.atoms_number_header = []

    def getAtomSymbol(self, atom_number):
        self.logger.debug("Getting {} atom symbol".format(atom_number))
        if atom_number == 0:
            self.logger.error("Atom_number must be a positive number")
            sys.exit(1)
        buffer = 0
        for j, atoms in enumerate(self.atoms_number_header):
            buffer += atoms
            if atom_number <= buffer:
                return self.atoms_header[j]

    def getCellVolume(self):
        main_volume = numpy.linalg.det(self.basis)
        if self.isCartesian():
            return main_volume*self.constant
        else:
            return main_volume

    def getAtomSymbols(self):
        return self.atoms_header

    def getScaledBasis(self):
        if self.isCartesian():
            return [[self.constant, 0, 0],
                    [0, self.constant, 0],
                    [0, 0, self.constant]]
        else:
            vec0 = [self.constant * x for x in [v for v in self.basis[0]]]
            vec1 = [self.constant * x for x in [v for v in self.basis[1]]]
            vec2 = [self.constant * x for x in [v for v in self.basis[2]]]
            return [vec0, vec1, vec2]

    def getCoordinates(self, atom_number):
        if atom_number > self.getNumberOfAtoms():
            raise Exception("There are only {} atoms, please choose a number between \
                    1 and {}".format(
                        self.getNumberOfAtoms(),
                        self.getNumberOfAtoms()
                        ))
            sys.exit(1)
        coords = self.atoms[atom_number-1]
        return coords

    def load(self, obj):
        self.logger.debug("Loading poscar from {}".format(obj))
        if hasattr(obj, "read"):
            f = obj
        elif type(obj) is str:
            f = open(obj, "r")
        for j, line in enumerate(f):
            line_number = j+1
            if re.match(r"^\s*$", line):
                continue
            if line_number == 1:
                self.logger.debug("comment = {}".format(line))
                self.comment = line
            elif line_number == 2:
                self.logger.debug("constant = {}".format(line))
                self.constant = float(line)
            elif 5 >= line_number >= 3:
                self.logger.debug("vector ({}) = {}".format(
                    line_number-2, line))
                self.basis.append([float(i)
                                  for i in re.sub(r"\s+", " ", line).split()])
            elif line_number == 6:
                self.atoms_header = re.sub(r"\s+", " ",  line).split()
            elif line_number == 7:
                self.atoms_number_header = [int(x) for x in re.sub(
                    r"\s+", " ",  line).split()]
            elif line_number == 8:
                self.mode = line
            elif self.getNumberOfAtoms()+9 >= line_number >= 9:
                self.atoms\
                    .append(
                            [float(i)
                                for i in re.sub(r"\s+", " ", line).split()]
                            )
            if line_number > self.getNumberOfAtoms()+9:
                break
        return self

    def getCartesian(self, atom_number):
        coords = self.getCoordinates(atom_number)
        basis = self.getScaledBasis()
        return [basis[0][i]*coords[0] +
                basis[1][i]*coords[1] +
                basis[2][i]*coords[2] for i in range(3)]

    def isCartesian(self):
        return self.mode[0] in "CcKk"

    def getNumberOfAtoms(self):
        return int(sum(self.atoms_number_header))

    def dump(self, fmt="vasp", fd=None):
        self.logger.debug("Dumping poscar in {} format".format(fmt))
        if fmt == "asy":
            content = self.dumpAsyAtoms()
        elif fmt == "vasp":
            content = self.dumpVasp()
        elif fmt == "blender":
            content = self.dumpBlender()
        else:
            self.logger.error("Format '{}' not recognised".format(fmt))
            sys.exit(1)
        if not fd:
            self.logger.debug("Returning output string")
            return content
        else:
            self.logger.debug("Writing output in {}".format(fd))
            fd.write(content)

    def dumpBlender(self):
        """TODO: Docstring for dumpBlender.
        :returns: TODO

        """
        pass

    def dumpVasp(self):
        """TODO: Docstring for dumpPoscar.
        :returns: TODO

        """
        templateString = open(self.vasp_template_path).read()
        template = string.Template(templateString)
        contents = template.substitute(
                comment=self.comment.strip("\n"),
                constant=self.constant,
                basis_1=str(self.basis[0]).strip("[]").replace(",", " "),
                basis_2=str(self.basis[1]).strip("[]").replace(",", " "),
                basis_3=str(self.basis[2]).strip("[]").replace(",", " "),
                atoms_header=" ".join(self.atoms_header),
                atoms_number_header=str(self.atoms_number_header)
                .strip("[]").replace(",", ""),
                mode=self.mode.replace("\n", ""),
                coordinates="\n".join(
                    [" ".join([str(c)
                     for c in vector]) for vector in self.atoms]
                    )
                )
        return contents

    def dumpAsyAtoms(
            self,
            max_length=2,
            min_length=0,
            bond_radius=5.9,
            radius_scale=1,
            asy_atom="atom.asy",
            camera=""
            ):
        """
        Print asy-atoms file
        """
        templateString = open(self.asy_template_path).read()
        template = string.Template(templateString)
        basis = self.getScaledBasis()
        atoms = []
        draw_atoms = []
        draw_bonds = []
        for i in range(1, self.getNumberOfAtoms()+1):
            symbol = self.getAtomSymbol(i)
            atom = self.getCoordinates(i)
            coords = str(atom).strip("[]")
            atoms.append(
                    "Atom {}{} = Atom(\"{}\", ({}), basis = basis);".format(
                        symbol, i, symbol, coords
                        )
                    )
        for symbol in self.getAtomSymbols():
            draw_atoms.append("""\
ALL_ATOMS.drawAtom(\"{}\", draw_label = false, radius_scale =\
radius_scale);\
""".format(symbol))
        for j, symbol in enumerate(self.getAtomSymbols()):
            for i, symbol2 in enumerate(self.getAtomSymbols()):
                if j < i:
                    continue
                else:
                    draw_bonds.append("""\
ALL_ATOMS.drawBond(\"{}\", \"{}\", bond_radius = bond_radius,\
max_dist = max_bond_dist);""".format(symbol, symbol2))
        content = template.substitute(
                    max_length=max_length,
                    min_length=min_length,
                    bond_radius=bond_radius,
                    radius_scale=radius_scale,
                    asy_atom=asy_atom,
                    camera=camera,
                    basis=re.sub(r"\]+", ")", re.sub(r"\[+", "(", str(basis))),
                    atoms="\n".join(atoms),
                    draw_bonds="\n".join(draw_bonds),
                    draw_atoms="\n".join(draw_atoms)
                    )
        return content
