# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.elements import Button
from uidom.dom.htmlelement import HTMLElement
from uidom.dom.icons import Icons
from uidom.dom.links import HtmxLink
from uidom.dom.tailwindcss import Absolute, InlineBlock, InlineFlex, Relative


class DropdownItem(HTMLElement):

    def __render__(self, *args, item_link, target_id, item_name=None, **kwargs):
        self.htmx_link = HtmxLink(*args,
                                  item_link=item_link,
                                  target_id=target_id,
                                  item_name=item_name,
                                  **kwargs)
        self.icon = Icons()
        drop_link = self.html_tags.div(self.icon, self.htmx_link)
        drop_link["class"] = ""
        return drop_link


class DropdownElement(HTMLElement):

    def __render__(self, *args, value="Options", **kwargs):
        self.icon = Icons()
        button = Button("Options", self.icon, value=value)
        button["class"] = ""
        button = InlineFlex(button)
        self.button = button
        self.absolute = self.html_tags.div(*args, **kwargs)
        self.absolute["class"] = ""
        self.absolute = Absolute(self.absolute)
        dropper = self.html_tags.div(self.html_tags.div(self.button), self.absolute)
        dropper["class"] = ""
        return InlineBlock(Relative(dropper))


if __name__ == '__main__':
    account = DropdownItem(item_link="/account", target_id="#account-data", item_name="account")
    account["class"] += " py-1"
    dropdown = DropdownElement(account)
    print(dropdown)
