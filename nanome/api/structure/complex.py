from nanome._internal._structure._complex import _Complex
from nanome.util import Vector3, Quaternion, Matrix
from .io import ComplexIO

from math import cos, sin

class Complex(_Complex):
    io = ComplexIO()
    def __init__(self):
        _Complex.__init__(self)
        self.rendering = self._rendering
        self.molecular = self._molecular
        self.transform = self._transform
        self.io = ComplexIO(self)

    def add_molecule(self, molecule):
        self._molecules.append(molecule)

    def remove_molecule(self, molecule):
        self._molecules.remove(molecule)

    class Rendering(_Complex.Rendering):
        @property
        def boxed(self):
            return self._boxed
        @boxed.setter
        def boxed(self, value):
            self._boxed = value
        
        @property
        def visible(self):
            return self._visible
        @visible.setter
        def visible(self, value):
            self._visible = value
        
        @property
        def computing(self):
            return self._computing
        @computing.setter
        def computing(self, value):
            self._computing = value

        @property
        def current_frame(self):
            return self._current_frame
        @current_frame.setter
        def current_frame(self, value):
            self._current_frame = value
    _Complex.Rendering._create = Rendering

    class Molecular(_Complex.Molecular):
        @property
        def name(self):
            return self._name
        @name.setter
        def name(self, value):
            self._name = value
    _Complex.Molecular._create = Molecular

    class Transform(_Complex.Transform):
        @property
        def position(self):
            return self._position
        @position.setter
        def position(self, value):
            self._position = value
        
        @property
        def rotation(self):
            return self._rotation
        @rotation.setter
        def rotation(self, value):
            self._rotation = value

        def get_absolute_to_relative_matrix(self):
            rot_x = Matrix(4, 4)
            rot_x[1][1] = cos(self._rotation.x)
            rot_x[1][2] = -sin(self._rotation.x)
            rot_x[2][1] = sin(self._rotation.x)
            rot_x[2][2] = cos(self._rotation.x)
            rot_x[0][0] = 1
            rot_y = Matrix(4, 4)
            rot_y[2][2] = cos(self._rotation.y)
            rot_y[2][0] = -sin(self._rotation.y)
            rot_y[0][2] = sin(self._rotation.y)
            rot_y[0][0] = cos(self._rotation.y)
            rot_y[1][1] = 1
            rot_z = Matrix(4, 4)
            rot_z[0][0] = cos(self._rotation.z)
            rot_z[0][1] = -sin(self._rotation.z)
            rot_z[1][0] = sin(self._rotation.z)
            rot_z[1][1] = cos(self._rotation.z)
            rot_z[2][2] = 1
            rotation = rot_z * rot_y * rot_x

            translation = Matrix.create_identity(4)
            translation[0][3] = self._position.x
            translation[1][3] = self._position.y
            translation[2][3] = self._position.z
            
            transformation = translation * rotation
            return transformation

        def get_relative_to_absolute_matrix(self):
            result = self.get_absolute_to_relative_matrix()
            result = result.get_inverse()
            return result

    _Complex.Transform._create = Transform

    #Generators:
    @property
    def molecules(self):
        for molecule in self._molecules:
            yield molecule

    @property
    def chains(self):
        for molecule in self.molecules:
            for chain in molecule.chains:
                yield chain

    @property
    def residues(self):
        for chain in self.chains:
            for residue in chain.residues:
                yield residue

    @property
    def atoms(self):
        for residue in self.residues:
            for atom in residue.atoms:
                yield atom
                
    @property
    def bonds(self):
        for residue in self.residues:
            for bond in residue.bonds:
                yield bond
Complex.io._setup_addon(Complex)
_Complex._create = Complex
