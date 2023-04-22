# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from dataclasses import dataclass

from uidom.dom.htmlelement import HTMLElement

__all__ = [
    "DateLabel",
    "DateInput",
]

@dataclass(eq=False)
class DateLabel(HTMLElement):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def render(self, *args, **kwargs):
        return self.html_tags.label(*args, **kwargs)    


@dataclass(eq=False)
class DateInput(HTMLElement):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, *args, **kwargs):
        return self.html_tags.input_(*args, type="date", **kwargs)


