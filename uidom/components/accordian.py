# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom import *


class Accordian(XComponent):

    def __render__(self, tag_name):
        return template(
            raw('''
    <div x-data="{
        ...accordianParam(),
        ...$el.parentElement.data(),
        get expanded() {
            return this.active === this.id
        },
        set expanded(value) {
            this.active = value ? this.id : null
        }
    }" role="region" class="border border-black p-1 border-collapse">
        <h2>
            <button
                @click="expanded = !expanded"
                :aria-expanded="expanded"
                class="flex items-center justify-between w-full font-bold text-xl px-6 py-3"
                :class="{'': this.active === this.id }"
                x-effect="console.log(this.active)"
            >
                <span x-text="title"></span>
                <span x-show="expanded" aria-hidden="true" class="ml-4">&minus;</span>
                <span x-show="!expanded" aria-hidden="true" class="ml-4">&plus;</span>
            </button>
        </h2>

        <div x-show="expanded" x-collapse>
            <div class="pb-4 px-6" x-html="content"></div>
        </div>
    </div>
            '''),
            script("function accordianParam(){ return {title:'', content:'', id: '', active: '' } }"),
            x_component=tag_name
        )


accordian = Accordian(tag_name="accordian")


class AccordianGroup(XComponent):
    def __render__(self, tag_name):
        return template(div(slot()), x_data="{}", x_component=tag_name)


accordianGroup = AccordianGroup(tag_name="accordian-group")
