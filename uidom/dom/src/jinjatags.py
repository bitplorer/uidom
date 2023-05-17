# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from jinja2.environment import Template

from uidom.dom.src.dom_tag import dom_tag
from uidom.dom.src.main import extension

__all__ = [
    "If",
    "Elif",
    "Else",
    "For",
    "AutoEscape",
    "Include",
    "Cycle",
    "Comment",
    "Extends",
    "Load",
    "CSRFToken",
    "Block",
    "Var",
    "render_jinja",
    "JinjaSingleTags",
    "JinjaDoubleTags",
    "JinjaBaseTag",
]


class JinjaBaseTag(object):
    pass


class JinjaDoubleTags(JinjaBaseTag, extension.DoubleTemplates):
    self_dedent = False
    child_dedent = False
    enable_left_delimiter_space = True
    enable_right_delimiter_space = True

    def __call__(self, **options):
        return render_jinja(self, **options)


class JinjaSingleTags(JinjaBaseTag, extension.SingleTemplates):
    self_dedent = False
    child_dedent = True
    enable_left_delimiter_space = True
    enable_right_delimiter_space = True

    def __call__(self, **options):
        return render_jinja(self, **options)


class Block(JinjaDoubleTags):
    def __init__(self, template_text, *dom_elements):
        """
        :param template_text:
        :param dom_elements: [optional] template
        """
        super(Block, self).__init__("block", template_text, *dom_elements)


class For(JinjaDoubleTags):
    def __init__(self, template_text, *dom_elements):
        """
        :param template_text:
        :param dom_elements: [optional] template
        """
        super(For, self).__init__("for", template_text, *dom_elements)


class If(JinjaDoubleTags):
    def __init__(self, template_text, *dom_elements):
        """
        :param template_text:
        :param dom_elements: [optional] template
        """
        super(If, self).__init__("if", template_text, *dom_elements)


class Elif(JinjaSingleTags):
    self_dedent = True
    child_dedent = False

    def __init__(self, template_text, *dom_elements):
        """
        :param template_text:
        :param dom_elements: [optional] template
        """

        super(Elif, self).__init__(
            "elif",
            template_text,
            *dom_elements,
        )


class Else(JinjaSingleTags):
    self_dedent = True
    child_dedent = False
    enable_right_delimiter_space = False

    def __init__(self, *dom_elements):
        """
        :param template_text:
        :param dom_elements: [optional] template
        """

        super(Else, self).__init__("else", "", *dom_elements)


class AutoEscape(JinjaSingleTags):
    def __init__(self, template_text, *dom_elements):
        """
        :param template_text:
        :param dom_elements: [optional] template
        """

        super(AutoEscape, self).__init__("autoescape", template_text, *dom_elements)


class Include(JinjaSingleTags):
    def __init__(self, template_text, *dom_elements):
        """
        :param template_text:
        :param dom_elements: [optional] template
        """

        super(Include, self).__init__("include", template_text, *dom_elements)


class Cycle(JinjaSingleTags):
    def __init__(self, template_text, *dom_elements):
        """
        :param template_text:
        :param dom_elements: [optional] template
        """

        super(Cycle, self).__init__("cycle", template_text, *dom_elements)


class Comment(JinjaDoubleTags):
    def __init__(self, template_text, *dom_elements):
        """
        :param template_text:
        :param dom_elements: [optional] template
        """

        super(Comment, self).__init__("comment", template_text, *dom_elements)


class Extends(JinjaSingleTags):
    def __init__(self, template_text, *dom_elements):
        """
        :param template_text:
        :param dom_elements: [optional] template
        """

        super(Extends, self).__init__("extends", template_text, *dom_elements)


class Load(JinjaSingleTags):
    def __init__(self, template_text, *dom_elements):
        """
        :param template_text:
        :param dom_elements: [optional] template
        """

        super(Load, self).__init__("load", template_text, *dom_elements)


class CSRFToken(JinjaSingleTags):
    def __init__(self, *dom_elements):
        """
        :param template_text:
        :param dom_elements: [optional] template
        """

        super(CSRFToken, self).__init__("csrf_token", "", *dom_elements)


class Var(JinjaSingleTags):
    left_delimiter = "{{"
    right_delimiter = "}}"

    def __init__(self, template_text, *dom_elements):
        """
        :param template_text:
        :param dom_elements: [optional] template
        """

        super(Var, self).__init__("", template_text, *dom_elements)


def render_jinja(template, **options):
    return raw(
        Template(
            template.__render__() if isinstance(template, dom_tag) else template,
            lstrip_blocks=True,
            trim_blocks=True,
            enable_async=True,
        ).render(**options)
    )


from uidom.dom.src.utils import raw
