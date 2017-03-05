#!/usr/local/bin/python2.7
import bpy
import math

ALL_ATOMS = []


def makeMaterial(name, diffuse, specular=(1, 1, 1), alpha=1):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.diffuse_shader = "LAMBERT"
    mat.diffuse_intensity = 1.0
    mat.specular_color = specular
    mat.specular_shader = "COOKTORR"
    mat.specular_intensity = 0.5
    mat.alpha = alpha
    mat.ambient = 1
    return mat


class AtomInfo:
    def __init__(self, symbol, ionic_r, hex_color, atomic_number):
        self.symbol = symbol
        self.ionic_r = ionic_r
        self.hex_color = hex_color
        self.rgb_color = self.hex2rgb(hex_color)
        self.atomic_number = atomic_number
        self.mat = makeMaterial(symbol, self.rgb_color)

    def hex2rgb(self, hexstr):
        return (
                int(hexstr[0:4], 16)/255.0,
                int("0x"+hexstr[4:6], 16)/255.0,
                int("0x"+hexstr[6:8], 16)/255.0
                )


ATOMS_INFO = [
  AtomInfo("H", 0.53, "0xffffff", 1),
  AtomInfo("He", 0.31, "0xffc0cb", 2),
  AtomInfo("Li", 1.67, "0xb22121", 3),
  AtomInfo("Be", 1.12, "0xff1493", 4),
  AtomInfo("B", 0.87, "0x00ff00", 5),
  AtomInfo("C", 0.67, "0xeed5b7", 6),
  AtomInfo("N", 0.56, "0x87cee6", 7),
  AtomInfo("O", 0.48, "0xff0000", 8),
  AtomInfo("F", 0.42, "0xdaa520", 9),
  AtomInfo("Ne", 0.38, "0xff1493", 10),
  AtomInfo("Na", 1.90, "0x0000ff", 11),
  AtomInfo("Mg", 1.45, "0x228b22", 12),
  AtomInfo("Al", 1.18, "0x696969", 13),
  AtomInfo("Si", 1.11, "0xdaa520", 14),
  AtomInfo("P", 0.98, "0xffaa00", 15),
  AtomInfo("S", 0.88, "0xffff00", 16),
  AtomInfo("Cl", 0.79, "0x00ff00", 17),
  AtomInfo("Ar", 0.71, "0xff1493", 18),
  AtomInfo("K", 2.43, "0xff1493", 19),
  AtomInfo("Ca", 1.94, "0x696969", 20),
  AtomInfo("Sc", 1.84, "0xff1493", 21),
  AtomInfo("Ti", 1.76, "0x696969", 22),
  AtomInfo("V", 1.71, "0xff1493", 23),
  AtomInfo("Cr", 1.66, "0x696969", 24),
  AtomInfo("Mn", 1.61, "0x696969", 25),
  AtomInfo("Fe", 1.56, "0xffaa00", 26),
  AtomInfo("Co", 1.52, "0xff1493", 27),
  AtomInfo("Ni", 1.49, "0x802828", 28),
  AtomInfo("Cu", 1.45, "0x802828", 29),
  AtomInfo("Zn", 0.74, "0x802828", 30),
  AtomInfo("Ga", 1.36, "0xff1493", 31),
  AtomInfo("Ge", 1.25, "0xff1493", 32),
  AtomInfo("As", 1.14, "0xff1493", 33),
  AtomInfo("Se", 1.03, "0xff1493", 34),
  AtomInfo("Br", 0.94, "0x802828", 35),
  AtomInfo("Kr", 0.88, "0xff1493", 36),
  AtomInfo("Rb", 2.65, "0xff1493", 37),
  AtomInfo("Sr", 2.19, "0xff1493", 38),
  AtomInfo("Y", 2.12, "0xff1493", 39),
  AtomInfo("Zr", 2.06, "0xff1493", 40),
  AtomInfo("Nb", 1.98, "0xff1493", 41),
  AtomInfo("Mo", 1.90, "0xff1493", 42),
  AtomInfo("Tc", 1.83, "0xff1493", 43),
  AtomInfo("Ru", 1.78, "0xff1493", 44),
  AtomInfo("Rh", 1.73, "0xff1493", 45),
  AtomInfo("Pd", 1.69, "0xff1493", 46),
  AtomInfo("Ag", 1.65, "0x696969", 47),
  AtomInfo("Cd", 1.61, "0xff1493", 48),
  AtomInfo("In", 1.56, "0xff1493", 49),
  AtomInfo("Sn", 1.45, "0xff1493", 50),
  AtomInfo("Sb", 1.33, "0xff1493", 51),
  AtomInfo("Te", 1.23, "0xff1493", 52),
  AtomInfo("I", 1.15, "0xa020f0", 53),
  AtomInfo("Xe", 1.08, "0xff1493", 54),
  AtomInfo("Cs", 2.98, "0xff1493", 55),
  AtomInfo("Ba", 2.53, "0xffaa00", 56),
  AtomInfo("La", 1.95, "0xff1493", 57),
  AtomInfo("Ce", 1.85, "0xff1493", 58),
  AtomInfo("Pr", 2.47, "0xff1493", 59),
  AtomInfo("Nd", 2.06, "0xff1493", 60),
  AtomInfo("Pm", 2.05, "0xff1493", 61),
  AtomInfo("Sm", 2.38, "0xff1493", 62),
  AtomInfo("Eu", 2.31, "0xff1493", 63),
  AtomInfo("Gd", 2.33, "0xff1493", 64),
  AtomInfo("Tb", 2.25, "0xff1493", 65),
  AtomInfo("Dy", 2.28, "0xff1493", 66),
  AtomInfo("Ho", 2.26, "0xff1493", 67),
  AtomInfo("Er", 2.26, "0xff1493", 68),
  AtomInfo("Tm", 2.22, "0xff1493", 69),
  AtomInfo("Yb", 2.22, "0xff1493", 70),
  AtomInfo("Lu", 2.17, "0xff1493", 71),
  AtomInfo("Hf", 2.08, "0xff1493", 72),
  AtomInfo("Ta", 2.00, "0xff1493", 73),
  AtomInfo("W", 1.93, "0xff1493", 74),
  AtomInfo("Re", 1.88, "0xff1493", 75),
  AtomInfo("Os", 1.85, "0xff1493", 76),
  AtomInfo("Ir", 1.80, "0xff1493", 77),
  AtomInfo("Pt", 1.77, "0xff1493", 78),
  AtomInfo("Au", 1.74, "0xdaa520", 79),
  AtomInfo("Hg", 1.71, "0xff1493", 80),
  AtomInfo("Tl", 1.56, "0xff1493", 81),
  AtomInfo("Pb", 1.54, "0xff1493", 82),
  AtomInfo("Bi", 1.43, "0xff1493", 83),
  AtomInfo("Po", 1.35, "0xff1493", 84),
  AtomInfo("At", 1.27, "0xff1493", 85),
  AtomInfo("Rn", 1.20, "0xff1493", 86),
  AtomInfo("Ac", 1.95, "0xff1493", 89),
  AtomInfo("Th", 1.80, "0xff1493", 90),
  AtomInfo("Pa", 1.80, "0xff1493", 91),
  AtomInfo("U", 1.75, "0xff1493", 92),
  AtomInfo("Np", 1.75, "0xff1493", 93),
  AtomInfo("Pu", 1.75, "0xff1493", 94),
  AtomInfo("Am", 1.75, "0xff1493", 95)
]


