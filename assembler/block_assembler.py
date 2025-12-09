#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实体组装工具类
将方块数据转换为protobuf格式的实体数据
"""

from typing import List
from model.block_model import BlockModel
from proto_gen.asset_pb2 import Asset, AssetMeta
from proto_gen.entity_pb2 import Component, Position, Scale, TransformComponent, Property, NameProperty, Entity, EntityData, \
    TemplateReference, Rotation
from proto_gen.gia_pb2 import GIACollection


class BlockAssembler:
    """
    方块组装器
    """

    def __init__(self, entity_id_start):
        self.entity_id_start = entity_id_start
        self.current_entity_id = entity_id_start

    @staticmethod
    def _create_component_transform(block: BlockModel) -> Component:
        """
        构建变换组件 (TransformComponent)
        对应 Proto 中的 Component component_data -> transform
        type: 1
        """
        position = Position(
            x=block.position_x,
            y=block.position_y,
            z=block.position_z,
        )
        rotation = Rotation(
            x=block.rotation_x,
            y=block.rotation_y,
            z=block.rotation_z,
        )
        scale = Scale(
            x=block.scale_x,
            y=block.scale_y,
            z=block.scale_z,
        )
        transform_data = TransformComponent(
            position=position,
            rotation=rotation,
            scale=scale,
            field_501=4294967295  # -1 unsigned
        )
        return Component(
            component_type=Component.ComponentType.TRANSFORM,
            transform=transform_data
        )

    @staticmethod
    def _create_property_name(name: str) -> Property:
        """
        构建名称属性 (NameProperty)
        对应 Proto 中的 Property value -> name_prop
        type: 1
        """
        name_prop = NameProperty(
            name=name,
            static_block=NameProperty.StaticBlock.STATIC
        )

        return Property(
            property_type=Property.PropertyType.NAME,
            name=name_prop
        )

    def _create_entity_core(self, block: BlockModel,
                            entity_id: int,
                            template_id: int) -> EntityData:
        """
        组装 EntityCore，注入组件和属性列表
        """
        template_ref = TemplateReference(
            template_id=template_id,
            field_2=1
        )

        core = EntityData(
            entity_id=entity_id,
            template=template_ref,
            template_id_ref=template_id
        )

        # 属性列表
        properties = []
        if block.name:
            prop_name = self._create_property_name(block.name)
            properties.append(prop_name)

        # 组件列表
        components = []
        comp_transform = self._create_component_transform(block)
        components.append(comp_transform)

        # 添加组件和属性
        if components:
            core.components.extend(components)
        if properties:
            core.properties.extend(properties)

        return core

    @staticmethod
    def _create_asset_meta(entity_id: int) -> AssetMeta:
        return AssetMeta(
            field_2=1,
            meta_type=AssetMeta.AssetMetaType.ENTITY,
            asset_id=entity_id
        )

    def _generate_entity_id(self, block: BlockModel) -> int:
        if block.entity_id is None:
            eid = self.current_entity_id
            self.current_entity_id += 1
            return eid
        return block.entity_id

    def _create_asset(self, block: BlockModel) -> Asset:
        """
        组装Asset
        """
        entity_id = self._generate_entity_id(block)
        entity_name = block.name if block.name else f"Entity_{entity_id}"

        data = self._create_entity_core(
            block=block,
            entity_id=entity_id,
            template_id=block.template_id
        )

        entity_data = Entity(
            data=data,
            field_2=0,
            template_id=block.template_id
        )

        meta = self._create_asset_meta(entity_id)

        asset = Asset(
            meta=meta,
            name=entity_name,
            type=Asset.AssetType.ENTITY,
            entity_data=entity_data
        )

        return asset

    def assemble(self, blocks: List[BlockModel]) -> bytes:
        """
        批量转换并序列化
        """
        collection = GIACollection()
        for block in blocks:
            asset = self._create_asset(block)
            collection.Assets.append(asset)
        return collection.SerializeToString()

    def reset_entity_id(self, start_id=None):
        if start_id is not None:
            self.current_entity_id = start_id
        else:
            self.current_entity_id = self.entity_id_start
