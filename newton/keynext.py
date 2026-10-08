import time, keyboard

class Keynext:

    @staticmethod
    def _read_next_key(required_keys: list[str] = []) -> str:
            try:
                while True:
                    next_key = keyboard.read_event()
        
                    if required_keys and not next_key.name in required_keys: continue

                    while next_key.event_type == keyboard.KEY_DOWN:
                        if time.time() - next_key.time > 0.01:
                            return next_key.name
                        
            except KeyboardInterrupt:
                return "exit"