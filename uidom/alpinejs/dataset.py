# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

""" This module contains data_* event functions that can be passed via 
    DataState to its childrens.
    
    
    eg: with DataState() as data_focused_pressed:
            data_focused()
            data_pressed()
        
        now use 
        with data_focusd_pressed:
            div("a"), div("b")
        
        both div's will receive attributes of data-focused and data-pressed.
"""

import json
from textwrap import dedent

from uidom.dom.src.component import Component, Fragment
from uidom.dom.src.dom_tag import attr

__all__ = [
    "dataset_focused",
    "dataset_focus_visible",
    "dataset_pressed",
    "dataset_hovered",
    "dataset_checked",
    "dataset_scrolled",
    "dataset_scrollable",
    "dataset_selected",
    "dataset_xdata",
    "dataset_ripple",
    "dataset_before",
    "dataset_after",
    "DataSet",
]


class MergeAlpineAttributes(Fragment):
    """Merging the attributes with subcontexts via uidom.dom.src.dom_tag.attr

    Args:
        None:
    Usage:
        with MergeAlpineAttributes():
            attr(x_data=..., x_on_*=...)
            attr(x_data=..., x_on_*=...)
            div()
            ### this div receives all the attributes set via attr methods contexts
            ### but all the x_data, x_on_*... kwargs are merged..

    """

    def _merge_x_data_attr(self, key, value):
        if self.attributes.get(key, None):
            x_data = json.loads(self.attributes.get(key).replace("'", '"'))

            if value is None:
                value = x_data
            else:
                value = json.loads(value.replace("'", '"'))
            if isinstance(x_data, dict) and isinstance(value, dict):
                value = x_data | value

            value = json.dumps(value).replace('"', "'")
            self.safe_attributes[key] = False

        return key, value

    def _merge_event_attr(self, key, value):
        # remove indentation and any newlines from the attribute value
        value = " ".join(map(lambda x: x.strip(), dedent(value).split("\n")))

        if self.attributes.get(key, None):
            value = "; ".join([self.attributes[key], value])

        self.safe_attributes[key] = False

        return key, value

    def _merge_bind_attr(self, key, value):
        if self.attributes.get(key, None) and key != ":class":
            raise ValueError(f"{key} merging not implemented yet")
        # am not sure how well have I handled this case, maybe in future
        # I will be more clear on how to merge bindings. Till then let
        # there be some working usage.
        value = "; ".join([self.attributes[key], value])
        return key, value

    def _merge_transition_attr(self, key, value):
        if self.attributes.get(key, None):
            if value:
                value = " ".join([self.attributes[key], value])

        return key, value

    def _merge_class_attr(self, key, value):
        if key == "class" and self.attributes.get(key, None):
            value = " ".join([self.attributes[key], value])
        self.safe_attributes[key] = False
        return key, value

    def set_attribute(self, key, value):
        if isinstance(key, str):
            if key == "x-data":
                key, value = self._merge_x_data_attr(key, value)

            if key.startswith("@"):
                key, value = self._merge_event_attr(key, value)

            if key.startswith(":"):
                key, value = self._merge_bind_attr(key, value)

            if key.startswith("x-transition"):
                key, value = self._merge_transition_attr(key, value)

            if key == "class":
                key, value = self._merge_class_attr(key, value)

        super().set_attribute(key, value)

    __setitem__ = set_attribute


class DataSet(MergeAlpineAttributes):
    """for setting data-* attributes in dom elements"""


def dataset_focused(**kwargs):
    # Whether the element is focused, either via a mouse or keyboard.
    attr(
        x_data="{'focused': false, 'data-focused': ''}",
        x_on_focus="focused = true",
        x_on_blur="focused = false",
        x_on_mousedown="focused = true",
        x_on_keydown="focused = true",
        x_bind_data_focused="focused",
        x_bind_aria_focused="focused",
        **kwargs,
    )


def dataset_focus_visible(**kwargs):
    # Whether the element is keyboard focused.
    # refer: https://css-tricks.com/almanac/selectors/f/focus-visible/
    attr(
        x_data="{'focusVisible': false, 'data-focus-visible': ''}",
        x_on_keydown_dot_tab="focusVisible = !focusVisible",
        x_on_keyup_dot_tab="focusVisible = !focusVisible",
        x_bind_data_focus_visible="focusVisible",
        x_bind_aria_focused="focusVisible",
        **kwargs,
    )


