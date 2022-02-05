from enum import Enum
from typing import Iterable, Any, Union


class AccessLevel(Enum):
    internal = 0  # internal, can never be accessed through API
    _reserved = 1  # do not use
    private = 2  # can only be accessed by the owner of the resource
    party = 3  # can be accessed by the members of the same party
    users = 4  # can be accessed by all users
    public = 5  # can be accessed by everyone


class AlManagedField:
    def __init__(self, name: str, r: AccessLevel, w: AccessLevel) -> None:
        self.name = name
        self.r = r
        self.w = w

    def getattr(self, obj: "AlManagedClass", al: AccessLevel) -> Union[Any, None]:
        if al.value <= self.r.value:
            return getattr(obj, self.name)

    def setattr(self, obj: "AlManagedClass", al: AccessLevel, value: Any):
        if al.value <= self.w.value:
            setattr(obj, self.name, value)


class AlManagedClass:
    _fields: Iterable[AlManagedField]

    def to_dict(self, al: AccessLevel = 0) -> dict:
        result = {}
        for field in self._fields:
            value = field.getattr(self, al)
            if value is not None:
                result[field.name] = value
        return result

    def update_from_dict(self, data: dict, al: AccessLevel = 0):
        for field in self._fields:
            value = data.get(field.name, None)
            if value is not None:
                field.setattr(self, al, value)
