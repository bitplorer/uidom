# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import os
import typing

from jinja2.utils import htmlsafe_json_dumps
from uidom.dom.src.dom1core import dom1core
from uidom.dom.src.dom_tag import dom_tag, unicode
from uidom.dom.src.utils.dom_util import escape

__all__ = ["SingleTemplates", "DoubleTemplates", "DoubleTags", "SingleTags", "StyleTags"]


class Tags(dom_tag, dom1core):
    left_delimiter = "<"
    right_delimiter = ">"
    self_dedent = False
    child_dedent = False
    render_tag = True
    new_line_at_end = False
    SELF_DEDENT = "self_dedent"
    CHILD_DEDENT = "child_dedent"
    OPEN_TAG = "open_tag"
    CLOSE_TAG = "close_tag"
    RENDER_TAG = "render_tag"
    NEW_LINE_AT_CHILD_END = "new_line_at_child_end"
    file_extension = ".html"

    def __init__(self, *args, **kwargs):
        if any(args):
            msg = f"can only pass {dom_tag!r} or {str!r} types in arguments, got {args!r} instead"
            if not all(map(lambda x: isinstance(x, (dom_tag, str)), args)):
                raise TypeError(msg)
        super(Tags, self).__init__(*args, **kwargs)

    def _render_open_tag(self, sb, indent_level, indent_str, pretty, xhtml, name, open_tag):
        if open_tag:
            sb.append("%s" % open_tag)
        else:
            # open tag is absent
            sb.append(self.left_delimiter)
            sb.append(name)
            sb = self._render_attribute(sb, indent_level, indent_str, pretty, xhtml)
            sb.append(''.join(["/", self.right_delimiter]) if self.is_single and xhtml else self.right_delimiter)
        return sb

    def _render_attribute(self, sb, indent_level, indent_str, pretty, xhtml):
        for attribute, value in sorted(self.attributes.items()):
            if value is not False and value not in [None]:  # False values must be omitted completely
                if not isinstance(value, (typing.MutableMapping, typing.MutableSequence)):
                    sb.append(' %s="%s"' % (attribute, escape(unicode(value), True)))
                else:
                    value = htmlsafe_json_dumps(value)
                    sb.append(" %s='%s'" % (attribute, escape(unicode(value), True)))
            if value in [None]:  # minified xhtml attributes are added
                sb.append(' %s' % attribute)
        return sb

    def _render_close_tag(self, sb, name, close_tag):
        if close_tag:
            sb.append("%s" % close_tag)
        else:
            sb.append(''.join([self.left_delimiter, "/"]))
            sb.append(name)
            sb.append(self.right_delimiter)
        return sb

    @staticmethod
    def _new_line_and_inline_handler(sb, indent_level, indent_str, pretty, is_inline):
        if pretty and not is_inline:
            is_inline = False
            sb.append("\n")
            sb.append(indent_str * indent_level)
        return sb, is_inline

    @staticmethod
    def _dedent_handler(dedent, indent_level):
        if dedent:
            indent_level -= 1
        return indent_level

    @staticmethod
    def clean_attribute(attribute):
        """
        Normalize attribute names for shorthand and work arounds for limitations
        in Python's syntax. Extended it to support VueJS, HTMX and AngularJS.
        """

        # Shorthand
        attribute = {
            'cls': 'class',
            'className': 'class',
            'class_name': 'class',
            'fr': 'for',
            'html_for': 'for',
            'htmlFor': 'for',
        }.get(attribute, attribute)

        # Workaround for Python's reserved words
        if len(attribute) >= 2:
            if attribute[0] == '_' and attribute[1] != "_":
                attribute = attribute[1:]

        # Workaround for dash plus support for VueJS, HTMX, Unpoly and AngularJS
        special_prefix = any(
            [attribute.startswith(x) for x in ('data_', 'aria_', 'x_', 'v_', 'ng_', "hx_", "__", "ws__", "up_",
                                               "remove_me")])
        if attribute in {'http_equiv'} or special_prefix:
            attribute = attribute.replace('_', '-')
            attribute = attribute.replace("--", ":")
            attribute = attribute.replace("v-bind-", ":")
            attribute = attribute.replace("v-bind", "")
            attribute = attribute.replace("x-bind-", ":")
            attribute = attribute.replace("x-bind", "")
            attribute = attribute.replace("x-transition-", "x-transition:")
            attribute = attribute.replace("v-on:", "@")
            attribute = attribute.replace("v-on-", "@")
            attribute = attribute.replace("x-on:", "@")
            attribute = attribute.replace("x-on-", "@")
            attribute = attribute.replace("-dot-", ".")

        # Workaround for colon
        if attribute.split('_')[0] in ('xlink', 'xml', 'xmlns'):
            attribute = attribute.replace('_', ':', 1)

        return attribute

    def _clean_name(self, name):
        # Workaround for python keywords and standard classes/methods
        # (del, object, input)
        if any(name):  # to handle the case when tagname = ""
            if name[-1] == '_':
                name = name[:-1]
        return name

    def _render_children(self, sb, indent_level, indent_str, pretty, xhtml):
        inline = True
        orig_indent = indent_level
        self_render_tag = self.attributes.pop(Tags.RENDER_TAG,
                                              getattr(self, Tags.RENDER_TAG)
                                              if hasattr(self, Tags.RENDER_TAG) else True)
        for child in self.children:
            if isinstance(child, dom_tag):

                child_self_dedent = child.attributes.pop(Tags.SELF_DEDENT,
                                                         getattr(child, Tags.SELF_DEDENT)
                                                         if hasattr(child, Tags.SELF_DEDENT) else False)

                # checks if the self.child_dedent or self.self_dedent if true and dedent the tags
                if pretty and not child.is_inline:
                    inline = False
                    dedent = child_self_dedent
                    if dedent:
                        if indent_level > orig_indent - 1:
                            indent_level = self._dedent_handler(dedent, indent_level)

                if self_render_tag:
                    sb, inline = self._new_line_and_inline_handler(
                        sb, indent_level, indent_str, pretty, inline and self.is_inline)

                child._render(sb, indent_level, indent_str, pretty, xhtml)

            else:
                if any(child):
                    if not (pretty and not self.is_inline):
                        sb.append(unicode(child))
                    else:
                        inline = False
                        sb, inline = self._new_line_and_inline_handler(
                            sb, indent_level, indent_str, pretty, inline)
                        sb.append(unicode(child))

            # new_line_at_end caters to DOCTYPE Tag as its wrapped in an empty wrapper
            new_line_at_child_end = self.attributes.pop(Tags.NEW_LINE_AT_CHILD_END,
                                                        getattr(self, Tags.NEW_LINE_AT_CHILD_END)
                                                        if hasattr(self, Tags.NEW_LINE_AT_CHILD_END) else False)

            # new_line_at_child_end caters to ConcatTag as its an empty wrapper and children needs
            # '\n' new line support except the last one
            if new_line_at_child_end and self.children[-1] != child:
                sb, _ = self._new_line_and_inline_handler(sb, indent_level, indent_str, pretty,
                                                          inline and self.is_inline)
        return inline

    def _render(self, sb, indent_level=1, indent_str="  ", pretty=True, xhtml=False):
        open_tag = self.attributes.pop(Tags.OPEN_TAG, False)
        close_tag = self.attributes.pop(Tags.CLOSE_TAG, False)
        pretty = pretty and self.is_pretty and not self.is_inline
        # name = self._clean_name(getattr(self, 'tagname', type(self).__name__))
        self_child_dedent = self.attributes.pop(Tags.CHILD_DEDENT,
                                                getattr(self, Tags.CHILD_DEDENT)
                                                if hasattr(self, Tags.CHILD_DEDENT) else False)

        self_render_tag = self.attributes.pop(Tags.RENDER_TAG,
                                              getattr(self, Tags.RENDER_TAG)
                                              if hasattr(self, Tags.RENDER_TAG) else True)

        dedent = (not self_render_tag) or self_child_dedent
        if pretty and dedent:
            indent_level = self._dedent_handler(dedent, indent_level)

        if self_render_tag:
            name = self._clean_name(getattr(self, 'tagname', type(self).__name__))
            self._render_open_tag(sb, indent_level, indent_str, pretty, xhtml, name, open_tag)

        inline = self._render_children(sb,
                                       indent_level + 1 if not self.is_single or not self_child_dedent else indent_level,
                                       indent_str, pretty, xhtml)
        inline = self.is_inline and inline
        if self_render_tag:
            if not self.is_single:
                sb, inline = self._new_line_and_inline_handler(sb, indent_level, indent_str, pretty, inline)
                name = self._clean_name(getattr(self, 'tagname', type(self).__name__))
                self._render_close_tag(sb, name, close_tag)

        return sb

    def save(
            self,
            file_name: str = None,
            template_folder: str = "static",
            html_template=None,
            current_dir=False,
    ):
        html_template = html_template or self.render()
        current_folder = os.getcwd()
        doc_folder = current_folder if current_dir else os.path.dirname(current_folder)
        template_folder = os.path.join(doc_folder, template_folder)
        file_name = file_name or str(self.__class__.__name__)
        if self.file_extension is None:
            raise ValueError(f"can not save file with {self.file_extension!r} type extension")
        template_file = (
            file_name
            if file_name.endswith(self.file_extension)
            else ".".join([file_name, self.file_extension[1:]])
        )
        if not os.path.exists(template_folder):
            os.makedirs(template_folder)

        template_file_path = os.path.join(template_folder, template_file)

        if not os.path.exists(template_file_path):
            with open(template_file_path, "w+") as f:
                f.write(html_template)
        else:
            with open(template_file_path, "r") as temp:
                old_html = temp.read()
                if old_html != html_template:
                    with open(template_file_path, "w") as f:
                        f.write(html_template)
        return template_file


