# <pep8 compliant>
# Written by Stephan Vedder and Michael Schnabel

import bpy
import bmesh
from bpy_extras import node_shader_utils

from io_mesh_w3d.common.utils.helpers import *
from io_mesh_w3d.w3d.structs.mesh_structs.vertex_material import *


    #node.color = (1, 0, 0)
    #node.use_custom_color = True
    #node.name = 'Test'
    #node.label


def create_material_pass():
    material = bpy.data.materials.new('meshName.MaterialPass1')

    material.material_type = 'VERTEX_MATERIAL'
    material.use_nodes = True
    material.shadow_method = 'CLIP'
    material.blend_method = 'BLEND'
    material.show_transparent_back = False

    # delete principled bsdf
    principled_bsdf = material.node_tree.nodes.get('Principled BSDF')
    material.node_tree.nodes.remove(principled_bsdf)

    # get or create node group


def create_material_node_group(nodes, name):
    group = bpy.data.node_groups.new(name, 'ShaderNodeTree')
    node_tree = group
    links = node_tree.links
    # create nodes
    shader = create_specular_shader_node(node_tree)

    # create group inputs
    group_inputs = group.nodes.new('NodeGroupInput')
    group_inputs.location = (-350,0)
    group.inputs.new('NodeSocketFloat', 'in_to_greater')
    group.inputs.new('NodeSocketFloat', 'in_to_less')

    # create group outputs
    group_outputs = group.nodes.new('NodeGroupOutput')
    group_outputs.location = (300,0)
    group.outputs.new('NodeSocketFloat', 'BSDF_out')

    links.new(shader.outputs['BSDF'], group_outputs.inputs['BSDF_out'])

    inst = nodes.new(type='ShaderNodeGroup')
    inst.node_tree = group
    return inst



def get_connected_nodes(links, node, input, types=[]):
    nodes = []
    for link in links:
        #print(link.to_node)
        #print(link.to_socket)
        if link.to_node == node and link.to_socket.identifier == input:
            # and link.from_socket in outputs:
            # and type(node) == bpy.types.ShaderNodeTexture....
            # and node.inputs[''].is_linked
            nodes.append(link.from_node)

    for node in nodes:
        print('###')
        print(node.bl_idname)
        print(node.name)
    return nodes


def create_specular_shader_node(node_tree):
    # inputs: Base Color, Specular, Roughness, Emissive Color, Transparency,
    #           Normal, Clear Coat, Clear Coat Radius, Clear Coat Normal, Ambient Occlusion
    # outputs: BSDF

    node = node_tree.nodes.new('ShaderNodeEeveeSpecular')
    node.label = 'Shader'
    # hide unused inputs
    node.inputs['Clear Coat'].hide = True
    node.inputs['Clear Coat Roughness'].hide = True
    node.inputs['Clear Coat Normal'].hide = True
    node.inputs['Ambient Occlusion'].hide = True
    return node


def create_texture_node(node_tree, texture):
    # inputs: Vector
    # outputs: Color, Alpha

    node = node_tree.nodes.new('ShaderNodeTexImage')
    #node.color_mapping
    #node.extension # interpolation past bounds
    node.image = texture
    #node.image_user
    #node.interpolation
    #node.projection
    #node.projection_blend
    #node.texture_mapping
    return node

def create_uv_map_node(node_tree):
    # outputs: UV

    node = node_tree.nodes.new('ShaderNodeUVMap')
    #node.uv_map = 'uvmapname'
    return node

def create_rgb_mix_node(node_tree):
    # inputs: Fac, Color1, Color2
    # outputs: Color

    node = node_tree.nodes.new('ShaderNodeMixRGB')
    #node.blend_type
    #node.use_alpha
    #node.use_clamp
    return node

def create_normal_map_node(node_tree):
    # inputs: Strength, Color
    # outputs: Normal

    node = node_tree.nodes.new('ShaderNodeNormalMap')
    node.space = 'TANGENT'
    #node.uv_map = 'uvmapname'
    return node

