#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
像素画生成器
将图片转换为方块组成的像素画
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "proto_gen"))

import tkinter as tk
from tkinter import filedialog
from PIL import Image
from typing import List, Tuple
from model.block_model import BlockModel
from assembler.block_assembler import BlockAssembler
from helper.file_helper import FileHelper
from config.block_config import BlockTemplate, BlockConfig
from helper.block_helper import BlockHelper


class Config:
    OUTPUT_WIDTH = 240  # 输出宽度
    OUTPUT_HEIGHT = 240  # 输出高度

    # 全局缩放
    GLOBAL_SCALE = 0.1

    # 忽略透明像素阈值
    ALPHA_THRESHOLD = 128

    AXIS_MAPPING = {
        'horizontal': 'x',  # 图片水平方向对应的轴
        'vertical': 'y',  # 图片垂直方向对应的轴
        'depth': 'z'  # 图片深度方向对应的轴
    }

    # 起始位置（左下角第一个方块的坐标）
    START_POSITION = {
        'x': 0.0,
        'y': 0.0,
        'z': 0.0
    }

    KEEP_ASPECT_RATIO = True  # 保持图片宽高比
    RESIZE_METHOD = Image.LANCZOS  # 缩放算法

    # 起始实体ID
    ENTITY_ID_START = 1078000000


class ImageSelector:
    """选择图片"""

    @staticmethod
    def select_file() -> str:
        """
        弹出文件选择对话框

        Returns:
            str: 选择的图片文件路径
        """
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口

        file_path = filedialog.askopenfilename(
            title="选择图片文件",
            filetypes=[
                ("图片文件", "*.png *.jpg *.jpeg *.bmp *.gif *.webp"),
                ("所有文件", "*.*")
            ]
        )

        return file_path


class ImageProcessor:
    """图片处理"""

    @staticmethod
    def load_and_resize(
            image_path: str,
            target_width: int,
            target_height: int,
            keep_aspect: bool = True,
            resize_method=Image.LANCZOS
    ) -> Image.Image:
        """
        加载并调整图片大小

        Args:
            image_path: 图片路径
            target_width: 目标宽度
            target_height: 目标高度
            keep_aspect: 是否保持宽高比
            resize_method: 缩放算法

        Returns:
            Image.Image: 调整后的图片
        """
        # 加载图片
        img = Image.open(image_path)

        # 转换为RGBA模式
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # 计算缩放尺寸
        if keep_aspect:
            # 保持宽高比，按较小的缩放比例
            img_width, img_height = img.size
            width_ratio = target_width / img_width
            height_ratio = target_height / img_height
            scale_ratio = min(width_ratio, height_ratio)

            new_width = int(img_width * scale_ratio)
            new_height = int(img_height * scale_ratio)
        else:
            new_width = target_width
            new_height = target_height

        # 缩放图片
        img_resized = img.resize((new_width, new_height), resize_method)

        return img_resized

    @staticmethod
    def get_pixel_colors(img: Image.Image) -> List[List[Tuple[int, int, int, int]]]:
        """
        获取图片的所有像素颜色

        Args:
            img: PIL图片对象

        Returns:
            List[List[Tuple[int, int, int]]]: 二维数组，每个元素是RGBA元组
                                               已翻转Y轴，[0][0]是左下角
        """
        width, height = img.size
        pixels = []

        # 翻转Y轴
        for y in range(height - 1, -1, -1):
            row = []
            for x in range(width):
                rgba = img.getpixel((x, y))
                row.append(rgba)
            pixels.append(row)

        return pixels


class ImageBlockConverter:
    """将图片像素转换为方块数据"""

    @staticmethod
    def calculate_position(img_x: int, img_y: int,
                           global_scale: float) -> Tuple[float, float, float]:
        """
        计算方块的3D世界坐标

        Args:
            img_x: 图片X坐标（列）
            img_y: 图片Y坐标（行，已翻转）
            global_scale: 全局缩放参数

        Returns:
            Tuple[float, float, float]: (x, y, z) 坐标
        """
        h_axis = Config.AXIS_MAPPING['horizontal']
        v_axis = Config.AXIS_MAPPING['vertical']
        d_axis = Config.AXIS_MAPPING['depth']

        position = {
            'x': Config.START_POSITION['x'] + img_x * global_scale,
            'y': Config.START_POSITION['y'] + img_y * global_scale,
            'z': Config.START_POSITION['z']
        }

        return position[h_axis], position[v_axis], position[d_axis]

    @staticmethod
    def pixels_to_blocks(pixels: List[List[Tuple[int, int, int, int]]],
                         templates: List[BlockTemplate]) -> List[BlockModel]:
        """
        将像素颜色转换为方块数据列表

        Args:
            pixels: 像素颜色数组
            templates: 可用模板列表

        Returns:
            List[BlockModel]: 方块数据列表
        """
        blocks = []
        height = len(pixels)
        width = len(pixels[0]) if height > 0 else 0

        total_pixels = width * height
        processed = 0

        for y in range(height):
            for x in range(width):
                rgba = pixels[y][x]

                if rgba[3] < Config.ALPHA_THRESHOLD:
                    processed += 1
                    continue

                # 查找最匹配的模板
                template = BlockHelper.find_closest_template_rgb((rgba[0], rgba[1], rgba[2]), templates)

                # 计算位置
                position_x, position_y, position_z = ImageBlockConverter.calculate_position(
                    x, y,
                    Config.GLOBAL_SCALE
                )

                # 获取该模板的缩放值
                scale_x, scale_y, scale_z = BlockHelper.calculate_scale(
                    template,
                    Config.GLOBAL_SCALE
                )

                # 创建方块数据
                block = BlockModel(
                    template_id=template.template_id,
                    name=f"Pixel_{x}_{y}",
                    position_x=position_x,
                    position_y=position_y,
                    position_z=position_z,
                    scale_x=scale_x,
                    scale_y=scale_y,
                    scale_z=scale_z
                )

                blocks.append(block)

                # 显示进度
                processed += 1
                if processed % 100 == 0 or processed == total_pixels:
                    progress = (processed / total_pixels) * 100
                    print(f"\r  进度: {processed}/{total_pixels} ({progress:.1f}%)", end='')

        print()  # 换行
        return blocks


