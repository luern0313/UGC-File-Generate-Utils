#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
镜头生成器
生成各种类型的镜头实例并保存到gia文件
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
from parser.parser_with_raw_data import decode_raw_protobuf


class Config:
    """配置类"""
    
    # 获取脚本所在目录的绝对路径
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # 导出gia文件路径
    OUTPUT_FILE = os.path.join(SCRIPT_DIR, "output/camera_templates.gia")
    
    # 是否导出单个镜头文件
    EXPORT_SINGLE = True
    
    # 单个镜头文件输出目录
    SINGLE_OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output/cameras/")


def parse_camera_data(parsed_data_str):
    """
    解析镜头数据字符串，返回结构化的镜头数据列表
    """
    # 简单的解析逻辑，逐行扫描
    lines = parsed_data_str.strip().split('\n')
    camera_data_list = []
    current_camera = None
    in_camera = False
    in_asset_meta = False
    in_camera_config = False
    in_camera_detail = False
    in_camera_data = False
    in_viewpoint_offset = False
    current_field = None
    
    # 解析文件级别的元数据
    file_metadata = {}
    in_file_metadata = True
    
    for line in lines:
        # 计算缩进级别
        indent = len(line) - len(line.lstrip(' '))
        level = indent // 2
        stripped_line = line.strip()
        
        if not stripped_line:
            continue
        
        # 处理文件级别的元数据
        if level == 0 and not in_camera and ':' in stripped_line and not stripped_line.endswith('{'):
            field_part, value_part = stripped_line.split(':', 1)
            field_number_str = field_part.strip()
            value_part = value_part.strip()
            
            if field_number_str.isdigit():
                field_number = int(field_number_str)
                # 提取字符串值
                if value_part.startswith('"') and value_part.endswith('"'):
                    # 直接保留原始字符串，包括引号和转义字符
                    # 我们需要的是原始字符串内容，而不是Python解释后的字符串
                    # 所以直接去掉引号，不做任何转义处理
                    file_metadata[field_number] = value_part[1:-1]
                # 提取整数值
                elif value_part.isdigit():
                    file_metadata[field_number] = int(value_part)
        # 处理顶层镜头开始
        elif stripped_line == '1 {' and level == 0:
            current_camera = {
                'asset_meta': {},
                'camera_data': {
                    'camera_id': 0,
                    'details': {},
                    'viewpoint_offset': {}
                }
            }
            camera_data_list.append(current_camera)
            in_camera = True
            in_file_metadata = False
        # 处理顶层镜头结束
        elif stripped_line == '}' and level == 0:
            in_camera = False
        # 处理AssetMeta开始
        elif stripped_line == '1 {' and level == 1 and in_camera:
            in_asset_meta = True
        # 处理AssetMeta结束
        elif stripped_line == '}' and level == 1 and in_asset_meta:
            in_asset_meta = False
        # 处理AssetMeta中的字段
        elif ':' in stripped_line and level == 2 and in_asset_meta:
            field_part, value_part = stripped_line.split(':', 1)
            field_number_str = field_part.strip()
            value_part = value_part.strip()
            
            if field_number_str.isdigit():
                field_number = int(field_number_str)
                # 提取整数值
                if value_part.isdigit():
                    current_camera['asset_meta'][field_number] = int(value_part)
        # 处理镜头名称
        elif stripped_line.startswith('3: "') and level == 1 and in_camera:
            camera_name = stripped_line.split(': "')[1].rstrip('"')
            current_camera['name'] = camera_name
        # 处理镜头类型
        elif stripped_line.startswith('5: ') and level == 1 and in_camera:
            type_value = stripped_line.split(': ')[1].strip()
            if type_value.isdigit():
                current_camera['type'] = int(type_value)
        # 处理CameraConfig开始
        elif stripped_line == '17 {' and level == 1 and in_camera:
            in_camera_config = True
        # 处理CameraConfig结束
        elif stripped_line == '}' and level == 1 and in_camera_config:
            in_camera_config = False
        # 处理CameraDetail列表开始
        elif stripped_line == '1 {' and level == 2 and in_camera_config:
            in_camera_detail = True
        # 处理CameraDetail列表结束
        elif stripped_line == '}' and level == 2 and in_camera_detail:
            in_camera_detail = False
        # 处理CameraDetail中的camera_id
        elif stripped_line.startswith('1: ') and level == 3 and in_camera_detail:
            camera_id_value = stripped_line.split(': ')[1].strip()
            if camera_id_value.isdigit():
                current_camera['camera_data']['camera_id'] = int(camera_id_value)
        # 处理CameraData开始
        elif stripped_line == '2 {' and level == 3 and in_camera_detail:
            in_camera_data = True
        # 处理CameraData结束
        elif stripped_line == '}' and level == 3 and in_camera_data:
            in_camera_data = False
        # 处理ViewpointOffset开始
        elif stripped_line == '4 {' and level == 4 and in_camera_data:
            in_viewpoint_offset = True
            current_camera['camera_data']['has_viewpoint_offset'] = True
        # 处理ViewpointOffset结束
        elif stripped_line == '}' and level == 4 and in_viewpoint_offset:
            in_viewpoint_offset = False
        # 处理ViewpointOffset中的字段
        elif ':' in stripped_line and level == 5 and in_viewpoint_offset:
            field_part, value_part = stripped_line.split(':', 1)
            field_number_str = field_part.strip()
            value_part = value_part.strip()
            
            if field_number_str.isdigit():
                field_number = int(field_number_str)
                # 提取浮点值
                if 'float: ' in value_part:
                    try:
                        float_value = float(value_part.split('float: ')[1].split(')')[0])
                        current_camera['camera_data']['viewpoint_offset'][field_number] = float_value
                    except (ValueError, IndexError):
                        pass
        # 处理CameraData中的字段
        elif ':' in stripped_line and level == 4 and in_camera_data and not in_viewpoint_offset:
            field_part, value_part = stripped_line.split(':', 1)
            field_number_str = field_part.strip()
            value_part = value_part.strip()
            
            if field_number_str.isdigit():
                field_number = int(field_number_str)
                
                # 处理空字符串
                if value_part == '""':
                    current_camera['camera_data']['details'][field_number] = ""
                # 提取浮点值
                elif 'float: ' in value_part:
                    try:
                        float_value = float(value_part.split('float: ')[1].split(')')[0])
                        current_camera['camera_data']['details'][field_number] = float_value
                    except (ValueError, IndexError):
                        pass
                # 提取整数值
                elif value_part.isdigit():
                    current_camera['camera_data']['details'][field_number] = int(value_part)
                # 提取字符串值
                elif value_part.startswith('"') and value_part.endswith('"'):
                    current_camera['camera_data']['details'][field_number] = value_part[1:-1]
    
    return camera_data_list, file_metadata

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
    print("镜头生成器")
    print("=" * 70)
    print()
    
    # 读取并解析"镜头.gia"文件
    print("读取并解析镜头.gia文件...")
    gia_file_path = os.path.join(os.path.dirname(__file__), "./镜头.gia")
    data, success = FileHelper.load(gia_file_path)
    if not success:
        print(f"Error: 读取文件失败: {gia_file_path}")
        return
    
    # 解析gia文件数据
    parsed_data_str = decode_raw_protobuf(data)
    print("解析完成")
    print()
    
    # 打印解析结果用于调试
    print("解析结果:")
    print(parsed_data_str)
    print()
    
    # 解析镜头数据
    camera_data_list, file_metadata = parse_camera_data(parsed_data_str)
    print(f"解析出 {len(camera_data_list)} 个镜头数据")
    print(f"文件元数据: {file_metadata}")
    # 打印文件元数据的详细信息
    for key, value in file_metadata.items():
        print(f"  元数据 {key}: {value} (类型: {type(value).__name__})")
    print()
    
    # 获取所有镜头模板
    print("获取镜头模板...")
    templates = CameraTemplateManager.get_all_templates()
    print(f"获取到 {len(templates)} 个镜头模板")
    print()
    
    # 将解析的数据赋值给对应的模板
    print("将解析的数据赋值给对应的模板...")
    for i, camera_data in enumerate(camera_data_list):
        print(f"  处理镜头数据 {i+1}: {camera_data['name']}")
        camera_name = camera_data.get('name')
        if not camera_name:
            print(f"  Warning: 镜头数据 {i+1} 没有名称")
            continue
        
        # 找到对应的模板
        template = CameraTemplateManager.get_template_by_name(camera_name)
        if not template:
            print(f"  Warning: 找不到名称为'{camera_name}'的模板")
            continue
        
        # 获取镜头详细数据
        camera_data_dict = camera_data.get('camera_data', {})
        details = camera_data_dict.get('details', {})
        viewpoint_offset = camera_data_dict.get('viewpoint_offset', {})
        
        print(f"  镜头ID: {camera_data_dict.get('camera_id')}")
        print(f"  AssetMeta: {camera_data.get('asset_meta')}")
        print(f"  镜头详细数据: {details}")
        print(f"  视点偏移: {viewpoint_offset}")
        
        # 更新模板数据
        # 字段映射：
        # 1-名称，2-默认视距，3-视野，4-视点偏移，5-最小视距，6-最大视距，
        # 12-镜头模式，13-跟随旋转，14-field_14，15-最小水平角度，16-最大水平角度，
        # 17-最小俯仰角度，18-最大俯仰角度，20-水平角度
        
        # 更新默认视距
        if 2 in details:
            template.default_distance = details[2]
            print(f"    更新默认视距: {details[2]}")
        
        # 更新视野
        if 3 in details:
            template.field_of_view = details[3]
            print(f"    更新视野: {details[3]}")
        
        # 更新最小视距
        if 5 in details:
            template.min_distance = details[5]
            print(f"    更新最小视距: {details[5]}")
        
        # 更新最大视距
        if 6 in details:
            template.max_distance = details[6]
            print(f"    更新最大视距: {details[6]}")
        
        # 更新镜头模式
        if 12 in details:
            template.camera_mode = details[12]
            print(f"    更新镜头模式: {details[12]}")
        
        # 更新跟随旋转
        if 13 in details:
            template.follow_rotation = bool(details[13])
            print(f"    更新跟随旋转: {bool(details[13])}")
        
        # 更新field_14
        if 14 in details:
            template.field_14 = details[14]
            print(f"    更新field_14: {details[14]}")
        
        # 更新最小水平角度
        if 15 in details:
            template.min_horizontal_angle = details[15]
            print(f"    更新最小水平角度: {details[15]}")
        
        # 更新最大水平角度
        if 16 in details:
            template.max_horizontal_angle = details[16]
            print(f"    更新最大水平角度: {details[16]}")
        
        # 更新最小俯仰角度
        if 17 in details:
            template.min_pitch_angle = details[17]
            print(f"    更新最小俯仰角度: {details[17]}")
        
        # 更新最大俯仰角度
        if 18 in details:
            template.max_pitch_angle = details[18]
            print(f"    更新最大俯仰角度: {details[18]}")
        
        # 更新水平角度
        if 20 in details:
            template.horizontal_angle = details[20]
            print(f"    更新水平角度: {details[20]}")
        
        # 更新视点偏移
        if camera_data_dict.get('has_viewpoint_offset', False):
            template.viewpoint_offset = ViewpointOffset(
                x=viewpoint_offset.get(1, 0.0),
                y=viewpoint_offset.get(2, 0.0),
                z=viewpoint_offset.get(3, 0.0)
            )
            print(f"    更新视点偏移: {template.viewpoint_offset}")
        
        # 保存镜头ID到模板
        template.camera_id = camera_data_dict.get('camera_id', 0)
        
        # 保存asset_id到模板
        if 'asset_meta' in camera_data and 4 in camera_data['asset_meta']:
            template.asset_id = camera_data['asset_meta'][4]
            print(f"    更新asset_id: {template.asset_id}")
        
        print(f"  已更新模板: {camera_name}")
    print()
    
    # 显示镜头模板信息
    print("镜头模板列表:")
    for i, template in enumerate(templates):
        print(f"  {i+1}. {template.name} (模式: {template.camera_mode})")
        print(f"     视野: {template.field_of_view}°, 默认视距: {template.default_distance}")
        print(f"     视距范围: {template.min_distance} - {template.max_distance}")
        print(f"     跟随旋转: {'是' if template.follow_rotation else '否'}")
        print(f"     忽略碰撞: {'是' if template.ignore_collision else '否'}")
    print()
    
    # 批量生成所有镜头
    print("批量生成所有镜头...")
    # 使用assembler生成方式
    proto_data = generate_raw_camera_protobuf(templates, file_metadata)
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
    
    print()
    print("=" * 70)
    print("生成完成！")
    print("=" * 70)
    print(f"批量输出文件: {Config.OUTPUT_FILE}")
    if Config.EXPORT_SINGLE:
        print(f"单个镜头输出目录: {Config.SINGLE_OUTPUT_DIR}")
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
