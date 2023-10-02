# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from __future__ import annotations

import json
import warnings
from dataclasses import asdict, dataclass, field
from html import unescape
from pathlib import Path
from textwrap import dedent
from typing import Iterable, List, Union

from marko import convert as markdown

from uidom.dom.src import csstags, htmltags, jinjatags, svgtags
from uidom.dom.src.dom_tag import dom_tag
from uidom.dom.src.html_string import defHTML
from uidom.dom.src.main import extension
from uidom.utils.parameters import Parameters

__all__ = ["Component", "ReactiveComponent", "Fragment", "MergeClassAttribute"]


@dataclass
class Component(extension.Tags):
    left_delimiter = "<"
    right_delimiter = ">"
    css_tags = csstags
    svg_tags = svgtags
    html_tags = htmltags
    jinja_tags = jinjatags
    file_extension: str = field(init=False, default=".html")
    render_tag: bool = field(init=False, default=False)
    attributes: dict = field(init=False, default_factory=dict)
    children: List[Union[str, html_tags.dom_tag]] = field(
        init=False, default_factory=list
    )
    parent: Union[html_tags.dom_tag, None] = field(init=False, default=None)
    document: Union[html_tags.dom_tag, None] = field(init=False, default=None)
    files_directory: Union[str, Path, None] = field(init=False, default=None)
    escape_string: bool = field(init=False, default=True)
    string_is_markdown: bool = field(init=False, default=False)

    def __init__(self, *args, **kwargs):
        super(Component, self).__init__()

        global markdown
        markdown = kwargs.pop("markdown", None) or markdown
        markdown = getattr(markdown, "convert", markdown)
        # first we get the child from the render method and sanitize it.
        child = self.render(*args, **kwargs)

        if isinstance(child, str):
            if self.string_is_markdown:
                child = (
                    markdown(child) if self.escape_string else unescape(markdown(child))
                )
            child = defHTML(child, escape=self.escape_string)

        elif isinstance(child, Path):
            string_is_markdown = child.suffix == ".md"
            child = self._from_file(child)
            if string_is_markdown:
                child = (
                    markdown(child) if self.escape_string else unescape(markdown(child))
                )
            child = defHTML(child, escape=self.escape_string)

        if isinstance(child, (list, tuple)) and len(child) == 1:
            child = child[0]
        # commented and shifted __init__ below to the first line because then Fragment can
        # add *args and **kwargs on initialization inside render method
        # super(Component, self).__init__()

        if child is not self:
            self.add(child)

        self._entry = self if isinstance(child, (list, tuple)) else child

        # we perform checks on the _entry "after" the dom initialization because .get method
        # looks into children
        self.__checks__(self._entry)

    def __checks__(
        self, element: Union[dom_tag, extension.Tags]
    ) -> Union[dom_tag, extension.Tags]:  # noqa
        if self.render_tag:
            raise ValueError(f"{self.render_tag=} can not be true for Components")
        return element

    def add(self, *args):
        """
        Adding tags to a component appends them to the render.
        """
        if not self.render_tag and hasattr(self, "_entry") and self._entry is not self:
            return self._entry.add(*args)
        return super().add(*args)

    def set_attribute(self, key, value):
        if not self.render_tag and hasattr(self, "_entry") and self._entry is not self:
            self._entry.set_attribute(key, value)
        else:
            super(Component, self).set_attribute(key, value)

    __setitem__ = set_attribute

    def delete_attribute(self, key):
        if not self.render_tag and hasattr(self, "_entry") and self._entry is not self:
            self._entry.delete_attribute(key)
        else:
            super(Component, self).delete_attribute(key)

    __delitem__ = delete_attribute

    def get(self, tag=None, **kwargs):
        if not self.render_tag and hasattr(self, "_entry") and self._entry is not self:
            # try to get the attribute of the children of the component
            return self._entry.get(tag, **kwargs)
        else:
            return super(Component, self).get(tag, **kwargs)

    def __getitem__(self, key):
        if not self.render_tag:
            entry = None
            try:
                entry: Union[dom_tag, extension.Tags] = object.__getattribute__(
                    self, "_entry"
                )
            except AttributeError:
                pass
            if entry and entry is not self:
                return entry.__getitem__(key)

        return super(Component, self).__getitem__(key)

    __getattr__ = __getitem__

    def clear(self):
        if not self.render_tag and hasattr(self, "_entry") and self._entry is not self:
            self._entry.clear()
        else:
            super().clear()

    def __len__(self):
        if not self.render_tag and hasattr(self, "_entry") and self._entry is not self:
            return len(self._entry)
        return super().__len__()

    def __iter__(self):
        if not self.render_tag and hasattr(self, "_entry") and self._entry is not self:
            return self._entry.__iter__()
        return super().__iter__()

    def __hash__(self) -> int:
        # **DON'T create** hash with self._entry that is hash(self._entry),
        # inside __exit__ stack frame has a 'set' of used tags. it uses
        # hash to check membership. if we use it like below the Component
        # classes will be skipped. SO PLEASE DON'T CHANGE IT. I wasted
        # 3 days for this simple issue with lots of head scratching.
        # if hasattr(self, "_entry") and self._entry is not self:
        #     return hash(self._entry)
        return super().__hash__()

    def __eq__(self, other) -> bool:
        if not self.render_tag and hasattr(self, "_entry") and self._entry is not self:
            # now check if the other isinstance of Component
            if (
                isinstance(other, Component)
                and not other.render_tag
                and hasattr(other, "_entry")
                and other._entry is not other
            ):
                return self._entry is other._entry
            return self._entry is other
        else:
            if (
                isinstance(other, Component)
                and not other.render_tag
                and hasattr(other, "_entry")
                and other._entry is not other
            ):
                return self is other._entry
            return self is other

    def _asdict(self, exclude=None) -> dict:
        exclude = exclude or [
            "file_extension",
            "render_tag",
            "children",
            "document",
            "parent",
            "attributes",
            "files_directory",
            "escape_string",
            "string_is_markdown",
        ]
        return {key: value for key, value in asdict(self).items() if key not in exclude}

    def to_dict(self, exclude=None) -> dict:
        return self._asdict(exclude=exclude)

    def render(self, *args, **kwargs) -> Union[dom_tag, extension.Tags, str]:  # noqa
        raise NotImplementedError(
            f"{self.__class__.__name__}.{self.render.__name__} method not implemented"
        )

    @classmethod
    def _from_file(cls, file_name: Union[str, Path]) -> str:
        file_location = None

        if isinstance(cls.files_directory, Path):
            if not cls.files_directory.exists():
                raise FileNotFoundError(f"file {cls.files_directory=} does not exists")

            if not cls.files_directory.is_dir():
                raise ValueError(f"{cls.files_directory=} is not a directory")

            file_location = cls.files_directory / file_name

        elif cls.files_directory:
            if not isinstance(cls.files_directory, str):
                raise ValueError(f"{cls.files_directory=} is not str")

            cls.files_directory = Path(cls.files_directory)

            if not cls.files_directory.exists():
                raise FileNotFoundError(f"file {cls.files_directory=} does not exists")

            if not cls.files_directory.is_dir():
                raise ValueError(f"{cls.files_directory=} is not a directory")

            file_location = cls.files_directory / file_name

        else:
            file_location = Path(file_name) if isinstance(file_name, str) else file_name

        if not file_location.exists():
            raise FileNotFoundError(f"{file_location} does not exists")

        if not file_location.is_file():
            raise ValueError(f"{file_location} is not a file")

        return file_location.read_text()

    @classmethod
    def from_file(cls, file_name: Union[str, Path]) -> "Component":
        return cls(cls._from_file(file_name))

    def script(self, *args, **kwargs):
        ...

    def call(self, *args, **kwargs):
        """
        This is basically a placeholder for using websocket communications.
        All sorts of fun stuffs can happens here.
        :param args:
        :param kwargs:
        :return:
        """

        raise NotImplemented(f"method: {self.call.__qualname__} not implemented")

    def __dir__(self) -> Iterable[str]:
        return sorted(iter(self.__dict__), key=lambda k: k)


