from typing import Optional

from bardapi.models.user_content import UserContent


class BardMapsPoint:
    def __init__(self, input_list: list):
        self._input_list = input_list

        self.geo_position = self._input_list[11]
        self.lat: float = self.geo_position[0]
        self.lng: float = self.geo_position[1]

    @property
    def id(self) -> str:
        return self._input_list[1]

    @property
    def address(self) -> str:
        # '12170 Dornans Rd, Moose, WY 83012, USA'
        return self._input_list[8]

    @property
    def address_short(self) -> str:
        # 'Dornans, 12170 Dornans Rd, Moose'
        return self._input_list[50]

    @property
    def geo_position_rect(self) -> list:
        return self._input_list[12]

    @property
    def rating(self) -> float:
        return self._input_list[13]

    @property
    def rating_count(self) -> int:
        return self._input_list[27]

    @property
    def gmaps_url(self) -> str:
        return self._input_list[14]

    @property
    def website_url(self) -> str:
        return self._input_list[15]

    @property
    def schedule(self) -> dict:
        v = self._input_list[20]
        return {
            "open": v[0],
            "value": v[1],
            "human": v[2],
        }

    @property
    def title(self) -> tuple[str, str]:
        # Albertsons, "en"
        return self._input_list[30]

    def description(self) -> Optional[tuple[str, str]]:
        # ['Gourmet groceries, cheeses & baked goods are available at this casual deli in a resort setting.', 'en']
        return self._input_list[51]

    @property
    def place_type(self) -> str:
        # supermarket
        return self._input_list[49]  # same [31], "en"

    @property
    def images(self) -> list:
        return (
            [{"url": img[0], "author": img[3]} for img in self._input_list[53]]
            if self._input_list[53]
            else []
        )

    def __str__(self) -> str:
        return (
            f"{self.title[0]}, {self.rating}*({self.rating_count}) - {self.place_type}"
        )


class BardMapsRoadSection:
    def __init__(self, input_list: list):
        self._input_list = input_list

    @property
    def distance(self) -> [int, str]:
        # [313054, '313 km']
        return self._input_list[2]

    @property
    def duration(self) -> [int, str]:
        # [16873, '4 hours 41 mins']
        return self._input_list[1]

    @property
    def instructions(self) -> list:
        return self._input_list[0]

    @property
    def source_geo(self) -> [float, float]:
        return self._input_list[5]

    @property
    def destination_geo(self) -> [float, float]:
        return self._input_list[6]

    @property
    def source(self) -> str:
        return self._input_list[7]

    @property
    def destination(self) -> str:
        return self._input_list[8]

    def __str__(self):
        return f"{self.source} to {self.destination} - {self.duration[1]}({self.distance[1]})"


class BardMapsDirections:
    def __init__(self, input_list: list):
        self._input_list = input_list

    @property
    def _map(self) -> list:
        return self._input_list[0][1][0]

    @property
    def url(self) -> str:
        return self._input_list[1]

    @property
    def road_name(self) -> str:
        return self._map[0]

    @property
    def sections(self) -> list[BardMapsRoadSection]:
        return [BardMapsRoadSection(s) for s in self._map[1]]

    @property
    def geo_position(self) -> [[float, float], [float, float]]:
        return self._map[6]

    def __str__(self):
        return "via " + self.road_name


class BardMapContent(UserContent):
    """http://googleusercontent.com/map_content/0"""

    def __init__(self, input_list: list):
        self._input_list = input_list

    @property
    def key(self) -> str:
        return self._input_list[2][0]

    @property
    def title(self) -> str:
        # Places
        return self._input_list[2][2]

    @property
    def tool_human_name(self) -> str:
        # Google Maps
        return self._input_list[2][6][0]

    @property
    def points(self) -> list[BardMapsPoint]:
        return (
            [BardMapsPoint(point) for point in self._input_list[0][1]]
            if self._input_list[0]
            else []
        )

    @property
    def directions(self) -> Optional[BardMapsDirections]:
        return BardMapsDirections(self._input_list[1]) if self._input_list[1] else None

    def __str__(self) -> str:
        return self.title

    def markdown_text(self) -> str:
        return f"# {self.title}\n\n" + "\n\n".join(
            [f"## {p.title[0]}\n\n{p.description()[0]}" for p in self.points]
        )