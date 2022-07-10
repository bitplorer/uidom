# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.elements import (CharFieldSet, CharLabel, CharLegend,
                                       PasswordInput, SubmitButton, TextInput)
from uidom.dom.htmlelement import HTMLElement
from uidom.dom.src.htmltags import div, form
from uidom.dom.src.svgtags import svg
from valio import Validator

__all__ = [
    "LoginForm",
    "FieldSetLoginForm"
]


class LoginForm(HTMLElement):
    text_icon: svg = Validator(logger=False, debug=True, required=True)
    text_label: CharLabel = Validator(logger=False, debug=True, required=True)
    text_input: TextInput = Validator(logger=False, debug=True, required=True)
    text_div: div = Validator(logger=False, debug=True, required=True)
    password_icon: svg = Validator(logger=False, debug=True, required=True)
    password_label: CharLabel = Validator(logger=False, debug=True, required=True)
    password_input: PasswordInput = Validator(logger=False, debug=True, required=True)
    password_div: div = Validator(logger=False, debug=True, required=True)
    button: SubmitButton = Validator(logger=False, debug=True, required=True)

    def __render__(
            self,
            *args,
            text_label,
            password_label,
            button_label,
            **kwargs
    ):
        self.text_icon = svg()
        self.text_label = CharLabel(label=text_label)
        self.text_input = TextInput(name="text", placeholder="Enter Username")
        self.text_div = self.html_tags.div(self.text_icon, self.text_label, self.text_input)
        self.password_icon = svg()
        self.password_label = CharLabel(label=password_label)
        self.password_input = PasswordInput(name="password", placeholder="Enter Password")
        self.password_div = self.html_tags.div(self.password_icon, self.password_label, self.password_input)
        self.button = SubmitButton(label=button_label, value="Submit")

        return form(self.text_div, self.password_div, self.button)


class RegisterForm(HTMLElement):
    text_icon: svg = Validator(logger=False, debug=True, required=True)
    text_label: CharLabel = Validator(logger=False, debug=True, required=True)
    text_input: TextInput = Validator(logger=False, debug=True, required=True)
    text_div: div = Validator(logger=False, debug=True, required=True)
    password_icon: svg = Validator(logger=False, debug=True, required=True)
    password_label: CharLabel = Validator(logger=False, debug=True, required=True)
    password_input: PasswordInput = Validator(logger=False, debug=True, required=True)
    password_div: div = Validator(logger=False, debug=True, required=True)
    confirm_password_icon: svg = Validator(logger=False, debug=True, required=True)
    confirm_password_label: CharLabel = Validator(logger=False, debug=True, required=True)
    confirm_password_input: PasswordInput = Validator(logger=False, debug=True, required=True)
    confirm_password_div: div = Validator(logger=False, debug=True, required=True)
    button: SubmitButton = Validator(logger=False, debug=True, required=True)

    def __render__(
            self,
            *args,
            text_label,
            password_label,
            button_label,
            **kwargs
    ):
        self.text_icon = svg()
        self.text_label = CharLabel(label=text_label)
        self.text_input = TextInput()
        self.text_div = div(self.text_icon, self.text_label, self.text_input)
        self.password_icon = svg()
        self.password_label = CharLabel(label=password_label)
        self.password_input = PasswordInput()
        self.password_div = div(self.password_icon, self.password_label, self.password_input)
        self.confirm_password_icon = svg()
        self.confirm_password_label = CharLabel(label=password_label)
        self.confirm_password_input = PasswordInput()
        self.confirm_password_div = div(
            self.confirm_password_icon,
            self.confirm_password_label,
            self.confirm_password_input
        )
        self.button = SubmitButton(label=button_label, value="Submit")

        return form(self.text_div, self.password_div, self.confirm_password_div, self.button)


class FieldSetLoginForm(HTMLElement):
    user_legend: CharLegend = Validator(logger=False, debug=True, required=True)
    user: TextInput = Validator(logger=False, debug=True, required=True)
    password: PasswordInput = Validator(logger=False, debug=True, required=True)
    button: SubmitButton = Validator(logger=False, debug=True, required=True)

    def __render__(
            self,
            *args,
            legend_label,
            text_label,
            password_label,
            button_label,
            **kwargs
    ):
        self.user_legend = CharLegend(legend_label)
        self.user = TextInput()
        self.password = PasswordInput()
        self.button = SubmitButton(label=button_label, value="Submit")
        return form(CharFieldSet(self.user_legend, self.user, self.password, self.button))


if __name__ == '__main__':
    seller_login = LoginForm(text_label="User ID", password_label="Password", button_label="Login")
    print(seller_login)
    # print(FieldSetLoginForm())
