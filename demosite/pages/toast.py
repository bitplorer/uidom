# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from dataclasses import dataclass

from uidom.dom import *

__all__ = ["ToastElement", "x_toast", "success_toast"]


@dataclass
class ToastElement(HTMLElement):
    def __init__(self, *args, **kwargs):
        super(ToastElement, self).__init__(*args, **kwargs)

    def render(self):
        with div(
            x_data=None, className="absolute top-16 right-10 p-4 overflow-x-hidden"
        ) as toast:
            with template(
                x_for="(toast, index) in $store.toasts.list", x_bind_key="toast.id"
            ):
                with div(
                    x_show="toast.visible",
                    x_on_click="$store.toasts.destroyToast(index)",
                    x_transition_enter="transition ease-in duration-200",
                    x_transition_enter_start="transform opacity-0 translate-y-2",
                    x_transition_enter_end="transform opacity-100",
                    x_transition_leave="transition ease-out duration-500",
                    x_transition_leave_start="transform translate-x-0 opacity-100",
                    x_transition_leave_end="transform translate-x-full opacity-0",
                    className="bg-stone-600 text-white p-3 px-5 rounded mb-1 shadow-lg "
                    "flex items-center justify-around z-10 backdrop-blur-sm fill-current "
                    "border-t-4 border-stone-900 ",
                    x_bind_class="""{
            ' bg-gradient-to-r from-yellow-500 to-transparent hover:text-white hover:from-gray-500 hover:to-gray-600': toast.type === 'info',
            ' bg-gradient-to-r from-green-500 to-green-600 hover:text-white hover:from-gray-500 hover:to-gray-600': toast.type === 'success',
            ' bg-gradient-to-r from-orange-400 to-yellow-500 hover:text-white hover:from-gray-500 hover:to-gray-600': toast.type === 'warning',
            ' bg-gradient-to-r from-yellow-500 to-rose-500 hover:text-white hover:from-gray-500 hover:to-gray-600': toast.type === 'error',
            ' bg-gradient-to-r from-blue-500 to-gray-500 hover:text-white hover:from-gray-500 hover:to-gray-600': toast.type === 'follow',
            ' bg-gradient-to-r from-yellow-500 to-rose-500 hover:text-white hover:from-gray-500 hover:to-gray-600': toast.type === 'unfollow',
            ' bg-gradient-to-r from-pink-500 to-rose-600 hover:text-white hover:from-gray-500 hover:to-gray-600': toast.type === 'heart',
            ' bg-gradient-to-r from-green-500 to-green-600 hover:text-white hover:from-gray-500 hover:to-gray-600': toast.type === 'track'
            }""",
                ):
                    div(
                        span(className="iconify", data_icon="fa-solid:info-circle"),
                        className="flex w-6 h-6 mx-2 justify-center items-center",
                        x_show="toast.type == 'info'",
                    ),
                    div(
                        span(
                            className="iconify",
                            data_icon="clarity:success-standard-solid",
                        ),
                        className="flex w-6 h-6 mr-2 justify-center items-center",
                        x_show="toast.type == 'success'",
                    ),
                    div(
                        span(
                            className="iconify", data_icon="ant-design:warning-filled"
                        ),
                        className="flex w-6 h-6 mr-2 justify-center items-center",
                        x_show="toast.type == 'warning'",
                    ),
                    div(
                        span(className="iconify", data_icon="akar-icons:chat-error"),
                        className="flex w-6 h-6 mr-2 justify-center items-center",
                        x_show="toast.type == 'error'",
                    ),
                    div(
                        follow_icon,
                        className="flex w-6 h-6 mr-2 justify-center items-center",
                        x_show="toast.type == 'follow'",
                    )
                    div(
                        unfollow_icon,
                        className="flex w-6 h-6 mr-2 justify-center items-center",
                        x_show="toast.type == 'unfollow'",
                    )
                    div(
                        heart_filled_icon,
                        className="flex w-6 h-6 mr-2 justify-center items-center",
                        x_show="toast.type == 'heart'",
                    )
                    div(
                        changes_icon,
                        className="flex w-6 h-6 mr-2 justify-center items-center",
                        x_show="toast.type == 'track'",
                    )
                    div(x_text="toast.message")
            self.script()
        return toast

    @script
    def script(self):
        return raw(
            """
        document.addEventListener('alpine:init', () => {
                       Alpine.store("toasts", {
                           counter: 0,
                           list: [],
                           createToast(message, type = "info") {
                               const index = this.list.length
                               let totalVisible =
                                   this.list.filter((toast) => {
                                       return toast.visible
                                   }).length + 1
                               this.list.push({
                                   id: this.counter++,
                                   message,
                                   type,
                                   visible: true,
                               })
                               setTimeout(() => {
                                   this.destroyToast(index)
                               }, 2000 * totalVisible)
                           },
                           destroyToast(index) {
                               this.list[index].visible = false
                           },
                       })
                       })
        """
        )


x_toast = ToastElement()


def success_toast(message):
    return div(
        x_data=None,
        x_on_click=f"$store.toasts.createToast('{message}', 'success')",
        className="bg-gray-700 border-t-4 border-blue-600 text-white p-3",
    )