class SingleTags(Tags):
    left_delimiter = "<"
    right_delimiter = ">"
    is_single = True


class DoubleTags(Tags):
    left_delimiter = "<"
    right_delimiter = ">"


class SingleTemplates(SingleTags):
    left_delimiter = "{%"
    right_delimiter = "%}"
    self_dedent = False
    child_dedent = False
    enable_left_delimiter_space = True
    enable_right_delimiter_space = True
    enable_space_in_between = True

    def __init__(self,
                 template_name,
                 template_text,
                 *dom_elements,
                 self_dedent=None,
                 child_dedent=None,
                 **kwargs
                 ):
        open_tag = (
            "".join(
                [
                    self.left_delimiter,
                    " " if self.enable_left_delimiter_space else "",
                    template_name,
                    " " if self.enable_space_in_between else "",
                    template_text,
                    " " if self.enable_right_delimiter_space else "",
                    self.right_delimiter,
                ]
            )
            if any(template_name)
            else (
                "".join(
                    [
                        self.left_delimiter,
                        " " if self.enable_left_delimiter_space else "",
                        template_text,
                        " " if self.enable_right_delimiter_space else "",
                        self.right_delimiter
                    ]
                )
            )
        )
        super(SingleTemplates, self).__init__(open_tag=open_tag,
                                              self_dedent=self_dedent or self.self_dedent,
                                              child_dedent=child_dedent or self.child_dedent,
                                              **kwargs)
        if any(dom_elements):
            self.add(*dom_elements)


