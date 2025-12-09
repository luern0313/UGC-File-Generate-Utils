import asset_pb2 as _asset_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GIACollection(_message.Message):
    __slots__ = ()
    ASSETS_FIELD_NUMBER: _ClassVar[int]
    Assets: _containers.RepeatedCompositeFieldContainer[_asset_pb2.Asset]
    def __init__(self, Assets: _Optional[_Iterable[_Union[_asset_pb2.Asset, _Mapping]]] = ...) -> None: ...
