import yaml
from datetime import datetime, timedelta
from _Fan import Fan


class ServerProperties:
    debug_enabled: bool
    all_fans = {}
    update_period: int
    last_update: datetime

    def __init__(self, path):
        self.path = path
        self.read_variables()

    def read_variables(self):
        with open(self.path, "r") as stream:
            content = yaml.full_load(stream)
            self.debug_enabled = content["debug"]
            self.update_period = content["update-period"]
            fans = content["fan"]

            for key, value in fans.items():
                pin = int(value["pin"])
                trigger = value["trigger"]
                start = int(value["start"])
                stop = int(value["stop"])
                fan = Fan(control_pin=pin, alias=key, start_at=start, stop_at=stop)
                self.all_fans[trigger] = fan
                print(f"registered fan \"{trigger}\": {fan}")
        self.last_update = datetime.now()

    def update_variables(self):
        next_update_at = self.last_update + timedelta(minutes=self.update_period)
        if next_update_at > datetime.now():
            if self.debug_enabled:
                print(f"Update time {next_update_at} has not yet been reached")
            return

        if self.debug_enabled:
            print("# Updating properties")
        with open(self.path, "r") as stream:
            content = yaml.full_load(stream)
            self.debug_enabled = content["debug"]
            self.update_period = content["update-period"]
            fans = content["fan"]

            for key, value in fans.items():
                trigger = value["trigger"]

                pin = int(value["pin"])
                start = int(value["start"])
                stop = int(value["stop"])

                fan = self.all_fans[trigger]
                fan._control_pin = pin
                fan._start_at = start
                fan._stop_at = stop

                if self.debug_enabled:
                    print(f"# Updated fan \"{trigger}\": {fan}")

        if self.debug_enabled:
            print("# Property update complete!")
