# <pep8 compliant>
# Written by Stephan Vedder and Michael Schnabel

import bpy
from shutil import copyfile

from io_mesh_w3d.export_utils import save
from io_mesh_w3d.w3d.import_w3d import load
from io_mesh_w3d.import_utils import create_data
from tests.common.helpers.animation import get_animation
from tests.common.helpers.collision_box import get_collision_box
from tests.common.helpers.hierarchy import *
from tests.common.helpers.hlod import *
from tests.common.helpers.mesh import get_mesh
from tests.utils import TestCase
from tests.w3d.helpers.dazzle import get_dazzle
from tests.w3d.helpers.compressed_animation import get_compressed_animation


class TestRoundtripW3D(TestCase):
    def test_roundtrip(self):
        hierarchy_name = 'testhiera_skl'
        hierarchy = get_hierarchy(hierarchy_name)
        meshes = [
            get_mesh(name='sword', skin=True),
            get_mesh(name='soldier', skin=True),
            get_mesh(name='TRUNK')]
        hlod = get_hlod('testmodelname', hierarchy_name)
        boxes = [get_collision_box()]
        dazzles = [get_dazzle()]
        animation = get_animation(hierarchy_name)

        self.filepath = self.outpath() + 'output_skn'
        create_data(self, meshes, hlod, hierarchy, boxes, animation, None, dazzles)

        # export
        self.filepath = self.outpath() + 'output_skn'
        export_settings = {'mode': 'HM', 'use_existing_skeleton': True}
        save(self, export_settings)

        self.filepath = self.outpath() + 'testhiera_skl'
        export_settings['mode'] = 'H'
        save(self, export_settings)

        self.filepath = self.outpath() + 'output_ani'
        export_settings['mode'] = 'A'
        export_settings['compression'] = 'U'
        save(self, export_settings)

        # reset scene
        bpy.ops.wm.read_homefile(use_empty=True)

        # import
        self.filepath = self.outpath() + 'output_skn.w3d'
        load(self)
        self.filepath = self.outpath() + 'output_ani.w3d'
        load(self)

        # check created objects
        self.assertTrue(hierarchy_name in bpy.data.objects)
        self.assertTrue(hierarchy_name in bpy.data.armatures)
        amt = bpy.data.armatures[hierarchy_name]
        self.assertEqual(6, len(amt.bones))

        self.assertTrue('sword' in bpy.data.objects)
        self.assertTrue('soldier' in bpy.data.objects)
        self.assertTrue('TRUNK' in bpy.data.objects)
        self.assertTrue('Brakelight' in bpy.data.objects)

    def test_roundtrip_compressed_animation(self):
        hierarchy_name = 'testhiera_skl'
        hierarchy = get_hierarchy(hierarchy_name)
        meshes = [
            get_mesh(name='sword', skin=True),
            get_mesh(name='soldier', skin=True),
            get_mesh(name='TRUNK')]
        hlod = get_hlod('testmodelname', hierarchy_name)
        boxes = [get_collision_box()]
        dazzles = [get_dazzle()]
        comp_animation = get_compressed_animation(hierarchy_name)

        self.filepath = self.outpath() + 'output_skn'
        create_data(self, meshes, hlod, hierarchy, boxes, None, comp_animation, dazzles)

        # export
        self.filepath = self.outpath() + 'output_skn'
        export_settings = {'mode': 'HM', 'use_existing_skeleton': True}
        save(self, export_settings)

        self.filepath = self.outpath() + 'testhiera_skl'
        export_settings['mode'] = 'H'
        save(self, export_settings)

        self.filepath = self.outpath() + 'output_comp_ani'
        export_settings['mode'] = 'A'
        export_settings['compression'] = 'TC'
        save(self, export_settings)

        # reset scene
        bpy.ops.wm.read_homefile(app_template='')

        # import
        self.filepath = self.outpath() + 'output_skn.w3d'
        load(self)
        self.filepath = self.outpath() + 'output_comp_ani.w3d'
        load(self)

        # check created objects
        self.assertTrue(hierarchy_name in bpy.data.objects)
        self.assertTrue(hierarchy_name in bpy.data.armatures)
        amt = bpy.data.armatures[hierarchy_name]
        self.assertEqual(6, len(amt.bones))

        self.assertTrue('sword' in bpy.data.objects)
        self.assertTrue('soldier' in bpy.data.objects)
        self.assertTrue('TRUNK' in bpy.data.objects)
        self.assertTrue('Brakelight' in bpy.data.objects)

    def test_roundtrip_HAM(self):
        hierarchy_name = 'TestName'
        hierarchy = get_hierarchy(hierarchy_name)
        meshes = [
            get_mesh(name='sword', skin=True),
            get_mesh(name='soldier', skin=True),
            get_mesh(name='TRUNK')]
        hlod = get_hlod(hierarchy_name, hierarchy_name)
        boxes = [get_collision_box()]
        dazzles = [get_dazzle()]
        animation = get_animation(hierarchy_name)

        self.filepath = self.outpath() + 'output'
        create_data(self, meshes, hlod, hierarchy, boxes, animation, None, dazzles)

        # export
        self.filepath = self.outpath() + 'output'
        export_settings = {'mode': 'HAM', 'compression': 'U'}
        save(self, export_settings)

        # reset scene
        bpy.ops.wm.read_homefile(app_template='')

        # import
        self.filepath = self.outpath() + 'output.w3d'
        load(self)

        # check created objects
        self.assertTrue('TestName' in bpy.data.armatures)
        amt = bpy.data.armatures['TestName']
        self.assertEqual(6, len(amt.bones))

        self.assertTrue('sword' in bpy.data.objects)
        self.assertTrue('soldier' in bpy.data.objects)
        self.assertTrue('TRUNK' in bpy.data.objects)
        self.assertTrue('Brakelight' in bpy.data.objects)

    def test_roundtrip_HAM_tc_animation(self):
        hierarchy_name = 'TestName'
        hierarchy = get_hierarchy(hierarchy_name)
        meshes = [
            get_mesh(name='sword', skin=True),
            get_mesh(name='soldier', skin=True),
            get_mesh(name='TRUNK')]
        hlod = get_hlod(hierarchy_name, hierarchy_name)
        boxes = [get_collision_box()]
        dazzles = [get_dazzle()]
        comp_animation = get_compressed_animation(hierarchy_name)

        self.filepath = self.outpath() + 'output'
        create_data(self, meshes, hlod, hierarchy, boxes, None, comp_animation, dazzles)

        # export
        self.filepath = self.outpath() + 'output'
        export_settings = {'mode': 'HAM', 'compression': 'TC'}
        save(self, export_settings)

        # reset scene
        bpy.ops.wm.read_homefile(app_template='')

        # import
        self.filepath = self.outpath() + 'output.w3d'
        load(self)

        # check created objects
        self.assertTrue('TestName' in bpy.data.armatures)
        amt = bpy.data.armatures['TestName']
        self.assertEqual(6, len(amt.bones))

        self.assertTrue('sword' in bpy.data.objects)
        self.assertTrue('soldier' in bpy.data.objects)
        self.assertTrue('TRUNK' in bpy.data.objects)
        self.assertTrue('Brakelight' in bpy.data.objects)

    def test_roundtrip_no_armature(self):
        hierarchy_name = 'TestModelName'
        hierarchy = get_hierarchy(hierarchy_name)
        hierarchy.pivots = [get_roottransform(),
                            get_hierarchy_pivot(name='sword', parent=0),
                            get_hierarchy_pivot(name='soldier', parent=0),
                            get_hierarchy_pivot(name='TRUNK', parent=0)]

        meshes = [get_mesh(name='sword'),
                  get_mesh(name='soldier'),
                  get_mesh(name='TRUNK')]
        hlod = get_hlod('TestModelName', hierarchy_name)
        hlod.lod_arrays[0].sub_objects = [
            get_hlod_sub_object(bone=1, name='containerName.sword'),
            get_hlod_sub_object(bone=2, name='containerName.soldier'),
            get_hlod_sub_object(bone=3, name='containerName.TRUNK')]
        hlod.lod_arrays[0].header.model_count = len(hlod.lod_arrays[0].sub_objects)

        self.filepath = self.outpath() + 'output'
        create_data(self, meshes, hlod, hierarchy, [], None, None, [])

        # export
        self.filepath = self.outpath() + 'output'
        export_settings = {'mode': 'HM', 'use_existing_skeleton': False}
        save(self, export_settings)

        # reset scene
        bpy.ops.wm.read_homefile(app_template='')

        # import
        self.filepath = self.outpath() + 'output.w3d'
        load(self)

        # check created objects
        self.assertTrue('TestModelName' in bpy.data.objects)
        self.assertTrue('TestModelName' in bpy.data.armatures)
        self.assertTrue('sword' in bpy.data.objects)
        self.assertTrue('soldier' in bpy.data.objects)
        self.assertTrue('TRUNK' in bpy.data.objects)

    def test_roundtrip_prelit(self):
        hierarchy_name = 'testhiera_skl'
        hierarchy = get_hierarchy(hierarchy_name)
        meshes = [get_mesh(name='sword', skin=True, prelit=True),
                  get_mesh(name='soldier', skin=True),
                  get_mesh(name='TRUNK', prelit=True)]
        hlod = get_hlod('TestModelName', hierarchy_name)

        self.filepath = self.outpath() + 'output'
        create_data(self, meshes, hlod, hierarchy, [], None, None, [])

        # export
        self.filepath = self.outpath() + 'output'
        export_settings = {'mode': 'HM', 'use_existing_skeleton': False}
        save(self, export_settings)

        # reset scene
        bpy.ops.wm.read_homefile(app_template='')

        # import
        self.filepath = self.outpath() + 'output.w3d'
        load(self)

        # check created objects
        self.assertTrue('testhiera_skl' in bpy.data.objects)
        self.assertTrue('testhiera_skl' in bpy.data.armatures)
        amt = bpy.data.armatures['testhiera_skl']
        self.assertEqual(6, len(amt.bones))

        self.assertTrue('sword' in bpy.data.objects)
        self.assertTrue('soldier' in bpy.data.objects)
        self.assertTrue('TRUNK' in bpy.data.objects)
