#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
方块工具类
"""
import colorsys
import math
from typing import Tuple, List, Optional

from config.block_config import BlockTemplate, BlockConfig


class BlockHelper:
    """方块数据转换器"""

    @staticmethod
    def calculate_scale(template: BlockTemplate, global_scale: float=1.0) -> Tuple[float, float, float]:
        """
        计算方块的缩放

        步骤：
        1. 应用default_scale_tuple使方块变为size_units的正方形
        2. 除以size_units使每个轴长度为1
        3. 乘以全局缩放系数

        Args:
            template: 方块模板
            global_scale: 全局缩放参数

        Returns:
            (scale_x, scale_y, scale_z) 最终缩放值
        """
        base_x, base_y, base_z = template.default_scale_tuple

        # 归一化到单位1
        normalized_x = base_x / template.size_units
        normalized_y = base_y / template.size_units
        normalized_z = base_z / template.size_units

        final_x = normalized_x * global_scale
        final_y = normalized_y * global_scale
        final_z = normalized_z * global_scale

        return final_x, final_y, final_z

    @staticmethod
    def calculate_position(x: int, y: int, z: int,
                           global_scale: float=1.0,
                           start_x: float=0.0,
                           start_y: float=0.0,
                           start_z: float=0.0) -> Tuple[float, float, float]:
        """
        计算方块的世界坐标

        考虑：
        - 方块间距为 GLOBAL_SCALE（因为每个方块归一化后是1单位）
        - 起始位置偏移

        Args:
            x: 坐标
            y: 坐标
            z: 坐标
            global_scale: 全局缩放参数
            start_x: 起始坐标
            start_y: 起始坐标
            start_z: 起始坐标

        Returns:
            {'x': float, 'y': float, 'z': float}
        """

        final_x = start_x + x * global_scale
        final_y = start_y + y * global_scale
        final_z = start_z + z * global_scale

        return final_x, final_y, final_z

    @staticmethod
    def get_template_by_id(template_id: int) -> Optional[BlockTemplate]:
        """
        根据template_id查找方块

        Args:
            template_id: 目标template_id

        Returns:
            BlockTemplate，未查找到则为None
        """
        for block in BlockConfig.AVAILABLE_BLOCKS:
            if block.template_id == template_id:
                return block
        return None

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """
        将16进制颜色转换为RGB

        Args:
            hex_color: 16进制颜色字符串，如 "#FF0000" 或 "FF0000"

        Returns:
            RGB元组，范围0-255
        """
        hex_color = hex_color.lstrip('#')
        return int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)

    @staticmethod
    def rgb_to_hsv(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
        """
        将RGB转换为HSV

        Args:
            rgb: RGB元组，范围0-255

        Returns:
            HSV元组
            - H: 色相 (0-360度)
            - S: 饱和度 (0-1)
            - V: 明度 (0-1)
        """
        r, g, b = [x / 255.0 for x in rgb]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return h * 360, s, v

    @staticmethod
    def color_distance_hsv(hsv1: Tuple[float, float, float],
                           hsv2: Tuple[float, float, float]) -> float:
        """
        计算两个HSV颜色之间的距离

        Args:
            hsv1, hsv2: HSV颜色元组

        Returns:
            float: 颜色距离
        """
        h1, s1, v1 = hsv1
        h2, s2, v2 = hsv2

        # 色相是循环的，计算最短角度距离
        dh = min(abs(h1 - h2), 360 - abs(h1 - h2)) / 360.0
        ds = abs(s1 - s2)
        dv = abs(v1 - v2)

        # 色相权重较高
        distance = math.sqrt(dh ** 2 * 2 + ds ** 2 + dv ** 2)
        return distance

    @staticmethod
    def find_closest_template(target_color: str,
                              templates: List[BlockTemplate]) -> BlockTemplate:
        """
        找到颜色最接近的模板模板

        Args:
            target_color: 目标颜色（16进制字符串）
            templates: 可用模板列表

        Returns:
            BlockTemplate: 最接近的模板
        """
        if not templates:
            raise ValueError("方块模板列表为空")

        target_rgb = BlockHelper.hex_to_rgb(target_color)
        target_hsv = BlockHelper.rgb_to_hsv(target_rgb)

        closest_template = None
        min_distance = float('inf')

        for template in templates:
            template_hsv = BlockHelper.rgb_to_hsv(template.color_tuple)
            distance = BlockHelper.color_distance_hsv(target_hsv, template_hsv)

            if distance < min_distance:
                min_distance = distance
                closest_template = template

        return closest_template