from .option import Option

from rich.tree import Tree
from rich.text import Text
from rich.panel import Panel
from rich.columns import Columns

from rich.console import RenderableType

class Page:
    name: str
    name_tree: str = "выберите опции"

    options: list[Option]
    soi: int = 0

    objects: list["RenderableType"] = []

    def move_soi(self, direction: str):
        match direction:
            case "up":
                self.soi = max(
                    0,
                    self.soi - 1
                )
            case "down":
                self.soi = min(
                    len(self.options) - 1,
                    self.soi + 1
                )

    def _build_objects(self):
        return Columns(
            object for object in self.objects
        )

    def _build_tree_options(self):
        tree_options = Tree(self.name_tree)

        for option in self.options:
            tree_options.add(
                Text(
                    option.name,
                    style = option.pressed_color if self.options.index(option) == self.soi else option.basic_color
                )
            )

        return tree_options

    def build_page(self):
        return Panel(
            self._build_tree_options(self),
            expand = False
        )