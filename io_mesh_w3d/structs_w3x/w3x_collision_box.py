# <pep8 compliant>
# Written by Stephan Vedder and Michael Schnabel

from mathutils import Vector

from io_mesh_w3d.structs_w3x.w3x_struct import Struct
from io_mesh_w3d.io_xml import *


class CollisionBox(Struct):
    center = Vector((0, 0, 0))
    extend = Vector((0, 0, 0))

    @staticmethod
    def parse(xml_collision_box):
        result = CollisionBox()

        xml_center = xml_collision_box.getElementsByTagName('Center')[0]
        result.center = parse_vector(xml_center)

        xml_extend = xml_collision_box.getElementsByTagName('Extend')[0]
        result.extend = parse_vector(xml_extend)
        return result

    def create(self, doc):
        result = doc.createElement('W3DCollisionBox')
        result.appendChild(create_vector(self.center, doc, 'Center'))
        result.appendChild(create_vector(self.extend, doc, 'Extend'))
        return result