def create_seperate_hsv_node(node_tree):
    # inputs: Color
    # outputs: H, S, V

    node = node_tree.nodes.new('ShaderNodeSeperateHSV')
    return node

def create_rgb_node(node_tree):
    # outputs: Color

    node = node_tree.nodes.new('ShaderNodeRGB')
    return node


def create_uvlayer2(tx_coords, mesh, b_mesh, triangles, name):
    uv_layer = mesh.uv_layers.new(do_init=False)
    uv_layer.name = name
    for i, face in enumerate(b_mesh.faces):
        for loop in face.loops:
            idx = triangles[i][loop.index % 3]
            uv_layer.data[loop.index].uv = tx_coords[idx].xy
    return name


##########################################################################
# vertex material
##########################################################################

def create_vertex_material(context, principleds, structure, mesh, name, triangles):
    for vertMat in structure.vert_materials:
        (material, principled) = create_material_from_vertex_material(name, vertMat)
        mesh.materials.append(material)
        materials.append(material)
        principleds.append(principled)

        if prelit_type is not None:
            material.material_type = 'PRELIT_MATERIAL'
            material.prelit_type = prelit_type

    b_mesh = bmesh.new()
    b_mesh.from_mesh(mesh)

    for mat_pass in structure.material_passes:
        create_uvlayer(context, mesh, b_mesh, triangles, mat_pass)

    for mat_pass in struct.material_passes:
        if mat_pass.tx_stages:
            tx_stage = mat_pass.tx_stages[0]
            mat_id = mat_pass.vertex_material_ids[0]
            tex_id = tx_stage.tx_ids[0]

            # hide unsupported inputs
            principleds[mat_id].inputs['Subsurface'].hide = True
            principleds[mat_id].inputs['Subsurface Radius'].hide = True
            principleds[mat_id].inputs['Subsurface Color'].hide = True
            principleds[mat_id].inputs['Metallic'].hide = True
            principleds[mat_id].inputs['Specular Tint'].hide = True
            principleds[mat_id].inputs['Roughness'].hide = True
            principleds[mat_id].inputs['Anisotropic'].hide = True
            principleds[mat_id].inputs['Anisotropic Rotation'].hide = True
            principleds[mat_id].inputs['Sheen'].hide = True
            principleds[mat_id].inputs['Sheen Tint'].hide = True
            principleds[mat_id].inputs['Clearcoat'].hide = True
            principleds[mat_id].inputs['Clearcoat Roughness'].hide = True
            principleds[mat_id].inputs['IOR'].hide = True
            principleds[mat_id].inputs['Transmission'].hide = True
            principleds[mat_id].inputs['Transmission Roughness'].hide = True
            principleds[mat_id].inputs['Clearcoat Normal'].hide = True
            principleds[mat_id].inputs['Tangent'].hide = True

            node_tree = materials[mat_id].node_tree
            links = node_tree.links

            create_material_node_group(node_tree.nodes, 'VertexMaterial1')

            #shade = create_specular_shader_node(node_tree)
            #out = node_tree.nodes.get('Material Output')
            #links.new(shade.outputs['BSDF'], out.inputs['Surface'])

            mix_node = create_rgb_mix_node(node_tree)
            mix_node.location = Vector((-250, 400))
            links.new(mix_node.outputs['Color'], principleds[mat_id].inputs['Base Color'])

            texture_struct = struct.textures[tex_id]
            texture = find_texture(context, texture_struct.file, texture_struct.id)

            texture_node = create_texture_node(node_tree, texture)
            texture_node.location = Vector((-550, 600))
            links.new(texture_node.outputs['Color'], mix_node.inputs['Color1'])
            links.new(texture_node.outputs['Alpha'], principleds[mat_id].inputs['Alpha'])

            uv_node = create_uv_map_node(node_tree)
            uv_node.uv_map = create_uvlayer2(mat_pass.tx_stages[0].tx_coords, mesh, b_mesh, triangles, 'diffuse')
            uv_node.location = Vector((-750, 600))
            links.new(uv_node.outputs['UV'], texture_node.inputs['Vector'])

            texture2_node = create_texture_node(node_tree, None)
            texture2_node.location = Vector((-550, 300))
            links.new(texture2_node.outputs['Color'], mix_node.inputs['Color2'])
            links.new(texture2_node.outputs['Alpha'], mix_node.inputs['Fac'])

            uv2_node = create_uv_map_node(node_tree)
            uv2_node.uv_map = create_uvlayer2(mat_pass.tx_stages[0].tx_coords, mesh, b_mesh, triangles, 'diffuse2')
            uv2_node.location = Vector((-750, 300))
            links.new(uv2_node.outputs['UV'], texture2_node.inputs['Vector'])

            texture_spec_node = create_texture_node(node_tree, None)
            texture_spec_node.location = Vector((-550, 0))
            links.new(texture_spec_node.outputs['Color'], principleds[mat_id].inputs['Specular'])

            uv_spec_node = create_uv_map_node(node_tree)
            uv_spec_node.uv_map = create_uvlayer2(mat_pass.tx_stages[0].tx_coords, mesh, b_mesh, triangles, 'specular')
            uv_spec_node.location = Vector((-750, 0))
            links.new(uv_spec_node.outputs['UV'], texture_spec_node.inputs['Vector'])

            emission_color_node = create_rgb_node(node_tree)
            emission_color_node.location = Vector((-250, -100))
            links.new(emission_color_node.outputs['Color'], principleds[mat_id].inputs['Emission'])

            normal_map_node = create_normal_map_node(node_tree)
            normal_map_node.location = Vector((-250, -300))
            links.new(normal_map_node.outputs['Normal'], principleds[mat_id].inputs['Normal'])

            texture_normal_node = create_texture_node(node_tree, None)
            texture_normal_node.location = Vector((-550, -300))
            links.new(texture_normal_node.outputs['Color'], normal_map_node.inputs['Color'])
            links.new(texture_normal_node.outputs['Alpha'], normal_map_node.inputs['Strength'])

            uv3_node = create_uv_map_node(node_tree)
            uv3_node.uv_map = create_uvlayer2(mat_pass.tx_stages[0].tx_coords, mesh, b_mesh, triangles, 'normal')
            uv3_node.location = Vector((-750, -300))
            links.new(uv3_node.outputs['UV'], texture_normal_node.inputs['Vector'])


            get_connected_nodes(links, principleds[mat_id], 'Base Color')
            get_connected_nodes(links, principleds[mat_id], 'Specular')


    for i, shader in enumerate(struct.shaders):
        set_shader_properties(materials[i], shader)


