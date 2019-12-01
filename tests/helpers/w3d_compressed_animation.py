# <pep8 compliant>
# Written by Stephan Vedder and Michael Schnabel

import unittest
from random import random
from mathutils import Quaternion

from io_mesh_w3d.structs.w3d_compressed_animation import *
from tests.helpers.w3d_version import get_version, compare_versions


def get_compressed_animation_header(hierarchy_name="hierarchy", flavor=1):
    return CompressedAnimationHeader(
        version=get_version(),
        name="containerName",
        hierarchy_name=hierarchy_name,
        num_frames=155,
        frame_rate=300,
        flavor=flavor)


def compare_compressed_animation_headers(self, expected, actual):
    compare_versions(self, expected.version, actual.version)
    self.assertEqual(expected.name, actual.name)
    self.assertEqual(expected.hierarchy_name, actual.hierarchy_name)
    self.assertEqual(expected.num_frames, actual.num_frames)
    self.assertEqual(expected.frame_rate, actual.frame_rate)
    self.assertEqual(expected.flavor, actual.flavor)


def get_time_coded_datum(time_code, type=0, random_interpolation=True):
    datum = TimeCodedDatum(
        time_code=time_code,
        non_interpolated=False)

    if random_interpolation:
        datum.non_interpolated = (random() < 0.5)

    if type == 6:
        datum.value = Quaternion((0.1, -2.0, -0.3, 2.0))
    else:
        datum.value = 3.14
    return datum


def compare_time_coded_datums(self, expected, actual):
    self.assertEqual(expected.time_code, actual.time_code)
    self.assertEqual(expected.non_interpolated, actual.non_interpolated)
    self.assertAlmostEqual(expected.value, actual.value, 5)


def get_time_coded_animation_channel(type_=0, random_interpolation=True):
    channel = TimeCodedAnimationChannel(
        num_time_codes=5,
        pivot=4,
        type=type_,
        time_codes=[])

    values = []
    if type_ == 6:
        channel.vector_len = 4
        values = [Quaternion((-.1, -2.1, -1.7, -1.7)),
                  Quaternion((-0.1, -2.1, 1.6, 1.6)),
                  Quaternion((0.9, -2.1, 1.6, 1.6)),
                  Quaternion((0.9, 1.8, 1.6, 1.6)),
                  Quaternion((0.9, 1.8, -1.6, 1.6))]
    else:
        channel.vector_len = 1
        values = [3.0, 3.5, 2.0, 1.0, -1.0]

    for i, value in enumerate(values):
        datum = TimeCodedDatum(
            time_code=i,
            value=value)
        if random_interpolation:
            datum.non_interpolated = (random() < 0.5)
        channel.time_codes.append(datum)
    return channel


def get_time_coded_animation_channel_minimal():
    return TimeCodedAnimationChannel(
        num_time_codes=55,
        pivot=4,
        type=1,
        time_codes=[get_time_coded_datum(0)])


def get_time_coded_animation_channel_empty():
    return TimeCodedAnimationChannel(
        num_time_codes=55,
        pivot=4,
        type=1,
        time_codes=[])


def compare_time_coded_animation_channels(self, expected, actual):
    self.assertEqual(expected.num_time_codes, actual.num_time_codes)
    self.assertEqual(expected.pivot, actual.pivot)
    self.assertEqual(expected.vector_len, actual.vector_len)
    self.assertEqual(expected.type, actual.type)

    self.assertEqual(len(expected.time_codes), len(actual.time_codes))
    for i in range(len(expected.time_codes)):
        compare_time_coded_datums(
            self, expected.time_codes[i], actual.time_codes[i])


def get_time_coded_bit_datum():
    return TimeCodedBitDatum(
        time_code=1,
        value=random() < 0.5)


def compare_time_coded_bit_datas(self, expected, actual):
    self.assertEqual(expected.time_code, actual.time_code)
    self.assertEqual(expected.value, actual.value)


def get_time_coded_bit_channel():
    channel = TimeCodedBitChannel(
        num_time_codes=55,
        pivot=1,
        type=0,
        default_value=12,
        time_codes=[])

    for _ in range(channel.num_time_codes):
        channel.time_codes.append(get_time_coded_bit_datum())
    return channel


def get_time_coded_bit_channel_minimal():
    return TimeCodedBitChannel(
        num_time_codes=55,
        pivot=1,
        type=0,
        default_value=12,
        time_codes=[get_time_coded_bit_datum()])


def get_time_coded_bit_channel_empty():
    return TimeCodedBitChannel(
        num_time_codes=55,
        pivot=1,
        type=0,
        default_value=12,
        time_codes=[])


def compare_time_coded_bit_channels(self, expected, actual):
    self.assertEqual(expected.num_time_codes, actual.num_time_codes)
    self.assertEqual(expected.pivot, actual.pivot)
    self.assertEqual(expected.type, actual.type)
    self.assertAlmostEqual(expected.default_value, actual.default_value, 5)

    self.assertEqual(len(expected.time_codes), len(actual.time_codes))
    for i in range(len(expected.time_codes)):
        compare_time_coded_bit_datas(
            self, expected.time_codes[i], actual.time_codes[i])