def get_atom_info(symbol):
    global ATOMS_INFO
    for atom in ATOMS_INFO:
        if atom.symbol == symbol:
            return atom


def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)


def clean_scene():
    bpy.ops.object.select_by_type(type="MESH")
    bpy.ops.object.delete()


def add_sphere(location, material=None, radius=1):
    bpy.ops.mesh.primitive_uv_sphere_add(location=location, size=radius)
    sphere = bpy.context.object
    setMaterial(sphere, material)
    return sphere


def add_atom(
        symbol,
        location,
        material=None,
        scale_radius=1
        ):
    atomi = get_atom_info(symbol)
    radius = atomi.ionic_r*scale_radius
    sphere = add_sphere(location, atomi.mat, radius)
    sphere["size"] = radius
    sphere.name = atomi.symbol
    ALL_ATOMS.append(sphere)
    return sphere


def add_bond(atom1, atom2, scale_radius=1):
    # TODO
    radius = max(atom1["size"], atom2["size"])*0.3
    dist_vec = [list(atom1.location)[i] - list(atom2.location)[i]
                for i in range(3)]
    dist = math.sqrt(sum([a**2 for a in dist_vec]))
    bpy.ops.mesh.primitive_cylinder_add(
            location=[
                dist_vec[i]/2 + list(atom2.location)[i]
                for i in range(3)
                ],
            radius=radius,
            depth=dist
            )
    phi = math.atan2(dist_vec[1], dist_vec[0])
    theta = math.acos(dist_vec[2]/dist)
    bpy.context.object.rotation_euler[1] = phi
    bpy.context.object.rotation_euler[2] = theta


clean_scene()
red = makeMaterial("Red", (1, 0, 0), (1, 1, 1), 1)

scale_radius = .3
# ATOM DEFINITION
C1 = add_atom("C", (0.5, 0.5, 0.0), scale_radius=scale_radius)
C2 = add_atom("C", (0.5, 0.0, 0.5), scale_radius=scale_radius)
C3 = add_atom("C", (0.0, 0.5, 0.5), scale_radius=scale_radius)
C4 = add_atom("C", (0.75, 0.75, 0.25), scale_radius=scale_radius)
C5 = add_atom("C", (0.75, 0.25, 0.75), scale_radius=scale_radius)
C6 = add_atom("C", (0.25, 0.75, 0.75), scale_radius=scale_radius)
N1 = add_atom("N", (0.0, 0.0, 0.0), scale_radius=scale_radius)


# vim-run: blender --python %