class DoubleTemplates(DoubleTags):
    left_delimiter = "{%"
    right_delimiter = "%}"
    self_dedent = True
    child_dedent = True
    closing_template_tag = "end"
    enable_left_delimiter_space = True
    enable_right_delimiter_space = True
    enable_space_in_between = True

    def __init__(self,
                 template_name,
                 template_text,
                 *dom_elements,
                 self_dedent=None,
                 child_dedent=None,
                 **kwargs
                 ):
        open_tag = "".join(
            [
                self.left_delimiter,
                " " if self.enable_left_delimiter_space else "",
                template_name,
                " " if self.enable_space_in_between else "",
                template_text,
                " " if self.enable_right_delimiter_space else "",
                self.right_delimiter,
            ]
        )
        close_tag = "".join([self.closing_template_tag, template_name])
        close_tag = "".join(
            [
                self.left_delimiter,
                " " if self.enable_left_delimiter_space else "",
                close_tag,
                " " if self.enable_right_delimiter_space else "",
                self.right_delimiter,
            ]
        )
        super(DoubleTemplates, self).__init__(open_tag=open_tag,
                                              close_tag=close_tag,
                                              self_dedent=self_dedent or self.self_dedent,
                                              child_dedent=child_dedent or self.child_dedent,
                                              **kwargs)
        if any(dom_elements):
            self.add(*dom_elements)


