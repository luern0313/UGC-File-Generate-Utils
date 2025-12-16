#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
镜头配置文件
定义镜头的配置信息和默认参数
"""


class CameraConfig:
    """镜头配置"""
    
    # 镜头模式映射
    CAMERA_MODE_NAMES = {
        0: "未知镜头",
        1: "3D背镜头",
        2: "2.5D镜头",
        3: "第一人称镜头",
        4: "第三人称镜头",
        5: "经典镜头"
    }
    
    # 镜头模式对应的显示名称
    CAMERA_MODE_DISPLAY_NAMES = {
        0: "未知",
        1: "3D背镜头",
        2: "2.5D镜头",
        3: "第一人称",
        4: "第三人称",
        5: "经典镜头"
    }
    
    # 默认镜头参数
    DEFAULT_CAMERA_PARAMS = {
        "field_of_view": 45.0,
        "default_distance": 6.0,
        "min_distance": 1.0,
        "max_distance": 30.0,
        "follow_rotation": True,
        "horizontal_angle": 0.0,
        "min_horizontal_angle": -180.0,
        "max_horizontal_angle": 180.0,
        "min_pitch_angle": -89.0,
        "max_pitch_angle": 89.0,
        "ignore_collision": False,
        "field_14": 1.0
    }
    
    # 镜头参数的显示名称
    PARAM_DISPLAY_NAMES = {
        "field_of_view": "镜头视野检测",
        "default_distance": "默认视距",
        "min_distance": "视距最小值",
        "max_distance": "视距最大值",
        "follow_rotation": "视点跟随旋转",
        "horizontal_angle": "水平角度",
        "min_horizontal_angle": "水平角度最小值",
        "max_horizontal_angle": "水平角度最大值",
        "min_pitch_angle": "俯仰角度最小值",
        "max_pitch_angle": "俯仰角度最大值",
        "ignore_collision": "忽略镜头碰撞",
        "field_14": "未知字段"
    }
    
    # 镜头参数的单位
    PARAM_UNITS = {
        "field_of_view": "度",
        "default_distance": "单位",
        "min_distance": "单位",
        "max_distance": "单位",
        "horizontal_angle": "度",
        "min_horizontal_angle": "度",
        "max_horizontal_angle": "度",
        "min_pitch_angle": "度",
        "max_pitch_angle": "度"
    }
