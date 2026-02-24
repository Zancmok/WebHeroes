from typing import Optional
from Prototype import FieldType
from .Intersection import Intersection


class Field:
    def __init__(self, field_type: FieldType, assigned_number: Optional[int] = None) -> None:
        self.field_type: FieldType = field_type
        self.assigned_number: Optional[int] = assigned_number

        self.up_left_int: Intersection
        self.up_middle_int: Intersection
        self.up_right_int: Intersection
        self.down_left_int: Intersection
        self.down_middle_int: Intersection
        self.down_right_int: Intersection
