#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
镜头组装工具类
将镜头模板数据转换为protobuf格式的镜头数据
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
# 添加proto_gen目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), "../proto_gen"))

from typing import List
from model.camera_model import CameraTemplate, CameraTemplateManager
from proto_gen.asset_pb2 import Asset, AssetMeta
from proto_gen.camera_pb2 import CameraConfig, CameraDetail, CameraData, ViewpointOffset
from proto_gen.gia_pb2 import GIACollection

# 导入google.protobuf.internal模块，用于直接操作protobuf字段
from google.protobuf.internal import encoder, decoder, wire_format


class CameraAssembler:
    """
    镜头组装器
    将镜头模板转换为protobuf格式的镜头数据
    """
    
    def __init__(self):
        """初始化镜头组装器"""
        pass
    
    @staticmethod
    def _create_asset_meta(asset_id: int) -> AssetMeta:
        """
        构建资产元信息 (AssetMeta)
        
        Args:
            asset_id: 资产ID
            
        Returns:
            资产元信息对象
        """
        return AssetMeta(
            field_2=25,  # 镜头资产的field_2值为25
            asset_id=asset_id
            # 注意：不设置meta_type字段，使用默认值
        )
    
    def assemble(self, templates: List[CameraTemplate], file_metadata: dict) -> bytes:
        """
        批量转换并序列化镜头模板
        
        Args:
            templates: 镜头模板列表
            file_metadata: 文件元数据
            
        Returns:
            序列化后的protobuf字节数据
        """
        # 创建一个空的字节流，用于存储所有protobuf数据
        import io
        from google.protobuf.internal import encoder
        
        output = io.BytesIO()
        
        # 为每个镜头模板创建一个Asset
        for template in templates:
            # 创建Asset
            asset = Asset()
            
            # 设置Asset基本信息
            asset.name = template.name
            asset.type = Asset.CAMERA
            
            # 设置AssetMeta
            asset.meta.field_2 = 25  # 镜头资产的field_2值为25
            asset.meta.asset_id = template.camera_id  # 使用模板中的camera_id
            asset.meta.meta_type = AssetMeta.CAMERA
            
            # 创建CameraConfig
            camera_config = asset.camera_config
            
            # 创建CameraDetail
            camera_detail = camera_config.camera_details.add()
            camera_detail.camera_id = template.camera_id  # 使用模板中的camera_id
            
            # 创建CameraData
            camera_data = camera_detail.camera_data
            
            # 设置镜头详细数据
            camera_data.name = template.name
            camera_data.default_distance = template.default_distance
            camera_data.field_of_view = template.field_of_view
            camera_data.min_distance = template.min_distance
            camera_data.max_distance = template.max_distance
            
            # 只在模板中存在camera_mode时设置，经典镜头在原始文件中没有camera_mode字段
            if template.camera_mode != CameraTemplateManager.CameraMode.CLASSIC:
                camera_data.camera_mode = template.camera_mode
            
            camera_data.follow_rotation = template.follow_rotation
            camera_data.field_14 = template.field_14
            
            # 对于第三人称镜头，设置最小和最大水平角度以及俯仰角度
            if template.camera_mode == CameraTemplateManager.CameraMode.THIRD_PERSON:
                camera_data.min_horizontal_angle = template.min_horizontal_angle
                camera_data.max_horizontal_angle = template.max_horizontal_angle
                camera_data.min_pitch_angle = template.min_pitch_angle
                camera_data.max_pitch_angle = template.max_pitch_angle
            # 对于2.5D镜头，设置最小和最大俯仰角度以及水平角度
            elif template.camera_mode == CameraTemplateManager.CameraMode.CAMERA_2_5D:
                camera_data.min_pitch_angle = template.min_pitch_angle
                camera_data.max_pitch_angle = template.max_pitch_angle
                camera_data.horizontal_angle = template.horizontal_angle
            # 对于第一人称、经典镜头和3D背镜头，设置所有角度字段
            elif template.camera_mode in [CameraTemplateManager.CameraMode.FIRST_PERSON, CameraTemplateManager.CameraMode.CLASSIC, CameraTemplateManager.CameraMode.BACK_CAMERA]:
                camera_data.min_horizontal_angle = template.min_horizontal_angle
                camera_data.max_horizontal_angle = template.max_horizontal_angle
                camera_data.min_pitch_angle = template.min_pitch_angle
                camera_data.max_pitch_angle = template.max_pitch_angle
            
            # 设置视点偏移
            if template.viewpoint_offset:
                camera_data.viewpoint_offset.x = template.viewpoint_offset.x
                camera_data.viewpoint_offset.y = template.viewpoint_offset.y
                camera_data.viewpoint_offset.z = template.viewpoint_offset.z
            
            # 序列化Asset并写入输出流
            asset_bytes = asset.SerializeToString()
            
            # 写入Asset数据，field_number=1, wire_type=2 (LENGTH_DELIMITED)
            tag = 1 << 3 | 2  # field_number=1, wire_type=2
            encoder._EncodeVarint(output.write, tag)
            encoder._EncodeVarint(output.write, len(asset_bytes))
            output.write(asset_bytes)
        
        # 写入文件元数据，使用与原始文件相同的顺序
        # 字段3: 文件名称 (string)
        if 3 in file_metadata:
            file_name = file_metadata[3]
            # 计算UTF-8编码后的字节数作为长度
            file_name_bytes = file_name.encode('utf-8')
            tag = 3 << 3 | 2  # field_number=3, wire_type=2 (LENGTH_DELIMITED)
            encoder._EncodeVarint(output.write, tag)
            # 使用字节长度，而不是字符长度
            encoder._EncodeVarint(output.write, len(file_name_bytes))
            # 写入UTF-8编码后的字节
            output.write(file_name_bytes)
        
        # 字段5: 版本号 (string)
        if 5 in file_metadata:
            version = file_metadata[5]
            # 计算UTF-8编码后的字节数作为长度
            version_bytes = version.encode('utf-8')
            tag = 5 << 3 | 2  # field_number=5, wire_type=2 (LENGTH_DELIMITED)
            encoder._EncodeVarint(output.write, tag)
            # 使用字节长度，而不是字符长度
            encoder._EncodeVarint(output.write, len(version_bytes))
            # 写入UTF-8编码后的字节
            output.write(version_bytes)
        
        # 返回最终的字节数据
        return output.getvalue()
    
    def assemble_single(self, template: CameraTemplate) -> bytes:
        """
        转换并序列化单个镜头模板
        
        Args:
            template: 镜头模板
            
        Returns:
            序列化后的protobuf字节数据
        """
        return self.assemble([template])
