from .page import Page

from rich.panel import Panel
from rich.console import Group
from rich.live import Live

import keyboard, time

class Menu:
    def __init__(
            self,
            title: str,
            version: int = 0.1,
            control_menu: dict[str, str] = {
                "up": "up_soi",
                "down": "down_soi",
                "left": "turn_page_left",
                "right": "turn_page_right",
                "enter": "execute_option",
                "right shift": "exit"
            }
        ) -> None:

        self.title = title
        self.version = version

        self.control_menu = control_menu

        self.local_pages: dict[str, Page] = {}
        self.global_pages: list[Page] = []

        self.current_page: Page = None


        self.need_stop = False

    def link_page(self, id_local_page: str = ""):
        def decorator(cls: Page):
            if id_local_page:
                self.local_pages[id_local_page] = cls
            else:
                self.global_pages.append(cls)
            return cls
        return decorator

    def switch_current_page(self, id_page: str | int):

        match type(id_page).__name__:
            case "int":
                if not 0 <= id_page < len(self.global_pages): return
                root = self.global_pages
            case "str":
                if not id_page in list(self.local_pages.keys()): return
                root = self.local_pages

        self.current_page = root[id_page]

    def show(self):
        self.switch_current_page(0)
        self._render()

    def _render(self):
        with Live(
            self._build_menu(),
            refresh_per_second = 20
        ) as live:

            while not self.need_stop:

                try: enter_key = self._read_next_key()
                except KeyboardInterrupt: break

                match self.control_menu[enter_key]:
                    case "up_soi":
                        self.current_page.move_soi(
                            self.current_page,
                            "up"
                        )
                    case "down_soi":
                        self.current_page.move_soi(
                            self.current_page,
                            "down"
                        )
                    case "turn_page_left":
                        if self.current_page in self.local_pages: return

                        self.switch_current_page(
                            self.global_pages.index(self.current_page) - 1
                        )
                    case "turn_page_right":
                        if self.current_page in self.local_pages: return

                        self.switch_current_page(
                            self.global_pages.index(self.current_page) + 1
                        )
                    case "execute_option":
                        option = self.current_page.options[self.current_page.soi]

                        option.execute_function(*option.args)
                    case "exit": break

                live.update(
                    self._build_menu()
                )

    def _read_next_key(self) -> str:
        while True:
            next_key = keyboard.read_event()

            if not next_key.name in list(self.control_menu.keys()): continue

            if next_key.event_type == keyboard.KEY_UP: continue

            start = time.time()
            while next_key.event_type == keyboard.KEY_DOWN:

                if start > 0.1: return next_key.name

    def _build_menu(self):
        controls = {action: keyword for keyword, action in self.control_menu.items()}

        return Group(
            Panel(f"[#535353]{self.title}:{self.version} /[/#535353] {self.current_page.name}"),
            self.current_page.build_page(self.current_page),
            Panel(
                "[#535353]"
                f"({controls["down_soi"]}/{controls["up_soi"]}): выбрать опции | "
                f"({controls["turn_page_left"]}/{controls["turn_page_right"]}): перелистнуть страницы | "
                f"({controls["execute_option"]}): вызвать опцию | "
                f"({controls["exit"]}): выйти из меню"
                "[/#535353]"
            )
        )
    