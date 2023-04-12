# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import json
from abc import ABC, abstractmethod
from asyncio import Queue, create_task, gather, iscoroutinefunction, sleep
from collections import defaultdict
from functools import partial, wraps
from json.decoder import JSONDecodeError
from types import AsyncGeneratorType
from typing import Any, Callable, Dict, List, Optional, Type, Union
from warnings import warn

from starlette.websockets import Message, WebSocket, WebSocketDisconnect

DATA = Optional[Union[Message, str]]
CALLABLE = Callable[..., Any]


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
    async def on_disconnect(self, *args, websocket: WebSocket, data: DATA, **kwargs):
        pass

    @abstractmethod
    async def receive(self, websocket: WebSocket):
        pass

    @abstractmethod
    async def on_receive(self, *args, websocket: WebSocket, data: DATA, **kwargs):
        pass

    @abstractmethod
    async def on_relay(
        self,
        *args,
        websocket: WebSocket,
        data: DATA,
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


class EventsManager(object):
    def __init__(self, registered_events: list[str]):
        # events registered in registered_events list will be allowed to be added
        self.__registered_events: list[str] = registered_events

        # __original_method_registry keeps the track of the original methods that are decorated and are going to be
        # added to the __events_when_activity and if the method has been already added to it then it won't
        # be added again as its the same method for the same event_name
        self.__original_method_registry: defaultdict = defaultdict(
            partial(defaultdict, list)
        )
        self.__events_with_activity: defaultdict = defaultdict(
            partial(defaultdict, list)
        )

        # this _event_queue is used to signal that the
        self._event_queue: Queue = Queue()

        # now adding the queue to the relay event so that anything that is pushed can be

    async def __aiter__(self):
        for activity in self.__events_with_activity:
            for event_name in self.__events_with_activity[activity]:
                yield activity, event_name, self.__events_with_activity[activity][
                    event_name
                ]

    def on(self, activity: str, event_name: str):
        def callback_decorator(method: CALLABLE) -> CALLABLE:
            if event_name not in self.__registered_events:
                raise ValueError(
                    f"event '{event_name}' is not in the registered_events list"
                )

            if not callable(method):
                raise ValueError(f"method {method!r} must be a callable")

            if method not in self.__original_method_registry[activity][event_name]:
                self.__original_method_registry[activity][event_name].append(method)

                @wraps(method)
                async def event_callback(*args, **kwargs):
                    if iscoroutinefunction(method):
                        return await method(*args, **kwargs)
                    return method(*args, **kwargs)

                self.__events_with_activity[activity][event_name].append(event_callback)
            else:
                warn(
                    message=f"{activity} already added event {event_name} to method {method!r}"
                )
            return method

        return callback_decorator

    async def _event_callbacks(self, event_name: str):
        for activity in self.__events_with_activity:
            if event_name in self.__events_with_activity[activity]:
                for event_callback in self.__events_with_activity[activity][event_name]:
                    yield event_callback
        else:
            yield

    def __getitem__(self, event_name: str) -> AsyncGeneratorType:
        # returns an async iterator of the event handlers
        # which can be used as follows:
        # event_mgr = EventManager([])
        # async for callback in event_mgr[event_name]:
        #         yield callback
        return self._event_callbacks(event_name)

    def __contains__(self, event_name):
        for activity in self.__events_with_activity:
            if event_name in self.__events_with_activity[activity]:
                return True
        return False

    @property
    def registered_events(self):
        return self.__registered_events

    def register_event(self, event_name):
        if event_name in self.__registered_events:
            raise ValueError(
                f"event {event_name} already added to the registered_events list"
            )
        self.__registered_events.append(event_name)

    def add_event_with_activity(
        self, activity: str, event_name_or_method: Union[str, CALLABLE]
    ) -> CALLABLE:
        method = None
        event_name = None
        if callable(event_name_or_method):
            event_name = event_name_or_method.__name__
            method = event_name_or_method
        else:
            event_name = event_name_or_method

        assert isinstance(event_name, str)

        if event_name not in self.__registered_events:
            self.__registered_events.append(event_name)

        if method:
            return self.on(activity, event_name)(method)
        return self.on(activity, event_name)

    def events_with_activity(self, activity: str) -> Dict[str, List[Callable]]:
        return self.__events_with_activity[activity]

    def on_relay(self, event_name_or_method: Union[str, CALLABLE]) -> CALLABLE:
        return self.add_event_with_activity("relay", event_name_or_method)

    @property
    def relay_events(self) -> Dict[str, List[Callable]]:
        return self.events_with_activity("relay")

    def on_receive(self, event_name_or_method: Union[str, CALLABLE]) -> CALLABLE:
        return self.add_event_with_activity("receive", event_name_or_method)

    @property
    def receive_events(self) -> Dict[str, List[Callable]]:
        return self.events_with_activity("receive")

    def on_connect(self, method: CALLABLE) -> CALLABLE:
        return self.add_event_with_activity("connect", method)

    @property
    def connect_events(self) -> Dict[str, List[Callable]]:
        return self.events_with_activity("connect")

    def on_disconnect(self, method: CALLABLE) -> CALLABLE:
        return self.add_event_with_activity("disconnect", method)

    @property
    def disconnect_events(self) -> Dict[str, List[Callable]]:
        return self.events_with_activity("disconnect")


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
        class_def: Type,
        events: EventsManager,
        data_fetcher: Optional[DataFetcher] = None,
    ):
        self.class_def: Type = class_def
        self.events: EventsManager = events
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

        # # Instantiate the data object based on whether a data fetcher object is provided.
        # if self.class_instance is None:
        #     # to make sure that even if the socket keeps reconnecting database connections are
        #     # continuously open
        #     if self.data_fetcher is None:
        #         self.class_instance = self.class_def(*args, **kwargs)
        #     else:
        #         self.class_instance = await self.data_fetcher.fetch(
        #             self.class_def, *args, **kwargs
        #         )

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
        response = {"event": "initialize", "data": self.class_instance.to_dict()}
        await self.send(websocket, response)

    async def disconnect(self, websocket: WebSocket):
        # Close the WebSocket connection.
        await websocket.close()

    async def on_disconnect(self, *args, websocket: WebSocket, data: DATA, **kwargs):
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
                        on_disconnect_handler(self.class_instance, websocket, data)
                    )
                    for on_disconnect_handler_list in self.events.disconnect_events.values()
                    for on_disconnect_handler in on_disconnect_handler_list
                ]
            )
        # await self.disconnect(websocket)

    async def receive(self, websocket: WebSocket):
        # Receive the WebSocket data.
        data = await websocket.receive()
        try:
            data = data["text"]
        except:
            data = data["bytes"]

        if isinstance(data, bytes):
            data = data.decode("utf-8")
            try:
                data = json.loads(data)  # parse bytes decoded data if its a json
            except JSONDecodeError:
                pass
        elif isinstance(data, str):
            try:
                data = json.loads(data)  # parse text data if its a json
            except JSONDecodeError:
                pass
        return data

    async def on_receive(self, *args, websocket: WebSocket, data: DATA, **kwargs):
        """
        Callback function called on receiving a message over the WebSocket.

        Args:
            websocket (WebSocket): The WebSocket instance.
            data (dict): The message data, with an "event" key indicating the event name and any additional parameters.
        """

        if isinstance(data, dict):
            if "data" in data and not "event" in data:
                raise KeyError(
                    f"{{'data': {data['data']}}} provided without any 'event'"
                )

            if "event" in data:
                if data["event"] in self.events.receive_events:
                    # Get the event name from the received data and corresponding event_handlers from event manager.
                    # If an event handler exists for the given event in data, call the corresponding event_handler
                    # methods passing the class_instance in place of self in event handler
                    async for on_receive_handler in self.events.receive_events[
                        data["event"]
                    ]:
                        # Component data classes can have any methods decorated
                        # eg: event_handler = EventManager()
                        # with EvenManager instance @event_handler.on
                        #
                        # @event_handler.on("some_event")
                        # def some_method(self, websocket, data): <-- here in place of 'self' we pass self.class_instance
                        #     # handle the data here now
                        await on_receive_handler(self.class_instance, websocket, data)
        # Send an "update" event with the updated state of the data object.
        response = {"event": "update", "data": self.class_instance.to_dict()}
        await self.sleep()
        await self.send(websocket, response)

    async def on_relay(self, *args, websocket, data, **kwargs):
        if isinstance(data, dict):
            if "data" in data and not "event" in data:
                raise KeyError(f"{data['data']} key provided without any 'event' key")

            if "event" in data:
                if data["event"] in self.events.relay_events:
                    async for on_relay_handler in self.events.relay_events[
                        data["event"]
                    ]:
                        await on_relay_handler(
                            self.class_instance, websocket, data, self.connections
                        )

        def get_enqueued_events():
            # need to add event queue.get() to receive server pushed notifications that needs to be sent
            # to the clients
            ...

        await self.sleep()

    async def __call__(self, *args, **kwargs):
        # Instantiate the data object based on whether a data fetcher object is provided.
        if self.class_instance is None:
            # to make sure that even if the socket keeps reconnecting database connections are
            # continuously open
            if self.data_fetcher is None:
                self.class_instance = self.class_def(*args, **kwargs)
            else:
                self.class_instance = await self.data_fetcher.fetch(
                    self.class_def, *args, **kwargs
                )


