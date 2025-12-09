#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
二维码转3D方块生成器
将用户输入的字符串转为二维码，并生成对应的3D方块实体
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "proto_gen"))

import qrcode
from PIL import Image
from typing import List, Tuple
from model.block_model import BlockModel
from assembler.block_assembler import BlockAssembler
from helper.file_helper import FileHelper
from config.block_config import BlockTemplate
from helper.block_helper import BlockHelper


class Config:
    """二维码生成配置"""

    # 方块模板ID配置
    BLACK_TEMPLATE_ID = 20002121  # 黑色方块
    WHITE_TEMPLATE_ID = 20002146  # 白色方块

    # 全局缩放
    GLOBAL_SCALE = 1.0

    # 空间配置
    AXIS_MAPPING = {
        'horizontal': 'x',  # 二维码水平方向对应的轴
        'vertical': 'y',    # 二维码垂直方向对应的轴
        'depth': 'z'        # 二维码深度方向对应的轴
    }

    # 起始位置（左下角第一个方块的坐标）
    START_POSITION = {
        'x': 0.0,
        'y': 0.0,
        'z': 0.0
    }

    # 二维码配置
    QR_VERSION = 1  # 二维码版本（1-40）
    QR_ERROR_CORRECTION = qrcode.constants.ERROR_CORRECT_L  # 纠错级别
    QR_BOX_SIZE = 1  # 每个格子的像素大小
    QR_BORDER = 1  # 边框大小（格子数）

    # 起始实体ID
    ENTITY_ID_START = 1078000000


class QRCodeGenerator:
    """二维码图片生成器"""

    @staticmethod
    def generate(text: str) -> Image.Image:
        """
        生成二维码图片

        Args:
            text: 要编码的字符串

        Returns:
            PIL.Image: 二维码图片（黑白）
        """
        qr = qrcode.QRCode(
            version=Config.QR_VERSION,
            error_correction=Config.QR_ERROR_CORRECTION,
            box_size=Config.QR_BOX_SIZE,
            border=Config.QR_BORDER,
        )

        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        return img

    @staticmethod
    def get_pixels(img: Image.Image) -> List[List[bool]]:
        """
        读取二维码的像素数据

        Args:
            img: PIL图片对象

        Returns:
            list: 二维数组，True表示黑色，False表示白色
                  已翻转Y轴，[0][0]是左下角
        """
        img = img.convert('1')  # 转为黑白模式
        width, height = img.size
        pixels = []

        # 从下往上读取（翻转Y轴）
        for y in range(height - 1, -1, -1):
            row = []
            for x in range(width):
                pixel = img.getpixel((x, y))
                is_black = (pixel == 0)  # 0表示黑色
                row.append(is_black)
            pixels.append(row)

        return pixels


class QRBlockConverter:
    """将二维码像素转换为方块数据"""

    @staticmethod
    def calculate_position(qr_x: int, qr_y: int,
                           global_scale: float) -> Tuple[float, float, float]:
        """
        计算方块的3D世界坐标

        Args:
            qr_x: 二维码中的X坐标（列）
            qr_y: 二维码中的Y坐标（行，已翻转）
            global_scale: 全局缩放参数

        Returns:
            dict: {'x': float, 'y': float, 'z': float}
        """

        h_axis = Config.AXIS_MAPPING['horizontal']
        v_axis = Config.AXIS_MAPPING['vertical']
        d_axis = Config.AXIS_MAPPING['depth']

        position = {
            'x': Config.START_POSITION['x'] + qr_x * global_scale,
            'y': Config.START_POSITION['y'] + qr_y * global_scale,
            'z': Config.START_POSITION['z']
        }

        return position[h_axis], position[v_axis], position[d_axis]

    @staticmethod
    def pixels_to_blocks(pixels: List[List[bool]],
                         black_template: BlockTemplate,
                         white_template: BlockTemplate) -> List[BlockModel]:
        """
        将二维码像素转换为方块数据列表

        Args:
            pixels: 二维码像素数组
            black_template: 黑色方块模板
            white_template: 白色方块模板

        Returns:
            List[BlockModel]: 方块数据列表
        """
        blocks = []
        height = len(pixels)
        width = len(pixels[0]) if height > 0 else 0

        for y in range(height):
            for x in range(width):
                is_black = pixels[y][x]

                if is_black:
                    template = black_template
                    name = f"QR_黑_{x}_{y}"
                else:
                    template = white_template
                    name = f"QR_白_{x}_{y}"

                # 计算位置
                position_x, position_y, position_z = QRBlockConverter.calculate_position(
                    x, y,
                    Config.GLOBAL_SCALE
                )

                # 获取该模板的缩放值
                scale_x, scale_y, scale_z = BlockHelper.calculate_scale(template, Config.GLOBAL_SCALE)

                # 创建BlockModel
                block_data = BlockModel(
                    template_id=template.template_id,
                    name=name,
                    position_x=position_x,
                    position_y=position_y,
                    position_z=position_z,
                    scale_x=scale_x,
                    scale_y=scale_y,
                    scale_z=scale_z
                )

                blocks.append(block_data)

        return blocks


