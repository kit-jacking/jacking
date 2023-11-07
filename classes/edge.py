from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.node import Node


class Edge:
    category_speed_dict = {'autostrada': 130, 'ekspresowa': 110, 'glowna': 40,'glownaRuchuPrzyspieszonego': 60, 'zbiorcza': 40,'dojazdowa': 20, 'wewnetrzna': 10, 'lokalna': 30, 'inna':10 }
    
    def __init__(self, start: "Node", end: "Node", cost: float, id: str | None = None, category: str | None = None):
        # in the future: change 'cost' to distance as it now means something else
        if start is None or end is None or cost < 0:
            raise RuntimeError("Edge initialization failed. Wrong arguments.")
        self.start: "Node" = start
        self.end: "Node" = end
        self.category = category
        self.cost = cost
        try:
            self.time = cost / self.category_speed_dict[category]
        except:
            self.time = cost / self.category_speed_dict['inna']
        self.id = id   

    def __str__(self):
        return f"{self.start.name} -> {self.end.name}"
