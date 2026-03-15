from typing import Optional
from Prototype import FieldPrototype


class Field:
    def __init__(self, q: int, r: int, field_type: FieldPrototype, assigned_number: Optional[int] = None) -> None:
        self.q: int = q
        self.r: int = r
        self.field_type: FieldPrototype = field_type
        self.assigned_number: Optional[int] = assigned_number
