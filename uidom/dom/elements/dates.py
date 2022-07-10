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

@dataclass
class DateLabel(HTMLElement):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def __render__(self, *args, **kwargs):
        return self.html_tags.label(*args, **kwargs)    


@dataclass
class DateInput(HTMLElement):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __render__(self, *args, **kwargs):
        return self.html_tags.input_(*args, type="date", **kwargs)


