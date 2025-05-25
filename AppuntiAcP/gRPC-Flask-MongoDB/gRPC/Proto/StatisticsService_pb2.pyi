from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StringMessage(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: str
    def __init__(self, data: _Optional[str] = ...) -> None: ...

class MeanRequest(_message.Message):
    __slots__ = ("sensor_id", "data_type")
    SENSOR_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    sensor_id: str
    data_type: str
    def __init__(self, sensor_id: _Optional[str] = ..., data_type: _Optional[str] = ...) -> None: ...

class Sensor(_message.Message):
    __slots__ = ("sensor_id", "data_type")
    SENSOR_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    sensor_id: str
    data_type: str
    def __init__(self, sensor_id: _Optional[str] = ..., data_type: _Optional[str] = ...) -> None: ...
