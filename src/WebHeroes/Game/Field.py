from typing import Optional
from Prototype import FieldType


class Field:
    def __init__(self, field_type: FieldType, assigned_number: Optional[int] = None) -> None:
        self.field_type: FieldType = field_type
        self.assigned_number: Optional[int] = assigned_number
