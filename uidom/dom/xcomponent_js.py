# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement
from uidom.dom.src.htmltags import script
from uidom.dom.src.utils.dom_util import raw

# The pure client-side code taken from https://stackoverflow.com/a/67276585
# and https://stackoverflow.com/a/48777481

__all__ = ["XComponentJS"]


class XComponentJS(HTMLElement):
    """
    Adaptor concept taken from:
        https://github.com/material-components/material-components-web/tree/9736ddce9c12f5485e746984225919568541e88d/packages/mdc-base
    """

    def __render__(self, *args, **kwargs):
        js = """
            
            function guidGenerator() {
                const S4 = function (){
                    return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
                };
                return S4() + S4() + '-' + S4() + '-' + S4() + '-' + S4() + '-' + S4() + S4() + S4();
            }
        
            const toCamel = (s) => {
                return s.replace(/([-_][a-z])/ig, ($1) => {
                    return $1.toUpperCase()
                        .replace('-', '')
                        .replace('_', '');
                });
            }

            const isJSON = (str) => {
                try {
                    return (JSON.parse(str) && !!str);
                } catch (e) {
                    return false;
                }
            }

            const observeAttrChange = (el, attributeChangedCallback) => {
                var observer = new MutationObserver(mutations => {
                    mutations.forEach((mutation) => {
                        if (mutation.type === 'attributes') {
                            let oldVal = mutation.oldValue;
                            let newVal = mutation.target.getAttribute(mutation.attributeName);
                            attributeChangedCallback(mutation.attributeName, oldVal, newVal);
                        }
                    });
                });
                observer.observe(el, {
                    attributes: true,
                    attributeOldValue: true,
                    attributeFilter: ['id', 'class', 'style']
                });
                return observer;
            }

            (() => {
                let socket = {};
                let messageHandler = {};
                
                const setUpOrGetWebSocket = (elementID, messageHandler, endPoint = 'ws') => {
                    if (!socket[`${endPoint}`]) {
                        let url = new URL(document.location);
                        const wsUrl = `${url.protocol.replace('http', 'ws')}//${url.hostname}:${url.port}/${endPoint}`;
                        socket[`${endPoint}`] = new WebSocket(wsUrl);
                        socket[`${endPoint}`].onopen = (event) => {
                            console.log(`connected to ${wsUrl}`);
                            socket[`${endPoint}`].send(`connection to client user ${elementID}:${JSON.stringify(event)}`);
                            console.log(event);
                        };
                        socket[`${endPoint}`].onclose = (event) => {
                            console.log(`connection closed to ${elementID}:${wsUrl}`);
                            socket[`${endPoint}`] = null;
                            setTimeout(
                                () => {socket[`${endPoint}`] = setUpOrGetWebSocket(elementID, messageHandler, endPoint)}
                                , 300);
                            clearTimeout();
                        };
                        socket[`${endPoint}`].onerror = (event) => {
                            console.log(`connection closed to ${elementID}:${wsUrl} due to error`);
                        };
                    }
                    socket[`${endPoint}`].onmessage = (message) => {
                        let data = message.data;
                        if (isJSON(data)) {
                            data = JSON.parse(data);
                        }
                        messageHandler[`${elementID}`](data);
                    };
                    return socket[`${endPoint}`];
                };
                document.setUpOrGetWebSocket = setUpOrGetWebSocket;
                document.messageHandler = messageHandler;
            })();

            
            document.querySelectorAll('[x-component]').forEach(component => {
                const componentName = `x-${component.getAttribute('x-component')}`;

                class XComponent extends HTMLElement {
                    
                    constructor() {
                        super();
                    }

                    connectedCallback() {
                        var isShadowRoot = component.getAttribute('shadowroot');
                        if (!!isShadowRoot){
                            
                            let shadow = this.attachShadow({mode: 'open'});
                            
                            let template;
                            if (component.tagName === 'TEMPLATE'){
                                template = component;
                            } else {
                                template = component.getElementsByTagName('template')[0];
                            }

                            if (template?.content.childElementCount) {
                                shadow.appendChild(template.content.cloneNode(true));
                                }
                            else {
                                let slot = document.createElement('slot');
                                shadow.appendChild(slot);
                                }
                            this.shadow = shadow;
                            this.checkId();
                            document.addEventListener('alpine:initialized', () => {
                                Alpine.initTree(this.shadow);
                            });
                        }
                        
                        if (!this.id){
                            this.append(component.content.cloneNode(true));
                            this.checkId();
                        }
                        
                        this.addEventListener('alpine:init', () => {
                            Alpine.data("parentElementData", () => ({
                                ...this.data()
                            }))
                        });
                        
                              
                        this.dataCallback = this.dataCallback.bind(this);              
                        // <my-div active="true", data-target="#accordian"></my-div>
                        // example: for setting up  name="cool-dude" value as this.name value
                        let _dataState = this.data();

                        // for setting up data-target value
                        let _dataTarget = this?.dataset.target || {};
                        if (isJSON(_dataTarget)){
                            _dataTarget = JSON.parse(_dataTarget);
                        }
                        // for setting up data-action value
                        let _dataAction = this?.dataset.action || {};
                        //console.log("DATA_STATE: ", _dataState);
                        if (!!_dataState) {
                            Object.keys(_dataState).forEach(attr => {
                                if (this.hasOwnProperty(attr)){
                                    throw new Error(`attribute ${attr} can't be assigned as its builtin HtmlElement property`);
                                }
                                Object.defineProperty(this, `_data_${attr}`, {
                                    get() {
                                        if (this.hasAttribute(`__${attr}`)) {
                                            return this.getAttribute(`__${attr}`);
                                        } else {
                                            let val = _dataState[attr];
                                            if (isJSON(val)) {
                                                this.setAttribute(`__${attr}`, JSON.parse(val));
                                            } else {
                                                this.setAttribute(`__${attr}`, val);
                                            }
                                            return this.getAttribute(`__${attr}`);
                                        }
                                    },
                                    set(value) {
                                        if (isJSON(value)) {
                                            this.setAttribute(`__${attr}`, JSON.parse(value));
                                        } else {
                                            this.setAttribute(`__${attr}`, value);
                                        }
                                        let oldValue = this.dataset.state[attr];
                                        if (oldValue !== value) {
                                            this.dataset.state[attr] = value;
                                        }
                                    }
                                });
                            });
                        }

                        // connecting to websockets
                        if (_dataState?.ws){
                            let messageHandler = document.messageHandler;
                            messageHandler[`${this.id}`] = () => {};
                            this.ws = document.setUpOrGetWebSocket(this.id, messageHandler, _dataState?.ws || 'ws');
                        }
                        if  (!!this?.ws?.readyState){
                            this.ws.send(JSON.stringify({id: this.id}));
                        }
                        
                        
                        this.observer = observeAttrChange(this, (attr, oldVal, newVal) => {
                            // slice :attr to remove leading '_' (underscore) to check in _dataState
                            //console.log(attr, _dataState.includes(attr.replace('__', '')));
                            if (_dataState?.includes(attr.replace('__', ''))) {
                                this.attributeChangedCallback(attr.replace('__', ''), oldVal, newVal);
                            }
                        });
                    }
                    
                    checkId() {
                        if (!this.id) this.id = `x-${component.getAttribute('x-component')}` + '-' + guidGenerator();
                    }
                    
                    dataCallback(message){
                        if (isJSON(message)){
                            message = JSON.parse(message);
                        }
                        if (typeof message === "[object String]"){
                            console.log("SERVER_MESSAGE", message);
                            return;
                        }
                        if (this.id === message.id){
                            this.attributeChangedCallback(message.attr, message.oldVal, message.newVal);
                        }
                        this.ws.send(
                            JSON.stringify(
                                {id: message.id , 
                                 attr:message.attr,
                                 oldVal: message.oldVal, 
                                 newVal: message.newVal}
                            )
                        );
                    }

                    attributeChangedCallback(attrName, o, n) {
                        console.log(attrName, o, n);
                        if (n !== o){
                            this[attrName] = n;   
                            //this.dataCallback(attrName, o, n);
                        }
                    }

                    disconnectedCallback() {
                        //super.disconnectedCallback();
                        this.observer.disconnect();
                        this.observer = null;
                    }

                    async getFile(url) {
                        const res = await fetch(url);
                        if (!res.ok) {
                            throw Object.assign(new Error(res.statusText + ' ' + url), {
                                res
                            });
                        }
                        return {
                            getContentData: asBinary => asBinary ? res.arrayBuffer() : res.text(),
                        };
                    }


                    dispatch(name, data, options = {
                        bubble: true,
                        cancelable: false,
                        composed: false
                    }) {
                        const event = new CustomEvent(name, {
                            bubbles: options.bubble,
                            cancelable: options.cancelable,
                            composed: options.composed,
                            detail: data
                        });
                        this.dispatchEvent(event);
                    }
                    

                    data() {
                        const attributes = this.getAttributeNames();
                        const data = {};

                        attributes.forEach(attribute => {

                            if (!isJSON(this.getAttribute(attribute))) {
                                data[attribute] = this.getAttribute(attribute);
                            } else {
                                data[attribute] = JSON.parse(this.getAttribute(attribute));
                            }
                        });
                        return data;
                    }

                }

                customElements.define(componentName, XComponent);
            }); 
            
            """
        return script(raw(js))
