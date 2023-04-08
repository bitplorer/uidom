# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from dataclasses import dataclass

from uidom.dom import *

__all__ = ["x_nav"]


@dataclass
class ToggleIconsWithoutClickAway(XComponent):
    default_icon: dom_tag
    non_default_icon: dom_tag

    def __post_init__(self, *args, **kwargs):
        super(ToggleIconsWithoutClickAway, self).__post_init__(
            *args,
            default_icon=self.default_icon,
            non_default_icon=self.non_default_icon,
            **kwargs
        )

    def render(self, tag_name, default_icon, non_default_icon):
        with template(x_component=tag_name) as toggele_witout_click_away:
            with div(
                className="flex rounded-full items-center justify-center cursor-pointer",
                x_data="{'clicked': 'false', ...$el.parentElement.data(), ...$el.parentElement.$data}",
                x_on_click="clicked = !clicked",
                x_transition_enter="transition ease-in duration-300",
                x_transition_enter_start="opacity-0",
                x_transition_enter_end="opacity-100",
                x_transition_leave="transition ease-in duration-300",
                x_transition_leave_start="opacity-100",
                x_transition_leave_end="opacity-0",
            ):
                button(
                    default_icon,
                    className="flex items-center justify-center text-center rounded-full",
                    x_show="!clicked",
                ),
                button(
                    non_default_icon,
                    className="flex items-center justify-center text-center rounded-full",
                    x_show="clicked",
                )
        return toggele_witout_click_away


x_toggle_dark_mode = ToggleIconsWithoutClickAway(
    tag_name="toggle-dark_mode",
    default_icon=div(
        span(className="iconify", data_icon="teenyicons:bulb-off-solid"),
        # span(data_icon="ic:baseline-light-mode", className="iconify"),
        className="flex h-6 w-6 items-center justify-center",
    ),
    non_default_icon=div(
        span(className="iconify", data_icon="teenyicons:bulb-on-solid"),
        # span(data_icon="ic:baseline-dark-mode", className="iconify"),
        className="flex h-6 w-6 items-center text-yellow-400 justify-center",
    ),
)


@dataclass
class DarkModeButton(XComponent):
    def render(self, tag_name):
        with template(x_component=tag_name) as dark_mode_btn:
            with button(
                className="items-center justify-center overflow-hidden",
            ):
                x_toggle_dark_mode(
                    className="items-center justify-center cursor-pointer",
                    x_data="""{
                    toggle: () => {
                        if (localStorage.theme === 'dark') {
                            localStorage.theme = 'light';
                            document.documentElement.classList.remove('dark');
                        } else {
                            localStorage.theme = 'dark';
                            document.documentElement.classList.add('dark');
                        }
                    },
                    ...$el.parentElement.$data
                }""",
                    x_on_click="toggle",
                    x_init="() => localStorage.theme = 'light'",
                    x_cloak=None,
                ),

        return dark_mode_btn


x_dark_mode = DarkModeButton(tag_name="dark-mode")


@dataclass
class Navigation(XComponent):
    def __post_init__(self, *args, **kwargs):
        super(Navigation, self).__post_init__(*args, **kwargs)

    def render(self, tag_name):
        with template(x_component=tag_name) as navigation:
            with ul(
                x_data="{...$el.parentElement.data()}",
                className="flex grow overflow-hidden w-full h-full self-stretch bg-inherit",
            ):
                with template(x_for="item in menu"):
                    with div(
                        className="flex flex-row grow md:grow-0 h-full w-full md:w-fit "
                        "bg-inherit space-x-2 overflow-hidden justify-center items-center "
                        "transform transition duration-400 ease-in ",
                    ):
                        with a(
                            className="flex flex-row grow md:grow-0 items-center justify-center overflow-hidden",
                            x_bind_href="item.href",
                        ):
                            with div(
                                className="flex items-center justify-center text-center ",
                            ):
                                with div(
                                    # wrapped menu icon paddings
                                    className="flex md:hidden text-center items-center justify-center px-1 pt-1 sm:pt-0",
                                ):
                                    # Menu Icon
                                    span(
                                        className="iconify",
                                        x_bind_data_icon="item.icon",
                                    ),

                                with div(
                                    # wrapped menu text paddings
                                    className="flex flex-grow pt-1 px-3 items-center justify-center text-center",
                                ):
                                    # Menu text
                                    li(
                                        x_text="item.text",
                                        className="sm:flex hidden grow text-center items-center justify-center "
                                        "whitespace-pre ",
                                    ),

                x_dark_mode(className="flex md:px-3", x_show="darkmode")

        return navigation


x_nav = Navigation(tag_name="nav")
x_nav_dependency = x_toggle_dark_mode & x_dark_mode & x_nav

if __name__ == "__main__":
    print(x_nav & x_nav)
