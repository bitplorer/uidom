# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.src import component


class VuetifyElement(component.Component):
    file_extension = ".vue"

    def __render__(self, *args, **kwargs):
        pass
