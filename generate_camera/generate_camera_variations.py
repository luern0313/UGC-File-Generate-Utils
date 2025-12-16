#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
镜头变体生成器
使用第三人称模板生成各种参数的镜头变体并保存到gia文件
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
# 添加proto_gen目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), "../proto_gen"))

from typing import List

from model.camera_model import CameraTemplateManager, CameraTemplate, ViewpointOffset
from assembler.camera_assembler import CameraAssembler
from helper.file_helper import FileHelper


class Config:
    """配置类"""
    
    # 获取脚本所在目录的绝对路径
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # 导出gia文件路径
    OUTPUT_FILE = os.path.join(SCRIPT_DIR, "output/camera_variations.gia")
    
    # 第三人称镜头模板
    BASE_TEMPLATE = CameraTemplateManager.THIRD_PERSON_TEMPLATE
    
    # 起始资产ID
    START_ASSET_ID = 1000000000


def generate_horizontal_angle_lenses(base_template: CameraTemplate, start_asset_id: int) -> List[CameraTemplate]:
    """
    生成水平角限制范围变化的镜头
    水平角限制范围，上下限相等，且值从-180递增1°到180，镜头名字用角度数字加500后的数字
    
    Args:
        base_template: 基础镜头模板
        start_asset_id: 起始资产ID
        
    Returns:
        生成的镜头模板列表
    """
    lenses = []
    asset_id = start_asset_id
    
    # 水平角度从-180到180，步长1°
    for angle in range(-180, 181):
        # 创建模板副本
        lens = CameraTemplate(
            name=f"{angle + 500}",  # 镜头名字用角度数字加500后的数字
            camera_mode=base_template.camera_mode,
            default_distance=base_template.default_distance,
            min_distance=base_template.min_distance,
            max_distance=base_template.max_distance,
            viewpoint_offset=ViewpointOffset(
                x=base_template.viewpoint_offset.x,
                y=base_template.viewpoint_offset.y,
                z=base_template.viewpoint_offset.z
            ),
            follow_rotation=base_template.follow_rotation,
            horizontal_angle=base_template.horizontal_angle,
            min_horizontal_angle=angle,  # 水平角下限等于当前角度
            max_horizontal_angle=angle,  # 水平角上限等于当前角度
            min_pitch_angle=base_template.min_pitch_angle,
            max_pitch_angle=base_template.max_pitch_angle,
            ignore_collision=base_template.ignore_collision,
            field_14=base_template.field_14,
            asset_id=asset_id,
            camera_id=asset_id,
            field_of_view=base_template.field_of_view
        )
        lenses.append(lens)
        asset_id += 1
    
    return lenses, asset_id


def generate_pitch_angle_lenses(base_template: CameraTemplate, start_asset_id: int) -> List[CameraTemplate]:
    """
    生成俯仰角限制范围变化的镜头
    俯仰角限制范围，上下限相等，且值从-89递增1°到89，镜头名字用角度数字加1000后的字符
    
    Args:
        base_template: 基础镜头模板
        start_asset_id: 起始资产ID
        
    Returns:
        生成的镜头模板列表
    """
    lenses = []
    asset_id = start_asset_id
    
    # 俯仰角度从-89到89，步长1°
    for angle in range(-89, 90):
        # 创建模板副本
        lens = CameraTemplate(
            name=f"{angle + 1000}",  # 镜头名字用角度数字加1000后的字符
            camera_mode=base_template.camera_mode,
            default_distance=base_template.default_distance,
            min_distance=base_template.min_distance,
            max_distance=base_template.max_distance,
            viewpoint_offset=ViewpointOffset(
                x=base_template.viewpoint_offset.x,
                y=base_template.viewpoint_offset.y,
                z=base_template.viewpoint_offset.z
            ),
            follow_rotation=base_template.follow_rotation,
            horizontal_angle=base_template.horizontal_angle,
            min_horizontal_angle=base_template.min_horizontal_angle,
            max_horizontal_angle=base_template.max_horizontal_angle,
            min_pitch_angle=angle,  # 俯仰角下限等于当前角度
            max_pitch_angle=angle,  # 俯仰角上限等于当前角度
            ignore_collision=base_template.ignore_collision,
            field_14=base_template.field_14,
            asset_id=asset_id,
            camera_id=asset_id,
            field_of_view=base_template.field_of_view
        )
        lenses.append(lens)
        asset_id += 1
    
    return lenses, asset_id


def generate_distance_lenses(base_template: CameraTemplate, start_asset_id: int) -> List[CameraTemplate]:
    """
    生成视距限制范围变化的镜头
    视距限制范围，上下限相等，且值从1递增0.1到30，默认视距与上下限相同，镜头名字用距离数字乘以10取整再加1500后的字符
    
    Args:
        base_template: 基础镜头模板
        start_asset_id: 起始资产ID
        
    Returns:
        生成的镜头模板列表
    """
    lenses = []
    asset_id = start_asset_id
    
    # 视距从1到30，步长0.1，使用整数计算以避免浮点数精度问题
    for i in range(0, 291):  # 291个值：1.0, 1.1, ..., 30.0
        # 使用整数计算距离，避免浮点数累加误差
        distance = 1.0 + i * 0.1
        # 四舍五入到一位小数，确保精度
        distance = round(distance, 1)
        
        # 创建模板副本
        lens = CameraTemplate(
            name=f"{int(distance * 10) + 1500}",  # 镜头名字用距离数字乘以10取整再加1500后的字符
            camera_mode=base_template.camera_mode,
            default_distance=distance,  # 默认视距等于当前距离
            min_distance=distance,  # 视距下限等于当前距离
            max_distance=distance,  # 视距上限等于当前距离
            viewpoint_offset=ViewpointOffset(
                x=base_template.viewpoint_offset.x,
                y=base_template.viewpoint_offset.y,
                z=base_template.viewpoint_offset.z
            ),
            follow_rotation=base_template.follow_rotation,
            horizontal_angle=base_template.horizontal_angle,
            min_horizontal_angle=base_template.min_horizontal_angle,
            max_horizontal_angle=base_template.max_horizontal_angle,
            min_pitch_angle=base_template.min_pitch_angle,
            max_pitch_angle=base_template.max_pitch_angle,
            ignore_collision=base_template.ignore_collision,
            field_14=base_template.field_14,
            asset_id=asset_id,
            camera_id=asset_id,
            field_of_view=base_template.field_of_view
        )
        lenses.append(lens)
        asset_id += 1
    
    return lenses, asset_id


