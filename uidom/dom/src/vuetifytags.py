# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

# Copyright (c) 2022 Valio
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from uidom.dom.src.main import extension


class VuetifyTags(extension.DoubleTags):
    child_dedent = False
    self_dedent = False
    left_tag = "<"
    right_tag = ">"


class VApp(VuetifyTags):
    tagname = "v-app"


class VAppBar(VuetifyTags):
    tagname = "v-app-bar"


class VAppBarNavIcon(VuetifyTags):
    tagname = "v-app-bar-nav-icon"


class VToolBarTitle(VuetifyTags):
    tagname = "v-toolbar-title"


class VToolbar(VuetifyTags):
    tagname = "v-toolbar"


class VSpacer(VuetifyTags):
    tagname = "v-spacer"


class VMain(VuetifyTags):
    tagname = "v-main"


class VContainer(VuetifyTags):
    tagname = "v-container"


class component(VuetifyTags):
    pass


if __name__ == '__main__':

    from uidom.dom.htmlelement import HTMLElement
    from uidom.dom.src.htmltags import comment

    class x(HTMLElement):

        def __render__(self, name, *args, **kwargs):
            return component(name, *args, **kwargs)

    from uidom.dom.src.htmltags import body, script
    print(x(body(script("jajajajaj"), comment("hahahah")), hello=1, x_dot_data="jk", _="sa"))
