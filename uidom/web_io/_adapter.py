# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import asyncio
import json
from abc import ABC, abstractmethod
from asyncio import create_task, gather, sleep
from collections import defaultdict
from json.decoder import JSONDecodeError
from typing import Any, Optional, Type

from uidom.web_io._events import WebSocketEvents
from uidom.web_io._protocol import WebSocketProtocol as WebSocket
from uidom.web_io._types import MESSAGE

__all__ = ["WebSocketAdapter", "WebSocketClientHandler", "EdgeDBFetcher"]


class GenericAdapter(ABC):
    connections: set

    @abstractmethod
    async def sleep(self):
        pass

    @abstractmethod
    async def connect(self, websocket: WebSocket):
        pass

    @abstractmethod
    async def on_connect(self, *args, websocket: WebSocket, **kwargs):
        pass

    @abstractmethod
    async def disconnect(self, websocket: WebSocket):
        pass

    @abstractmethod
    async def on_disconnect(
        self, *args, websocket: WebSocket, message: Optional[MESSAGE], **kwargs
    ):
        pass

    @abstractmethod
    async def receive(self, websocket: WebSocket) -> MESSAGE:
        pass

    @abstractmethod
    async def on_receive(self, *args, websocket: WebSocket, message: MESSAGE, **kwargs):
        pass

    @abstractmethod
    async def on_relay(
        self,
        *args,
        websocket: WebSocket,
        message: MESSAGE,
        connections: Optional[set[WebSocket]] = None,
        **kwargs,
    ):
        pass

    async def __call__(self, *args, **kwargs):
        pass


class DataFetcher:
    def __init__(self, data_class: type):
        self.data_class = data_class

    async def fetch(self, *args, **kwargs) -> Any:
        raise NotImplementedError


class WebSocketAdapter(GenericAdapter):
    """
    A WebSocket adapter that handles stateful communication with a data class instance.

    Attributes:
        class_def (type): The class of the data object to be instantiated.
        events (dict): A mapping of event names to the corresponding method names in the data class.
        data_fetcher (DataFetcher, optional): A data fetcher object to retrieve data from a data store.
                                               Defaults to None, in which case a new instance of the data_class is used.
        class_instance (Any): The instance of the class_def to be used in stateful communication.
    """

    def __init__(
        self,
        data_class: type,
        events: WebSocketEvents,
        data_fetcher: Optional[DataFetcher] = None,
    ):
        self.data_class: Type = data_class
        self.events: WebSocketEvents = events
        self.data_fetcher: Optional[DataFetcher] = data_fetcher
        self.class_instance: Any = None
        self.connections: set = set()

    async def sleep(self, time: float = 0.2):
        await sleep(time)

    async def send(self, websocket: WebSocket, response: dict):
        await websocket.send_json(response)

    async def connect(self, websocket: WebSocket):
        # Accept the WebSocket connection.
        await websocket.accept()

    async def on_connect(self, *args, websocket: WebSocket, **kwargs):
        """
        Callback function called on WebSocket connection.

        Args:
            websocket (WebSocket): The WebSocket instance.
        """
        await self.connect(websocket)

        if self.events.connect_events:
            await asyncio.wait(
                [
                    asyncio.create_task(
                        on_connect_handler(self.class_instance, websocket)
                    )
                    for on_connect_handler_list in self.events.connect_events.values()
                    for on_connect_handler in on_connect_handler_list
                ]
            )

        # Send an "initialize" event with the initial state of the data object.
        # response = {"event": "initialize", "data": self.class_instance.to_dict()}
        # await self.send(websocket, response)

    async def disconnect(self, websocket: WebSocket):
        # Close the WebSocket connection.
        await websocket.close()

    async def on_disconnect(
        self, *args, websocket: WebSocket, message: Optional[MESSAGE], **kwargs
    ):
        """
        Callback function called on WebSocket disconnection.

        Args:
            websocket (WebSocket): The WebSocket instance.
        """
        # Call the `on_disconnect` handlers of the data object, if it exists.
        if self.events.disconnect_events:
            await asyncio.wait(
                [
                    asyncio.create_task(
                        on_disconnect_handler(self.class_instance, websocket, message)
                    )
                    for on_disconnect_handler_list in self.events.disconnect_events.values()
                    for on_disconnect_handler in on_disconnect_handler_list
                ]
            )
        # await self.disconnect(websocket)

    async def receive(self, websocket: WebSocket) -> MESSAGE:
        # Receive the WebSocket message.
        message = await websocket.receive()
        try:
            message = message["text"]
        except:
            message = message["bytes"]

        if isinstance(message, bytes):
            message = message.decode("utf-8")
            try:
                message = json.loads(
                    message
                )  # parse bytes decoded message if its a json
            except JSONDecodeError:
                pass
        elif isinstance(message, str):
            try:
                message = json.loads(message)  # parse text message if its a json
            except JSONDecodeError:
                pass
        return message

    async def on_receive(self, *args, websocket: WebSocket, message: MESSAGE, **kwargs):
        """
        Callback function called on receiving a message over the WebSocket.

        Args:
            websocket (WebSocket): The WebSocket instance.
            data (dict): The message data, with an "event" key indicating the event name and any additional parameters.
        """

        if isinstance(message, dict):
            if "data" in message and not "event" in message:
                raise KeyError(
                    f"{{'data': {message['data']}}} provided without any 'event'"
                )

            if "event" in message:
                if message["event"] in self.events.receive_events:
                    # Get the event name from the received data and corresponding event_handlers from event manager.
                    # If an event handler exists for the given event in data, call the corresponding event_handler
                    # methods passing the class_instance in place of self in event handler
                    await asyncio.wait(
                        [
                            asyncio.create_task(
                                on_receive_handler(
                                    self.class_instance, websocket, message
                                )
                            )
                            for on_receive_handler in self.events.receive_events[
                                message["event"]
                            ]
                        ]
                    )
                    # Component data classes can have any methods decorated
                    # eg: event_handler = EventManager()
                    # with EvenManager instance @event_handler.on
                    #
                    # @event_handler.on_receive("some_event")
                    # def some_method(self, websocket, data): <-- here in place of 'self' we pass self.class_instance
                    # # Send an "update" event with the updated state of the data object.
                    # response = {
                    #     "event": "update",
                    #     "data": self.class_instance.to_dict(),
                    # }
                    # await self.sleep()
                    # await self.send(websocket, response)

    async def on_relay(self, *args, websocket, message, **kwargs):
        if isinstance(message, dict):
            if "data" in message and not "event" in message:
                raise KeyError(
                    f"{message['data']} key provided without any 'event' key"
                )

            if "event" in message:
                if message["event"] in self.events.relay_events:
                    await asyncio.wait(
                        [
                            asyncio.create_task(
                                on_relay_handler(
                                    self.class_instance, websocket, message
                                )
                            )
                            for on_relay_handler in self.events.relay_events[
                                message["event"]
                            ]
                        ]
                    )

                    await self.sleep()

    async def __call__(self, *args, **kwargs):
        # Instantiate the data object based on whether a data fetcher object is provided.
        if self.class_instance is None:
            # to make sure that even if the socket keeps reconnecting database connections are
            # continuously open
            if self.data_fetcher is None:
                self.class_instance = self.data_class(*args, **kwargs)
            else:
                self.class_instance = await self.data_fetcher.fetch(
                    self.data_class, *args, **kwargs
                )