def generate_fov_lenses(base_template: CameraTemplate, start_asset_id: int) -> List[CameraTemplate]:
    """
    生成视野变化的镜头
    镜头视野，值从30递增1°到60，镜头名字用角度数字加2000后的字符
    
    Args:
        base_template: 基础镜头模板
        start_asset_id: 起始资产ID
        
    Returns:
        生成的镜头模板列表
    """
    lenses = []
    asset_id = start_asset_id
    
    # 视野从30到60，步长1°
    for fov in range(30, 61):
        # 创建模板副本
        lens = CameraTemplate(
            name=f"{fov + 2000}",  # 镜头名字用角度数字加2000后的字符
            camera_mode=base_template.camera_mode,
            default_distance=base_template.default_distance,
            min_distance=base_template.min_distance,
            max_distance=base_template.max_distance,
            viewpoint_offset=ViewpointOffset(
                x=base_template.viewpoint_offset.x,
                y=base_template.viewpoint_offset.y,
                z=base_template.viewpoint_offset.z
            ),
            follow_rotation=base_template.follow_rotation,
            horizontal_angle=base_template.horizontal_angle,
            min_horizontal_angle=base_template.min_horizontal_angle,
            max_horizontal_angle=base_template.max_horizontal_angle,
            min_pitch_angle=base_template.min_pitch_angle,
            max_pitch_angle=base_template.max_pitch_angle,
            ignore_collision=base_template.ignore_collision,
            field_14=base_template.field_14,
            asset_id=asset_id,
            camera_id=asset_id,
            field_of_view=fov  # 视野等于当前角度
        )
        lenses.append(lens)
        asset_id += 1
    
    return lenses, asset_id


def generate_raw_camera_protobuf(templates: List[CameraTemplate], file_metadata: dict) -> bytes:
    """
    使用assembler生成相机数据
    
    Args:
        templates: 镜头模板列表
        file_metadata: 文件元数据
        
    Returns:
        序列化后的protobuf字节数据
    """
    assembler = CameraAssembler()
    return assembler.assemble(templates, file_metadata)


def main():
    """主函数"""
    print("=" * 70)
    print("镜头变体生成器")
    print("=" * 70)
    print()
    
    # 生成各种类型的镜头
    print("生成各种类型的镜头...")
    
    all_lenses = []
    asset_id = Config.START_ASSET_ID
    
    # 1. 生成水平角限制范围变化的镜头
    print("生成水平角限制范围变化的镜头...")
    horizontal_lenses, asset_id = generate_horizontal_angle_lenses(Config.BASE_TEMPLATE, asset_id)
    all_lenses.extend(horizontal_lenses)
    print(f"生成了 {len(horizontal_lenses)} 个水平角限制范围变化的镜头")
    
    # 2. 生成俯仰角限制范围变化的镜头
    print("生成俯仰角限制范围变化的镜头...")
    pitch_lenses, asset_id = generate_pitch_angle_lenses(Config.BASE_TEMPLATE, asset_id)
    all_lenses.extend(pitch_lenses)
    print(f"生成了 {len(pitch_lenses)} 个俯仰角限制范围变化的镜头")
    
    # 3. 生成视距限制范围变化的镜头
    print("生成视距限制范围变化的镜头...")
    distance_lenses, asset_id = generate_distance_lenses(Config.BASE_TEMPLATE, asset_id)
    all_lenses.extend(distance_lenses)
    print(f"生成了 {len(distance_lenses)} 个视距限制范围变化的镜头")
    
    # 4. 生成视野变化的镜头
    print("生成视野变化的镜头...")
    fov_lenses, asset_id = generate_fov_lenses(Config.BASE_TEMPLATE, asset_id)
    all_lenses.extend(fov_lenses)
    print(f"生成了 {len(fov_lenses)} 个视野变化的镜头")
    
    print(f"总共生成了 {len(all_lenses)} 个镜头")
    print()
    
    # 文件元数据 - 可以为空字典，因为我们不使用它
    file_metadata = {}
    
    # 批量生成所有镜头
    print("批量生成所有镜头...")
    proto_data = generate_raw_camera_protobuf(all_lenses, file_metadata)
    print(f"Protobuf数据大小: {len(proto_data)} 字节")
    print()
    
    # 创建output目录
    os.makedirs(os.path.dirname(Config.OUTPUT_FILE), exist_ok=True)
    
    # 保存到gia文件
    print("保存到gia文件...")
    success = FileHelper.save(proto_data, Config.OUTPUT_FILE)
    
    if success:
        print(f"成功保存到: {Config.OUTPUT_FILE}")
    else:
        print(f"Error: 保存失败: {Config.OUTPUT_FILE}")
    print()
    
    print("=" * 70)
    print("生成完成！")
    print("=" * 70)
    print(f"批量输出文件: {Config.OUTPUT_FILE}")
    print()


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
