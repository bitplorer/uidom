# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import typing as T
from dataclasses import dataclass

from uidom.dom.htmlelement import HTMLElement
from uidom.dom.src.htmltags import html_tag
from valio import StringValidator, Validator

__all__ = [
    "Button",
    "SubmitButton",
    "ResetButton",
    "ButtonInput",
    "SubmitButtonInput",
    "ResetButtonInput",
    "ImageButtonInput",
    "FileButtonInput",
]


@dataclass
class _Button(HTMLElement):

    label: str = StringValidator(logger=False, debug=True)
    type: str = StringValidator(in_choice=["submit", "reset", "button"], logger=False, debug=True)
    value: str = StringValidator(logger=False, debug=True)
    icon: T.Union[html_tag, None] = Validator(logger=False, debug=True, default=None)

    def __post_init__(self, *args, **kwargs):
        super(_Button, self).__init__(
            *args,
            label=self.label,
            type=self.type,
            value=self.value,
            icon=self.icon if self.icon is not None else False,
            **kwargs)

    def __render__(self, *args, label, type, value, icon=None, **kwargs):
        return self.html_tags.button(icon or '', label, *args, type=type, value=value, **kwargs)


@dataclass
class _ButtonInput(HTMLElement):
    type: str = StringValidator(in_choice=["submit", "reset", "button", "file", "image"], logger=False, debug=True)
    value: str = StringValidator(logger=False, debug=True)

    def __post_init__(self, *args, **kwargs):
        super(_ButtonInput, self).__init__(*args, type=self.type, value=self.value, **kwargs)

    def __render__(self, *args, type, value, **kwargs):
        return self.html_tags.input_(*args, type=type, value=value, **kwargs)


@dataclass
class Button(HTMLElement):
    label: str
    value: str

    def __post_init__(self, *args, **kwargs):
        super(Button, self).__init__(*args, label=self.label, value=self.value, **kwargs)

    def __render__(self, *args, label, value, **kwargs):
        return _Button(label=label, type="button", value=value)


@dataclass
class SubmitButton(HTMLElement):
    label: str
    value: str
    icon: T.Union[html_tag, None] = None

    def __post_init__(self, *args, **kwargs):
        super(SubmitButton, self).__init__(*args, label=self.label, value=self.value, icon=self.icon, **kwargs)

    def __render__(self, *args, value, label, icon, **kwargs):
        return _Button(type="submit", value=value, label=label, icon=icon)


@dataclass
class ResetButton(HTMLElement):
    label: str
    value: str
    icon: T.Union[html_tag, None] = None

    def __post_init__(self, *args, **kwargs):
        super(ResetButton, self).__init__(*args, label=self.label, value=self.value, icon=self.icon, **kwargs)

    def __render__(self, *args, label, value, icon, **kwargs):
        return _Button(*args, type="reset", label=label, value=value, icon=icon, **kwargs)


class ButtonInput(HTMLElement):
    def __render__(self, *args, value, **kwargs):
        return _ButtonInput(type="button", value=value)


class SubmitButtonInput(HTMLElement):

    def __render__(self, *args, value, **kwargs):
        return _ButtonInput(type="submit", value=value)


class ResetButtonInput(HTMLElement):

    def __render__(self, *args, value, **kwargs):
        return _ButtonInput(type="reset", value=value)


class FileButtonInput(HTMLElement):

    def __render__(self, *args, value, **kwargs):
        return _ButtonInput(type="file", value=value)


class ImageButtonInput(HTMLElement):

    def __render__(self, *args, value, **kwargs):
        return _ButtonInput(type="image", value=value)


if __name__ == '__main__':
    print(SubmitButton(label="submit", value="upload", icon=None))
    print(ResetButton(label="reset", value="reset", icon=None))
    # print(FileButtonInput(value="a"))
