// Copyright (c) 2023 UiDOM
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT


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
    let connection_resolvers = {};
    let waitForConnection = {}
    // connection_resolvers is taken from https://stackoverflow.com/a/68559559
    
    const setUpOrGetWebSocket = (elementID, messageHandler, endPoint = '/ws') => {
        if (!socket[`${endPoint}`]) {
            let url = new URL(document.location);
            const wsUrl = `${url.protocol.replace('http', 'ws')}//${url.hostname}:${url.port}${endPoint}`;
            console.log(`creating new WebSocket Instance to ${wsUrl}`);
            socket[`${endPoint}`] = new WebSocket(wsUrl);
            if (!connection_resolvers[`${endPoint}`]){
                connection_resolvers[`${endPoint}`] = [];
            }
            
            if (!waitForConnection[`${endPoint}`]){
                waitForConnection[`${endPoint}`] = () => {
                    return new Promise((resolve, reject) => {
                        connection_resolvers[`${endPoint}`].push({resolve, reject});
                    });
                }
            }

            socket[`${endPoint}`].addEventListener('open', () => {
                connection_resolvers[`${endPoint}`].forEach(r => r.resolve())
            });
            
            socket[`${endPoint}`].onopen = (event) => {
                console.log(`connected to ${wsUrl}`);
                socket[`${endPoint}`].send(`connection open to client element ${elementID}:${JSON.stringify(event)}`);
            };
            socket[`${endPoint}`].onclose = (event) => {
                console.log(`connection closed to ${elementID}: ${wsUrl}`);
                socket[`${endPoint}`] = null;
                timeOut = setTimeout(
                    () => {socket[`${endPoint}`] = setUpOrGetWebSocket(elementID, messageHandler, endPoint)}
                    , 300);
                clearTimeout(timeOut);
            };
            socket[`${endPoint}`].onerror = (event) => {
                console.log(`connection closed to ${elementID}:${wsUrl} due to error {event}`);
            };
        }
        socket[`${endPoint}`].onmessage = (message) => {
            let data = message.data;
            if (isJSON(message)) {
                data = JSON.parse(data);
            }
            messageHandler[`${elementID}`](data);
        };
        return socket[`${endPoint}`];
    };
    document.setUpOrGetWebSocket = setUpOrGetWebSocket;
    document.messageHandler = messageHandler;
    document.waitForConnection = waitForConnection;
})();


// taken from https://stackoverflow.com/a/73956155
// and https://github.com/alpinejs/alpine/blob/0a360fbae712fd6bf98b382140cdd7af3dc69644/packages/ui/src/menu.js
// document.addEventListener("alpine:init", () => {
//     window.Alpine.directive('uidom', (el, directive) => {
//         window.Alpine.bind(el, {
//         'x-data'() {
//             return el.parentElement.data();
//         }
//         })
//     }) 
// });


