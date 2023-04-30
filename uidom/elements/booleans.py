# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import typing as T
from dataclasses import dataclass

from valio import StringValidator, Validator

from uidom.dom.htmlelement import HTMLElement
from uidom.elements.buttons import SubmitButton

__all__ = [
    # boolean html
    "BooleanLabel",
    "BooleanLegend",
    "BooleanInput",
    "CheckboxInput",
    "RadioInput",
    "BooleanField",
]


@dataclass(eq=False)
class BooleanLabel(HTMLElement):
    label: str = StringValidator(logger=False, debug=True)

    def __post_init__(self, *args, **kwargs):
        super(BooleanLabel, self).__init__(self.label, *args, **kwargs)

    def render(self, label: str, *args, **kwargs):  # noqa
        return self.html_tags.label(label, *args, **kwargs)


class BooleanLabelValidator(Validator):
    annotation = T.Union[BooleanLabel, None]


@dataclass(eq=False)
class BooleanLegend(HTMLElement):
    label: str = StringValidator(logger=False, debug=True)

    def __post_init__(self, *args, **kwargs):
        super(BooleanLegend, self).__init__(self.label, *args, **kwargs)

    def render(self, label: str, *args, **kwargs):
        return self.html_tags.legend(label, *args, **kwargs)


@dataclass(eq=False)
class BooleanInput(HTMLElement):
    name: str = StringValidator(logger=False, debug=True)
    type: str = StringValidator(
        in_choice=["checkbox", "radio"], logger=False, debug=True, default="checkbox"
    )
    checked: T.Union[str, bool] = Validator(
        in_choice=["unchecked", "checked", "null", True, False],
        logger=False,
        debug=True,
        default="checked",
    )

    def __post_init__(self, *args, **kwargs):
        super(BooleanInput, self).__init__(
            *args, name=self.name, type=self.type, checked=self.checked, **kwargs
        )

    def render(self, *args, name, type, checked, **kwargs):
        return self.html_tags.input_(
            *args,
            name=name,
            type=type,
            checked=checked if checked != "null" else False,
            **kwargs,
        )


class BooleanInputValidator(Validator):
    annotation = T.Union[BooleanInput, None]


@dataclass(eq=False)
class CheckboxInput(BooleanInput):
    name: str = StringValidator(logger=False, debug=True)
    checked: T.Union[str, bool] = Validator(
        in_choice=["unchecked", "checked", "null", True, False],
        logger=False,
        debug=True,
    )

    def __post_init__(self, *args, **kwargs):
        super(BooleanInput, self).__init__(
            *args, name=self.name, checked=self.checked, **kwargs
        )

    def render(self, *args, name, checked, **kwargs):
        return super().render(
            *args,
            name=name,
            type="checkbox",
            checked=checked,
            **kwargs,
        )


@dataclass(eq=False)
class RadioInput(BooleanInput):
    name: str = StringValidator(logger=False, debug=True)
    checked: T.Union[str, bool] = Validator(
        in_choice=["unchecked", "checked", "null", True, False],
        logger=False,
        debug=True,
        default="checked",
    )

    def __post_init__(self, *args, **kwargs):
        super(BooleanInput, self).__init__(
            *args, name=self.name, checked=self.checked, **kwargs
        )

    def render(self, *args, name, checked, **kwargs):
        return super().render(
            *args,
            name=name,
            type="radio",
            checked=checked,
            **kwargs,
        )


@dataclass(eq=False)
class BooleanField(HTMLElement):
    labeled = BooleanLabelValidator(logger=False, debug=True)
    input = BooleanInputValidator(logger=False, debug=True)
    label: str
    name: str
    type: str
    checked: T.Union[str, bool]

    def __post_init__(self, *args, **kwargs):
        super(BooleanField, self).__init__(
            *args,
            label=self.label,
            name=self.name,
            type=self.type,
            checked=self.checked,
            **kwargs,
        )

    @property
    def input_id(self):
        return self.input["id"]

    @input_id.setter
    def input_id(self, id):
        self.labeled["for"] = self.input["id"] = id

    def render(self, *args, label, name, type, checked, **kwargs):
        self.labeled = BooleanLabel(label)
        self.input = BooleanInput(
            name=name,
            type=type,
            checked=checked,
        )
        return self.html_tags.div(*args, self.labeled, self.input, **kwargs)


if __name__ == "__main__":
    from uidom.dom import form

    field = BooleanField(
        label="Terms and Conditions", checked="null", name="select", type="radio"
    )
    button = SubmitButton(label="Agree", value="agree")
    field.input_id = "select"
    button["for"] = field["id"] = "xyz"
    print(form(field, button, method="POST"))
    print(RadioInput(checked="unchecked", name="deliver"))
