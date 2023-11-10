from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.node import Node


class Edge:
    category_speed_dict = {'autostrada': 130, 'ekspresowa': 110, 'glowna': 60, 'glownaRuchuPrzyspieszonego': 75,
                           'zbiorcza': 50, 'dojazdowa': 20, 'wewnetrzna': 10, 'lokalna': 40, 'inna': 10}

    def __init__(self, start: "Node", end: "Node", length: float, id: int | None = None, category: str | None = None):
        if start is None or end is None or length < 0:
            raise RuntimeError("Edge initialization failed. Wrong arguments.")
        self.start: "Node" = start
        self.end: "Node" = end
        self.category = category
        self.length = length
        try:
            self.time = length / self.category_speed_dict[category]
        except:
            self.time = length / self.category_speed_dict['inna']
        self.id = id

    def __str__(self):
        return f"{self.start.name} -> {self.end.name}"