document.querySelectorAll('[x-component]').forEach(component => {
    const componentName = `x-${component.getAttribute('x-component')}`;

    class XComponent extends HTMLElement {
        
        constructor() {
            super();
        }

        async connectedCallback() {
            var isShadowRoot = component.getAttribute('shadowroot');
            let template;
            if (component.tagName === 'TEMPLATE'){
                template = component;
            } else {
                template = component.getElementsByTagName('template')[0];
            }
            if (!!isShadowRoot){
                
                let shadow = this.attachShadow({mode: 'open'});

                if (template?.content.childElementCount) {
                    shadow.appendChild(template.content.cloneNode(true));
                    }
                else {
                    let slot = document.createElement('slot');
                    shadow.appendChild(slot);
                    }
                this.shadow = shadow;
                this.checkOrCreateId();
                document.addEventListener('alpine:initialized', () => {
                    Alpine.initTree(this.shadow);
                });
            }
            
            else {
                if (!!template){
                    this.append(component.content.cloneNode(true));
                    }
                else {
                    this.append(component.cloneNode(true));
                }
                
                this.checkOrCreateId();
                document.addEventListener('alpine:initialized', () => {
                    Alpine.initTree(this);
                });
            }
                     
                  
            this.dataCallback = this.dataCallback.bind(this);              
            // <my-div active="true", data-target="#accordian"></my-div>
            // example: for setting up  name="cool-dude" value as this.name value
            this._dataState = this.stateData();
            
            // for setting up data-target value
            let _dataTarget = this?.dataset.target || new Map();
            if (isJSON(_dataTarget)){
                _dataTarget = JSON.parse(_dataTarget);
            }
            // for setting up data-action value
            let _dataAction = this?.dataset.action || new Map();
            
            if (!!this._dataState) {
                this._dataState.forEach((value, attr) => {
                    if (this.hasOwnProperty(attr)){
                        throw new Error(`attribute ${attr} can't be assigned as its builtin HtmlElement property`);
                    }
                    Object.defineProperty(this, `_data_${attr}`, {
                        get() {
                            if (this.hasAttribute(`${attr}`)) {
                                return this.getAttribute(`${attr}`);
                            } 
                            return;
                        },
                        
                        set(value) {
                            if (isJSON(value)) {
                                this.setAttribute(`${attr}`, JSON.parse(value));
                            } else {
                                this.setAttribute(`${attr}`, value);
                            }
                        }
                    });
                });
            }

            // connecting to websockets
            if (this._dataState.get('ws')){
                let messageHandler = document.messageHandler;
                messageHandler[`${this.id}`] = this.dataCallback;
                this.ws = document.setUpOrGetWebSocket(this.id, messageHandler, this._dataState.get('ws'));
                this.waitForConnection = document.waitForConnection[`${this._dataState.get('ws')}`]
            }
            
            
            this.observer = observeAttrChange(this, (attr, oldVal, newVal) => {
                // slice :attr to remove leading '_' (underscore) to check in this._dataState
                // console.log('from observer',attr, oldVal, newVal);
                //console.log(attr, this._dataState.get(attr.replace('_data_', '')));
                if (this._dataState.get(attr.replace('_data_', ''))) {
                    this.attributeChangedCallback(attr.replace('_data_', ''), oldVal, newVal);
                }
            });
            
            //setTimeout(() => {this.ws.send(JSON.stringify(this.data()));}, 300);
            if (this.getAttribute('ws_send')){
                this.send(JSON.stringify(this._dataState.get('ws_send')));
            }
        }
        
        
        checkOrCreateId() {
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
            this.send(JSON.stringify(message));
        }

        attributeChangedCallback(attrName, o, n) {
            console.log('from attributeChangedCallback', attrName, o, n);
            if (n !== o){
                this[attrName] = n;
            }
        }

        disconnectedCallback() {
            //super.disconnectedCallback();
            this.observer.disconnect();
            this.observer = null;
            if (this.ws){
                this.ws.close();
                this.ws = null;
            }
        }
        
        send(data, retries = 4) {
            try {
                this.ws.send(data);
                return data;
            } 
            catch (error) {
                if (retries > 0 && error.name === "InvalidStateError") {
                    this.waitForConnection()
                        .then(()=> this.send(data, retries - 1));
                }
                else {
                    throw error;
                }
            }
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
            
            let filterAttr = ["@", "x-", "id", "class", ":"]
            let thisEtries = Object.entries(
                Object.fromEntries(this.stateData())
                ).filter(([attr, value]) => !filterAttr.some((letter) => attr.startsWith(letter)));
            return Object.fromEntries(thisEtries);            
        }

        stateData() {
            const attributes = this.getAttributeNames();
            const data = new Map();

            attributes.forEach(attribute => {

                if (!isJSON(this.getAttribute(attribute))) {
                    data.set(attribute, this.getAttribute(attribute));
                } else {
                    data.set(attribute, JSON.parse(this.getAttribute(attribute)));
                }
            });
            return data;
        }

    }

    customElements.define(componentName, XComponent);
});