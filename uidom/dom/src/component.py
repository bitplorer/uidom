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
    file_extension:str = field(init=False, default='')
    render_tag: bool = field(init=False, default=False)
    children: list = field(init=False, default_factory=list)
    document: Union[extension.Tags, None] = field(init=False, default=None)
    attributes: dict = field(init=False, default_factory=dict)

    def __init__(self, *args, **kwargs):
        super(Component, self).__init__()
        self._entry = super(Component, self).add(self.__render__(*args, **kwargs))
        # we perform checks on the _entry "after" the dom initialization because .get method
        # looks into children
        self.__checks__(self._entry)

    def __checks__(self, element: extension.Tags) -> extension.Tags:  # noqa
        if self.render_tag:
            raise ValueError(f"{self.render_tag} can not be true for Components")
        return element

    def add(self, *args):
        '''
        Adding tags to a component appends them to the __render__.
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
    
    def asdict(self, exclude=None):
        exclude = exclude or ['file_extension', 'render_tag', 'children', 'document', 'attributes']
        return {key: value for key, value in asdict(self).items() if key not in exclude} 

    def __hash__(self) -> int:
        return hash(self._entry)

    def __render__(self, *args, **kwargs) -> htmltags.html_tag:  # noqa
        raise NotImplementedError(f"method: {self.__render__.__qualname__} not implemented")

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
    from valio import StringValidator

    # using @dataclass(eq=False) to use super class hash function
    @dataclass(eq=False)
    class vue(Component):
        a: str = StringValidator(logger=False, debug=True)
        
        def __post_init__(self):
            super(vue, self).__init__(a=self.a)
            
        def __render__(self, a) -> htmltags.html_tag: # type: ignore[override]
            return self.html_tags.p(a=a)

    print(vue(a='1'))