def main():
    print("当前配置:")
    print(f"  输出分辨率: {Config.OUTPUT_WIDTH}x{Config.OUTPUT_HEIGHT}")
    print(f"  保持宽高比: {'是' if Config.KEEP_ASPECT_RATIO else '否'}")
    print(f"  全局缩放: {Config.GLOBAL_SCALE}")
    print(f"  起始位置: X={Config.START_POSITION['x']}, "
          f"Y={Config.START_POSITION['y']}, "
          f"Z={Config.START_POSITION['z']}")
    print(f"  坐标映射: 水平→{Config.AXIS_MAPPING['horizontal']}, "
          f"垂直→{Config.AXIS_MAPPING['vertical']}, "
          f"深度→{Config.AXIS_MAPPING['depth']}")
    print()

    print("选择图片文件...")
    image_path = ImageSelector.select_file()

    if not image_path:
        print("Error: 未选择图片，程序退出")
        return

    print(f"已选择图片: {image_path}")
    print()

    print("加载并处理图片...")
    try:
        img = ImageProcessor.load_and_resize(
            image_path,
            Config.OUTPUT_WIDTH,
            Config.OUTPUT_HEIGHT,
            keep_aspect=Config.KEEP_ASPECT_RATIO,
            resize_method=Config.RESIZE_METHOD
        )
        actual_width, actual_height = img.size
        print(f"图片已调整为: {actual_width}x{actual_height} 像素")

        # 保存预览图
        preview_path = "output/image_preview_resized.png"
        os.makedirs(os.path.dirname(preview_path), exist_ok=True)
        img.save(preview_path)
        print(f"预览图已保存: {preview_path}")
    except Exception as e:
        print(f"Error: 处理图片失败: {e}")
        return
    print()

    pixels = ImageProcessor.get_pixel_colors(img)

    try:
        blocks = ImageBlockConverter.pixels_to_blocks(pixels, BlockConfig.AVAILABLE_BLOCKS)
        print(f"成功转换 {len(blocks)} 个方块")
    except Exception as e:
        print(f"Error: 转换失败: {e}")
        import traceback
        traceback.print_exc()
        return
    print()

    # 统计模板使用情况
    print("方块模板使用统计:")
    template_stats = {}
    for block in blocks:
        template_stats[block.template_id] = template_stats.get(block.template_id, 0) + 1

    for template_id, count in sorted(template_stats.items(), key=lambda x: -x[1])[:10]:
        template = next((t for t in BlockConfig.AVAILABLE_BLOCKS if t.template_id == template_id), None)
        if template:
            percentage = (count / len(blocks)) * 100
            print(f"  模板 {template_id} RGB{template.color_tuple}: "
                  f"{count} 个 ({percentage:.1f}%)")

    if len(template_stats) > 10:
        print(f"  ... 还有 {len(template_stats) - 10} 种模板")
    print()

    # 组装并保存
    print("组装实体并保存...")
    assembler = BlockAssembler(entity_id_start=Config.ENTITY_ID_START)
    proto_data = assembler.assemble(blocks)
    print(f"Protobuf数据大小: {len(proto_data)} 字节")

    output_filename = f"output/image_pixelart.gia"
    success = FileHelper.save(proto_data, output_filename)

    if success:
        print()
        print("=" * 70)
        print("生成完成！")
        print("=" * 70)
        print(f"输入图片: {image_path}")
        print(f"原始尺寸: {Image.open(image_path).size[0]}x{Image.open(image_path).size[1]} 像素")
        print(f"输出分辨率: {actual_width}x{actual_height} 方块")
        print(f"方块总数: {len(blocks)}")
        print(f"使用模板种类: {len(template_stats)}")
        print(f"实体ID范围: {Config.ENTITY_ID_START} - {assembler.current_entity_id - 1}")
        print()
    else:
        print("Error: 保存失败")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Error: 程序被用户中断")
    except Exception as e:
        print(f"Error: {e}")

        import traceback

        traceback.print_exc()
