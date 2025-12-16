import entity_pb2 as _entity_pb2
import camera_pb2 as _camera_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Asset(_message.Message):
    __slots__ = ("meta", "dependent_assets", "name", "type", "entity_data", "camera_config")
    class AssetType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[Asset.AssetType]
        ENTITY: _ClassVar[Asset.AssetType]
        TERRAIN: _ClassVar[Asset.AssetType]
        PLAYER_TEMPLATE: _ClassVar[Asset.AssetType]
        PROFESSION_TEMPLATE: _ClassVar[Asset.AssetType]
        CAMERA: _ClassVar[Asset.AssetType]
        LAYOUT: _ClassVar[Asset.AssetType]
        PRESET_POINT: _ClassVar[Asset.AssetType]
        UNIT_TAG: _ClassVar[Asset.AssetType]
        ENVIRONMENT_CONFIGURATION: _ClassVar[Asset.AssetType]
    UNKNOWN: Asset.AssetType
    ENTITY: Asset.AssetType
    TERRAIN: Asset.AssetType
    PLAYER_TEMPLATE: Asset.AssetType
    PROFESSION_TEMPLATE: Asset.AssetType
    CAMERA: Asset.AssetType
    LAYOUT: Asset.AssetType
    PRESET_POINT: Asset.AssetType
    UNIT_TAG: Asset.AssetType
    ENVIRONMENT_CONFIGURATION: Asset.AssetType
    META_FIELD_NUMBER: _ClassVar[int]
    DEPENDENT_ASSETS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ENTITY_DATA_FIELD_NUMBER: _ClassVar[int]
    CAMERA_CONFIG_FIELD_NUMBER: _ClassVar[int]
    meta: AssetMeta
    dependent_assets: _containers.RepeatedCompositeFieldContainer[AssetMeta]
    name: str
    type: Asset.AssetType
    entity_data: _entity_pb2.Entity
    camera_config: _camera_pb2.CameraConfig
    def __init__(self, meta: _Optional[_Union[AssetMeta, _Mapping]] = ..., dependent_assets: _Optional[_Iterable[_Union[AssetMeta, _Mapping]]] = ..., name: _Optional[str] = ..., type: _Optional[_Union[Asset.AssetType, str]] = ..., entity_data: _Optional[_Union[_entity_pb2.Entity, _Mapping]] = ..., camera_config: _Optional[_Union[_camera_pb2.CameraConfig, _Mapping]] = ...) -> None: ...

class AssetMeta(_message.Message):
    __slots__ = ("field_2", "meta_type", "asset_id")
    class AssetMetaType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CAMERA: _ClassVar[AssetMeta.AssetMetaType]
        ENTITY: _ClassVar[AssetMeta.AssetMetaType]
        TERRAIN: _ClassVar[AssetMeta.AssetMetaType]
        PLAYER_TEMPLATE: _ClassVar[AssetMeta.AssetMetaType]
        PROFESSION_TEMPLATE: _ClassVar[AssetMeta.AssetMetaType]
        LAYOUT: _ClassVar[AssetMeta.AssetMetaType]
        PRESET_POINT: _ClassVar[AssetMeta.AssetMetaType]
        UNIT_TAG: _ClassVar[AssetMeta.AssetMetaType]
        ENVIRONMENT_CONFIGURATION: _ClassVar[AssetMeta.AssetMetaType]
    CAMERA: AssetMeta.AssetMetaType
    ENTITY: AssetMeta.AssetMetaType
    TERRAIN: AssetMeta.AssetMetaType
    PLAYER_TEMPLATE: AssetMeta.AssetMetaType
    PROFESSION_TEMPLATE: AssetMeta.AssetMetaType
    LAYOUT: AssetMeta.AssetMetaType
    PRESET_POINT: AssetMeta.AssetMetaType
    UNIT_TAG: AssetMeta.AssetMetaType
    ENVIRONMENT_CONFIGURATION: AssetMeta.AssetMetaType
    FIELD_2_FIELD_NUMBER: _ClassVar[int]
    META_TYPE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    field_2: int
    meta_type: AssetMeta.AssetMetaType
    asset_id: int
    def __init__(self, field_2: _Optional[int] = ..., meta_type: _Optional[_Union[AssetMeta.AssetMetaType, str]] = ..., asset_id: _Optional[int] = ...) -> None: ...
