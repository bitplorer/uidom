# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from asyncio import Queue, iscoroutinefunction
from collections import defaultdict
from functools import partial, wraps
from typing import Any, Callable, Dict, List, Union
from warnings import warn

__all__ = ["EventsManager"]

CALLABLE = Callable[..., Any]


class EventsManager(object):
    def __init__(self):
        # events registered in registered_events list will be allowed to be added
        self.__registered_events: list[str] = []

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

    def _event_callbacks(self, event_name: str):
        callbacks = []
        for activity in self.__events_with_activity:
            if event_name in self.__events_with_activity[activity]:
                callbacks.extend(self.__events_with_activity[activity][event_name])

        return callbacks

    def __getitem__(self, event_name: str):
        # returns an async iterator of the event handlers
        # which can be used as follows:
        # event_mgr = EventManager()
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

    def get_events_with_activity(self, activity: str) -> Dict[str, List[Callable]]:
        return self.__events_with_activity[activity]

    def on_relay(self, event_name_or_method: Union[str, CALLABLE]) -> CALLABLE:
        return self.add_event_with_activity("relay", event_name_or_method)

    @property
    def relay_events(self) -> Dict[str, List[Callable]]:
        return self.get_events_with_activity("relay")

    def on_receive(self, event_name_or_method: Union[str, CALLABLE]) -> CALLABLE:
        return self.add_event_with_activity("receive", event_name_or_method)

    @property
    def receive_events(self) -> Dict[str, List[Callable]]:
        return self.get_events_with_activity("receive")

    def on_connect(self, method: CALLABLE) -> CALLABLE:
        return self.add_event_with_activity("connect", method)

    @property
    def connect_events(self) -> Dict[str, List[Callable]]:
        return self.get_events_with_activity("connect")

    def on_disconnect(self, method: CALLABLE) -> CALLABLE:
        return self.add_event_with_activity("disconnect", method)

    @property
    def disconnect_events(self) -> Dict[str, List[Callable]]:
        return self.get_events_with_activity("disconnect")
