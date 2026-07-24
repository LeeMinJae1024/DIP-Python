"""과정 1 - 문제 6: 더미 환경 센서."""

from datetime import datetime
import json
import os
import random


LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sensor.log")


class DummySensor:
    """화성 기지 환경값을 지정 범위에서 임의로 생성하는 센서."""

    def __init__(self):
        self.env_values = {
            "mars_base_internal_temperature": None,
            "mars_base_external_temperature": None,
            "mars_base_internal_humidity": None,
            "mars_base_external_illuminance": None,
            "mars_base_internal_co2": None,
            "mars_base_internal_oxygen": None,
        }

    def set_env(self):
        self.env_values["mars_base_internal_temperature"] = random.randint(18, 30)
        self.env_values["mars_base_external_temperature"] = random.randint(0, 21)
        self.env_values["mars_base_internal_humidity"] = random.randint(50, 60)
        self.env_values["mars_base_external_illuminance"] = random.randint(500, 715)
        self.env_values["mars_base_internal_co2"] = round(random.uniform(0.02, 0.1), 3)
        self.env_values["mars_base_internal_oxygen"] = round(random.uniform(4, 7), 2)

    def get_env(self):
        self._write_log()
        return self.env_values

    def _write_log(self):
        """보너스: 센서값을 날짜·시간과 함께 로그 파일에 기록한다."""
        log_record = {"datetime": datetime.now().isoformat(timespec="seconds")}
        log_record.update(self.env_values)
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as file:
                file.write(json.dumps(log_record, ensure_ascii=False) + "\n")
        except (OSError, TypeError) as error:
            print(f"센서 로그를 기록하지 못했습니다: {error}")


ds = DummySensor()


def main():
    ds.set_env()
    print(json.dumps(ds.get_env(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
