#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
镜头模板模型
根据proto定义和UI配置，为每种镜头类型提供默认参数和取值范围
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ViewpointOffset:
    """视点偏移"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    # 视点偏移不限制范围


@dataclass
class CameraTemplate:
    """镜头模板"""
    # 基础参数
    name: str
    camera_mode: int
    
    # 视距参数
    default_distance: float
    min_distance: float
    max_distance: float
    
    # 视点偏移
    viewpoint_offset: ViewpointOffset
    
    # 旋转参数
    follow_rotation: bool
    horizontal_angle: float
    min_horizontal_angle: float
    max_horizontal_angle: float
    min_pitch_angle: float
    max_pitch_angle: float
    
    # 碰撞参数
    ignore_collision: bool
    
    # 未知字段
    field_14: float
    
    # 资产ID - 非默认参数必须在默认参数之前
    asset_id: int = None
    camera_id: int = 0
    
    # 视野参数 - 默认参数必须在非默认参数之后
    field_of_view: float = 45.0  # 统一默认FOV为45
    
    # 可设置参数标记 - 默认参数
    can_edit_fov: bool = True
    can_edit_distance: bool = True
    can_edit_viewpoint_offset: bool = True
    can_edit_follow_rotation: bool = True
    can_edit_horizontal_angle: bool = True
    can_edit_horizontal_angle_range: bool = True
    can_edit_pitch_angle_range: bool = True
    can_edit_ignore_collision: bool = True
    
    # 取值范围限制
    # 视距范围
    DISTANCE_MIN = 0.1
    DISTANCE_MAX = 50.0
    
    # 视野范围
    FIELD_OF_VIEW_MIN = 30.0
    FIELD_OF_VIEW_MAX = 60.0
    
    # 水平角度范围
    HORIZONTAL_ANGLE_MIN = -180.0
    HORIZONTAL_ANGLE_MAX = 180.0
    
    # 俯仰角度范围
    PITCH_ANGLE_MIN = -89.0
    PITCH_ANGLE_MAX = 89.0
    
    # 未知字段范围
    FIELD_14_MIN = 0.0
    FIELD_14_MAX = 1.0


class CameraTemplateManager:
    """镜头模板管理器"""
    
    # 镜头模式枚举
    class CameraMode:
        UNKNOWN = 0
        THIRD_PERSON = 4
        CLASSIC = 5
        FIRST_PERSON = 3
        BACK_CAMERA = 1
        CAMERA_2_5D = 2
    
    # 预定义镜头模板
    
    # 2.5D镜头模板
    CAMERA_2_5D_TEMPLATE = CameraTemplate(
        name="2.5D镜头",
        camera_mode=CameraMode.CAMERA_2_5D,
        default_distance=15.0,
        min_distance=3.0,
        max_distance=25.0,
        field_of_view=45.0,  # 统一默认FOV为45
        viewpoint_offset=ViewpointOffset(x=0.0, y=0.0, z=0.0),
        follow_rotation=True,
        horizontal_angle=0.0,
        min_horizontal_angle=-180.0,
        max_horizontal_angle=180.0,
        min_pitch_angle=-89.0,
        max_pitch_angle=89.0,
        ignore_collision=False,
        field_14=0.800000011920929,
        # 根据图片，2.5D镜头几乎所有参数都可编辑
        can_edit_fov=True,
        can_edit_distance=True,
        can_edit_viewpoint_offset=True,
        can_edit_follow_rotation=True,
        can_edit_horizontal_angle=True,
        can_edit_horizontal_angle_range=True,
        can_edit_pitch_angle_range=True,
        can_edit_ignore_collision=True
    )
    
    # 3D背镜头模板
    BACK_CAMERA_TEMPLATE = CameraTemplate(
        name="3D背镜头",
        camera_mode=CameraMode.BACK_CAMERA,
        default_distance=3.0,
        min_distance=1.0,
        max_distance=5.0,
        field_of_view=45.0,  # 统一默认FOV为45
        viewpoint_offset=ViewpointOffset(x=0.6, y=0.1, z=0.0),
        follow_rotation=True,
        horizontal_angle=0.0,
        min_horizontal_angle=-180.0,
        max_horizontal_angle=180.0,
        min_pitch_angle=-89.0,
        max_pitch_angle=89.0,
        ignore_collision=False,
        field_14=1.0,
        # 根据图片，3D背镜头几乎所有参数都可编辑
        can_edit_fov=True,
        can_edit_distance=True,
        can_edit_viewpoint_offset=True,
        can_edit_follow_rotation=True,
        can_edit_horizontal_angle=True,
        can_edit_horizontal_angle_range=True,
        can_edit_pitch_angle_range=True,
        can_edit_ignore_collision=True
    )
    
    # 第一人称镜头模板
    FIRST_PERSON_TEMPLATE = CameraTemplate(
        name="第一人称镜头",
        camera_mode=CameraMode.FIRST_PERSON,
        default_distance=0.1,
        min_distance=0.1,
        max_distance=0.1,
        field_of_view=45.0,  # 统一默认FOV为45
        viewpoint_offset=ViewpointOffset(x=0.0, y=0.3, z=0.0),
        follow_rotation=False,
        horizontal_angle=0.0,
        min_horizontal_angle=-180.0,
        max_horizontal_angle=180.0,
        min_pitch_angle=-89.0,
        max_pitch_angle=89.0,
        ignore_collision=False,
        field_14=1.0,
        # 根据图片，第一人称镜头仅可编辑部分参数
        can_edit_fov=True,
        can_edit_distance=False,  # 视距固定
        can_edit_viewpoint_offset=False,  # 视点偏移固定
        can_edit_follow_rotation=False,  # 跟随旋转固定
        can_edit_horizontal_angle=True,
        can_edit_horizontal_angle_range=True,
        can_edit_pitch_angle_range=True,
        can_edit_ignore_collision=True
    )
    
    # 经典镜头模板
    CLASSIC_TEMPLATE = CameraTemplate(
        name="经典镜头",
        camera_mode=CameraMode.CLASSIC,
        default_distance=6.0,
        min_distance=1.0,
        max_distance=6.0,
        field_of_view=45.0,  # 统一默认FOV为45
        viewpoint_offset=ViewpointOffset(x=0.0, y=0.0, z=0.0),
        follow_rotation=False,
        horizontal_angle=0.0,
        min_horizontal_angle=-180.0,
        max_horizontal_angle=180.0,
        min_pitch_angle=-89.0,
        max_pitch_angle=89.0,
        ignore_collision=False,
        field_14=1.0,
        # 根据图片，经典镜头仅可查看参数，不可编辑
        can_edit_fov=False,
        can_edit_distance=False,
        can_edit_viewpoint_offset=False,
        can_edit_follow_rotation=False,
        can_edit_horizontal_angle=False,
        can_edit_horizontal_angle_range=False,
        can_edit_pitch_angle_range=False,
        can_edit_ignore_collision=False
    )
    
    # 第三人称镜头模板
    THIRD_PERSON_TEMPLATE = CameraTemplate(
        name="第三人称镜头",
        camera_mode=CameraMode.THIRD_PERSON,
        default_distance=6.0,
        min_distance=1.0,
        max_distance=30.0,
        field_of_view=45.0,  # 统一默认FOV为45
        viewpoint_offset=ViewpointOffset(x=0.0, y=0.0, z=0.0),
        follow_rotation=True,
        horizontal_angle=0.0,
        min_horizontal_angle=-180.0,
        max_horizontal_angle=180.0,
        min_pitch_angle=-89.0,
        max_pitch_angle=89.0,
        ignore_collision=False,
        field_14=1.0,
        # 根据图片，第三人称镜头几乎所有参数都可编辑
        can_edit_fov=True,
        can_edit_distance=True,
        can_edit_viewpoint_offset=True,
        can_edit_follow_rotation=True,
        can_edit_horizontal_angle=True,
        can_edit_horizontal_angle_range=True,
        can_edit_pitch_angle_range=True,
        can_edit_ignore_collision=True
    )
    
    # 根据镜头模式获取模板
    @staticmethod
    def get_template_by_mode(mode: int) -> Optional[CameraTemplate]:
        """
        根据镜头模式获取对应的模板
        
        Args:
            mode: 镜头模式
            
        Returns:
            对应的镜头模板，如果不存在则返回None
        """
        templates = {
            CameraTemplateManager.CameraMode.THIRD_PERSON: CameraTemplateManager.THIRD_PERSON_TEMPLATE,
            CameraTemplateManager.CameraMode.CLASSIC: CameraTemplateManager.CLASSIC_TEMPLATE,
            CameraTemplateManager.CameraMode.FIRST_PERSON: CameraTemplateManager.FIRST_PERSON_TEMPLATE,
            CameraTemplateManager.CameraMode.BACK_CAMERA: CameraTemplateManager.BACK_CAMERA_TEMPLATE,
            CameraTemplateManager.CameraMode.CAMERA_2_5D: CameraTemplateManager.CAMERA_2_5D_TEMPLATE
        }
        return templates.get(mode)
    
    # 根据镜头名称获取模板
    @staticmethod
    def get_template_by_name(name: str) -> Optional[CameraTemplate]:
        """
        根据镜头名称获取对应的模板
        
        Args:
            name: 镜头名称
            
        Returns:
            对应的镜头模板，如果不存在则返回None
        """
        templates = {
            "第三人称镜头": CameraTemplateManager.THIRD_PERSON_TEMPLATE,
            "经典镜头": CameraTemplateManager.CLASSIC_TEMPLATE,
            "第一人称镜头": CameraTemplateManager.FIRST_PERSON_TEMPLATE,
            "3D背镜头": CameraTemplateManager.BACK_CAMERA_TEMPLATE,
            "2.5D镜头": CameraTemplateManager.CAMERA_2_5D_TEMPLATE
        }
        return templates.get(name)
    
    # 获取所有模板
    @staticmethod
    def get_all_templates() -> list[CameraTemplate]:
        """
        获取所有镜头模板
        
        Returns:
            镜头模板列表
        """
        return [
            CameraTemplateManager.THIRD_PERSON_TEMPLATE,
            CameraTemplateManager.CLASSIC_TEMPLATE,
            CameraTemplateManager.FIRST_PERSON_TEMPLATE,
            CameraTemplateManager.BACK_CAMERA_TEMPLATE,
            CameraTemplateManager.CAMERA_2_5D_TEMPLATE
        ]


# 常量定义
class CameraConstants:
    """镜头相关常量"""
    
    # 镜头类型名称映射
    CAMERA_TYPE_NAMES = {
        CameraTemplateManager.CameraMode.UNKNOWN: "未知镜头",
        CameraTemplateManager.CameraMode.THIRD_PERSON: "第三人称镜头",
        CameraTemplateManager.CameraMode.CLASSIC: "经典镜头",
        CameraTemplateManager.CameraMode.FIRST_PERSON: "第一人称镜头",
        CameraTemplateManager.CameraMode.BACK_CAMERA: "3D背镜头",
        CameraTemplateManager.CameraMode.CAMERA_2_5D: "2.5D镜头"
    }