def main():
    print("当前配置:")
    print(f"  黑色方块模板ID: {Config.BLACK_TEMPLATE_ID}")
    print(f"  白色方块模板ID: {Config.WHITE_TEMPLATE_ID}")

    black_template = BlockHelper.get_template_by_id(Config.BLACK_TEMPLATE_ID)
    white_template = BlockHelper.get_template_by_id(Config.WHITE_TEMPLATE_ID)

    print()
    print(f"  起始位置: X={Config.START_POSITION['x']}, "
          f"Y={Config.START_POSITION['y']}, "
          f"Z={Config.START_POSITION['z']}")
    print(f"  坐标映射: 水平→{Config.AXIS_MAPPING['horizontal']}, "
          f"垂直→{Config.AXIS_MAPPING['vertical']}, "
          f"深度→{Config.AXIS_MAPPING['depth']}")
    print()

    text = input("请输入要生成二维码的文本: ").strip()

    if not text:
        print("Error: 输入为空，程序退出")
        return

    print()

    # 生成二维码
    print("生成二维码...")
    qr_generator = QRCodeGenerator()
    img = qr_generator.generate(text)
    width, height = img.size
    print(f"二维码大小: {width}x{height} 像素")

    # 保存二维码图片
    qr_filename = "output/qrcode_preview.png"
    os.makedirs(os.path.dirname(qr_filename), exist_ok=True)
    img.save(qr_filename)
    print(f"二维码预览已保存: {qr_filename}")
    print()

    print("读取像素数据...")
    pixels = qr_generator.get_pixels(img)

    # 统计黑白像素
    black_count = sum(sum(1 for pixel in row if pixel) for row in pixels)
    white_count = sum(sum(1 for pixel in row if not pixel) for row in pixels)
    total_count = black_count + white_count

    print(f"黑色像素: {black_count} 个")
    print(f"白色像素: {white_count} 个")
    print(f"总计: {total_count} 个方块")
    print()

    converter = QRBlockConverter()
    blocks = converter.pixels_to_blocks(
        pixels,
        black_template,
        white_template
    )
    print(f"已生成 {len(blocks)} 个方块数据")
    print()

    # 组装并保存
    print("组装实体并保存...")
    assembler = BlockAssembler(entity_id_start=Config.ENTITY_ID_START)
    proto_data = assembler.assemble(blocks)
    print(f"Protobuf数据大小: {len(proto_data)} 字节")

    # 保存为GIA文件
    output_filename = "output/qrcode_entities.gia"
    success = FileHelper.save(proto_data, output_filename)

    if success:
        print()
        print("=" * 70)
        print("生成完成！")
        print("=" * 70)
        print(f"输入文本: {text}")
        print(f"二维码大小: {width}x{height} 像素")
        print(f"方块数量: {total_count}")
        print(f"  - 黑色: {black_count}")
        print(f"  - 白色: {white_count}")
        print(f"实体ID范围: {Config.ENTITY_ID_START} - {assembler.current_entity_id - 1}")
        print(f"输出文件: {output_filename}")
        print(f"预览图片: {qr_filename}")
        print()
    else:
        print("Error: 保存失败")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print()
        print("Error: 程序被用户中断")
    except Exception as e:
        print()
        print(f"Error: {e}")

        import traceback
        traceback.print_exc()