def dataset_pressed(**kwargs):
    attr(
        x_data="{'pressed': false, 'data-pressed': ''}",
        x_on_mousedown="pressed = !pressed",
        x_on_mouseup="pressed = !pressed",
        x_on_blur="pressed = false",
        x_bind_data_pressed="pressed",
        x_bind_aria_pressed="pressed",
        **kwargs,
    )


def dataset_hovered(**kwargs):
    attr(
        x_data="{'hovered': false, 'data-hovered': ''}",
        x_on_mouseenter="hovered = !hovered",
        x_on_mouseleave="hovered = !hovered",
        x_bind_data_hovered="hovered",
        **kwargs,
    )


def dataset_checked(checked: bool, **kwargs):
    attr(
        x_data="{'checked': %s, 'data-state': ''}" % ("true" if checked else "false"),
        x_bind_data_state="[checked == true ? 'checked' : 'unchecked']",
        x_on_click="checked = !checked",
        x_bind_checked="checked",
        x_on_keydown_dot_enter="checked = !checked",
        x_bind_aria_checked="checked",
        **kwargs,
    )


def dataset_scrolled(**kwargs):
    attr(
        x_data="{'scrolled': false, 'data-scrolled': ''}",
        # taken from https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollHeight
        x_on_scroll_dot_window_dot_throttle="[scrolled = Math.abs($el.scrollHeight - $el.clientHeight - $el.scrollTop) < 1]",
        x_bind_data_scrolled="scrolled",
        **kwargs,
    )


def dataset_scrollable(**kwargs):
    attr(
        x_data="{'vscrollable': false, 'hscrollable': false, 'data-scrollable':''}",
        # taken from https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollHeight
        x_bind_vscrollable="window.getComputedStyle($el).overflowY === 'visible' | window.getComputedStyle($el).overflowY !== 'hidden'",
        x_bind_hscrollable="window.getComputedStyle($el).overflowX === 'visible' | window.getComputedStyle($el).overflowX !== 'hidden'",
        x_bind_data_scrollable="vscrollable | hscrollable",
        **kwargs,
    )


def dataset_selected(**kwargs):
    attr(
        x_data="{'selected': false, 'data-selected': ''}",
        x_on_select="selected = true",
        x_on_blur="selected = false",
        x_bind_data_selected="selected",
        **kwargs,
    )


def dataset_xdata(**kwargs):
    attr(x_data="{'data-xdata': ''}", x_bind_data_xdata="$data", **kwargs)


def dataset_ripple(**kwargs):
    # FROM: https://github.com/creativetimofficial/material-tailwind/blob/7535af58990f589e9f5ebdf25164572166a2d60a/public/material-tailwind-html-v2.js#L109

    attr(
        x_data="{'mouseX': 0, 'mouseY': 0, 'x': 0,'y': 0, 'radius': ''}",
        x_on_mousemove="""(event) => {
            let element = event.currentTarget;
            let clientX = event.clientX; 
            let clientY = event.clientY;
            let rect = element.getBoundingClientRect();
            let elementWidth = element.offsetWidth;
            let elementHeight = element.offsetHeight;
            let left = rect.left;
            let top = rect.top;
            mouseX = clientX - left;
            mouseY = clientY - top;
            x = mouseX > elementWidth / 2 ? 0 : elementWidth;
            y = mouseY > elementHeight / 2 ? 0 : elementHeight;        
        }
        """,
        x_on_mouseup="""(event)=> {
            let element = event.currentTarget;
            radius = Math.hypot(x - mouseX, y - mouseY);
            let rippleElem = document.createElement('span');
            rippleElem.style.left = mouseX - radius + 'px';
            rippleElem.style.top = mouseY - radius + 'px';
            rippleElem.style.width = rippleElem.style.height = radius * 2 + 'px';
            rippleElem.setAttribute('data-ripple', true);
            element.appendChild(rippleElem);
            setTimeout(function () {
                rippleElem.setAttribute('data-ripple', false);
                return rippleElem.remove();
            }, 500);
        }
        """,
        **kwargs,
    )


def dataset_before(**kwargs):
    attr(
        x_data="{'data-before': ''}",
        x_bind_data_before="window.getComputedStyle($el, 'before').content",
        **kwargs,
    )


def dataset_after(**kwargs):
    attr(
        x_data="{'data-after': ''}",
        x_bind_data_after="window.getComputedStyle($el, 'after').content",
        **kwargs,
    )
