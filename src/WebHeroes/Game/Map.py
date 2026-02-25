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
        for field_type in distributed_field_types:
            fields.append(Field(field_type))

        self.initial_field = fields[0]
