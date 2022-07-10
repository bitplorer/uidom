# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.src import extension


class Sphinx(extension.SingleTemplates):
    self_dedent = True
    left_delimiter = ''
    right_delimiter = ''
    enable_left_delimiter_space = False
    enable_right_delimiter_space = False


class Heading(Sphinx):
    child_dedent = True

    def __init__(self, heading_name, *dom_elements):
        """
        :param heading_name:
        :param dom_elements:
        """
        super(Heading, self).__init__("", heading_name, Sphinx("", "=" * len(heading_name)), *dom_elements)


class VarName(Sphinx):
    left_delimiter = "`"
    right_delimiter = "`"

    def __init__(self, type_text, *dom_elements):
        """
        :param type_text:
        :param dom_elements: [optional] template
        """
        super(VarName, self).__init__("", type_text, *dom_elements)


class Class(Sphinx):
    left_delimiter = ":"
    right_delimiter = ":"
    self_dedent = True

    def __init__(self, template_text, *dom_elements):
        """
        :param template_text:
        :param dom_elements: [optional] template
        """
        super(Class, self).__init__("class", template_text, *dom_elements)


class Function(Sphinx):
    left_delimiter = ""

    def __init__(self, template_text, *dom_elements):
        """
        :param template_text:
        :param dom_elements: [optional] template
        """
        super(Function, self).__init__(":class:", template_text, *dom_elements)


if __name__ == "__main__":
    var_name = VarName("something")
    class_name = Class("BaseClass", var_name)
    print(Heading("Hello0ijj", class_name, Function("ls")))
