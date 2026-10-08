from typing import Callable
from rich.console import RenderableType

class Option:
    def __init__(
        self,

        name: str,
        description: "RenderableType",
        execute_function: Callable,
        args: list = [],

        basic_color: str = "white",
        pressed_color: str = "white on green"
    ) -> None:
        self.name = name
        self.description = description
        self.execute_function = execute_function
        self.args = args

        self.basic_color = basic_color
        self.pressed_color = pressed_color