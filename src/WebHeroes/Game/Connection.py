from typing import Optional
from .Road import Road


class Connection:
    def __init__(self) -> None:
        self.road: Optional[Road] = None
