# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import typing as T
from dataclasses import dataclass, field

from valio import StringValidator, Validator

from uidom.dom.htmlelement import HTMLElement

__all__ = [
    # integer html
    "IntegerLabel",
    "IntegerLegend",
    "IntegerInput",
    "IntegerNumberInput",
    "IntegerRangeInput",
    "TelephoneInput",
    "IntegerField",
]


@Validator.register
@dataclass(eq=False)
class IntegerLabel(HTMLElement):
    label: str = StringValidator(logger=False, debug=True)

    def __post_init__(self, *args, **kwargs):
        super(IntegerLabel, self).__init__(*args, label=self.label, **kwargs)

    def render(self, label, *args, **kwargs):
        return self.html_tags.label(label, *args, **kwargs)


class IntegerLabelValidator(Validator):
    annotation = T.Union[IntegerLabel, None]


@dataclass(eq=False)
class IntegerLegend(HTMLElement):
    label: str = StringValidator(logger=False, debug=True)

    def __post_init__(self, *args, **kwargs):
        super(IntegerLegend, self).__init__(label=self.label, *args, *kwargs)

    def render(self, label, *args, **kwargs):
        return self.html_tags.legend(label, *args, **kwargs)


min_field = StringValidator(logger=False, debug=True, name="min")
max_field = StringValidator(logger=False, debug=True, name="max")


@dataclass(eq=False)
class IntegerInput(HTMLElement):
    @max_field.add_validator
    @min_field.add_validator
    def cast2int(self, value):
        if value not in ["null", None]:
            try:
                int(value)
            except TypeError as e:
                raise ValueError(f"{value} is not an integer value") from e

    name: str = StringValidator(logger=False, debug=True)
    placeholder: str = StringValidator(logger=False, debug=True)
    type: str = StringValidator(
        in_choice=["number", "range", "tel"], logger=False, debug=True, default="number"
    )
    min: str = min_field
    max: str = max_field
    pattern: str = StringValidator(logger=False, debug=True, default=None)

    def __post_init__(self, *args, **kwargs):
        super(IntegerInput, self).__init__(
            *args,
            name=self.name,
            placeholder=self.placeholder,
            type=self.type,
            min=self.min,
            max=self.max,
            pattern=self.pattern,
            **kwargs,
        )

    def render(self, *args, name, placeholder="", type, min, max, pattern, **kwargs):
        return self.html_tags.input_(
            *args,
            name=name,
            placeholder=placeholder,
            type=type,
            min=min if min not in ["null", None] else False,
            max=max if max not in ["null", None] else False,
            pattern=pattern if pattern not in ["null", None] else False,
            **kwargs,
        )


Validator.register(IntegerInput)  # noqa


class IntegerInputValidator(Validator):
    annotation = T.Union[IntegerInput, None]


@dataclass(eq=False)
class IntegerNumberInput(HTMLElement):
    name: str
    placeholder: str
    min: T.Union[str, None] = field(default=None)
    max: T.Union[str, None] = field(default=None)
    pattern: T.Union[str, None] = field(default=None)

    def __post_init__(self, *args, **kwargs):
        super(IntegerNumberInput, self).__init__(
            *args,
            name=self.name,
            placeholder=self.placeholder,
            min=self.min,
            max=self.max,
            pattern=self.pattern,
            **kwargs,
        )

    def render(self, *args, name, placeholder="", min, max, pattern="null", **kwargs):
        return IntegerInput(
            name=name,
            placeholder=placeholder,
            type="number",
            min=min,
            max=max,
            pattern=pattern,
        )


Validator.register(IntegerNumberInput)  # noqa


class IntegerNumberInputValidator(Validator):
    annotation = T.Union[IntegerNumberInput, None]


@dataclass(eq=False)
class IntegerRangeInput(HTMLElement):
    name: str
    placeholder: str
    min: T.Union[str, None] = field(default=None)
    max: T.Union[str, None] = field(default=None)
    pattern: T.Union[str, None] = field(default=None)

    def __post_init__(self, *args, **kwargs):
        super(IntegerRangeInput, self).__init__(
            *args,
            name=self.name,
            placeholder=self.placeholder,
            min=self.min,
            max=self.max,
            pattern=self.pattern,
            **kwargs,
        )

    def render(
        self,
        *args,
        name,
        placeholder="",
        min="null",
        max="null",
        pattern="null",
        **kwargs,
    ):
        return IntegerInput(
            type="range",
            name=name,
            placeholder=placeholder,
            min=min,
            max=max,
            pattern=pattern,
        )


