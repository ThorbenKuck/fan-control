import RPi.GPIO as GPIO


class Fan:
    _running: bool = False
    _control_pin: int
    _alias: str
    _start_at: int
    _stop_at: int
    _running_causes: []

    def __init__(self, control_pin: int, alias: str, start_at: int, stop_at: int):
        self._control_pin = control_pin
        self._alias = alias
        self._start_at = start_at
        self._stop_at = stop_at
        GPIO.setup(control_pin, GPIO.OUT)
        self.stop()
        self._running_causes = []

    def stop(self):
        print("Stopping fan", self._alias)
        GPIO.output(self._control_pin, GPIO.LOW)
        self._running = False

    def start(self):
        print("Starting fan", self._alias, "at pin", self._control_pin)
        GPIO.output(self._control_pin, GPIO.HIGH)
        self._running = True

    def trigger(self, temp, debug, target: str):
        if debug:
            print(f"[{self._alias}]: ({self._start_at},{self._stop_at}) => {temp}")

        if temp >= self._start_at and not self._running_causes.__contains__(target):
            if debug:
                print(f"Adding {target} to ${self._running_causes}")
            self._running_causes.append(target)
        elif temp <= self._stop_at and self._running_causes.__contains__(target):
            if debug:
                print(f"Removing {target} from {self._running_causes}")
            self._running_causes.remove(target)

        if debug:
            print(f"Past state: {self._running_causes} AND {self._running}")

        if not self._running and len(self._running_causes) > 0:
            if debug:
                print(" ==> Triggered running with the causes", self._running_causes)
            self.start()
        elif self._running and len(self._running_causes) <= 0:
            if debug:
                print(" <== Stopping because all running causes have cooled down", self._running_causes)
            self.stop()

    def __str__(self):
        return "Fan(alias=" + self._alias + \
               ", pin=" + str(self._control_pin) + \
               ", starts_at=" + str(self._start_at) + \
               ", stops_at=" + str(self._stop_at)

