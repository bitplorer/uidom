# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import typing as T
from dataclasses import dataclass, field

from valio import StringValidator

from uidom.dom.src import component

__all__ = [
    # integer html
    "FloatLabel",
    "FloatLegend",
    "FloatInput",
    "FloatNumberInput",
    "FloatRangeInput",
]


@dataclass(eq=False)
class FloatLabel(component.Component):
    label: str = StringValidator(logger=False, debug=True)
    className: str = StringValidator(logger=False, debug=True, default="")

    def __post_init__(self, *args, **kwargs):
        super(FloatLabel, self).__init__(
            self.label, *args, className=self.className, **kwargs
        )

    def render(self, label, *args, className, **kwargs):
        return self.html_tags.label(
            label, *args, className=className if className else False, **kwargs
        )


@dataclass(eq=False)
class FloatLegend(component.Component):
    label: str = StringValidator(logger=False, debug=True)
    className: str = StringValidator(logger=False, debug=True, default="")

    def __post_init__(self, *args, **kwargs):
        super(FloatLegend, self)._init__(
            self.label, *args, className=self.className, **kwargs
        )

    def render(self, label, *args, className, **kwargs):
        return self.html_tags.legend(
            label, *args, className=className if className else False, **kwargs
        )


min_field = StringValidator(logger=False, debug=True)
max_field = StringValidator(logger=False, debug=True)


@dataclass(eq=False)
class FloatInput(component.Component):
    @max_field.add_post_validator
    @min_field.add_post_validator
    def cast2float(self, value):
        if value not in ["null", None]:
            try:
                return float(value)
            except ValueError as e:
                raise ValueError(f"got an invalid float value {value}") from e

    name: str = StringValidator(logger=False, debug=True)
    type: str = StringValidator(
        in_choice=["number", "range"], logger=False, debug=True, default="number"
    )
    placeholder: str = StringValidator(logger=False, debug=True)
    min: str = min_field
    max: str = max_field
    pattern: str = StringValidator(logger=False, debug=True)
    className: str = StringValidator(logger=False, debug=True, default="")

    def __post_init__(self, *args, **kwargs):
        super(FloatInput, self).__init__(
            *args,
            name=self.name,
            placeholder=self.placeholder,
            type=self.type,
            min=self.min,
            max=self.max,
            pattern=self.pattern,
            className=self.className,
            **kwargs,
        )

    def render(
        self, *args, name, placeholder="", type, min, max, pattern, className, **kwargs
    ):
        return self.html_tags.input_(
            *args,
            type=type,
            name=name,
            placeholder=placeholder,
            min=min if min not in ["null", None] else False,
            max=max if max not in ["null", None] else False,
            pattern=pattern if pattern not in ["null", None] else False,
            className=className if className else False,
            **kwargs,
        )


@dataclass(eq=False)
class FloatNumberInput(component.Component):
    name: str
    placeholder: str
    min: T.Union[str, None] = None
    max: T.Union[str, None] = None
    pattern: T.Union[str, None] = None
    className: str = field(default="")

    def __post_init__(self, *args, **kwargs):
        super(FloatNumberInput, self).__init__(
            *args,
            name=self.name,
            placeholder=self.placeholder,
            min=self.min,
            max=self.max,
            pattern=self.pattern,
            className=self.className,
            **kwargs,
        )

    def render(
        self, *args, name, placeholder="", min, max, pattern, className, **kwargs
    ):
        return FloatInput(
            name=name,
            placeholder=placeholder,
            type="number",
            min=min,
            max=max,
            pattern=pattern,
            className=className,
        )


@dataclass(eq=False)
class FloatRangeInput(component.Component):
    name: str
    placeholder: str
    min: T.Union[str, None] = None
    max: T.Union[str, None] = None
    pattern: T.Union[str, None] = None
    className: str = field(default="")

    def __post_init__(self, *args, **kwargs):
        super(FloatRangeInput, self).__init__(
            *args,
            name=self.name,
            placeholder=self.placeholder,
            min=self.min,
            max=self.max,
            pattern=self.pattern,
            className=self.className,
            **kwargs,
        )

    def render(
        self, *args, name, placeholder="", min, max, pattern, className, **kwargs
    ):
        return FloatInput(
            name=name,
            placeholder=placeholder,
            type="range",
            min=min,
            max=max,
            pattern=pattern,
            className=className,
        )


if __name__ == "__main__":
    from valio import Pattern, SetOf

    print(FloatRangeInput(name="test", placeholder="xyz"))
    print(
        FloatInput(
            name="test",
            type="number",
            placeholder="space",
            pattern=SetOf(Pattern("0-9", count_min=1, count_max=3)).pattern,
            min="100",
        )
    )
