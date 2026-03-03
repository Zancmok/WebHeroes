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
    def _generate_tile_distribution(self, field_types: list[FieldType], actual_field_count: int) -> list[FieldType]:
        fields: list[FieldType] = []
        field_ranges: dict[range, FieldType] = {}

        total_weight: int = 0
        for field_type in field_types:
            for _ in range(field_type.minimum_amount):
                fields.append(field_type)

            if field_type is self.outer_bound_field_type:
                field_ranges[range(-1, 0)] = field_type

                continue

            field_ranges[range(total_weight, total_weight + field_type.weight)] = field_type
            total_weight += field_type.weight

        for _ in range(len(fields), actual_field_count):
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

        self.outer_bound_field_type: FieldType
        for field in field_types:
            if field.name == "outer-bound":
                self.outer_bound_field_type = field

        self.fields: list[list[Field]] = []

        # map_size ** 2 - 6 = map_size + 2 * sum(from i = 3 to i = map_size - 1 : i)
        map_tiles: list[FieldType] = self._generate_tile_distribution(field_types, settings_type.map_size ** 2 - 6)

        inner_map_width: int = settings_type.map_size
        inner_map_height: int = 1 + 2 * (settings_type.map_size - 3)

        DEEP_SEA_BORDER_SIZE: int = 4
        outer_map_width: int = inner_map_width + DEEP_SEA_BORDER_SIZE
        outer_map_height: int = inner_map_height + DEEP_SEA_BORDER_SIZE

        # Generate map

        # Top row
        for _ in range(DEEP_SEA_BORDER_SIZE):
            new_row: list[Field] = []

            for _ in range(outer_map_width):
                new_row.append(Field(self.outer_bound_field_type))

            self.fields.append(new_row)

        # Middle row
        actual_tiles_appended: int = 0
        for i in range(inner_map_height):
            new_row: list[Field] = []

            sea_tiles_in_row: int = abs(i - inner_map_height // 2)

            for _ in range((DEEP_SEA_BORDER_SIZE // 2) + (sea_tiles_in_row // 2)):
                new_row.append(Field(self.outer_bound_field_type))

            for _ in range(inner_map_width - sea_tiles_in_row):
                new_row.append(Field(map_tiles[actual_tiles_appended]))

                actual_tiles_appended += 1

            for _ in range((DEEP_SEA_BORDER_SIZE // 2) + (sea_tiles_in_row // 2) + (sea_tiles_in_row % 2)):
                new_row.append(Field(self.outer_bound_field_type))

            self.fields.append(new_row)

        # Bottom row
        for _ in range(DEEP_SEA_BORDER_SIZE):
            new_row: list[Field] = []

            for _ in range(outer_map_width):
                new_row.append(Field(self.outer_bound_field_type))

            self.fields.append(new_row)
