from typing import Callable

class Option:
    def __init__(
        self,

        name: str,
        execute_function: Callable,

        basic_color: str = "white",
        pressed_color: str = "white on green"
    ) -> None:
        self.name = name
        self.execute_function = execute_function

        self.basic_color = basic_color
        self.pressed_color = pressed_color