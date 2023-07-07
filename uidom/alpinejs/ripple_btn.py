# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from uidom.alpinejs import DataSet, dataset_pressed, dataset_ripple
from uidom.dom import *


def data_ripple(className="", **kwargs):
    with DataSet() as _ripple:
        dataset_ripple()
        dataset_pressed()
        attr(
            className="""
            relative w-24 h-10 rounded
            [&>[data-ripple=true]]:absolute
            [&>[data-ripple=true]]:rounded-full
            [&>[data-ripple=true]]:pointer-events-none
            [&>[data-ripple=true]]:bg-rose-400
            [&>[data-ripple=true]]:animate-pulse
            %s
            """
            % className,
            **kwargs,
        )
    return _ripple


class Button(Component):
    def render(self, *args, className="", asElement=None, **kwargs):
        with data_ripple(
            className=f"overflow-hidden m-2 p-2 {className}",
            **kwargs,
        ) as ripple_btn:
            button(*args) if asElement is None else asElement(*args)
        return ripple_btn
