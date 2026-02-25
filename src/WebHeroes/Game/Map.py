from typing import Optional
import random
from Prototype import FieldType, SettingsType
from .Field import Field
from .Intersection import Intersection
from .Connection import Connection


type FieldReference = tuple[
    Intersection,
    Intersection,
    Intersection,
    Intersection,
    Intersection,
    Intersection
]

type IntersectionReference = tuple[
    tuple[Field],
    tuple[Connection, Connection]
] | tuple[
    tuple[Field, Field] | tuple[Field, Field, Field],
    tuple[Connection, Connection, Connection]
]

type ConnectionReference = tuple[
    Intersection,
    Intersection
]

class Map:
    def _generate_tile_distribution(self, field_types: list[FieldType]) -> list[FieldType]:
            fields: list[FieldType] = []
            field_ranges: dict[range, FieldType] = {}

            total_weight: int = 0
            for field_type in field_types:
                for _ in range(field_type.minimum_amount):
                    fields.append(field_type)

                field_ranges[range(total_weight, total_weight + field_type.weight)] = field_type
                total_weight += field_type.weight

            for _ in range(len(fields), self._tile_amount):
                random_num: int = random.randint(0, total_weight - 1)

                for v in field_ranges:
                    if random_num in v:
                        fields.append(field_ranges[v])
                        break

            random.shuffle(fields)

            return fields

    def __init__(self, field_types: list[FieldType], settings_type: SettingsType) -> None:
        self.initial_field: Field
        self._field_references: dict[Field, FieldReference] = {}
        self._intersection_references: dict[Intersection, IntersectionReference] = {}
        self._connection_references: dict[Connection, ConnectionReference] = {}
        self._tile_amount: int = settings_type.map_size + 2 * sum(range(3, settings_type.map_size))

        distributed_field_types: list[FieldType] = self._generate_tile_distribution(field_types)

        fields: list[Field] = []
        intersections: list[Intersection] = []
        connections: list[Connection] = []

        shrinking: bool = False
        curr_row_size: int = 3
        for i in range(settings_type.map_size):
            for j in range(curr_row_size):
                new_field: Field = Field(distributed_field_types[len(fields)])

                if i == 0 and j == 0:
                    self.initial_field = new_field

                bottom_middle_intersection: Intersection = Intersection()
                intersections.append(bottom_middle_intersection)
                bottom_right_intersection: Intersection = Intersection()
                intersections.append(bottom_right_intersection)

                bottom_left_intersection: Intersection
                
                if j == 0:
                    bottom_left_intersection = Intersection()

                    intersections.append(bottom_left_intersection)
                else:
                    bottom_left_intersection = self.get_field_data(fields[-1])["bottom-left"]

                top_left_intersection: Intersection
                if j == 0 and not shrinking:
                    top_left_intersection = Intersection()

                    intersections.append(top_left_intersection)

                top_middle_intersection: Intersection
                if i == 0:
                    top_middle_intersection = Intersection()

                    intersections.append(top_middle_intersection)
                else:
                    top_middle_intersection = self.get_field_data(fields[-1])["top-middle"]

                top_right_intersection: Intersection
                if i == 0 or (j == curr_row_size - 1 and not shrinking):
                    top_right_intersection = Intersection()

                    intersections.append(top_right_intersection)
                else:
                    top_right_intersection = self.get_field_data(fields[-1])["top-right"]

                self._field_references[new_field] = (
                    top_left_intersection,
                    top_middle_intersection,
                    top_right_intersection,
                    bottom_left_intersection,
                    bottom_middle_intersection,
                    bottom_right_intersection
                )
                fields.append(new_field)

            if curr_row_size == settings_type.map_size:
                shrinking = True

            if shrinking:
                curr_row_size -= 1
            else:
                curr_row_size += 1

        print(flush=True)
        print(len(fields), len(intersections), len(self._field_references), flush=True)
        print(self._field_references, flush=True)

        self.initial_field = fields[0]

    def get_field_data(self, field: Field) -> dict[str, Optional[Intersection]]:
        output: dict[str, Optional[Intersection]] = {
            "top-left": None,
            "top-middle": None,
            "top-right": None,
            "bottom-left": None,
            "bottom-middle": None,
            "bottom-right": None
        }

        data: Optional[FieldReference] = self._field_references.get(field)

        if not data:
            return output
        
        output["top-left"] = data[0]
        output["top-middle"] = data[1]
        output["top-right"] = data[2]
        output["bottom-left"] = data[3]
        output["bottom-middle"] = data[4]
        output["bottom-right"] = data[5]

        return output


    """
    def get_intersection_data(self, intersection: Intersection) -> Optional[IntersectionReference]:
        return self._intersection_references.get(intersection)
    
    def get_connection_data(self, connection: Connection) -> Optional[ConnectionReference]:
        return self._connection_references.get(connection)
    """
