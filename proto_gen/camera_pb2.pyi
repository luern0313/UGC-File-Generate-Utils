from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CameraConfig(_message.Message):
    __slots__ = ("camera_details",)
    CAMERA_DETAILS_FIELD_NUMBER: _ClassVar[int]
    camera_details: _containers.RepeatedCompositeFieldContainer[CameraDetail]
    def __init__(self, camera_details: _Optional[_Iterable[_Union[CameraDetail, _Mapping]]] = ...) -> None: ...

class CameraDetail(_message.Message):
    __slots__ = ("camera_id", "camera_data")
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    CAMERA_DATA_FIELD_NUMBER: _ClassVar[int]
    camera_id: int
    camera_data: CameraData
    def __init__(self, camera_id: _Optional[int] = ..., camera_data: _Optional[_Union[CameraData, _Mapping]] = ...) -> None: ...

class CameraData(_message.Message):
    __slots__ = ("name", "default_distance", "field_of_view", "viewpoint_offset", "min_distance", "max_distance", "camera_mode", "follow_rotation", "field_14", "min_horizontal_angle", "max_horizontal_angle", "min_pitch_angle", "max_pitch_angle", "ignore_collision", "horizontal_angle")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    FIELD_OF_VIEW_FIELD_NUMBER: _ClassVar[int]
    VIEWPOINT_OFFSET_FIELD_NUMBER: _ClassVar[int]
    MIN_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    MAX_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    CAMERA_MODE_FIELD_NUMBER: _ClassVar[int]
    FOLLOW_ROTATION_FIELD_NUMBER: _ClassVar[int]
    FIELD_14_FIELD_NUMBER: _ClassVar[int]
    MIN_HORIZONTAL_ANGLE_FIELD_NUMBER: _ClassVar[int]
    MAX_HORIZONTAL_ANGLE_FIELD_NUMBER: _ClassVar[int]
    MIN_PITCH_ANGLE_FIELD_NUMBER: _ClassVar[int]
    MAX_PITCH_ANGLE_FIELD_NUMBER: _ClassVar[int]
    IGNORE_COLLISION_FIELD_NUMBER: _ClassVar[int]
    HORIZONTAL_ANGLE_FIELD_NUMBER: _ClassVar[int]
    name: str
    default_distance: float
    field_of_view: float
    viewpoint_offset: ViewpointOffset
    min_distance: float
    max_distance: float
    camera_mode: int
    follow_rotation: bool
    field_14: float
    min_horizontal_angle: float
    max_horizontal_angle: float
    min_pitch_angle: float
    max_pitch_angle: float
    ignore_collision: float
    horizontal_angle: float
    def __init__(self, name: _Optional[str] = ..., default_distance: _Optional[float] = ..., field_of_view: _Optional[float] = ..., viewpoint_offset: _Optional[_Union[ViewpointOffset, _Mapping]] = ..., min_distance: _Optional[float] = ..., max_distance: _Optional[float] = ..., camera_mode: _Optional[int] = ..., follow_rotation: bool = ..., field_14: _Optional[float] = ..., min_horizontal_angle: _Optional[float] = ..., max_horizontal_angle: _Optional[float] = ..., min_pitch_angle: _Optional[float] = ..., max_pitch_angle: _Optional[float] = ..., ignore_collision: _Optional[float] = ..., horizontal_angle: _Optional[float] = ...) -> None: ...

class ViewpointOffset(_message.Message):
    __slots__ = ("x", "y", "z")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    z: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ...) -> None: ...