def create_material_from_vertex_material(name, vert_mat):
    name = name + "." + vert_mat.vm_name
    if name in bpy.data.materials:
        material = bpy.data.materials[name]
        principled_bsdf = material.node_tree.nodes.get('Principled BSDF')
        return material, principled_bsdf

    material = bpy.data.materials.new(name)
    material.material_type = 'VERTEX_MATERIAL'
    material.use_nodes = True
    material.shadow_method = 'CLIP'
    material.blend_method = 'BLEND'
    material.show_transparent_back = False

    attributes = {'DEFAULT'}
    attribs = vert_mat.vm_info.attributes
    if attribs & USE_DEPTH_CUE:
        attributes.add('USE_DEPTH_CUE')
    if attribs & ARGB_EMISSIVE_ONLY:
        attributes.add('ARGB_EMISSIVE_ONLY')
    if attribs & COPY_SPECULAR_TO_DIFFUSE:
        attributes.add('COPY_SPECULAR_TO_DIFFUSE')
    if attribs & DEPTH_CUE_TO_ALPHA:
        attributes.add('DEPTH_CUE_TO_ALPHA')

    material.attributes = atts

    principled_bsdf = material.node_tree.nodes.get('Principled BSDF')
    #principled_bsdf.base_color = vert_mat.vm_info.diffuse.to_vector_rgb()
    #principled_bsdf.alpha = vert_mat.vm_info.opacity
    
    material.specular_intensity = vert_mat.vm_info.shininess
    material.specular_color = vert_mat.vm_info.specular.to_vector_rgb()
    material.emission = vert_mat.vm_info.emissive.to_vector_rgba()
    material.ambient = vert_mat.vm_info.ambient.to_vector_rgba()
    material.translucency = vert_mat.vm_info.translucency
    material.opacity = vert_mat.vm_info.opacity

    material.vm_args_0 = vert_mat.vm_args_0
    material.vm_args_1 = vert_mat.vm_args_1

    return material, principled_bsdf


