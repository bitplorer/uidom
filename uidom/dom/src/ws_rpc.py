# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from dataclasses import dataclass

from uidom.dom.htmlelement import HTMLElement

# from uidom.dom.src.htmltags import script
from uidom.dom.src.utils.dom_util import raw


class ws_rpc(HTMLElement):
    file_extension = ".js"

    def render(self):
        return raw(
            """

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
                        console.log(`creating new WebSocket Instance to ${wsUrl} for element ${elementID}`);
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
                            //clearTimeout(timeOut);
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


                   
function addEventListenerWithSocket(socket, element, eventType, payload, targetElement, swapMethod, loadingBar, errorBar) {
  element.addEventListener("click", function(event) {
    event.preventDefault();
    
    if (loadingBar) {
      hideElement(targetElement);
      showElement(loadingBar);
    }
    
    if (errorBar) hideElement(errorBar);
    
    var responseHandler = function(response) {
      if ("error" in response) {
        if (loadingBar) hideElement(loadingBar);
        if (errorBar) {
          errorBar.textContent = response.error;
          showElement(errorBar);
          setTimeout(function() {
            hideElement(errorBar);
            showElement(targetElement);
          }, 5000);
        } else {
          showElement(targetElement);
          console.error(response.error);
        }
        return;
      }
      const elementId = response.element_id;
      const data = response.data;
      const target = targetElement ? document.querySelector(targetElement) : document.getElementById(elementId);
      if (target) {
        target[swapMethod] = data;
        if (loadingBar) hideElement(loadingBar);
      } else {
        console.error(`Element with ID ${elementId} or selector ${targetElement} not found`);
      }
    }
    
    element.messageHandler = responseHandler;
    
    // send(JSON.stringify({
    //  event_type: eventType,
    //  payload: payload
    //}));
    element.waitForConnection().then(()=> socket.send(
      JSON.stringify({
        event_type: eventType,
        payload: payload
      }))
    );
    
  });
}

function dispatchEventWithSocket(socket, event) {
  const eventType = event.target.getAttribute("data-event-type");
  const payload = JSON.parse(event.target.getAttribute("data-payload"));
  const targetElement = event.target.getAttribute("data-target-element") || event.target;
  const swapMethod = event.target.getAttribute("data-swap-method") || "innerHTML";
  const loadingBar = document.querySelector("[data-loading-bar]") || null;
  const errorBar = document.querySelector("[data-error-bar]") || null;
  
  addEventListenerWithSocket(socket, event.target, eventType, payload, targetElement, swapMethod, loadingBar, errorBar);
}


function hideElement(element){
    element.classList.add("hidden");
}

function showElement(element){
    element.classList.remove("hidden");
}

const elements = document.querySelectorAll("[data-event-type]");
for (let i = 0; i < elements.length; i++) {
  let id = elements[i].getAttribute('id');
  let ws_url = elements[i].getAttribute("data-socket");
  let messageHandler = document.messageHandler;
  messageHandler[id] = (message) => elements[i].messageHandler(message);
  let web_socket = document.setUpOrGetWebSocket(id, messageHandler, ws_url);
  elements[i].waitForConnection = document.waitForConnection[ws_url];
  elements[i].addEventListener("click", function(event) {
    dispatchEventWithSocket(web_socket, event);
  });
}
"""
        )
