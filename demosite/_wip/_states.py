# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import typing
from dataclasses import dataclass, field

from uidom.dom import Component


@dataclass
class State(object):
    default: typing.Optional[typing.Any] = field(default=None)
    annotation: typing.Optional[typing.Any] = None

    def __set_name__(self, owner: Component, name: str):
        self.owner_name = type(owner).__name__
        self.owner: Component = owner
        self.name: str = name

        self.value = None
        self.value_class: typing.Optional[type] = None
        self.annotation = owner.__annotations__.get(name, typing.Any)
        self.__annotations__[self.name] = self.annotation

    def __set__(self, obj: Component, value: typing.Any):
        """sets descriptor field"""
        try:
            value = (
                value
                or (self.default if not callable(self.default) else self.default())
                if self.default is not None
                else value
            )

            old_value = self.value

            if self.value_class is None:
                if not isinstance(value, type):
                    ValueType = type(value)  # type: typing.Any
                    # why have I use typing.Any! see the below link for the issue
                    # https://github.com/python/mypy/issues/2477#issuecomment-262734005

                    class value_class(ValueType):
                        pass

                    self.value_class = (
                        value_class if value is not None else self.value_class
                    )

                else:
                    raise TypeError(f"{value=} must be an instance of type not a type")
            else:
                if value is not None:
                    self.value = self.value_class(value)
                    self.value.name = self.name + str(id(self.value))
                else:
                    self.value = value

                self.value.name = self.name + str(id(self.value))

        finally:
            if val := obj.get(str):
                for v in val:
                    if v == str(old_value):
                        v.parent[v.parent.children.index(v)] = str(value)

    def __get__(self, obj, obj_type=None):
        """gets descriptor field"""
        if obj is None:
            return
        return self.value

    def __delete__(self, obj):
        """deletes descriptor"""
        del self.value

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return f"<{self.owner_name}.{self.name} at {id(self)} {self.value}"