##########################################################################
# shader material
##########################################################################

def create_shader_materials(context, struct, mesh, triangles):
    for i, shaderMat in enumerate(struct.shader_materials):
        (material, principled) = create_material_from_shader_material(
            context, mesh.name, shaderMat)
        mesh.materials.append(material)

    if struct.material_passes:
        b_mesh = bmesh.new()
        b_mesh.from_mesh(mesh)

    for mat_pass in struct.material_passes:
        create_uvlayer(context, mesh, b_mesh, triangles, mat_pass)


def create_material_from_shader_material(context, name, shader_mat):
    name = name + '.' + shader_mat.header.type_name
    if name in bpy.data.materials:
        material = bpy.data.materials[name]
        principled = node_shader_utils.PrincipledBSDFWrapper(material, is_readonly=False)
        return material, principled

    material = bpy.data.materials.new(name)
    material.material_type = 'SHADER_MATERIAL'
    material.use_nodes = True
    material.blend_method = 'BLEND'
    material.show_transparent_back = False

    if shader_mat.header.technique is not None:
        material.technique = shader_mat.header.technique

    principled = node_shader_utils.PrincipledBSDFWrapper(material, is_readonly=False)

    for prop in shader_mat.properties:
        if prop.name == 'DiffuseTexture' and prop.value != '':
            principled.base_color_texture.image = find_texture(context, prop.value)
        elif prop.name == 'NormalMap' and prop.value != '':
            principled.normalmap_texture.image = find_texture(context, prop.value)
        elif prop.name == 'BumpScale':
            principled.normalmap_strength = prop.value
        elif prop.name == 'SpecMap' and prop.value != '':
            principled.specular_texture.image = find_texture(context, prop.value)
        elif prop.name == 'SpecularExponent' or prop.name == 'Shininess':
            material.specular_intensity = prop.value / 200.0
        elif prop.name == 'DiffuseColor' or prop.name == 'ColorDiffuse':
            material.diffuse_color = prop.to_rgba()
        elif prop.name == 'SpecularColor' or prop.name == 'ColorSpecular':
            material.specular_color = prop.to_rgb()
        elif prop.name == 'CullingEnable':
            material.use_backface_culling = prop.value
        elif prop.name == 'Texture_0':
            principled.base_color_texture.image = find_texture(context, prop.value)

        # all props below have no effect on shading -> custom properties for roundtrip purpose
        elif prop.name == 'AmbientColor' or prop.name == 'ColorAmbient':
            material.ambient = prop.to_rgba()
        elif prop.name == 'EmissiveColor' or prop.name == 'ColorEmissive':
            material.emission = prop.to_rgba()
        elif prop.name == 'Opacity':
            material.opacity = prop.value
        elif prop.name == 'AlphaTestEnable':
            material.alpha_test = prop.value
        elif prop.name == 'BlendMode':  # is blend_method ?
            material.blend_mode = prop.value
        elif prop.name == 'BumpUVScale':
            material.bump_uv_scale = prop.value.xy
        elif prop.name == 'EdgeFadeOut':
            material.edge_fade_out = prop.value
        elif prop.name == 'DepthWriteEnable':
            material.depth_write = prop.value
        elif prop.name == 'Sampler_ClampU_ClampV_NoMip_0':
            material.sampler_clamp_uv_no_mip_0 = prop.value
        elif prop.name == 'Sampler_ClampU_ClampV_NoMip_1':
            material.sampler_clamp_uv_no_mip_1 = prop.value
        elif prop.name == 'NumTextures':
            material.num_textures = prop.value  # is 1 if texture_0 and texture_1 are set
        elif prop.name == 'Texture_1':  # second diffuse texture
            material.texture_1 = prop.value
        elif prop.name == 'SecondaryTextureBlendMode':
            material.secondary_texture_blend_mode = prop.value
        elif prop.name == 'TexCoordMapper_0':
            material.tex_coord_mapper_0 = prop.value
        elif prop.name == 'TexCoordMapper_1':
            material.tex_coord_mapper_1 = prop.value
        elif prop.name == 'TexCoordTransform_0':
            material.tex_coord_transform_0 = prop.value
        elif prop.name == 'TexCoordTransform_1':
            material.tex_coord_transform_1 = prop.value
        elif prop.name == 'EnvironmentTexture':
            material.environment_texture = prop.value
        elif prop.name == 'EnvMult':
            material.environment_mult = prop.value
        elif prop.name == 'RecolorTexture':
            material.recolor_texture = prop.value
        elif prop.name == 'RecolorMultiplier':
            material.recolor_mult = prop.value
        elif prop.name == 'UseRecolorColors':
            material.use_recolor = prop.value
        elif prop.name == 'HouseColorPulse':
            material.house_color_pulse = prop.value
        elif prop.name == 'ScrollingMaskTexture':
            material.scrolling_mask_texture = prop.value
        elif prop.name == 'TexCoordTransformAngle_0':
            material.tex_coord_transform_angle = prop.value
        elif prop.name == 'TexCoordTransformU_0':
            material.tex_coord_transform_u_0 = prop.value
        elif prop.name == 'TexCoordTransformV_0':
            material.tex_coord_transform_v_0 = prop.value
        elif prop.name == 'TexCoordTransformU_1':
            material.tex_coord_transform_u_1 = prop.value
        elif prop.name == 'TexCoordTransformV_1':
            material.tex_coord_transform_v_1 = prop.value
        elif prop.name == 'TexCoordTransformU_2':
            material.tex_coord_transform_u_2 = prop.value
        elif prop.name == 'TexCoordTransformV_2':
            material.tex_coord_transform_v_2 = prop.value
        elif prop.name == 'TextureAnimation_FPS_NumPerRow_LastFrame_FrameOffset_0':
            material.tex_ani_fps_NPR_lastFrame_frameOffset_0 = prop.value
        elif prop.name == 'IonHullTexture':
            material.ion_hull_texture = prop.value
        elif prop.name == 'MultiTextureEnable':
            material.multi_texture_enable = prop.value
        else:
            context.error('shader property not implemented: ' + prop.name)

    return material, principled


##########################################################################
# set shader properties
##########################################################################


def set_shader_properties(material, shader):
    material.shader.depth_compare = shader.depth_compare
    material.shader.depth_mask = shader.depth_mask
    material.shader.color_mask = shader.color_mask
    material.shader.dest_blend = shader.dest_blend
    material.shader.fog_func = shader.fog_func
    material.shader.pri_gradient = shader.pri_gradient
    material.shader.sec_gradient = shader.sec_gradient
    material.shader.src_blend = shader.src_blend
    material.shader.texturing = shader.texturing
    material.shader.detail_color_func = shader.detail_color_func
    material.shader.detail_alpha_func = shader.detail_alpha_func
    material.shader.shader_preset = shader.shader_preset
    material.shader.alpha_test = shader.alpha_test
    material.shader.post_detail_color_func = shader.post_detail_color_func
    material.shader.post_detail_alpha_func = shader.post_detail_alpha_func