# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import typing as T
from dataclasses import dataclass, field

from valio import StringValidator, Validator

from uidom.dom.htmlelement import HTMLElement

__all__ = [
    # char html
    "CharLabel",
    "CharLegend",
    "CharInput",
    "TextInput",
    "PasswordInput",
    "HiddenInput",
    "SearchInput",
    "CharField",
    "CharFieldSet"
]


@dataclass(eq=False)
class CharLabel(HTMLElement):
    label: str = StringValidator(logger=False, debug=True)

    def __post_init__(self, *args, **kwargs):
        super(CharLabel, self).__init__(label=self.label, *args, **kwargs)

    def render(self, label: str, *args, **kwargs):  # noqa
        return self.html_tags.label(label, *args, **kwargs)


class CharLabelValidator(Validator):
    annotation = T.Union[CharLabel, None]


@dataclass(eq=False)
class CharLegend(HTMLElement):
    label: str = StringValidator(logger=False, debug=True)

    def __post_init__(self, *args, **kwargs):
        super(CharLegend, self).__init__(label=self.label, *args, **kwargs)

    def render(self, label, *args, **kwargs):
        return self.html_tags.legend(label, *args, **kwargs)


min_length_field = StringValidator(logger=False, debug=True, name="min_length")
max_length_field = StringValidator(logger=False, debug=True, name="max_length")
spell_check_field = StringValidator(in_choice=["true", "false"], 
                                    logger=False, debug=True, name="spell_check", 
                                    default="true")


@dataclass(eq=False)
class CharInput(HTMLElement):

    @max_length_field.add_validator
    @min_length_field.add_validator
    def cast2int(self, value):
        if value not in ["null", None]:
            try:
                int(value)
            except TypeError as e:
                raise ValueError(f"{value} is not an int value") from e

    @spell_check_field.add_post_validator
    def password_spell_check_false(self, value):
        if self.type in ["password", "hidden"]:
            return "false"
        return value

    name: T.Union[str, None] = StringValidator(logger=False, debug=True)
    type: T.Union[str, None] = StringValidator(
        in_choice=["text", "password", "hidden", "email", "search"],
        debug=True, logger=False, default="text"
        )

    placeholder: T.Union[str, None] = StringValidator(logger=False, debug=True)
    spell_check: T.Union[str, None] = spell_check_field
    min_length: T.Union[str, None] = min_length_field
    max_length: T.Union[str, None] = max_length_field
    pattern: T.Union[str, None] = StringValidator(logger=False, debug=True, default="null")

    def __post_init__(self, *args, **kwargs):
        super(CharInput, self).__init__(*args,
                                        name=self.name,
                                        placeholder=self.placeholder,
                                        spell_check=self.spell_check,
                                        type=self.type,
                                        min_length=self.min_length,
                                        max_length=self.max_length,
                                        pattern=self.pattern,
                                        **kwargs)

    def render(
            self,
            *args,
            name: str = None,
            placeholder: str = "",
            spell_check: str,
            type: str,
            min_length: str,
            max_length: str,
            pattern: str,
            **kwargs
    ):  
        
        return self.html_tags.input_(
            *args,
            type=type,
            name=name if name is not None else False,
            placeholder=placeholder if placeholder not in ["", None] else False,
            minlength=min_length if min_length not in ["null", None] else False,
            maxlength=max_length if max_length not in ["null", None] else False,
            spellcheck=spell_check if spell_check not in ["null", None] else False,
            pattern=pattern if pattern not in ["null", None] else False,
            **kwargs,
        )


class CharInputValidator(Validator):
    annotation = T.Union[CharInput, None]


@dataclass(eq=False)
class TextInput(HTMLElement):

    name: str
    placeholder: str
    spell_check: T.Union[str, None] = field(default=None)
    min_length: T.Union[str, None] = field(default=None)
    max_length: T.Union[str, None] = field(default=None)
    pattern: T.Union[str, None] = field(default=None)

    def __post_init__(self, *args, **kwargs):
        super(TextInput, self).__init__(*args,
                                        name=self.name,
                                        placeholder=self.placeholder,
                                        spell_check=self.spell_check,
                                        min_length=self.min_length,
                                        max_length=self.max_length,
                                        pattern=self.pattern,
                                        **kwargs)

    def render(
            self,
            *args,
            name: str = None,
            placeholder: str = "",
            spell_check: str = "true",
            min_length: str,
            max_length: str = "null",
            pattern: str = "null",
            **kwargs
    ):
        return CharInput(
            name=name,
            placeholder=placeholder,
            type="text",
            spell_check=spell_check,
            min_length=min_length,
            max_length=max_length,
            pattern=pattern,
        )


