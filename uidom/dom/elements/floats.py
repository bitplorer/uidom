# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import typing as T
from dataclasses import dataclass, field

from valio import StringValidator

from uidom.dom.htmlelement import HTMLElement

__all__ = [
    # integer html
    "FloatLabel",
    "FloatLegend",
    "FloatInput",
    "FloatNumberInput",
    "FloatRangeInput",
]


@dataclass(eq=False)
class FloatLabel(HTMLElement):
    label: str = StringValidator(logger=False, debug=True)

    def __post_init__(self, *args, **kwargs):
        super(FloatLabel, self).__init__(self.label, *args, **kwargs)

    def render(self, label, *args, **kwargs):
        return self.html_tags.label(label, *args, **kwargs)


@dataclass(eq=False)
class FloatLegend(HTMLElement):
    label: str = StringValidator(logger=False, debug=True)

    def __post_init__(self, *args, **kwargs):
        super(FloatLegend, self)._init__(self.label, *args, **kwargs)

    def render(self, label, *args, **kwargs):
        return self.html_tags.legend(label, *args, **kwargs)


min_field = StringValidator(logger=False, debug=True)
max_field = StringValidator(logger=False, debug=True)


@dataclass(eq=False)
class FloatInput(HTMLElement):
    
    @max_field.add_validator
    @min_field.add_validator
    def cast2float(self, value):
        if value not in ["null", None]:
            try:
                float(value)
            except TypeError as e:
                raise ValueError(f"{value} is not a float value") from e
    

    name: str = StringValidator(logger=False, debug=True)
    type: str = StringValidator(in_choice=["number", "range"], logger=False, debug=True, default="number")
    placeholder: str = StringValidator(logger=False, debug=True)
    min: str = min_field
    max: str = max_field
    pattern: str = StringValidator(logger=False, debug=True)

    def __post_init__(self, *args, **kwargs):
        super(FloatInput, self).__init__(*args,
                                         name=self.name,
                                         placeholder=self.placeholder,
                                         type=self.type,
                                         min=self.min,
                                         max=self.max,
                                         pattern=self.pattern,
                                         **kwargs
                                         )

    def render(
            self,
            *args,
            name,
            placeholder="",
            type,
            min,
            max,
            pattern,
            **kwargs
    ):
        return self.html_tags.input_(
            *args,
            type=type,
            name=name,
            placeholder=placeholder,
            min=min if min not in ["null", None] else False,
            max=max if max not in ["null", None] else False,
            pattern=pattern if pattern not in ["null", None] else False,
            **kwargs,
        )


@dataclass(eq=False)
class FloatNumberInput(HTMLElement):

    name: str
    placeholder: str
    min: T.Union[str, None] = None
    max: T.Union[str, None] = None
    pattern: T.Union[str, None] = None

    def __post_init__(self, *args, **kwargs):
        super(FloatNumberInput, self).__init__(*args,
                                               name=self.name,
                                               placeholder=self.placeholder,
                                               min=self.min,
                                               max=self.max,
                                               pattern=self.pattern,
                                               **kwargs
                                               )

    def render(
            self,
            *args,
            name,
            placeholder="",
            min,
            max,
            pattern,
            **kwargs
    ):
        return FloatInput(
            name=name,
            placeholder=placeholder,
            type="number",
            min=min,
            max=max,
            pattern=pattern,
        )


@dataclass(eq=False)
class FloatRangeInput(HTMLElement):
    name: str
    placeholder: str
    min: T.Union[str, None] = None
    max: T.Union[str, None] = None
    pattern: T.Union[str, None] = None

    def __post_init__(self, *args, **kwargs):
        super(FloatRangeInput, self).__init__(*args,
                                              name=self.name,
                                              placeholder=self.placeholder,
                                              min=self.min,
                                              max=self.max,
                                              pattern=self.pattern,
                                              **kwargs
                                              )

    def render(
            self,
            *args,
            name,
            placeholder="",
            min,
            max,
            pattern,
            **kwargs
    ):
        return FloatInput(
            name=name,
            placeholder=placeholder,
            type="range",
            min=min,
            max=max,
            pattern=pattern,
        )


if __name__ == '__main__':
    from valio import Pattern, SetOf
    print(FloatRangeInput(name="test", placeholder="xyz"))
    print(FloatInput(name="test", type="number", placeholder="space",
                     pattern=SetOf(Pattern("0-9", count_min=1, count_max=6)).pattern, min="100"))
