from typing import NamedTuple, Sequence

from ._types import ReloadFunc


class WatchPath(NamedTuple):
    path: str
    on_reload: Sequence[ReloadFunc] = ()
