from typing import Optional
from Prototype import FieldType


class Field:
    def __init__(self, q: int, r: int, field_type: FieldType, assigned_number: Optional[int] = None) -> None:
        self.q: int = q
        self.r: int = r
        self.field_type: FieldType = field_type
        self.assigned_number: Optional[int] = assigned_number
