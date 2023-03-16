# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from dataclasses import asdict, dataclass, field
from typing import Iterable, Union

from uidom.dom.src import csstags, htmltags, jinjatags, svgtags, vuetifytags
from uidom.dom.src.main import extension

__all__ = [
    "Component"
]

@dataclass
class Component(extension.Tags):
    left_delimiter = "<"
    right_delimiter = ">"
    css_tags = csstags
    svg_tags = svgtags
    html_tags = htmltags
    jinja_tags = jinjatags
    vuetify_tags = vuetifytags
    file_extension:str = field(init=False, default=".html")
    render_tag: bool = field(init=False, default=False)
    attributes: dict = field(init=False, default_factory=dict)
    children: list = field(init=False, default_factory=list)
    parent: Union[extension.Tags, None] = field(init=False, default=None)
    document: Union[extension.Tags, None] = field(init=False, default=None)
    
    def __init__(self, *args, **kwargs):
        super(Component, self).__init__()
        self._entry: htmltags.html_tag = super(Component, self).add(self.render(*args, **kwargs))
        # we perform checks on the _entry "after" the dom initialization because .get method
        # looks into children
        self.__checks__(self._entry)
        self._states: dict = kwargs
        
    def __post_init__(self, *args, **kwargs):
        self._states = self._states | self._asdict()

    def __checks__(self, element: extension.Tags) -> extension.Tags:  # noqa
        if self.render_tag:
            raise ValueError(f"{self.render_tag} can not be true for Components")
        return element

    def add(self, *args):
        '''
        Adding tags to a component appends them to the render.
        '''
        return self._entry.add(*args)

    def set_attribute(self, key, value):
        if not self.render_tag:
            self.children[0].set_attribute(key, value)
        else:
            super(Component, self).set_attribute(key, value)

    __setitem__ = set_attribute

    def delete_attribute(self, key):
        if not self.render_tag:
            self.children[0].delete_attribute(key)
        else:
            super(Component, self).delete_attribute(key)

    __delitem__ = delete_attribute

    def get(self, tag=None, **kwargs):
        if not self.render_tag:
            return self.children[0].get(tag, **kwargs)
        else:
            return super(Component, self).get(tag, **kwargs)

    def __getitem__(self, key):
        if not self.render_tag:
            if any(object.__getattribute__(self, 'children')):
                return object.__getattribute__(self, 'children')[0].__getitem__(key)
        return super(Component, self).__getitem__(key)

    __getattr__ = __getitem__
    
    def _asdict(self, exclude=None):
        exclude = exclude or ['file_extension', 'render_tag', 'children', 'document', 'parent', 'attributes']
        return {key: value for key, value in asdict(self).items() if key not in exclude} 

    def __hash__(self) -> int:
        return hash(self._entry)
    
    def __eq__(self, other):
        if isinstance(other, Component):
            return self._entry == other._entry
        return self._entry == other
    
    def __html__(self, indent="  ", pretty=True, xhtml=False):
        current_states = self._asdict()
        original_states = self._states
        
        self._states = original_states | current_states
        if original_states != self._states:
            # self._re_render(**current_states)
            self._re_render(**self._states)
            
        return super().__html__(indent, pretty, xhtml)
    
    async def __async_html__(self, indent="  ", pretty=True, xhtml=False):
        current_states = self._asdict()
        original_states = self._states
        
        self._states = original_states | current_states
        if original_states != self._states:
            # self._re_render(**current_states)
            self._re_render(**self._states)
        
        async for html_token in super().__async_html__(indent, pretty, xhtml):
            yield html_token

    def render(self, *args, **kwargs) -> htmltags.html_tag:  # noqa
        raise NotImplementedError(f"method: {self.render.__qualname__} not implemented")

    def _re_render(self, **kwargs) -> htmltags.html_tag: # noqa
        # here is an example below how re_rendering handles function calls like 'increment' 
        # changing variables 
        # with document(x_toggle) as counters:
        # with div(className="relative flex w-full h-screen"):
        #    Counter(),
        #    with Counter(count=2) as counter_2:
        #        div("kml")
        #        div("lakd")
        # counter_2.increment() <- running the method re_renders and updates counter_2
        # counter_2.increment()
        # return counters
        old_parent = self.parent
        old_sub_children = self._entry.children

        if old_parent is not None:
            index_of_entry = old_parent.children.index(self._entry)            
        
        self.clear()
        self._entry = super().add(self.render(**kwargs))
        new_sub_children = self._entry.children
        
        if old_sub_children:
            not_updated_sub_children = old_sub_children[len(new_sub_children):]
            self._entry.add(not_updated_sub_children)
        if old_parent is not None:
            old_parent.set_attribute(index_of_entry, self._entry)
            
        return self._entry
    
    def script(self, *args, **kwargs):
        ...
    
    def call(self, *args, **kwargs):
        """
        This method is basically placeholder for using websocket communications.
        All sorts of fun stuffs can happens here.
        :param args:
        :param kwargs:
        :return:
        """

        raise NotImplemented(f"method: {self.call.__qualname__} not implemented")

    def __dir__(self) -> Iterable[str]:
        return sorted(iter(self.__dict__), key=lambda k: k)


if __name__ == '__main__':
    from valio import IntegerValidator

    # using @dataclass(eq=False) to use super class hash function
    @dataclass(eq=False)
    class vue(Component):
        a: int = IntegerValidator(logger=False, debug=True)
        
        def __post_init__(self):
            super(vue, self).__init__(a=self.a)
            
        def render(self, a) -> htmltags.html_tag: # type: ignore[override]
            return self.html_tags.p(a=a)
        
    class test(Component):
        
        def render(self, *args, **kwargs) -> htmltags.html_tag: # type: ignore[override]
            return self.html_tags.div(*args, **kwargs)
    
    v = vue(a=1)
    print(v)
    print(v._states)
    v.a += 6
    print(v)
    print(v._states)
    print(test("1", className="flex w-10"))