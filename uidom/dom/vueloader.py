# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom import HTMLElement, raw, script

__all__ = [
    "VueLoader",
]


class VueLoader(HTMLElement):
    # for more details look at
    # https://github.com/FranckFreiburger/vue3-sfc-loader

    def __render__(self, *args, **kwargs):
        return script(
            raw('''
        // Options from the vue3-sfc-loader Example at https://github.com/FranckFreiburger/vue3-sfc-loader#example
        const options = {
            moduleCache: {
                vue: Vue
            },
            async getFile(url) {
                const res = await fetch(url);
                if (!res.ok)
                    throw Object.assign(new Error(res.statusText + ' ' + url), { res });
                return {
                    getContentData: asBinary => asBinary ? res.arrayBuffer() : res.text(),
                }
            },
            addStyle(textContent) {
                const style = Object.assign(document.createElement('style'), { textContent });
                const ref = document.head.getElementsByTagName('style')[0] || null;
                document.head.insertBefore(style, ref);
            },
        }
        const { loadModule } = window['vue3-sfc-loader'];
        const app = createApp({
            components: {
                'vue-card': vue_card, // Vue Component from Razor Partial
                'vue-card2': Vue.defineAsyncComponent(() => loadModule('./js/vue-card2.vue', options)) // Vue SFC
            }
        });
        app.mount('#app');
        '''),
            type="text/javascript"
        )
