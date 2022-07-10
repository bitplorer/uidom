# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.src import extension


class Python(extension.SingleTemplates):
    enable_right_delimiter_space = False
    enable_left_delimiter_space = True
    enable_space_in_between = False

    def render(self, indent="    ", pretty=True, xhtml=False):
        data = self._render([], 0, indent, pretty, xhtml)
        return "".join(data)


class Class(Python):
    self_dedent = True
    child_dedent = False
    left_delimiter = "class"
    right_delimiter = ":"

    def __init__(self, class_name, *dom_elements, bases=None):
        """
        :param class_name:
        :param dom_elements: [optional] template
        """

        super(Class, self).__init__(
            f"{class_name}",
            f"({', '.join(bases.split(' ')) if bases is not None else 'object'})",
            *dom_elements,
        )


class Args(Python):
    def __init__(self, func_name, *dom_elements):
        super(Args, self).__init__(f"{func_name}", "(self)", *dom_elements)


class Kwargs(Python):
    pass


class Def(Python):
    left_delimiter = "def"
    right_delimiter = ":"

    def __init__(self, func_name, *dom_elements, args=""):
        super(Def, self).__init__(f"{func_name}", f"({', '.join(['self', *args.split(' ')]) if any(args) else 'self'})",
                                  *dom_elements)
        if func_name == "__init__" and any(args):
            [self.add(SelfAttr(arg)) for arg in args.split(" ")]


class SelfAttr(Python):
    left_delimiter = ""
    right_delimiter = ""
    enable_left_delimiter_space = False

    def __init__(self, atr_name, *dom_elements):
        super(SelfAttr, self).__init__(f"self.{atr_name}", '', *dom_elements)


if __name__ == "__main__":
    import ast
    person = Class("Person",
                   # Def("__init__", args="name address"),
                   Def('__render__', args="*args **kwargs"),
                   bases="models.Model logging.Logger")
    print(person)