def get_adaptive_delta_block(data, type, index):
    ad_block = AdaptiveDeltaBlock(
        vector_index=0,
        block_index=3,
        delta_bytes=data)
    if type == 6:
        ad_block.vector_index = index
    return ad_block


def compare_adaptive_delta_blocks(self, expected, actual):
    self.assertEqual(expected.vector_index, actual.vector_index)
    self.assertEqual(expected.block_index, actual.block_index)
    self.assertEqual(len(expected.delta_bytes), len(actual.delta_bytes))
    for i in range(len(expected.delta_bytes)):
        self.assertEqual(expected.delta_bytes[i], actual.delta_bytes[i])


def get_adaptive_delta_data(type, num_bits, num_time_codes=33):
    data = []
    for _ in range(num_bits * 2):
        data.append(0x00)
    data = bytes(data)

    ad_data = AdaptiveDeltaData(
        bit_count=num_bits,
        delta_blocks=[])

    count = (num_time_codes + 15) >> 4

    if type == 6:
        vec_len = 4
        ad_data.initial_value = Quaternion((3.14, 2.0, -1.0, 0.1))
    else:
        vec_len = 1
        ad_data.initial_value = -3.14

    for _ in range(count):
        for i in range(vec_len):
            ad_data.delta_blocks.append(
                get_adaptive_delta_block(data, type, i))
    return ad_data


def compare_adaptive_delta_datas(self, expected, actual, type):
    self.assertEqual(expected.size(
        type), actual.size(type))
    self.assertEqual(expected.bit_count, actual.bit_count)
    self.assertEqual(len(expected.delta_blocks), len(actual.delta_blocks))
    for i in range(len(expected.delta_blocks)):
        compare_adaptive_delta_blocks(
            self, expected.delta_blocks[i], actual.delta_blocks[i])


def get_adaptive_delta_animation_channel(type, num_bits=4):
    channel = AdaptiveDeltaAnimationChannel(
        pivot=3,
        type=type,
        scale=4,
        num_time_codes=5,
        data=None)

    if type == 6:
        channel.vector_len = 4
    else:
        channel.vector_len = 1

    channel.data = get_adaptive_delta_data(
        type, num_bits, channel.num_time_codes)
    return channel


def get_adaptive_delta_animation_channel_minimal():
    return AdaptiveDeltaAnimationChannel(
        pivot=3,
        type=2,
        scale=4,
        vector_len=1,
        num_time_codes=5,
        data=get_adaptive_delta_data(2, 4, 5))


def compare_adaptive_delta_animation_channels(self, expected, actual):
    self.assertEqual(expected.pivot, actual.pivot)
    self.assertEqual(expected.vector_len, actual.vector_len)
    self.assertEqual(expected.type, actual.type)
    self.assertEqual(expected.scale, actual.scale)
    self.assertEqual(expected.num_time_codes, actual.num_time_codes)
    compare_adaptive_delta_datas(
        self, expected.data, actual.data, expected.type)


def get_adaptive_delta_motion_animation_channel(
        type, num_bits, num_time_codes):
    channel = AdaptiveDeltaMotionAnimationChannel(
        scale=4.0,
        data=get_adaptive_delta_data(type, num_bits, num_time_codes))
    return channel


def compare_adaptive_delta_motion_animation_channels(
        self, expected, actual, type):
    self.assertAlmostEqual(expected.scale, actual.scale, 5)
    compare_adaptive_delta_datas(self, expected.data, actual.data, type)


def get_motion_channel(type, delta_type, num_time_codes=55):
    channel = MotionChannel(
        delta_type=delta_type,
        type=type,
        num_time_codes=num_time_codes,
        pivot=3,
        data=[])

    if type == 6:
        channel.vector_len = 4
    else:
        channel.vector_len = 1

    if delta_type == 0:
        for _ in range(channel.num_time_codes):
            channel.data.append(get_time_coded_datum(0, type, False))
    elif delta_type == 1:
        channel.data = get_adaptive_delta_motion_animation_channel(
            type, 4, channel.num_time_codes)
    elif delta_type == 2:
        channel.data = get_adaptive_delta_motion_animation_channel(
            type, 8, channel.num_time_codes)
    return channel


def get_motion_channel_minimal():
    return MotionChannel(
        delta_type=0,
        type=2,
        num_time_codes=1,
        pivot=3,
        data=[get_time_coded_datum(0, 2, False)])


def get_motion_channel_empty():
    return MotionChannel(
        delta_type=0,
        type=2,
        num_time_codes=1,
        pivot=3,
        data=[])