class Fragment(Component):
    """Its just a placeholder which renders all its childrens
        but not itself and passes all it attributes to its childrens.

    Args:
        None

    Returns:
        Fragment: it returns fragment which renders all its childrens
    """

    render_tag = False

    def _add_attrs_to_child(self, child: Union[extension.Tags, dom_tag]):
        # here we are adding safe_attributes because we need a way to bypass
        # escaping of attribute values for

        if hasattr(child, "safe_attributes"):
            child.safe_attributes.update(self.safe_attributes)

        for attr, value in self.attributes.items():
            # ===================================================================
            # --------------------------^ x-data section ------------------------
            # ===================================================================
            # merging x-data attr from Fragment class to child class
            if attr == "x-data" and child.attributes.get(attr, None):
                x_data = json.loads(child.attributes.get(attr).replace("'", '"'))

                if value is None:
                    value = x_data
                else:
                    value = json.loads(value.replace("'", '"'))
                if isinstance(x_data, dict) and isinstance(value, dict):
                    value = x_data | value

                value = json.dumps(value).replace('"', "'")
            # ===================================================================
            # --------------------------$ x-data section ------------------------
            # ===================================================================

            # ===================================================================
            # --------------------------^ class section -------------------------
            # ===================================================================
            # merging class attr from Fragment class to child class
            if attr == "class" and child.attributes.get(attr, None):
                value = " ".join([child.attributes[attr], value])

            # ===================================================================
            # --------------------------$ class section -------------------------
            # ===================================================================

            # ===================================================================
            # --------------------------^ x-on @ event section ------------------
            # ===================================================================
            # merging event attr (starting with @) from Fragment class to child
            # class
            if attr.startswith("@") and child.attributes.get(attr, None):
                # remove indentation and any newlines from the child attribute value
                child_attr_value = " ".join(
                    map(lambda x: x.strip(), dedent(child.attributes[attr]).split("\n"))
                )

                value = "; ".join([child_attr_value, value])
            # ===================================================================
            # --------------------------$ x-on @ event section ------------------
            # ===================================================================

            # ===================================================================
            # --------------------------^ x-tansition section -------------------
            # ===================================================================
            # merging x-tansition from Fragment class to child class
            if attr.startswith("x-transition") and child.attributes.get(attr, None):
                if value:
                    value = " ".join([child.attributes[attr], value])
            # ===================================================================
            # --------------------------^ x-tansition section -------------------
            # ===================================================================

            # ===================================================================
            # --------------------------^ x-bind : section ----------------------
            # ===================================================================
            if attr.startswith(":") and child.attributes.get(attr, None):
                warnings.warn(
                    message=f"{self.__class__.__name__} has not implemented merging attribute: x-bind"
                )

            child.set_attribute(*child.clean_pair(attr, value))

    def add(self, *args):
        for arg in args:
            if isinstance(arg, (extension.Tags, dom_tag)):
                self._add_attrs_to_child(arg)
        super().add(*args)

    def render(self, *args, **kwargs):
        self.add(kwargs)
        [
            self.add(defHTML(arg)) if isinstance(arg, str) else self.add(arg)
            for arg in args
        ]

        # for this component to behave as a fragment we must simply return self
        # Component class will take care of all the things itself.
        return self


