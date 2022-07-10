# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement
from uidom.dom.src.htmltags import script
from uidom.dom.src.utils.dom_util import raw

# The pure client-side code taken from https://stackoverflow.com/a/67276585
# and https://stackoverflow.com/a/48777481


class XShadowComponent(HTMLElement):

    # "init-alpine-tree" directive signal's browser to initialise the alpine tree with shadow-dom

    def __render__(self, *args, **kwargs):
        return script(raw("""
    document.querySelectorAll('[x-shadow-component]').forEach(component => {
        const componentName = `x-${component.getAttribute('x-shadow-component')}`
        class XShadowComponent extends HTMLElement {
            constructor() {
                super();
                var shadow = this.attachShadow({mode: 'open'});
                var slot = document.createElement('slot');
                var template = component.getElementsByTagName('template');
                if (template.length > 0) {
                    shadow.appendChild(template[0].content.cloneNode(true));
                    }
                else {
                    shadow.appendChild(slot);
                    }
                this.shadow = shadow
                }
                        
            connectedCallback() {
               if (component.hasAttribute("init-alpine-tree") && component.getAttribute("init-alpine-tree")) {
                    document.addEventListener('alpine:initialized', () => Alpine.initTree(this.shadow));
                }
            }

            attributeChangedCallback() {
                super.attributeChangedCallback();
            }

            disconnectedCallback() {
                super.disconnectedCallback();
            }

            data() {
                const attributes = this.getAttributeNames()
                const data = {}

                function isJSON(str) {
                    try {
                        return (JSON.parse(str) && !!str);
                    } catch (e) {
                        return false;
                        }
                    }


                attributes.forEach(attribute => {

                    if (!isJSON(this.getAttribute(attribute))) {
                        data[attribute] = this.getAttribute(attribute)
                    } else {
                        data[attribute] = JSON.parse(this.getAttribute(attribute))   
                    }
                })
                return data
            }
        }
        
        customElements.define(componentName, XShadowComponent)
    })
"""))