class StyleTags(Tags):
    left_delimiter = "{"
    right_delimiter = "}"
    self_dedent = False
    is_class = False
    is_id = False
    is_apply = False

    def _render_open_tag(self, sb, indent_level, indent_str, pretty, xhtml, name, open_tag):
        sb.append(name)
        if pretty:
            sb.append(" ")
        sb.append(self.left_delimiter)
        if pretty:
            sb.append("\n")
            sb.append(indent_str * indent_level)
        sb = self._render_attribute(sb, indent_level, indent_str, pretty, xhtml)
        # sb.append(''.join(["/", self.right_delimiter]) if self.is_single and xhtml else self.right_delimiter)
        return sb

    def _render_attribute(self, sb, indent_level, indent_str, pretty, xhtml):
        attribute_joiner = '%s:%s;' if not pretty else '    %s: %s;\n' + (
                indent_str * indent_level) if not self.is_apply else '@%s %s;' if not pretty else '    @%s %s;\n' + (
                indent_str * indent_level)
        for attribute, value in sorted(self.attributes.items()):
            if value is not False and value is not None:  # False values must be omitted completely
                sb.append(attribute_joiner % (attribute, escape(unicode(value), True)))

            if value is None:  # minified xhtml attributes are added
                sb.append(' %s' % attribute)
        return sb

    def _render_close_tag(self, sb, name, close_tag):
        sb.append(self.right_delimiter)
        return sb

    def _clean_name(self, name):
        # Workaround for python keywords and standard classes/methods
        # (del, object, input)
        if any(name):  # to handle the case when tagname = ""
            if name[-1] == '_':
                name = name[:-1]

        if all([self.is_class, self.is_id]):
            raise AttributeError(f"{name} can not have both is_class and is_id as True")

        if self.is_class:
            name = ''.join([".", name])

        if self.is_id:
            name = ''.join(["#", name])

        return name

    @property
    def attr(self):
        r = []
        attribute_joiner = '%s:%s;' if not self.is_apply else "@%s %s;"

        for attribute, value in sorted(self.attributes.items()):
            if value is not False and value is not None:  # False values must be omitted completely
                r.append(attribute_joiner % (attribute, escape(unicode(value), True)))

            if value is None:  # minified xhtml attributes are added
                r.append(' %s' % attribute)
        return u''.join(r)

    @staticmethod
    def clean_attribute(attribute):
        """
        Normalize attribute names for shorthand and work around for limitations
        in Python's syntax.
        """

        # Shorthand
        attribute = {
            'cls': 'class',
            'className': 'class',
            'class_name': 'class',
            'fr': 'for',
            'html_for': 'for',
            'htmlFor': 'for',
        }.get(attribute, attribute)

        # Workaround for Python's reserved words
        if attribute[0] == '_':
            attribute = attribute[1:]

        attribute = attribute.replace('_', '-')

        # Workaround for colon
        if attribute.split('_')[0] in ('xlink', 'xml', 'xmlns'):
            attribute = attribute.replace('_', ':', 1)

        return attribute


