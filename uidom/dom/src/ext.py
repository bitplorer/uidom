# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import os
import re
import textwrap
import typing

from jinja2.utils import htmlsafe_json_dumps

from uidom.dom.src.dom1core import dom1core
from uidom.dom.src.dom_tag import dom_tag, unicode
from uidom.dom.src.utils.dom_util import escape

__all__ = [
    "SingleTemplates",
    "DoubleTemplates",
    "DoubleTags",
    "SingleTags",
    "StyleTags",
]


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

    def _render_open_tag(self, sb, xhtml, name, open_tag):
        if open_tag:
            sb.append("%s" % open_tag)
        else:
            # open tag is absent
            sb.append(self.left_delimiter)
            sb.append(name)
            sb = self._render_attribute(sb)
            sb.append(
                "".join(["/", self.right_delimiter])
                if self.is_single and xhtml
                else self.right_delimiter
            )
        return sb

    def _render_attribute(self, sb):
        for attribute, value in sorted(self.attributes.items()):
            if value is not False and value not in [
                None
            ]:  # False values must be omitted completely
                if attribute == "class":
                    # adding support to write multiline tailwindcss classes
                    multiline_string = textwrap.dedent(value)
                    wrapped_string = textwrap.fill(
                        multiline_string, break_long_words=False, break_on_hyphens=False
                    )
                    value = re.sub(r"\s+", " ", wrapped_string.strip())
                if not isinstance(
                    value, (typing.MutableMapping, typing.MutableSequence)
                ):
                    sb.append(' %s="%s"' % (attribute, escape(unicode(value), True)))
                else:
                    value = htmlsafe_json_dumps(value)
                    sb.append(" %s='%s'" % (attribute, escape(unicode(value), True)))
            if value in [None]:  # minified xhtml attributes are added
                sb.append(" %s" % attribute)
        return sb

    def _render_close_tag(self, sb, name, close_tag):
        if close_tag:
            sb.append("%s" % close_tag)
        else:
            sb.append("".join([self.left_delimiter, "/"]))
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
            "cls": "class",
            "className": "class",
            "class_name": "class",
            "fr": "for",
            "html_for": "for",
            "htmlFor": "for",
        }.get(attribute, attribute)

        # Workaround for Python's reserved words
        if len(attribute) >= 2:
            if attribute[0] == "_" and attribute[1] != "_":
                attribute = attribute[1:]

        # Workaround for dash plus support for VueJS, HTMX, Unpoly and AngularJS
        special_prefix = any(
            [
                attribute.startswith(x)
                for x in (
                    "data_",  # for data-type="value" support
                    "aria_",  # for aria support
                    "x_",  # for AlpineJS and x-component
                    "v_",  # for Vue support
                    "ng_",  # for Angular support
                    "hx_",  # for HTMX support
                    "__",  #
                    "ws__",  #
                    "up_",  # for Unpoly JS support
                    "remove_me",  # for HTMX remove extension support
                )
            ]
        )
        if attribute in {"http_equiv"} or special_prefix:
            attribute = attribute.replace("_", "-")
            attribute = attribute.replace("--", ":")
            attribute = attribute.replace("v-bind-", ":")
            attribute = attribute.replace("v-bind", "")
            attribute = attribute.replace("x-bind-", ":")
            attribute = attribute.replace("x-bind", "")
            attribute = attribute.replace("x-transition-enter", "x-transition:enter")
            attribute = attribute.replace("x-transition-leave", "x-transition:leave")
            attribute = attribute.replace("x-intersect-enter", "x-intersect:enter")
            attribute = attribute.replace("x-intersect-leave", "x-intersect:leave")
            attribute = attribute.replace("v-on:", "@")
            attribute = attribute.replace("v-on-", "@")
            attribute = attribute.replace("x-on:", "@")
            attribute = attribute.replace("x-on-", "@")
            attribute = attribute.replace("-dot-", ".")

        # Workaround for colon
        if attribute.split("_")[0] in ("xlink", "xml", "xmlns"):
            attribute = attribute.replace("_", ":", 1)

        return attribute

    def _clean_name(self, name):
        # Workaround for python keywords and standard classes/methods
        # (del, object, input)
        if any(name):  # to handle the case when tagname = ""
            if name[-1] == "_":
                name = name[:-1]
        return name

    def _render_children(self, sb, indent_level, indent_str, pretty, xhtml):
        inline = True
        orig_indent = indent_level
        self_render_tag = self.attributes.pop(
            Tags.RENDER_TAG,
            getattr(self, Tags.RENDER_TAG) if hasattr(self, Tags.RENDER_TAG) else True,
        )
        for child in self.children:
            if isinstance(child, dom_tag):
                # get the dedent status of child from the parent or the child

                # the dedent status of the child from the parent via self.child_dedent is
                # extracted in the '_render' method already and is already taken care of

                # the dedent status of the child from the child via child.self_dedent is
                # extracted here
                child_self_dedent = child.attributes.pop(
                    Tags.SELF_DEDENT,
                    getattr(child, Tags.SELF_DEDENT)
                    if hasattr(child, Tags.SELF_DEDENT)
                    else False,
                )

                # check if we are pretty-fying the html and only then try to dedent the indentation
                if pretty and not child.is_inline:
                    inline = False
                    # parent or child both can dedent the indentation, but childs value takes the presedence
                    # always so we are skipping self_child_dedent as its already dealt with in '_render' method
                    dedent = child_self_dedent
                    # incase if self.is_single flag is True the dedentation has already happended while
                    # calling "_render_children" inside "_render" method by not incrementing indentation
                    # so we skip dedentation in case the parent has is_single flag True
                    if dedent and not self.is_single:
                        # even while dedentation we will never dedent more than the original parent indentation
                        # it is wrong syntax so we keep checking this
                        # for example:
                        # --------------- ** this can happen
                        # "   "<parent>\n
                        # "   "<child>
                        # -----------
                        # but not this notice how indentation before <child> is less than that of <parent>
                        # "    "<parent>\n
                        # "  "<child>

                        # thus we always ensure that while we dedent the <child> to
                        #
                        if indent_level > orig_indent - 1:
                            indent_level = self._dedent_handler(dedent, indent_level)

                # we will apply the changes only when the render_tag flag is set to True
                # NOTE: we should **not add** checks for (pretty and not self.is_inline) here as this is
                # where we are adding the indentation and new-line **before** child is rendered
                # for eg:
                # <parent>\n
                # "    "<child> // so here '\n' and "    " represents the newline and indentation added
                # <parent>      // after <parent> this is done below here after checking self_render_tag
                if self_render_tag:
                    sb, inline = self._new_line_and_inline_handler(
                        sb, indent_level, indent_str, pretty, inline and self.is_inline
                    )

                child._render(sb, indent_level, indent_str, pretty, xhtml)

            else:
                # check if the child is not an empty string '' via any(child)
                if any(child):
                    # if any child exists maybe its a string or some object here check if the pretty is True
                    if pretty:
                        inline = False
                        if self_render_tag:
                            sb, inline = self._new_line_and_inline_handler(
                                sb, indent_level, indent_str, pretty, inline
                            )
                        sb.append(unicode(child))
                    else:
                        sb.append(unicode(child))

            # new_line_at_end caters to ConcatTag that supports DOCTYPE Tag when
            # its wrapped inside an empty wrapper like ConcatTag
            new_line_at_child_end = self.attributes.pop(
                Tags.NEW_LINE_AT_CHILD_END,
                getattr(self, Tags.NEW_LINE_AT_CHILD_END)
                if hasattr(self, Tags.NEW_LINE_AT_CHILD_END)
                else False,
            )

            # new_line_at_child_end caters to ConcatTag as its an empty wrapper and children needs
            # '\n' new line support except the last one
            if new_line_at_child_end and self.children[-1] != child:
                sb, _ = self._new_line_and_inline_handler(
                    sb, indent_level, indent_str, pretty, inline and self.is_inline
                )
        return inline

    def _render(self, sb, indent_level=1, indent_str="  ", pretty=True, xhtml=False):
        open_tag = self.attributes.pop(Tags.OPEN_TAG, False)
        close_tag = self.attributes.pop(Tags.CLOSE_TAG, False)
        # prettify only if _render method has pretty=True
        pretty = pretty and self.is_pretty and not self.is_inline

        # take out the 'self_dedent' attribute from the self.attributes if any present else fallback to
        # class defined 'self_dedent' if any present else fallback to False
        self_dedent = self.attributes.pop(
            Tags.SELF_DEDENT,
            getattr(self, Tags.SELF_DEDENT)
            if hasattr(self, Tags.SELF_DEDENT)
            else False,
        )

        # assignment to self.self_dedent is necessary to ensure that next time
        # when the self_dedent is popped from attribute it will fallback to the currently assigned value
        self.self_dedent = self_dedent

        # take out the 'child_dedent' attribute from the self.attributes if any present else fallback to
        # class defined 'child_dedent' if any present else fallback to False
        self_child_dedent = self.attributes.pop(
            Tags.CHILD_DEDENT,
            getattr(self, Tags.CHILD_DEDENT)
            if hasattr(self, Tags.CHILD_DEDENT)
            else False,
        )

        # assignment to self.child_dedent is necessary to ensure that next time
        # when the child_dedent is popped from attribute it will fallback to the currently assigned value
        # if the value is popped again
        self.child_dedent = self_child_dedent

        # take out the 'render_tag' attribute from the self.attributes if any present else fallback to
        # class defined 'render_tag' if any present else fallback to True
        self_render_tag = self.attributes.pop(
            Tags.RENDER_TAG,
            getattr(self, Tags.RENDER_TAG) if hasattr(self, Tags.RENDER_TAG) else True,
        )

        # now if "render_tag" is False or self_dedent is True for any reason we will reduce the indentation
        # level but we will not mess with the self dedent here as is_single flag ensures single tags are
        # dedented by default (see '_render_children' method call below) so what remains is the double tags
        # but we dedent double tags only when there is a child involved thus child.self_dedent is parsed
        # under '_render_children' method, thats why commenting
        dedent = not self_render_tag  # or self_dedent
        if pretty and dedent:
            indent_level = self._dedent_handler(dedent, indent_level)

        # if we have to render the self tag
        if self_render_tag:
            name = self._clean_name(getattr(self, "tagname", type(self).__name__))
            self._render_open_tag(sb, xhtml, name, open_tag)

        # here lies the important logic
        inline = self._render_children(
            sb,
            indent_level + 1
            if not self.is_single or not self_child_dedent
            else indent_level,
            indent_str,
            pretty,
            xhtml,
        )
        inline = self.is_inline and inline
        if self_render_tag:
            if not self.is_single:
                sb, inline = self._new_line_and_inline_handler(
                    sb, indent_level, indent_str, pretty, inline
                )
                name = self._clean_name(getattr(self, "tagname", type(self).__name__))
                self._render_close_tag(sb, name, close_tag)

        return sb

    def save(
        self,
        file_name: str = None,
        folder_name: str = None,
        current_dir=False,
        file_path=None,
    ):

        if file_path is not None:
            assert (
                folder_name is None and current_dir is False
            ), "folder_name and current_dir can't be initialised with file_path"
        else:
            folder_name = folder_name or "static"  # passing default folder_name here
            assert folder_name is not None, "folder_name should be initialised"

        if self.file_extension is None:
            raise ValueError(
                f"can not save file with {self.file_extension!r} type extension"
            )

        file_name = file_name or str(self.__class__.__name__)
        file_name = (
            file_name
            if file_name.endswith(self.file_extension)
            else ".".join([file_name, self.file_extension[1:]])
        )

        if folder_name is not None:
            current_work_dir = os.getcwd()
            dirname = (
                current_work_dir if current_dir else os.path.dirname(current_work_dir)
            )
            folder_name = os.path.join(dirname, folder_name)

            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            file_path = os.path.join(folder_name, file_name)
        else:
            file_path = (
                os.path.join(file_path, file_name)
                if not os.path.isfile(file_path)
                else file_path
            )

        html_string = self.__render__()

        if not os.path.exists(file_path):
            with open(file_path, "w+") as f:
                f.write(html_string)
        else:
            with open(file_path, "r") as temp:
                old_html = temp.read()
                if old_html != html_string:
                    with open(file_path, "w") as f:
                        f.write(html_string)
        return file_name


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

    def __init__(
        self,
        template_name,
        template_text,
        *dom_elements,
        self_dedent=None,
        child_dedent=None,
        **kwargs,
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
                        self.right_delimiter,
                    ]
                )
            )
        )
        super(SingleTemplates, self).__init__(
            open_tag=open_tag,
            self_dedent=self_dedent or self.self_dedent,
            child_dedent=child_dedent or self.child_dedent,
            **kwargs,
        )
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

    def __init__(
        self,
        template_name,
        template_text,
        *dom_elements,
        self_dedent=None,
        child_dedent=None,
        **kwargs,
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
        super(DoubleTemplates, self).__init__(
            open_tag=open_tag,
            close_tag=close_tag,
            self_dedent=self_dedent or self.self_dedent,
            child_dedent=child_dedent or self.child_dedent,
            **kwargs,
        )
        if any(dom_elements):
            self.add(*dom_elements)


class StyleTags(Tags):
    left_delimiter = "{"
    right_delimiter = "}"
    self_dedent = False
    is_class = False
    is_id = False
    is_apply = False

    def _render_open_tag(
        self, sb, indent_level, indent_str, pretty, xhtml, name, open_tag
    ):
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
        attribute_joiner = (
            "%s:%s;"
            if not pretty
            else "    %s: %s;\n" + (indent_str * indent_level)
            if not self.is_apply
            else "@%s %s;"
            if not pretty
            else "    @%s %s;\n" + (indent_str * indent_level)
        )
        for attribute, value in sorted(self.attributes.items()):
            if (
                value is not False and value is not None
            ):  # False values must be omitted completely
                sb.append(attribute_joiner % (attribute, escape(unicode(value), True)))

            if value is None:  # minified xhtml attributes are added
                sb.append(" %s" % attribute)
        return sb

    def _render_close_tag(self, sb, name, close_tag):
        sb.append(self.right_delimiter)
        return sb

    def _clean_name(self, name):
        # Workaround for python keywords and standard classes/methods
        # (del, object, input)
        if any(name):  # to handle the case when tagname = ""
            if name[-1] == "_":
                name = name[:-1]

        if all([self.is_class, self.is_id]):
            raise AttributeError(f"{name} can not have both is_class and is_id as True")

        if self.is_class:
            name = "".join([".", name])

        if self.is_id:
            name = "".join(["#", name])

        return name

    @property
    def attr(self):
        r = []
        attribute_joiner = "%s:%s;" if not self.is_apply else "@%s %s;"

        for attribute, value in sorted(self.attributes.items()):
            if (
                value is not False and value is not None
            ):  # False values must be omitted completely
                r.append(attribute_joiner % (attribute, escape(unicode(value), True)))

            if value is None:  # minified xhtml attributes are added
                r.append(" %s" % attribute)
        return "".join(r)

    @staticmethod
    def clean_attribute(attribute):
        """
        Normalize attribute names for shorthand and work around for limitations
        in Python's syntax.
        """

        # Shorthand
        attribute = {
            "cls": "class",
            "className": "class",
            "class_name": "class",
            "fr": "for",
            "html_for": "for",
            "htmlFor": "for",
        }.get(attribute, attribute)

        # Workaround for Python's reserved words
        if attribute[0] == "_":
            attribute = attribute[1:]

        attribute = attribute.replace("_", "-")

        # Workaround for colon
        if attribute.split("_")[0] in ("xlink", "xml", "xmlns"):
            attribute = attribute.replace("_", ":", 1)

        return attribute
