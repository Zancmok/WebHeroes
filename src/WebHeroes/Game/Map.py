from typing import Optional
import random
from Prototype import FieldPrototype, SettingsPrototype, RoadPrototype
from .Field import Field
from .Intersection import Intersection
from .Connection import Connection
from .Player import Player
from .Road import Road


class Map:
    def _generate_tile_distribution(self, field_types: list[FieldPrototype], actual_field_count: int) -> list[FieldPrototype]:
        fields: list[FieldPrototype] = []
        field_ranges: dict[range, FieldPrototype] = {}

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

    @staticmethod
    def _to_axial(col: int, row: int) -> tuple[int, int]:
        #  row & 1 == row % 2 but works with negative numbers
        parity: int = row & 1
        q: int = col - (row - parity) // 2
        r: int = row

        return q, r

    def __init__(self, field_types: list[FieldPrototype], settings_type: SettingsPrototype) -> None:
        self.initial_field: Field

        self.outer_bound_field_type: FieldPrototype
        for field in field_types:
            if field.name == "outer-bound":
                self.outer_bound_field_type = field

        self.field_map: list[list[Field]] = []

        # map_size ** 2 - 6 = map_size + 2 * sum(from i = 3 to i = map_size - 1 : i)
        map_tiles: list[FieldPrototype] = self._generate_tile_distribution(field_types, settings_type.map_size ** 2 - 6)

        inner_map_width: int = settings_type.map_size
        inner_map_height: int = 1 + 2 * (settings_type.map_size - 3)

        DEEP_SEA_BORDER_SIZE: int = 4
        outer_map_width: int = inner_map_width + DEEP_SEA_BORDER_SIZE
        outer_map_height: int = inner_map_height + DEEP_SEA_BORDER_SIZE

        # Generate map

        # Top row
        for row in range(DEEP_SEA_BORDER_SIZE):
            new_row: list[Field] = []

            for col in range(outer_map_width):
                new_row.append(Field(
                    *Map._to_axial(col, row),
                    field_type=self.outer_bound_field_type
                ))

            self.field_map.append(new_row)

        # Middle row
        actual_tiles_appended: int = 0
        for row in range(inner_map_height):
            new_row: list[Field] = []

            sea_tiles_in_row: int = abs(row - inner_map_height // 2)

            for _ in range((DEEP_SEA_BORDER_SIZE // 2) + (sea_tiles_in_row // 2)):
                new_row.append(Field(
                    *Map._to_axial(len(new_row), row + DEEP_SEA_BORDER_SIZE),
                    field_type=self.outer_bound_field_type
                ))

            for _ in range(inner_map_width - sea_tiles_in_row):
                new_row.append(Field(
                    *Map._to_axial(len(new_row), row + DEEP_SEA_BORDER_SIZE),
                    field_type=map_tiles[actual_tiles_appended]
                ))

                actual_tiles_appended += 1

            for _ in range((DEEP_SEA_BORDER_SIZE // 2) + (sea_tiles_in_row // 2) + (sea_tiles_in_row % 2)):
                new_row.append(Field(
                    *Map._to_axial(len(new_row), row + DEEP_SEA_BORDER_SIZE),
                    field_type=self.outer_bound_field_type
                ))

            self.field_map.append(new_row)

        # Bottom row
        for row in range(DEEP_SEA_BORDER_SIZE):
            new_row: list[Field] = []

            for col in range(outer_map_width):
                new_row.append(Field(
                    *Map._to_axial(col, row + DEEP_SEA_BORDER_SIZE + inner_map_height),
                    field_type=self.outer_bound_field_type
                ))
            
            self.field_map.append(new_row)

        self.fields: dict[tuple[int, int], Field] = {}
        for row in self.field_map:
            for field in row:
                self.fields[(field.q, field.r)] = field

                if field.field_type.resource:
                    field.assigned_number = random.randint(1, 6) + random.randint(1, 6)

        # Calculate neighbours + connections
        axial_direction_vectors: list[tuple[int, int]] = [
            (+1, 0), (+1, -1), (0, -1),
            (-1, 0), (-1, +1), (0, +1)
        ]

        self.intersections: dict[frozenset[tuple[int, int]], Intersection] = {}
        self.connections: dict[frozenset[tuple[int, int]], Connection] = {}
        for field_cords in self.fields:
            first_field: Optional[Field] = None
            previous_field: Optional[Field] = None
            for direction_vector in axial_direction_vectors:
                directed_field: Optional[Field] = self.fields.get((field_cords[0] + direction_vector[0], field_cords[1] + direction_vector[1]))

                if not directed_field:
                    continue

                new_connection_set: frozenset[tuple[int, int]] = frozenset({
                    field_cords,
                    (directed_field.q, directed_field.r)
                })
                if new_connection_set not in self.connections:
                    self.connections[new_connection_set] = Connection()

                if previous_field:
                    new_set: frozenset[tuple[int, int]] = frozenset({
                        field_cords,
                        (directed_field.q, directed_field.r),
                        (previous_field.q, previous_field.r)
                    })

                    if new_set not in self.intersections:
                        self.intersections[new_set] = Intersection()
                else:
                    first_field = directed_field

                previous_field = directed_field

            new_set: frozenset[tuple[int, int]] = frozenset({
                field_cords,
                (first_field.q, first_field.r),
                (previous_field.q, previous_field.r)
            })

            if new_set not in self.intersections:
                self.intersections[new_set] = Intersection()

    def build_road(self, location: frozenset[tuple[int, int]], player: Player, road_prototype: RoadPrototype) -> bool:
        connection: Optional[Connection] = self.connections.get(location)

        if not connection or connection.road:
            return False
        connection: Connection

        neighboring_intersections: list[Intersection] = [
            intersection for fields_set, intersection in self.intersections.items()
            if location.issubset(fields_set)
        ]

        if not neighboring_intersections:
            return False

        can_place: bool = any(
            (intersection.settlement and intersection.settlement.owner == player)
            or any(
                conn.road and conn.road.owner == player
                for conn_fields, conn in self.connections.items()
                if conn_fields.issubset(fields_set) and conn_fields != location
            )
            for fields_set, intersection in self.intersections.items()
            if location.issubset(fields_set)
        )
        if not can_place:
            return False

        connection.road = Road(
            road_type=road_prototype,
            owner=player
        )

        return True
