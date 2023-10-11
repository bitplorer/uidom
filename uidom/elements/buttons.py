# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import typing as T
from dataclasses import dataclass, field

from valio import StringValidator, Validator

from uidom.dom.src import component
from uidom.dom.src.dom_tag import dom_tag

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


@dataclass(eq=False)
class _Button(component.Component):
    label: str = StringValidator(logger=False, debug=True)
    type: str = StringValidator(
        in_choice=["submit", "reset", "button"], logger=False, debug=True
    )
    value: str = StringValidator(logger=False, debug=True)
    icon: T.Union[dom_tag, None] = Validator(logger=False, debug=True, default=None)
    className: str = StringValidator(logger=False, debug=True, default="")

    def __post_init__(self, *args, **kwargs):
        super(_Button, self).__init__(
            *args,
            label=self.label,
            type=self.type,
            value=self.value,
            icon=self.icon if self.icon is not None else False,
            className=self.className,
            **kwargs
        )

    def render(self, *args, label, type, value, icon=None, className, **kwargs):
        return self.html_tags.button(
            icon or "",
            label,
            *args,
            type=type,
            value=value,
            className=className if className else False,
            **kwargs
        )


@dataclass(eq=False)
class _ButtonInput(component.Component):
    """`Input Button` base type:
    NOTE: here we are not passing icons because we can't
    pass html elements inside <input /> types.
    """

    type: str = StringValidator(
        in_choice=["submit", "reset", "button", "file", "image"],
        logger=False,
        debug=True,
    )
    value: str = StringValidator(logger=False, debug=True)
    className: str = StringValidator(logger=False, debug=True, default="")

    def __post_init__(self, *args, **kwargs):
        super(_ButtonInput, self).__init__(
            *args, type=self.type, value=self.value, className=self.className, **kwargs
        )

    def render(self, *args, type, value, className, **kwargs):
        return self.html_tags.input_(
            *args,
            type=type,
            value=value if value else False,
            className=className if className else False,
            **kwargs
        )


@dataclass(eq=False)
class Button(component.Component):
    label: str
    value: str
    icon: T.Union[dom_tag, None] = None
    className: str = field(default="")

    def __post_init__(self, *args, **kwargs):
        super(Button, self).__init__(
            *args,
            label=self.label,
            value=self.value,
            icon=self.icon,
            className=self.className,
            **kwargs
        )

    def render(self, *args, label, value, icon, className, **kwargs):
        return _Button(
            label=label, type="button", value=value, icon=icon, className=className
        )


@dataclass(eq=False)
class SubmitButton(component.Component):
    label: str
    value: str
    icon: T.Union[dom_tag, None] = None
    className: str = field(default="")

    def __post_init__(self, *args, **kwargs):
        super(SubmitButton, self).__init__(
            *args,
            label=self.label,
            value=self.value,
            icon=self.icon,
            className=self.className,
            **kwargs
        )

    def render(self, *args, value, label, icon, className, **kwargs):
        return _Button(
            type="submit", value=value, label=label, icon=icon, className=className
        )


@dataclass(eq=False)
class ResetButton(component.Component):
    label: str
    value: str
    icon: T.Union[dom_tag, None] = None
    className: str = field(default="")

    def __post_init__(self, *args, **kwargs):
        super(ResetButton, self).__init__(
            *args,
            label=self.label,
            value=self.value,
            icon=self.icon,
            className=self.className,
            **kwargs
        )

    def render(self, *args, label, value, icon, className, **kwargs):
        return _Button(
            *args,
            type="reset",
            label=label,
            value=value,
            icon=icon,
            className=className,
            **kwargs
        )


@dataclass(eq=False)
class ButtonInput(component.Component):
    value: str
    className: str = field(default="")

    def __post_init__(self, *args, **kwargs):
        super().__init__(*args, value=self.value, className=self.className, **kwargs)

    def render(self, *args, value, className, **kwargs):
        return _ButtonInput(type="button", value=value, className=className)


@dataclass(eq=False)
class SubmitButtonInput(component.Component):
    value: str
    className: str = field(default="")

    def __post_init__(self, *args, **kwargs):
        super().__init__(*args, value=self.value, className=self.className, **kwargs)

    def render(self, *args, value, className, **kwargs):
        return _ButtonInput(type="submit", value=value, className=className)


@dataclass(eq=False)
class ResetButtonInput(component.Component):
    value: str
    className: str = field(default="")

    def __post_init__(self, *args, **kwargs):
        super().__init__(*args, value=self.value, className=self.className, **kwargs)

    def render(self, *args, value, className, **kwargs):
        return _ButtonInput(type="reset", value=value, className=className)


@dataclass(eq=False)
class FileButtonInput(component.Component):
    value: str
    className: str = field(default="")

    def __post_init__(self, *args, **kwargs):
        super().__init__(*args, value=self.value, className=self.className, **kwargs)

    def render(self, *args, value, className, **kwargs):
        return _ButtonInput(type="file", value=value, className=className)


@dataclass(eq=False)
class ImageButtonInput(component.Component):
    value: str
    className: str = field(default="")

    def __post_init__(self, *args, **kwargs):
        super().__init__(*args, value=self.value, className=self.className, **kwargs)

    def render(self, *args, value, className, **kwargs):
        return _ButtonInput(type="image", value=value, className=className)


if __name__ == "__main__":
    print(SubmitButton(label="submit", value="upload"))
    print(ResetButton(label="reset", value="reset"))
    print(FileButtonInput(value="a"))