# if __name__ == '__main__':

    # class TestTag(Tags):
    #     pass
    #
    # class TestSingle(TestTag, SingleTags):
    #     pass
    #
    # class TestDouble(TestTag, DoubleTags):
    #     pass
    #
    # class SelfDedentTestSingle(TestSingle):
    #     self_dedent = True
    #
    # class SelfDedentTestDouble(TestDouble):
    #     self_dedent = True
    #
    # class DoubleSelfDedent(SelfDedentTestDouble):
    #     # is_inline = True
    #     pass
    #
    # class SingleSelfDedent(SelfDedentTestSingle):
    #     pass
    #
    #
    # tags = [
    #     Tags(Tags()),
    #     Tags(DoubleSelfDedent(Tags())),
    #     Tags(SingleSelfDedent(Tags())),
    #     Tags(SingleSelfDedent(SingleSelfDedent(Tags()))),
    #     Tags(DoubleSelfDedent(DoubleSelfDedent(Tags()))),
    #     Tags(SingleSelfDedent(DoubleSelfDedent(Tags()))),
    #     Tags(DoubleSelfDedent(SelfDedentTestDouble(Tags()))),
    #     Tags(SingleSelfDedent(Tags(SingleSelfDedent()))),
    #     Tags(DoubleSelfDedent(Tags(DoubleSelfDedent()))),
    #     Tags(SingleSelfDedent(Tags(DoubleSelfDedent()))),
    #     Tags(DoubleSelfDedent(Tags(SingleSelfDedent()))),
    #  ]
    #
    # for i, tag in enumerate(tags, 1):
    #     print(tag)

    # class TestTag(Tags):
    #     pass


    # class TestSingle(TestTag, SingleTags):
    #     pass


    # class TestDouble(TestTag, DoubleTags):
    #     pass


    # class SelfDedentTestSingle(TestSingle):
    #     self_dedent = True


    # class ChildDedentTestSingle(TestSingle):
    #     child_dedent = True


    # class SelfDedentTestDouble(TestDouble):
    #     self_dedent = True


    # class ChildDedentTestDouble(TestDouble):
    #     child_dedent = True


    # class DoubleSelfChildDedent(SelfDedentTestDouble, ChildDedentTestDouble):
    #     pass


    # class SingleSelfChildDedent(SelfDedentTestSingle, ChildDedentTestSingle):
    #     pass


    # class DoubleSelfDedent(SelfDedentTestDouble):
    #     # is_inline = True
    #     pass


    # class SingleSelfDedent(SelfDedentTestSingle):
    #     pass


    # class DoubleChildDedent(ChildDedentTestDouble):
    #     # render_tag = False
    #     pass


    # class SingleChildDedent(ChildDedentTestSingle):
    #     # render_tag = False
    #     pass


    # tags = [Tags(SingleSelfChildDedent(SingleSelfChildDedent(Tags()))),
    #         Tags(DoubleSelfChildDedent(DoubleSelfChildDedent(Tags()))),
    #         Tags(SingleSelfChildDedent(SingleSelfDedent(Tags()))),
    #         Tags(DoubleSelfChildDedent(DoubleSelfDedent("hb", Tags()))),
    #         Tags(SingleSelfChildDedent(SingleChildDedent(Tags()))),
    #         Tags(DoubleSelfChildDedent(DoubleChildDedent(Tags()))),
    #         Tags(SingleSelfChildDedent(Tags(SingleSelfChildDedent()))),
    #         Tags(DoubleSelfChildDedent(Tags(DoubleSelfChildDedent()))),
    #         Tags(SingleSelfChildDedent(Tags(SingleSelfDedent()))),
    #         Tags(DoubleSelfChildDedent(Tags(DoubleSelfDedent()))),
    #         Tags(SingleSelfChildDedent(Tags(SingleChildDedent()))),
    #         Tags(DoubleSelfChildDedent(Tags(DoubleChildDedent()))),
    #         Tags(SingleSelfDedent(SingleSelfChildDedent(Tags()))),
    #         Tags(DoubleSelfDedent(DoubleSelfChildDedent(Tags()))),
    #         Tags(SingleChildDedent(SingleSelfChildDedent(Tags()))),
    #         Tags(DoubleChildDedent(DoubleSelfChildDedent(Tags()))),
    #         Tags(SingleSelfDedent(SingleSelfDedent(Tags()))),
    #         Tags(DoubleSelfDedent(DoubleSelfDedent(Tags()))),
    #         Tags(SingleChildDedent(SingleChildDedent(Tags()))),
    #         Tags(DoubleChildDedent(DoubleChildDedent(Tags()))),
    #         ]

    # for i, tag in enumerate(tags, 1):
    #     print(i, "++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #     print(tag)
    #     print(i, "++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    # x = Tags(Tags(x_bind_name="name"), x_for="name in names")
    # x["class"] = "a"
    # print(x)
