from typing import Optional
from .Settlement import Settlement


class Intersection:
    def __init__(self) -> None:
        self.settlement: Optional[Settlement] = None
