# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from asyncio import Queue, iscoroutinefunction
from collections import defaultdict
from functools import partial, wraps
from typing import Any, Callable, Dict, List, Union
from warnings import warn

__all__ = ["BaseEventManager", "WebSocketEvents", "HtmxEvents"]

CALLABLE = Callable[..., Any]


class BaseEventManager(object):
    def __init__(self):
        # events registered in registered_events list will be allowed to be added
        self.__registered_events: list[str] = []

        # __original_method_registry keeps the track of the original methods that are decorated and are going to be
        # added to the __events_with_activity and if the method has been already added to it then it won't
        # be added again as its the same method for the same event_name
        self.__original_method_registry: defaultdict = defaultdict(
            partial(defaultdict, list)
        )
        self.__events_with_activities: defaultdict = defaultdict(
            partial(defaultdict, list)
        )

        # this _event_queue can be used to signal for any purpose
        self._event_queue: Queue = Queue()

        # now adding the queue to the relay event so that anything that is pushed can be

    async def __aiter__(self):
        for activity in self.__events_with_activities:
            for event_name in self.__events_with_activities[activity]:
                yield activity, event_name, self.__events_with_activities[activity][
                    event_name
                ]

    def _on(self, activity: str, event_name: str):
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

                self.__events_with_activities[activity][event_name].append(
                    event_callback
                )
            else:
                warn(
                    message=f"{activity} already added event {event_name} to method {method!r}"
                )
            return method

        return callback_decorator

    def _event_callbacks(self, event_name: str):
        callbacks = []
        for activity in self.__events_with_activities:
            if event_name in self.__events_with_activities[activity]:
                callbacks.extend(self.__events_with_activities[activity][event_name])

        return callbacks

    def __getitem__(self, event_name: str):
        # returns an async iterator of the event handlers
        # which can be used as follows:
        # event_mgr = EventManager()
        # for callback in event_mgr[event_name]:
        #     yield callback
        return self._event_callbacks(event_name)

    def __contains__(self, event_name):
        for activity in self.__events_with_activities:
            if event_name in self.__events_with_activities[activity]:
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

    @property
    def registered_activities(self) -> Dict[str, Dict[str, List[Callable]]]:
        return self.__events_with_activities

    def _set_event_with_activity(
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
            return self._on(activity, event_name)(method)
        return self._on(activity, event_name)

    def _get_events_with_activity(self, activity: str) -> Dict[str, List[Callable]]:
        return self.registered_activities[activity]

    def set_event(
        self, activity: str, event_name_or_method: Union[str, CALLABLE]
    ) -> CALLABLE:
        return self._set_event_with_activity(activity, event_name_or_method)

    def get_events(self, activity: str) -> Dict[str, List[Callable]]:
        return self._get_events_with_activity(activity)


class WebSocketEvents(BaseEventManager):
    def on_relay(self, event_name_or_method: Union[str, CALLABLE]) -> CALLABLE:
        return self.set_event("relay", event_name_or_method)

    @property
    def relay_events(self) -> Dict[str, List[Callable]]:
        return self.get_events("relay")

    def on_receive(self, event_name_or_method: Union[str, CALLABLE]) -> CALLABLE:
        return self.set_event("receive", event_name_or_method)

    @property
    def receive_events(self) -> Dict[str, List[Callable]]:
        return self.get_events("receive")

    def on_connect(self, method: CALLABLE) -> CALLABLE:
        return self.set_event("connect", method)

    @property
    def connect_events(self) -> Dict[str, List[Callable]]:
        return self.get_events("connect")

    def on_disconnect(self, method: CALLABLE) -> CALLABLE:
        return self.set_event("disconnect", method)

    @property
    def disconnect_events(self) -> Dict[str, List[Callable]]:
        return self.get_events("disconnect")


class HtmxEvents(BaseEventManager):
    def get(self, event: Union[str, Callable]) -> Callable:
        return super().set_event(activity="hx-get", event_name_or_method=event)

    @property
    def get_events(self):
        return super().get_events(activity="hx-get")

    def post(self, event: Union[str, Callable]) -> Callable:
        return super().set_event(activity="hx-post", event_name_or_method=event)

    @property
    def post_events(self):
        return super().get_events(activity="hx-post")

    def put(self, event: Union[str, Callable]) -> Callable:
        return super().set_event(activity="hx-put", event_name_or_method=event)

    @property
    def put_events(self):
        return super().get_events(activity="hx-put")

    def patch(self, event: Union[str, Callable]) -> Callable:
        return super().set_event(activity="hx-patch", event_name_or_method=event)

    @property
    def patch_events(self):
        return super().get_events(activity="hx-patch")

    def delete(self, event: Union[str, Callable]) -> Callable:
        return super().set_event(activity="hx-delete", event_name_or_method=event)

    @property
    def delete_events(self):
        return super().get_events(activity="hx-delete")