@dataclass(eq=False)
class PasswordInput(HTMLElement):
    name: str
    placeholder: str
    spell_check: T.Union[str, None] = field(default=None)
    min_length: T.Union[str, None] = field(default=None)
    max_length: T.Union[str, None] = field(default=None)
    pattern: T.Union[str, None] = field(default=None)

    def __post_init__(self, *args, **kwargs):
        super(PasswordInput, self).__init__(*args,
                                            name=self.name,
                                            placeholder=self.placeholder,
                                            spell_check=self.spell_check,
                                            min_length=self.min_length,
                                            max_length=self.max_length,
                                            pattern=self.pattern,
                                            **kwargs)

    def render(
            self,
            *args,
            name,
            placeholder,
            spell_check,
            min_length,
            max_length,
            pattern,
            **kwargs
    ):
        return CharInput(
            *args,
            name=name,
            placeholder=placeholder,
            type="password",
            spell_check=spell_check,
            min_length=min_length,
            max_length=max_length,
            pattern=pattern,
            **kwargs
        )


@dataclass(eq=False)
class HiddenInput(HTMLElement):
    name: str
    placeholder: str
    spell_check: T.Union[str, None] = field(default=None)
    min_length: T.Union[str, None] = field(default=None)
    max_length: T.Union[str, None] = field(default=None)
    pattern: T.Union[str, None] = field(default=None)

    def __post_init__(self, *args, **kwargs):
        super(HiddenInput, self).__init__(*args,
                                          name=self.name,
                                          placeholder=self.placeholder,
                                          spell_check=self.spell_check,
                                          min_length=self.min_length,
                                          max_length=self.max_length,
                                          pattern=self.pattern,
                                          **kwargs)

    def render(
            self,
            *args,
            name: str = None,
            placeholder: str = "",
            spell_check: str = "true",
            min_length: str = "null",
            max_length: str = "null",
            pattern: str = "null",
            **kwargs
    ):
        return CharInput(
            *args,
            name=name,
            placeholder=placeholder,
            type="hidden",
            spell_check=spell_check,
            min_length=min_length,
            max_length=max_length,
            pattern=pattern,
            **kwargs
        )


@dataclass(eq=False)
class EmailInput(HTMLElement):
    name: str
    placeholder: str
    spell_check: T.Union[str, None] = field(default=None)
    min_length: T.Union[str, None] = field(default=None)
    max_length: T.Union[str, None] = field(default=None)
    pattern: T.Union[str, None] = field(default=None)

    def __post_init__(self, *args, **kwargs):
        super(EmailInput, self).__init__(*args,
                                         name=self.name,
                                         placeholder=self.placeholder,
                                         spell_check=self.spell_check,
                                         min_length=self.min_length,
                                         max_length=self.max_length,
                                         pattern=self.pattern,
                                         **kwargs)

    def render(
            self,
            *args,
            name: str = None,
            placeholder: str = "",
            spell_check: str = "true",
            min_length: str = "null",
            max_length: str = "null",
            pattern: str = "null",
            **kwargs
    ):
        return CharInput(
            *args, 
            name=name,
            placeholder=placeholder,
            spell_check=spell_check,
            type="email",
            min_length=min_length,
            max_length=max_length,
            pattern=pattern,
            **kwargs
        )


@dataclass(eq=False)
class SearchInput(HTMLElement):
    name: str
    placeholder: str
    spell_check: T.Union[str, None] = field(default=None)
    min_length: T.Union[str, None] = field(default=None)
    max_length: T.Union[str, None] = field(default=None)
    pattern: T.Union[str, None] = field(default=None)

    def __post_init__(self, *args, **kwargs):
        super(SearchInput, self).__init__(*args,
                                          name=self.name,
                                          placeholder=self.placeholder,
                                          spell_check=self.spell_check,
                                          min_length=self.min_length,
                                          max_length=self.max_length,
                                          pattern=self.pattern,
                                          **kwargs)

    def render(
            self,
            *args,
            name: str = None,
            placeholder: str = "",
            spell_check: str = "true",
            min_length: str = "null",
            max_length: str = "null",
            pattern: str = "null",
            **kwargs
    ):
        return CharInput(
            *args,
            name=name,
            placeholder=placeholder,
            type="search",
            spell_check=spell_check,
            min_length=min_length,
            max_length=max_length,
            pattern=pattern,
            **kwargs
        )


@dataclass(eq=False)
class CharField(HTMLElement):
    labeled = CharLabelValidator(logger=False, debug=True)
    input = CharInputValidator(logger=False, debug=True)

    label: str
    name: str
    placeholder: str
    type: str

    def __post_init__(self, *args, **kwargs):
        super(CharField, self).__init__(*args,
                                        label=self.label,
                                        name=self.name,
                                        placeholder=self.placeholder,
                                        type=self.type,
                                        **kwargs
                                        )

    def render(self, *args, label, name, placeholder, type, **kwargs):
        self.labeled = CharLabel(label)
        self.input = CharInput(
                  name=name,
                  placeholder=placeholder,
                  type=type
              )
        return self.html_tags.div(*args, self.labeled, self.input, **kwargs)


class CharFieldSet(HTMLElement):

    def render(self, legend: CharLegend, *fields: HTMLElement, **kwargs):
        return self.html_tags.fieldset(legend, *fields, **kwargs)


if __name__ == '__main__':
    print(CharField(label="Cut", name="cut", placeholder="Diamond Cut", type="text"))
    print(HiddenInput(name="password", placeholder="Enter Password", min_length="4"))
    print(CharInput(name="text", placeholder="Enter Password", min_length="13", spell_check="false"))
    