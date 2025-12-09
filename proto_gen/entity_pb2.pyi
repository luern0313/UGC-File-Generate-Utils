from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Entity(_message.Message):
    __slots__ = ()
    DATA_FIELD_NUMBER: _ClassVar[int]
    FIELD_2_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    data: EntityData
    field_2: int
    template_id: int
    def __init__(self, data: _Optional[_Union[EntityData, _Mapping]] = ..., field_2: _Optional[int] = ..., template_id: _Optional[int] = ...) -> None: ...

class EntityData(_message.Message):
    __slots__ = ()
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    FIELD_7_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_REF_FIELD_NUMBER: _ClassVar[int]
    entity_id: int
    template: TemplateReference
    properties: _containers.RepeatedCompositeFieldContainer[Property]
    components: _containers.RepeatedCompositeFieldContainer[Component]
    field_7: _containers.RepeatedScalarFieldContainer[bytes]
    template_id_ref: int
    def __init__(self, entity_id: _Optional[int] = ..., template: _Optional[_Union[TemplateReference, _Mapping]] = ..., properties: _Optional[_Iterable[_Union[Property, _Mapping]]] = ..., components: _Optional[_Iterable[_Union[Component, _Mapping]]] = ..., field_7: _Optional[_Iterable[bytes]] = ..., template_id_ref: _Optional[int] = ...) -> None: ...

class TemplateReference(_message.Message):
    __slots__ = ()
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    FIELD_2_FIELD_NUMBER: _ClassVar[int]
    template_id: int
    field_2: int
    def __init__(self, template_id: _Optional[int] = ..., field_2: _Optional[int] = ...) -> None: ...

class Property(_message.Message):
    __slots__ = ()
    class PropertyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[Property.PropertyType]
        NAME: _ClassVar[Property.PropertyType]
        REMARK: _ClassVar[Property.PropertyType]
    UNKNOWN: Property.PropertyType
    NAME: Property.PropertyType
    REMARK: Property.PropertyType
    PROPERTY_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    REMARK_FIELD_NUMBER: _ClassVar[int]
    FIELD_23_FIELD_NUMBER: _ClassVar[int]
    FIELD_28_FIELD_NUMBER: _ClassVar[int]
    FIELD_48_FIELD_NUMBER: _ClassVar[int]
    FIELD_50_FIELD_NUMBER: _ClassVar[int]
    FIELD_62_FIELD_NUMBER: _ClassVar[int]
    FIELD_65_FIELD_NUMBER: _ClassVar[int]
    FIELD_66_FIELD_NUMBER: _ClassVar[int]
    property_type: Property.PropertyType
    name: NameProperty
    remark: RemarkProperty
    field_23: bytes
    field_28: bytes
    field_48: bytes
    field_50: bytes
    field_62: bytes
    field_65: bytes
    field_66: bytes
    def __init__(self, property_type: _Optional[_Union[Property.PropertyType, str]] = ..., name: _Optional[_Union[NameProperty, _Mapping]] = ..., remark: _Optional[_Union[RemarkProperty, _Mapping]] = ..., field_23: _Optional[bytes] = ..., field_28: _Optional[bytes] = ..., field_48: _Optional[bytes] = ..., field_50: _Optional[bytes] = ..., field_62: _Optional[bytes] = ..., field_65: _Optional[bytes] = ..., field_66: _Optional[bytes] = ...) -> None: ...

class NameProperty(_message.Message):
    __slots__ = ()
    class StaticBlock(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DYNAMIC: _ClassVar[NameProperty.StaticBlock]
        STATIC: _ClassVar[NameProperty.StaticBlock]
    DYNAMIC: NameProperty.StaticBlock
    STATIC: NameProperty.StaticBlock
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATIC_BLOCK_FIELD_NUMBER: _ClassVar[int]
    name: str
    static_block: NameProperty.StaticBlock
    def __init__(self, name: _Optional[str] = ..., static_block: _Optional[_Union[NameProperty.StaticBlock, str]] = ...) -> None: ...

class RemarkProperty(_message.Message):
    __slots__ = ()
    REMARK_FIELD_NUMBER: _ClassVar[int]
    remark: str
    def __init__(self, remark: _Optional[str] = ...) -> None: ...

class Component(_message.Message):
    __slots__ = ()
    class ComponentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[Component.ComponentType]
        TRANSFORM: _ClassVar[Component.ComponentType]
        PRESET_STATE: _ClassVar[Component.ComponentType]
        BASIC_COMBAT: _ClassVar[Component.ComponentType]
        NODE: _ClassVar[Component.ComponentType]
    UNKNOWN: Component.ComponentType
    TRANSFORM: Component.ComponentType
    PRESET_STATE: Component.ComponentType
    BASIC_COMBAT: Component.ComponentType
    NODE: Component.ComponentType
    COMPONENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    PRESET_STATE_FIELD_NUMBER: _ClassVar[int]
    FIELD_13_FIELD_NUMBER: _ClassVar[int]
    FIELD_14_FIELD_NUMBER: _ClassVar[int]
    FIELD_15_FIELD_NUMBER: _ClassVar[int]
    FIELD_16_FIELD_NUMBER: _ClassVar[int]
    BASIC_COMBAT_FIELD_NUMBER: _ClassVar[int]
    FIELD_18_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    FIELD_22_FIELD_NUMBER: _ClassVar[int]
    FIELD_27_FIELD_NUMBER: _ClassVar[int]
    FIELD_29_FIELD_NUMBER: _ClassVar[int]
    component_type: Component.ComponentType
    transform: TransformComponent
    preset_state: PresetStateComponent
    field_13: bytes
    field_14: bytes
    field_15: bytes
    field_16: bytes
    basic_combat: BasicCombatComponent
    field_18: bytes
    node: NodeComponent
    field_22: bytes
    field_27: bytes
    field_29: bytes
    def __init__(self, component_type: _Optional[_Union[Component.ComponentType, str]] = ..., transform: _Optional[_Union[TransformComponent, _Mapping]] = ..., preset_state: _Optional[_Union[PresetStateComponent, _Mapping]] = ..., field_13: _Optional[bytes] = ..., field_14: _Optional[bytes] = ..., field_15: _Optional[bytes] = ..., field_16: _Optional[bytes] = ..., basic_combat: _Optional[_Union[BasicCombatComponent, _Mapping]] = ..., field_18: _Optional[bytes] = ..., node: _Optional[_Union[NodeComponent, _Mapping]] = ..., field_22: _Optional[bytes] = ..., field_27: _Optional[bytes] = ..., field_29: _Optional[bytes] = ...) -> None: ...

class TransformComponent(_message.Message):
    __slots__ = ()
    POSITION_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    FIELD_501_FIELD_NUMBER: _ClassVar[int]
    position: Position
    rotation: Rotation
    scale: Scale
    field_501: int
    def __init__(self, position: _Optional[_Union[Position, _Mapping]] = ..., rotation: _Optional[_Union[Rotation, _Mapping]] = ..., scale: _Optional[_Union[Scale, _Mapping]] = ..., field_501: _Optional[int] = ...) -> None: ...

class Position(_message.Message):
    __slots__ = ()
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    z: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ...) -> None: ...

