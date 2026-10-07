from .page import Page

class Menu:
    def __init__(
            self,
            title: str,
            version: int = 0.1,
            control_menu: dict[str, str] = {
                "up_soi": "up",
                "down_soi": "down",
                "turn_page_left": "left",
                "turn_page_right": "right",
                "execute_option": "rshift"
            }
        ) -> None:

        self.title = title
        self.version = version

        self.control_menu = control_menu

        self.local_pages: dict[str, Page] = {}
        self.global_pages: list[Page] = []

        self.current_page: Page = None

    def link_page(self, id_local_page: str = ""):
        def decorator(cls: Page):
            if id_local_page:
                self.local_pages[id_local_page] = cls
            else:
                self.global_pages.append(cls)
            return cls
        return decorator

    def show(self):
        pass