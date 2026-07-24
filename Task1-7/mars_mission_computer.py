"""과정 1 - 문제 7: 살아난 미션 컴퓨터 환경 모니터."""

from datetime import datetime
import json
import random
import time


ENVIRONMENT_KEYS = (
    "mars_base_internal_temperature",
    "mars_base_external_temperature",
    "mars_base_internal_humidity",
    "mars_base_external_illuminance",
    "mars_base_internal_co2",
    "mars_base_internal_oxygen",
)


class DummySensor:
    def __init__(self):
        self.env_values = {key: None for key in ENVIRONMENT_KEYS}

    def set_env(self):
        self.env_values.update(
            {
                "mars_base_internal_temperature": random.randint(18, 30),
                "mars_base_external_temperature": random.randint(0, 21),
                "mars_base_internal_humidity": random.randint(50, 60),
                "mars_base_external_illuminance": random.randint(500, 715),
                "mars_base_internal_co2": round(random.uniform(0.02, 0.1), 3),
                "mars_base_internal_oxygen": round(random.uniform(4, 7), 2),
            }
        )

    def get_env(self):
        return self.env_values


class MissionComputer:
    def __init__(self, sensor):
        self.sensor = sensor
        self.env_values = {key: None for key in ENVIRONMENT_KEYS}
        self._history = []

    def get_sensor_data(self, interval=5, iterations=None, average_interval=300):
        """센서값을 JSON으로 출력한다. 기본값은 5초마다 무한 반복이다."""
        count = 0
        last_average_time = time.monotonic()

        while iterations is None or count < iterations:
            self.sensor.set_env()
            self.env_values = self.sensor.get_env().copy()
            self._history.append(self.env_values.copy())
            print(json.dumps(self.env_values, ensure_ascii=False, indent=2))
            count += 1

            if time.monotonic() - last_average_time >= average_interval:
                self.print_five_minute_average()
                self._history.clear()
                last_average_time = time.monotonic()

            if iterations is None or count < iterations:
                time.sleep(interval)

    def print_five_minute_average(self):
        """보너스: 누적된 환경값의 5분 평균을 JSON으로 출력한다."""
        if not self._history:
            return

        averages = {}
        for key in ENVIRONMENT_KEYS:
            averages[key] = round(
                sum(record[key] for record in self._history) / len(self._history), 3
            )
        print("5분 평균")
        print(json.dumps(averages, ensure_ascii=False, indent=2))


ds = DummySensor()
RunComputer = MissionComputer(ds)


def main():
    print("센서 모니터링을 시작합니다. Ctrl+C를 누르면 종료합니다.")
    try:
        RunComputer.get_sensor_data()
    except KeyboardInterrupt:
        print("Sytem stoped....")
        RunComputer.print_five_minute_average()


if __name__ == "__main__":
    main()