class Rotation(_message.Message):
    __slots__ = ()
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    z: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ...) -> None: ...

class Scale(_message.Message):
    __slots__ = ()
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    z: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ...) -> None: ...

class PresetStateComponent(_message.Message):
    __slots__ = ()
    PRESET_STATE_FIELD_NUMBER: _ClassVar[int]
    preset_state: PresetState
    def __init__(self, preset_state: _Optional[_Union[PresetState, _Mapping]] = ...) -> None: ...

class PresetState(_message.Message):
    __slots__ = ()
    PRESET_STATE_ID_FIELD_NUMBER: _ClassVar[int]
    PRESET_STATE_FIELD_NUMBER: _ClassVar[int]
    preset_state_id: int
    preset_state: int
    def __init__(self, preset_state_id: _Optional[int] = ..., preset_state: _Optional[int] = ...) -> None: ...

class BasicCombatComponent(_message.Message):
    __slots__ = ()
    class IsInvincible(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NOT_INVINCIBLE: _ClassVar[BasicCombatComponent.IsInvincible]
        INVINCIBLE: _ClassVar[BasicCombatComponent.IsInvincible]
    NOT_INVINCIBLE: BasicCombatComponent.IsInvincible
    INVINCIBLE: BasicCombatComponent.IsInvincible
    BASE_HEALTH_FIELD_NUMBER: _ClassVar[int]
    BASE_ATTACK_FIELD_NUMBER: _ClassVar[int]
    BASIC_DEFENSE_FIELD_NUMBER: _ClassVar[int]
    IS_INVINCIBLE_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    FIELD_6_FIELD_NUMBER: _ClassVar[int]
    FIELD_8_FIELD_NUMBER: _ClassVar[int]
    FIELD_9_FIELD_NUMBER: _ClassVar[int]
    FIELD_10_FIELD_NUMBER: _ClassVar[int]
    FIELD_11_FIELD_NUMBER: _ClassVar[int]
    FIELD_12_FIELD_NUMBER: _ClassVar[int]
    FIELD_13_FIELD_NUMBER: _ClassVar[int]
    FIELD_14_FIELD_NUMBER: _ClassVar[int]
    FIELD_15_FIELD_NUMBER: _ClassVar[int]
    base_health: float
    base_attack: float
    basic_defense: float
    is_invincible: BasicCombatComponent.IsInvincible
    level: int
    field_6: bytes
    field_8: float
    field_9: float
    field_10: float
    field_11: float
    field_12: float
    field_13: float
    field_14: float
    field_15: float
    def __init__(self, base_health: _Optional[float] = ..., base_attack: _Optional[float] = ..., basic_defense: _Optional[float] = ..., is_invincible: _Optional[_Union[BasicCombatComponent.IsInvincible, str]] = ..., level: _Optional[int] = ..., field_6: _Optional[bytes] = ..., field_8: _Optional[float] = ..., field_9: _Optional[float] = ..., field_10: _Optional[float] = ..., field_11: _Optional[float] = ..., field_12: _Optional[float] = ..., field_13: _Optional[float] = ..., field_14: _Optional[float] = ..., field_15: _Optional[float] = ...) -> None: ...

class NodeComponent(_message.Message):
    __slots__ = ()
    NODE_INFO_FIELD_NUMBER: _ClassVar[int]
    node_info: NodeInfo
    def __init__(self, node_info: _Optional[_Union[NodeInfo, _Mapping]] = ...) -> None: ...

class NodeInfo(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    FIELD_2_FIELD_NUMBER: _ClassVar[int]
    FIELD_3_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FIELD_504_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    field_2: bytes
    field_3: bytes
    description: str
    field_504: int
    name: str
    def __init__(self, id: _Optional[str] = ..., field_2: _Optional[bytes] = ..., field_3: _Optional[bytes] = ..., description: _Optional[str] = ..., field_504: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...
