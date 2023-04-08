# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from uidom.dom import *


class Modal(HTMLElement):
    def render(self, *args, icon="", **kwargs):
        with div(
            x_data="{open: false}",
            x_cloak=None,
            className="w-full h-screen border bg-stone-300 border-gray-400",
        ) as modal:

            comment("Button"),
            with div(x_on_click="open = true", className="m-2"):
                button(
                    div(icon),
                    className="px-5 py-2 text-lg rounded-2xl bg-gradient-to-b from-zinc-700/50  to-zinc-800/70 "
                    "text-zinc-50/90 outline outline-black/10 "
                    "shadow-[inset_0px_0px_1px_1px_rgba(255,255,255,0.2),_0_1px_1px_1px_rgba(0,0,0,0.08)] "
                    "active:outline-black/5 hover:to-zinc-700/40 active:from-zinc-700/50 active:to-zinc-700/60",
                ),

            comment("Modal"),
            with div(
                x_show="open",
                x_on_keydown_dot_escape_dot_prevent_dot_stop_dot_window="open = false",
                role="dialog",
                aria_modal="true",
                x_id="['modal-title']",
                x_bind_aria_labelledby="$id('modal-title')",
                className="fixed inset-0 scroll-smooth p-10 bg-transparent/20 bg-opacity-90 ",
                # x_on_keypress="console.log($event)",
                x_on_keydown_dot_ctrl_dot_slash_dot_window="open = true",
                x_bind_class="{'backdrop-blur-sm': open == true}",
            ):
                comment("Overlay"),
                div(
                    x_show="open",
                    x_transition_dot_opacity=None,
                    className="fixed inset-0 bg-transparent bg-opacity-80",
                ),
                comment("Panel"),
                with div(
                    x_show="open",
                    x_transition=None,
                    x_on_click="open = false",
                    className="relative min-h-screen flex items-center justify-center",
                ):
                    with div(
                        *args,
                        **kwargs,
                        x_on_click_dot_stop=None,
                        x_trap_dot_noscroll_dot_inert="open",
                        className="relative h-96 w-2/3 bg-gray-50 p-8 overflow-y-auto flex rounded-lg "
                        "border border-gray-400/40 shadow-md shadow-gray-400/40",
                    ):
                        div(
                            div(hero_x_icon, className="flex items-center mt-0.5 "),
                            className="flex h-8 w-8 absolute right-0 top-0 z-10 cursor-pointer bg-gray-200/40 "
                            "items-center text-center justify-center p-1 rounded-bl-xl "
                            "shadow-sm shadow-gray-400 hover:shadow-none",
                            x_on_click="open = false",
                        )

        return modal