class WebSocketClientHandler(object):
    def __init__(self, adapters: dict[str, GenericAdapter]):
        self.adapters: dict[str, GenericAdapter] = adapters
        self.all_connections: defaultdict = defaultdict(set)

    async def __call__(self, websocket: WebSocket, adapter_name: str, *args, **kwargs):
        adapter = self.adapters.get(adapter_name, None)
        data = None
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
                    data = await adapter.receive(websocket)
                    on_receive_task = create_task(
                        adapter.on_receive(
                            websocket=websocket,
                            data=data,
                        )
                    )
                    on_relay_task = create_task(
                        adapter.on_relay(websocket=websocket, data=data)
                    )
                    await gather(on_receive_task, on_relay_task)
            except Exception as e:
                if websocket in adapter.connections:
                    adapter.connections.discard(websocket)
                    self.all_connections[adapter_name].discard(websocket)

                await adapter.on_disconnect(
                    *args, websocket=websocket, data=data, **kwargs
                )


class EdgeDBFetcher(DataFetcher):
    """
    A data fetcher that retrieves data from an EdgeDB database.

    Attributes:
        dsn (str): The DSN of the EdgeDB database to connect to.
    """

    def __init__(self, dsn: str):
        self.dsn = dsn

    async def fetch(self, data_class: Type, **kwargs) -> Any:
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

