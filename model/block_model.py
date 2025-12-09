#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
方块数据类
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class BlockModel:
    """
    方块数据类
    """
    template_id: int
    entity_id: Optional[int] = None
    name: str = ""

    position_x: float = 0.0
    position_y: float = 0.0
    position_z: float = 0.0
    rotation_x: float = 0.0
    rotation_y: float = 0.0
    rotation_z: float = 0.0
    scale_x: float = 1.0
    scale_y: float = 1.0
    scale_z: float = 1.0
