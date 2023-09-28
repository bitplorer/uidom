# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from uidom.alpinejs import DataSet, dataset_ripple  # , dataset_pressed
from uidom.dom import *


def data_ripple(className="[&>[data-ripple=true]]:bg-white/30", **kwargs):
    with DataSet() as _ripple:
        dataset_ripple()
        # dataset_pressed()
        attr(
            className="""
            relative overflow-hidden
            [&>[data-ripple=true]]:absolute
            [&>[data-ripple=true]]:rounded-full
            [&>[data-ripple=true]]:pointer-events-none
            [&>[data-ripple=true]]:animate-ripple
            %s
            """
            % className,
            **kwargs,
        )
    return _ripple


class Button(Component):
    def render(self, *args, _as=button, **kwargs):
        with data_ripple(className="[&>[data-ripple=true]]:bg-stone-400/40"):
            return _as(*args, **kwargs)


if __name__ == "__main__":
    print(
        Button(
            "Login",
            className="flex px-4 py-2 bg-rose-400 [data-loading=true]:animate-pulse",
            x_on_mouseup="data-loading=true",
            x_data="{'data-loading': false}",
        )
    )
