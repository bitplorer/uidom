# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import typing
from dataclasses import dataclass


class BaseState(dict):
    """
    Base States
    """


@dataclass
class BaseDBManager(object):
    database: typing.Any
    password: typing.Any
    table: typing.Any

    async def post(self, *args, **kwargs: BaseState):
        ...

    async def put(self, *args, **kwargs: BaseState):
        ...

    async def delete(self, *args, **kwargs: BaseState):
        ...

    async def get(self, *args, **kwargs: BaseState):
        ...


@dataclass
class BaseStateManager(object):
    state_names = ["id", "name"]  # just a placeholder
    state_db: BaseDBManager

    async def client_state_handler(self, **client_states: BaseState):
        if not all(state in client_states for state in self.state_names):
            return

        if not self.state_db.get(self.state_names, **client_states):
            return

        # updating client_states' value for state_names
        client_states = await self.update_states(self.state_names, **client_states)

        # updating state_db's value for state_names
        return await self.state_db.put(self.state_names, **client_states)

    async def server_state_handler(self, **server_states: BaseState):
        if not all(state in server_states for state in self.state_names):
            server_states = await self.create_states(self.state_names, **server_states)

        if self.state_db.get(self.state_names, **server_states):
            return server_states

        return await self.state_db.post(self.state_names, **server_states)

    async def create_states(self, state_names, **states):  # noqa
        return states

    async def update_states(self, state_names,  **states):  # noqa
        return states


@dataclass
class BaseEventManager(object):
    event_name = "events"
    states_manager: BaseStateManager
    events_db: BaseDBManager

    async def dispatch_event(self, **states):  # noqa
        return states

    # async def client_event_manager(self, **client_states: BaseState):
    #     client_states = await self.states_manager.client_state_handler(**client_states)
    #     if not client_states or self.event_name not in client_states:
    #         return client_states
    #     client_states = await self.events_store.get(self.event_name, **client_states)
    #     async for client_event in self.events_store.get(self.event_name, **client_states):
    #         await self.dispatch_event(**client_event)

    async def server_event_manager(self, **current_data: BaseState):
        ...