if __name__ == "__main__":
    import asyncio

    click_events = EventsManager(registered_events=["increment", "decrement"])

    # class Counter:
    #     def __init__(self):
    #         self.count = 0

    #     def increment(self):
    #         self.count += 1

    #     def decrement(self):
    #         self.count -= 1

    #     def to_dict(self) -> Dict[str, Any]:
    #         return {
    #             "count": self.count,
    #         }

    class ClickCounter:
        def __init__(self):
            self.clicks = 0

        @click_events.on("increment")
        def increment(self, count):
            self.clicks += count
            return self.clicks

        def to_dict(self) -> Dict[str, Any]:
            return {
                "clicks": self.clicks,
            }

    c = ClickCounter()

    async def main():
        async for callback in click_events("increment"):
            print(await callback(c, count=3))

    asyncio.run(main())

    c.increment(3)
    print(c.to_dict())

# counter_adapter = GenericAdapter(
#     Counter,
#     events={
#         "increment": "increment",
#         "decrement": "decrement",
#     }
# )

# click_counter_adapter = GenericAdapter(
#     ClickCounter,
#     events={
#         "increment": "increment",
#     }
# )

# ADAPTERS = {
#     "counter": counter_adapter,
#     "click-counter": click_counter_adapter,
# }


# @app.websocket("/ws/{name}")
# async def websocket_endpoint(name: str, websocket: WebSocket):
#     adapter = ADAPTERS.get(name)
#     if adapter is None:
#         await websocket.close()
#         return

#     await adapter.on_connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_json()
#             await adapter.on_receive(websocket, data)
#     except WebSocketDisconnect:
#         await adapter.on_disconnect(websocket)