def compare_motion_channels(self, expected, actual):
    self.assertEqual(expected.delta_type, actual.delta_type)
    self.assertEqual(expected.type, actual.type)
    self.assertEqual(expected.num_time_codes, actual.num_time_codes)
    self.assertEqual(expected.pivot, actual.pivot)

    if expected.delta_type == 0:
        self.assertEqual(len(expected.data), len(actual.data))
        for i in range(len(expected.data)):
            compare_time_coded_datums(self, expected.data[i], actual.data[i])
    else:
        compare_adaptive_delta_motion_animation_channels(
            self, expected.data, actual.data, expected.type)


def get_compressed_animation(
        hierarchy_name="TestHierarchy",
        flavor=0,
        bit_channels=True,
        motion_tc=True,
        motion_ad4=True,
        motion_ad8=True,
        random_interpolation=True):

    animation = CompressedAnimation(
        header=get_compressed_animation_header(hierarchy_name, flavor),
        time_coded_channels=[],
        adaptive_delta_channels=[],
        time_coded_bit_channels=[],
        motion_channels=[])

    if flavor == 0:
        animation.time_coded_channels.append(
            get_time_coded_animation_channel(type_=0, random_interpolation=random_interpolation))
        animation.time_coded_channels.append(
            get_time_coded_animation_channel(type_=1, random_interpolation=random_interpolation))
        animation.time_coded_channels.append(
            get_time_coded_animation_channel(type_=2, random_interpolation=random_interpolation))
        animation.time_coded_channels.append(
            get_time_coded_animation_channel(type_=6, random_interpolation=random_interpolation))

    else:
        animation.adaptive_delta_channels.append(
            get_adaptive_delta_animation_channel(type=0, num_bits=4))
        animation.adaptive_delta_channels.append(
            get_adaptive_delta_animation_channel(type=1, num_bits=4))
        animation.adaptive_delta_channels.append(
            get_adaptive_delta_animation_channel(type=2, num_bits=4))
        animation.adaptive_delta_channels.append(
            get_adaptive_delta_animation_channel(type=6, num_bits=4))

    if bit_channels:
        animation.time_coded_bit_channels.append(get_time_coded_bit_channel())
        animation.time_coded_bit_channels.append(get_time_coded_bit_channel())

    if motion_tc:
        animation.motion_channels.append(get_motion_channel(
            type=0, delta_type=0, num_time_codes=50))
        animation.motion_channels.append(get_motion_channel(
            type=1, delta_type=0, num_time_codes=50))
        animation.motion_channels.append(
            get_motion_channel(type=2, delta_type=0))
        animation.motion_channels.append(
            get_motion_channel(type=6, delta_type=0))

    if motion_ad4:
        animation.motion_channels.append(
            get_motion_channel(type=0, delta_type=1))
        animation.motion_channels.append(
            get_motion_channel(type=1, delta_type=1))
        animation.motion_channels.append(
            get_motion_channel(type=2, delta_type=1))
        animation.motion_channels.append(
            get_motion_channel(type=6, delta_type=1))

    if motion_ad8:
        animation.motion_channels.append(
            get_motion_channel(type=0, delta_type=2))
        animation.motion_channels.append(
            get_motion_channel(type=1, delta_type=2))
        animation.motion_channels.append(
            get_motion_channel(type=2, delta_type=2))
        animation.motion_channels.append(
            get_motion_channel(type=6, delta_type=2))

    return animation


def get_compressed_animation_minimal():
    return CompressedAnimation(
        header=get_compressed_animation_header(),
        time_coded_channels=[get_time_coded_animation_channel_minimal()],
        adaptive_delta_channels=[
            get_adaptive_delta_animation_channel_minimal()],
        time_coded_bit_channels=[get_time_coded_bit_channel_minimal()],
        motion_channels=[get_motion_channel_minimal()])


def get_compressed_animation_empty():
    return CompressedAnimation(
        header=get_compressed_animation_header(),
        time_coded_channels=[],
        adaptive_delta_channels=[],
        time_coded_bit_channels=[],
        motion_channels=[])


def compare_compressed_animations(self, expected, actual):
    compare_compressed_animation_headers(self, expected.header, actual.header)
    self.assertEqual(len(expected.time_coded_channels),
                     len(actual.time_coded_channels))
    for i in range(len(expected.time_coded_channels)):
        compare_time_coded_animation_channels(
            self, expected.time_coded_channels[i], actual.time_coded_channels[i])
    self.assertEqual(len(expected.adaptive_delta_channels),
                     len(actual.adaptive_delta_channels))
    for i in range(len(expected.adaptive_delta_channels)):
        compare_adaptive_delta_animation_channels(
            self, expected.adaptive_delta_channels[i], actual.adaptive_delta_channels[i])
    self.assertEqual(len(expected.time_coded_bit_channels),
                     len(actual.time_coded_bit_channels))
    for i in range(len(expected.time_coded_bit_channels)):
        compare_time_coded_bit_channels(self,
                                        expected.time_coded_bit_channels[i],
                                        actual.time_coded_bit_channels[i])
    self.assertEqual(len(expected.motion_channels),
                     len(actual.motion_channels))
    for i in range(len(expected.motion_channels)):
        compare_motion_channels(
            self, expected.motion_channels[i], actual.motion_channels[i])