class WebSocketClientHandler(object):
    def __init__(self, adapters: dict[str, GenericAdapter]):
        self.adapters: dict[str, GenericAdapter] = adapters
        self.all_connections: defaultdict = defaultdict(set)

    async def __call__(self, websocket: WebSocket, adapter_name: str, *args, **kwargs):
        adapter = self.adapters.get(adapter_name, None)
        message = None
        if adapter is None:
            await websocket.close()
            return
        else:
            if websocket not in adapter.connections:
                # await websocket.accept()
                adapter.connections.add(websocket)
                self.all_connections[adapter_name].add(websocket)

            try:
                await adapter.on_connect(websocket=websocket)
                await adapter(*args, **kwargs)
                while True:
                    message = await adapter.receive(websocket)
                    on_receive_task = create_task(
                        adapter.on_receive(websocket=websocket, message=message)
                    )
                    on_relay_task = create_task(
                        adapter.on_relay(websocket=websocket, message=message)
                    )
                    await gather(on_receive_task, on_relay_task)
            except Exception as e:
                if websocket in adapter.connections:
                    adapter.connections.discard(websocket)
                    self.all_connections[adapter_name].discard(websocket)

                await adapter.on_disconnect(
                    *args, websocket=websocket, message=message, **kwargs
                )


class EdgeDBFetcher(DataFetcher):
    """
    A data fetcher that retrieves data from an EdgeDB database.

    Attributes:
        dsn (str): The DSN of the EdgeDB database to connect to.
    """

    def __init__(self, dsn: str):
        self.dsn = dsn

    async def fetch(self, data_class, **kwargs):
        """
        Fetches an instance of the specified data class from the EdgeDB database.

        Args:
            data_class_name (str): The name of the data class.
            **kwargs: Additional keyword arguments.

        Returns:
            Any: An instance of the specified data class.

        """
        return data_class()
        # async with edgedb.async_connect(dsn=self.dsn) as conn:
        #     query = f"SELECT {data_class_name} {{@__computed__: true}};"
        #     result = await conn.query_single(query)
        #     return dataclasses.replace(result, **kwargs)


"""
usage 

app = Starlette()

class MyAdapter(WebSocketAdapter):
    ...

adapter = MyAdapter()
websocket_endpoint = WebSocketEndpoint(app, "/ws", adapter)

@app.websocket_route("/ws")
async def my_handler(websocket: WebSocket):
    await websocket_endpoint(websocket)
"""