class MergeClassAttribute(Fragment):
    """Merging the attributes with subcontexts via uidom.dom.src.dom_tag.attr

    Args:
        None:
    Usage:
        with MergeClassAttribute():
            attr(className=...)
            attr(className=...)
            div()
            ### this div receives all the attributes set via attr methods contexts
            ### but all the className kwargs are merged..

    """

    def _merge_class_attr(self, key, value):
        if key == "class" and self.attributes.get(key, None):
            value = " ".join([self.attributes[key], value])
        return key, value

    def set_attribute(self, key, value):
        if key == "class":
            key, value = self._merge_class_attr(key, value)

        super().set_attribute(key, value)

    __setitem__ = set_attribute


@dataclass(eq=False)
class ReactiveComponent(Component):
    def __init__(self, *args, **kwargs):
        super(ReactiveComponent, self).__init__(*args, **kwargs)
        self.__states: dict = kwargs

    def __post_init__(self, *args, **kwargs):
        self.__states: dict = self.__states | self.to_dict()  # ** <-- Mark this line
        # ** this line of code creates infinite recursive loop of deepcopy if used as follows
        # class App(ReactiveComponent):
        #   def render(self, *args, **kwargs):
        #       return document(*args, **kwargs)
        # where document is also an instance of the ReactiveComponent.
        # as to_dict method of dataclass probably calls for locals that gets mangled with document locals

    def _get_param(self, function, new_kwargs):
        param = Parameters(function, in_single_kwargs=False)
        _arg_dict, _kwarg_dict = param.parameters
        var_arg_name = param.var_arg_name
        arg_dict = {k: new_kwargs.get(k, v) for k, v in _arg_dict.items()}
        kwargs = {k: new_kwargs.get(k, v) for k, v in _kwarg_dict.items()}
        args = []
        for arg_name in arg_dict:
            arg_val = arg_dict[arg_name]
            if (
                param.default(arg_name) is param.empty
                and arg_name not in new_kwargs
                and not any([arg_val])
            ):
                # So when we land here in this block of code, arg_name is not in new_kwargs
                # so we haven't updated arg_dict from new_kwargs for sure, also we are sure
                # that sign_params[arg_name].default is not None here in this block of code.
                # But arg_dict[arg_name] is None, so it means Parameters class replaced
                # default=_empty with default=None, so we should raise error
                raise ValueError(
                    f"{arg_name} is a required parameter for {function.__name__}"
                )
            else:
                if isinstance(arg_val, tuple) and arg_name == var_arg_name:
                    args.extend(arg_val)
                else:
                    args.append(arg_val)
        return args, kwargs

    def _re_render(self, **states) -> extension.Tags:  # noqa
        # here is an example below how re_rendering handles function calls like 'increment'
        # changing variables
        # with document(x_toggle) as counters:
        #     with div(className="relative flex w-full h-screen"):
        #         Counter(),
        #         with Counter(count=2) as counter_2:
        #             div("kml")
        #             div("lakd")
        # counter_2.increment() <- running the method re renders and updates counter_2 states
        # counter_2.increment()
        # return counters
        old_parent = self.parent
        old_entry_children = self._entry.children

        if old_parent is not None:
            index_of_entry = old_parent.children.index(self)

        self.clear()
        # this self.clear is to clear any self._entry's childs that are present
        if self._entry is not self:
            # deleting self._entry makes sure that the stale self entry is removed
            # from the tree completely.
            del self._entry

        # this clear runs on the self instead of self._entry as we have deleted
        # this._entry so it ensures any trace of old children in the self is removed
        self.clear()

        args, kwargs = self._get_param(self.render, states)
        if args and kwargs:
            elements = self.render(*args, **kwargs)
        elif args:
            elements = self.render(*args)
        elif kwargs:
            elements = self.render(**kwargs)
        else:
            elements = self.render()
        self._entry = extension.Tags.add(
            self, elements
        )  ## <--- important to call Tags .add method
        new_entry_children = self._entry.children

        if old_entry_children:
            unadded_old_entry_children = old_entry_children[len(new_entry_children) :]
            self._entry.add(unadded_old_entry_children)

        if old_parent is not None:
            old_parent.set_attribute(index_of_entry, self)

        return self._entry

    def _check_states_and_update(self) -> None:
        current_states = self.to_dict()
        original_states = self.__states

        self.__states = original_states | current_states
        if self.__states != original_states:
            # IMPORTANT: There is a reason we are not setting self._re_render(**current_states).
            # When dataclass creates dictionary it only creates dictionary of the declared fields
            # but kwargs that are passed in the above can contain key=value pairs such as tailwind
            # classes for example class = someclass, so we have to always remember that we take care
            # of those values and pass them while we re_render the Component.
            self._re_render(**self.__states)

    def set_attribute(self, key, value):
        self._check_states_and_update()
        super().set_attribute(key=key, value=value)

    __setitem__ = set_attribute

    def _render(self, sb, indent_level, indent_str, pretty, xhtml):
        self._check_states_and_update()
        return super()._render(sb, indent_level, indent_str, pretty, xhtml)
