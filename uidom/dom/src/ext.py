# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import re
import textwrap
import typing
from pathlib import Path

from jinja2.utils import htmlsafe_json_dumps

from uidom.dom.src.dom1core import dom1core
from uidom.dom.src.dom_tag import dom_tag, unicode
from uidom.dom.src.utils.dom_util import dom_text, escape

__all__ = [
    "SingleTemplates",
    "DoubleTemplates",
    "DoubleTags",
    "SingleTags",
    "StyleTags",
    "PlaceholderTag",
]


class Tags(dom_tag, dom1core):
    left_delimiter = "<"
    right_delimiter = ">"
    self_dedent = False
    child_dedent = False
    render_tag = True
    new_line = "\n"
    SELF_DEDENT = "self_dedent"
    CHILD_DEDENT = "child_dedent"
    OPEN_TAG = "open_tag"
    CLOSE_TAG = "close_tag"
    RENDER_TAG = "render_tag"
    file_extension = ".html"
    attribute_prefix_map: dict = {}
    safe_attributes: dict = {}

    def __init__(self, *args, **kwargs):
        # if any(args):
        # msg = f"can only pass {dom_tag!r} or {str!r} types in arguments, got {args!r} instead"
        # if not all(map(lambda x: isinstance(x, (dom_tag, str)), args)):
        #     raise TypeError(msg)
        super(Tags, self).__init__(*args, **kwargs)

    def _render_open_tag(
        self,
        /,
        sb,
        name,
        open_tag,
        xhtml,
        indent_level=None,
        indent_str=None,
        pretty=None,
    ):
        if open_tag:
            sb.append("%s" % open_tag)
        else:
            # open tag is absent
            sb.append(self.left_delimiter)
            sb.append(name)
            sb = self._render_attribute(sb, indent_level, indent_str, pretty)
            sb.append(
                "".join(["/", self.right_delimiter])
                if self.is_single and xhtml
                else self.right_delimiter
            )
        return sb

    def _wrap_attr_value(self, value, indent_level, indent_str, pretty):
        # adding support to write multiline tailwindcss classes
        value = textwrap.dedent(value)
        # value = textwrap.fill(
        #     value,
        #     break_long_words=False,
        #     break_on_hyphens=False,
        # )
        value = re.sub(r"\s+", " ", value.strip())

        return value

    def _render_attribute(self, sb, indent_level, indent_str, pretty):
        for attribute, value in sorted(self.attributes.items()):
            if value is not False and value not in [
                None
            ]:  # False values must be omitted completely
                if attribute == "class":
                    value = self._wrap_attr_value(
                        value, indent_level, indent_str, pretty
                    )
                if not isinstance(value, (dict, list)):
                    if self.safe_attributes.get(attribute, True):
                        sb.append(
                            ' %s="%s"' % (attribute, escape(unicode(value), True))
                        )
                    else:
                        sb.append(' %s="%s"' % (attribute, unicode(value)))
                else:
                    value = htmlsafe_json_dumps(value)
                    sb.append(
                        " %s='%s'" % (attribute, escape(unicode(value), quote=False))
                    )
            if value in [None]:  # minified xhtml attributes are added
                sb.append(" %s" % attribute)
        return sb

    def _render_close_tag(self, /, sb, name, close_tag):
        if close_tag:
            sb.append("%s" % close_tag)
        else:
            sb.append("".join([self.left_delimiter, "/"]))
            sb.append(name)
            sb.append(self.right_delimiter)
        return sb

    def _new_line_and_inline_handler(
        self, sb, indent_level, indent_str, pretty, is_inline
    ):
        if pretty and not is_inline:
            is_inline = False
            sb.append(self.new_line)
            sb.append(indent_str * indent_level)
        return sb, is_inline

    @staticmethod
    def _dedent_handler(dedent, indent_level):
        if dedent:
            indent_level -= 1
        return indent_level

    @classmethod
    def clean_attribute(cls, attribute):
        """
        Normalize attribute names for shorthand and work arounds for limitations
        in Python's syntax. Extended it to support VueJS, HTMX and AngularJS.
        """

        # Shorthand
        attribute = {
            "cls": "class",
            "className": "class",
            "classname": "class",
            "classes": "class",
            "class_name": "class",
            "fr": "for",
            "html_for": "for",
            "htmlFor": "for",
        }.get(attribute, attribute)

        # Workaround for Python's reserved words
        if len(attribute) >= 2:
            if attribute[0] == "_" and attribute[1] != "_":
                attribute = attribute[1:]

        # Workaround for dash plus support for VueJS, HTMX, AlpineJS, Unpoly and AngularJS
        special_prefix = any(
            [
                attribute.startswith(x)
                for x in (
                    "data_",  # for data-type="value" support
                    "aria_",  # for aria support
                    "x_",  # for AlpineJS and x-component support
                    "v_",  # for Vue support
                    "ng_",  # for Angular support
                    "hx_",  # for HTMX support
                    "__",  #
                    "ws__",  #
                    "up_",  # for Unpoly JS support
                    "remove_me",  # for HTMX remove extension support
                    *cls.attribute_prefix_map.keys(),
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
            attribute = attribute.replace("transition-enter", "transition:enter")
            attribute = attribute.replace("transition-leave", "transition:leave")
            attribute = attribute.replace("intersect-enter", "intersect:enter")
            attribute = attribute.replace("intersect-leave", "intersect:leave")
            attribute = attribute.replace("v-on:", "@")
            attribute = attribute.replace("v-on-", "@")
            attribute = attribute.replace("x-on:", "@")
            attribute = attribute.replace("x-on-", "@")
            attribute = attribute.replace("-dot-", ".")
            if attribute in cls.attribute_prefix_map:
                attribute = attribute.replace(
                    attribute, cls.attribute_prefix_map[attribute]
                )

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
            if name[0] == "_":
                name = name[1:]
        return name

    def _render_children(self, sb, indent_level, indent_str, pretty, xhtml):
        # we want to partially inline only childrens so initially we set
        # inline flag as True here but if child.is_line is False we will
        # set this flag as False
        inline = True

        # we want to keep track of indentation level so that we dont dedent the child
        # below original indentation level of the parent
        orig_indent = indent_level

        self_render_tag = self.attributes.pop(
            Tags.RENDER_TAG,
            getattr(self, Tags.RENDER_TAG) if hasattr(self, Tags.RENDER_TAG) else True,
        )
        for child in self.children:
            if isinstance(child, dom_tag) and not isinstance(child, dom_text):
                # Get the dedent status of child from the parent or the child.
                # The dedent status of the child from the parent via self.child_dedent is
                # extracted in the '_render' method already and is already taken care of.
                # we have already **not** incremented the indentation in '__render' method
                # while calling '_render_childern' method if child_dedent is True. Thus
                # in effect decrementing the child indentation.

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

                        # thus we always ensure that while we dedent the <child> we don't dedent it below
                        # parent indentation
                        if indent_level > orig_indent - 1:
                            indent_level = self._dedent_handler(dedent, indent_level)

                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                # we will apply the changes only when the render_tag flag is set to True
                # NOTE: we should **not add** checks for (pretty and not self.is_inline) here with
                # 'self_render_tag' as this is where we are adding the indentation and
                # new-line **before** child is rendered.
                #
                # ======================Lets see the reason behind this in details.======================
                #
                # variable 'pretty' comes from the parent and if we are rendering tag of parent
                # for eg:
                #
                # =======================================================================================
                # <parent>\n
                # "    "<child> // so here '\n' and "    " represents the newline and indentation added
                # <parent>      // after <parent> this is done here after checking 'self_render_tag'
                # =======================================================================================
                #
                # also notice we do (inline and self.is_inline) check inside _new_line_and_inline_handler
                # method because we want to make only childrens are partially inlined.
                # if we dont add (inline and self.is_inline) we will get the tree something like this if
                # parent.is_inline = False
                #
                # =======================================================================================
                # <parent><child></child> // notice how the <child></child> tag is inlined but its mangling
                # </parent>               // the indentation after opening of the <parent> tag
                # =======================================================================================
                #
                # this is happening because when self.is_inline is False for parent we should add indentation
                # and '\n' before the child, if 'child.is_inline' is True but not the 'parent.is_inline' then
                # we need to make inline False in _new_line_and_inline_handler below to ensure that '\n' and
                # indentation is added after opening of parent tag, but we have already overwritten inline = True
                # in the starting and child.is_inline is True so in effect (pretty and not child.is_inline)
                # condition is False so we didn't override value of inline which is still True.
                #
                # Thus if we only pass 'inline' inside _new_line_and_inline_handler it will not add any "\n"
                # or indentation. Only way to do this is by adding "and" operator between inline and self.is_inline.
                # Thus we make sure even if the child is inlined the parent adds the "\n" and indentation before
                # child if parent self.is_inline is False.
                #
                # This can be quickly and easily checked by removing self.is_inline inside _new_line_and_inline_handler
                # below and running div(div(div(div(script("aa")), __inline=True)))
                # what we actually want is:
                # -----------------------
                # <parent>\n
                # "    "<child></child>
                # </parent>
                # and we get this only by adding (inline and self.is_inline) inside _new_line_and_inline_handler
                # method below so don't remove or edit it in future.
                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                if self_render_tag:
                    if not isinstance(child, PlaceholderTag) or (
                        isinstance(child, PlaceholderTag) and any(child)
                    ):
                        sb, inline = self._new_line_and_inline_handler(
                            sb,
                            indent_level,
                            indent_str,
                            pretty,
                            inline and self.is_inline,
                        )

                child._render(sb, indent_level, indent_str, pretty, xhtml)

            else:
                if isinstance(child, dom_text):
                    child = child.__render__()

                # check if the child is not an empty string '' via if child:
                if child or any(child):
                    # if any child exists maybe its a string or some object, here we check if the pretty is True.
                    # Notice here the child is only string or we force it to act like string by casting it into unicode and
                    # we can't check child.is_inline so we fallback on 'pretty' flag. if its True we set the inline flag as
                    # False. The logic of adding (inline and self.is_inline) inside _new_line_and_inline_handler is same as
                    # given above. Ideally we should check for both (pretty and not self.is_inline) but due to the fact that
                    # 'pretty' has included that condition when its defined we skip it.

                    if pretty:
                        inline = False
                        if self_render_tag:
                            sb, inline = self._new_line_and_inline_handler(
                                sb,
                                indent_level,
                                indent_str,
                                pretty,
                                inline and self.is_inline,
                            )
                        lines = child.splitlines()
                        for line in lines:
                            sb.append(unicode(line))
                            if line and line != lines[-1]:
                                sb, inline = self._new_line_and_inline_handler(
                                    sb,
                                    indent_level,
                                    indent_str,
                                    pretty,
                                    inline and self.is_inline,
                                )
                    else:
                        sb.append(unicode(child))

            if child or any(child):
                # don't use any(child) alone as condition above because it will check
                # __iter__ method and it will depend on its children solely so will not work as expected
                if not isinstance(child, PlaceholderTag) or (
                    isinstance(child, PlaceholderTag) and any(child)
                ):
                    if not self_render_tag and pretty and self.children[-1] != child:
                        sb, inline = self._new_line_and_inline_handler(
                            sb,
                            indent_level,
                            indent_str,
                            pretty,
                            inline and self.is_inline,
                        )

        return inline

    def _render(self, sb, indent_level=1, indent_str="  ", pretty=True, xhtml=False):
        self.open_tag = self.attributes.pop(
            Tags.OPEN_TAG,
            getattr(self, Tags.OPEN_TAG) if hasattr(self, Tags.OPEN_TAG) else False,
        )
        self.close_tag = self.attributes.pop(
            Tags.CLOSE_TAG,
            getattr(self, Tags.CLOSE_TAG) if hasattr(self, Tags.CLOSE_TAG) else False,
        )
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
        # level but we will not mess with the self_dedent here as is_single flag ensures single tags are
        # dedented by default (see '_render_children' method call below) so what remains is the double tags
        # but we dedent double tags only when there is a child involved thus child.self_dedent is parsed
        # inside '_render_children' method, thats why commenting.
        dedent = not self_render_tag  # or self_dedent
        if pretty and dedent:
            # A **Potential BUG** that we can introduce here is if we dedent to the level below parent element.
            # Baically we are assuming that the parent has sent the indent level to us after incrementing it
            # and when we are not rendering self-tag, we are decrementing it. And thats the actual case.
            # Personally I dont think there will be any bug here as we can be sure that "_render" method is run
            # inside "_render_children", and when it happes, child takes care of its indentation and all,
            # so leave it while it works. Don't remove the line below it breaks indentation in the code. :)
            indent_level = self._dedent_handler(dedent, indent_level)

        if self_render_tag:
            name = self._clean_name(getattr(self, "tagname", type(self).__name__))
            self._render_open_tag(
                sb=sb,
                name=name,
                open_tag=self.open_tag,
                xhtml=xhtml,
                indent_level=indent_level,
                indent_str=indent_str,
                pretty=pretty,
            )

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
        if self_render_tag and not self.is_single:
            sb, inline = self._new_line_and_inline_handler(
                sb, indent_level, indent_str, pretty, inline
            )
            name = self._clean_name(getattr(self, "tagname", type(self).__name__))
            self._render_close_tag(sb=sb, name=name, close_tag=self.close_tag)

        return sb

    def __and__(self, other: dom_tag) -> "Tags":
        return (
            PlaceholderTag(__inline=self.is_inline, __pretty=self.is_pretty)
            & self
            & other
        )

    def __iter__(self) -> typing.List[typing.Union[str, dom_tag, "Tags"]]:
        return super().__iter__()

    def save(
        self,
        file_name: typing.Union[str, Path, None] = None,
        folder_name: typing.Union[str, Path, None] = None,
        current_dir: bool = False,
        file_or_dir: typing.Union[str, Path, None] = None,
    ):
        if file_or_dir is not None:
            assert (
                folder_name is None and current_dir is False
            ), "folder_name and current_dir can't be initialised with file_path"
            file_or_dir = Path(file_or_dir)
        else:
            folder_name = Path(folder_name or Path(__file__).parent / "static")
            assert folder_name is not None, "folder_name should be initialised"

        if self.file_extension is None:
            raise ValueError(
                f"can not save file with {self.file_extension=} type extension"
            )

        def _filename() -> Path:
            nonlocal file_name
            file_name = Path(file_name or str(self.__class__.__name__))

            if file_name.suffix:
                if not file_name.suffix == self.file_extension:
                    raise ValueError(
                        f"{file_name.suffix=} and {self.file_extension=} did not match"
                    )
            else:
                file_name = file_name.with_suffix(self.file_extension)
            return file_name

        if folder_name is not None:
            current_work_dir = Path.cwd()
            dir_name = current_work_dir if current_dir else current_work_dir.parent
            dir_folder = dir_name / folder_name

            if not dir_folder.exists():
                dir_folder.mkdir()

            file_path = dir_folder / _filename()

        elif file_or_dir is not None:
            file_path = (
                file_or_dir / _filename() if file_or_dir.is_dir() else file_or_dir
            )

        html_string = self.__render__()

        if not file_path.exists():
            with file_path.open(mode="w+") as f:
                f.write(html_string)
        else:
            with file_path.open(mode="r") as temp:
                old_html = temp.read()
                if old_html != html_string:
                    with file_path.open(mode="w") as f:
                        f.write(html_string)
        return file_path.name


class PlaceholderTag(Tags):
    render_tag = False

    def __and__(self, other: dom_tag) -> Tags:
        return PlaceholderTag(
            self, other, __inline=self.is_inline, __pretty=self.is_pretty
        )


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
    tagname_prefix = ""
    attribute_joiner = "%s: %s;"

    def _render_open_tag(
        self,
        /,
        sb,
        name,
        open_tag,
        xhtml,
        indent_level,
        indent_str,
        pretty,
    ):
        sb.append(name)
        if pretty:
            sb.append(" ")
        sb.append(self.left_delimiter)
        if pretty:
            sb.append("\n")
            sb.append(indent_str * indent_level)
        sb = self._render_attribute(
            sb=sb,
            indent_level=indent_level,
            indent_str=indent_str,
            pretty=pretty,
            xhtml=xhtml,
        )
        return sb

    def _render_attribute(self, /, sb, indent_level, indent_str, pretty, xhtml):
        attribute_joiner = (
            f"{self.attribute_joiner}".replace(" ", "")
            if not pretty
            else f"{indent_str}{self.attribute_joiner}\n" + (indent_str * indent_level)
        )

        attribute_items = self.attributes.items()

        for attribute, value in attribute_items:
            if (
                value is not False and value is not None
            ):  # False values must be omitted completely
                sb.append(attribute_joiner % (attribute, escape(unicode(value), True)))

            if value is None:  # minified xhtml attributes are added
                sb.append(" %s" % attribute)
        return sb

    def _render_close_tag(self, /, sb, name, close_tag):
        sb.append(self.right_delimiter)
        return sb

    def _clean_name(self, name):
        # Workaround for python keywords and standard classes/methods
        # (del, object, input)
        if any(name):  # to handle the case when tagname = ""
            if name[-1] == "_":
                name = name[:-1]
            if name[0] == "_":
                name = name[1:]

        name = "".join([self.tagname_prefix, name])

        return name

    @property
    def attr(self):
        r = []
        attribute_joiner = self.attribute_joiner

        for attribute, value in self.attributes.items():
            if (
                value is not False and value is not None
            ):  # False values must be omitted completely
                r.append(attribute_joiner % (attribute, escape(unicode(value), True)))

            if value is None:  # minified xhtml attributes are added
                r.append(" %s" % attribute)
        return " ".join(r)

    @classmethod
    def clean_attribute(cls, attribute):
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