Validator.register(IntegerRangeInput)  # noqa


class IntegerRangeInputValidator(Validator):
    annotation = T.Union[IntegerRangeInput, None]


@dataclass(eq=False)
class TelephoneInput(HTMLElement):
    name: str
    placeholder: str
    min: T.Union[str, None] = field(default=None)
    max: T.Union[str, None] = field(default=None)
    pattern: T.Union[str, None] = field(default=None)

    def __post_init__(self, *args, **kwargs):
        super(TelephoneInput, self).__init__(
            *args,
            name=self.name,
            placeholder=self.placeholder,
            min=self.min,
            max=self.max,
            pattern=self.pattern,
            **kwargs,
        )

    def render(self, *args, name, placeholder="", min, max, pattern, **kwargs):
        return IntegerInput(
            type="tel",
            name=name,
            placeholder=placeholder,
            min=min,
            max=max,
            pattern=pattern,
        )


@dataclass(eq=False)
class IntegerField(HTMLElement):
    labeled = IntegerLabelValidator(logger=False, debug=True)
    input = IntegerInputValidator(logger=False, debug=True)

    label: str
    name: str
    placeholder: str
    type: str

    def __post_init__(self, *args, **kwargs):
        super(IntegerField, self).__init__(
            *args,
            label=self.label,
            name=self.name,
            placeholder=self.placeholder,
            type=self.type,
            **kwargs,
        )

    def render(self, *args, label, name, placeholder, type, **kwargs):
        self.labeled = IntegerLabel(label=label)
        self.input = IntegerInput(name=name, placeholder=placeholder, type=type)
        return self.html_tags.div(*args, self.labeled, self.input, **kwargs)


@dataclass(eq=False)
class IntegerNumberField(HTMLElement):
    labeled = IntegerLabelValidator(logger=False, debug=True)
    input = IntegerNumberInputValidator(logger=False, debug=True)

    label: str
    name: str
    placeholder: str

    def __post_init__(self, *args, **kwargs):
        super(IntegerNumberField, self).__init__(
            *args,
            label=self.label,
            name=self.name,
            placeholder=self.placeholder,
            **kwargs,
        )

    def render(self, *args, label, name, placeholder, **kwargs):
        self.labeled = IntegerLabel(label=label)
        self.input = IntegerNumberInput(name=name, placeholder=placeholder)
        return self.html_tags.div(*args, self.labeled, self.input, **kwargs)


@dataclass(eq=False)
class IntegerRangeField(HTMLElement):
    labeled = IntegerLabelValidator(logger=False, debug=True)
    input = IntegerRangeInputValidator(logger=False, debug=True)

    label: str
    name: str
    placeholder: str

    def __post_init__(self, *args, **kwargs):
        super(IntegerRangeField, self).__init__(
            *args,
            label=self.label,
            name=self.name,
            placeholder=self.placeholder,
            **kwargs,
        )

    def render(self, *args, label, name, placeholder, **kwargs):
        self.labeled = IntegerLabel(label=label)
        self.input = IntegerRangeInput(name=name, placeholder=placeholder)
        return self.html_tags.div(*args, self.labeled, self.input, **kwargs)


if __name__ == "__main__":
    from uidom.dom import form
    from uidom.elements import SubmitButton

    quantity = IntegerNumberField(
        label="Quantity", name="quantity", placeholder="quantity"
    )
    quantity.input["id"] = quantity.labeled["for"] = "quantity-id"
    price = IntegerNumberField(label="Price", name="price", placeholder="price")
    price.input["id"] = price.labeled["for"] = "price-id"
    button = SubmitButton("Submit", value="submit")
    forms = form(IntegerLegend("Product"), price, quantity, button)
    print(forms)
    print(IntegerNumberInput(name="price", placeholder="Price", min="2"))
