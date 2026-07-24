"""과정 1 - 문제 9: 멀티스레드·멀티프로세스 미션 컴퓨터 모니터링."""

import json
import multiprocessing
import os
import platform
import random
import subprocess
import threading
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
        return self.env_values.copy()


class MissionComputer:
    def __init__(self, name="MissionComputer"):
        self.name = name
        self.sensor = DummySensor()
        self.env_values = {key: None for key in ENVIRONMENT_KEYS}

    def get_mission_computer_info(self, interval=20, stop_event=None, cycles=None):
        """시스템 정보를 기본 20초 간격으로 JSON 출력한다."""
        self._repeat(self._print_system_info, interval, stop_event, cycles)

    def get_mission_computer_load(self, interval=20, stop_event=None, cycles=None):
        """시스템 부하를 기본 20초 간격으로 JSON 출력한다."""
        self._repeat(self._print_system_load, interval, stop_event, cycles)

    def get_sensor_data(self, interval=5, stop_event=None, cycles=None):
        """센서 데이터를 기본 5초 간격으로 JSON 출력한다."""
        self._repeat(self._print_sensor_data, interval, stop_event, cycles)

    def _repeat(self, action, interval, stop_event, cycles):
        executed = 0
        while cycles is None or executed < cycles:
            if stop_event is not None and stop_event.is_set():
                break
            action()
            executed += 1
            if cycles is None or executed < cycles:
                if stop_event is not None and stop_event.wait(interval):
                    break
                if stop_event is None:
                    time.sleep(interval)

    def _print_system_info(self):
        info = {
            "computer": self.name,
            "operating_system": platform.system(),
            "operating_system_version": platform.release(),
            "cpu_type": platform.processor() or platform.machine(),
            "cpu_core_count": os.cpu_count(),
            "memory_size_bytes": self._memory_total_bytes(),
        }
        print(json.dumps(info, ensure_ascii=False), flush=True)

    def _print_system_load(self):
        cpu_count = os.cpu_count() or 1
        try:
            cpu_percent = round(min(os.getloadavg()[0] / cpu_count * 100, 100), 2)
        except OSError:
            cpu_percent = 0.0
        load = {
            "computer": self.name,
            "cpu_usage_percent": cpu_percent,
            "memory_usage_percent": self._memory_usage_percent(),
        }
        print(json.dumps(load, ensure_ascii=False), flush=True)

    def _print_sensor_data(self):
        self.sensor.set_env()
        self.env_values = self.sensor.get_env()
        print(
            json.dumps(
                {"computer": self.name, "sensor": self.env_values},
                ensure_ascii=False,
            ),
            flush=True,
        )

    @staticmethod
    def _memory_total_bytes():
        if platform.system() == "Darwin":
            try:
                result = subprocess.run(
                    ["sysctl", "-n", "hw.memsize"],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                return int(result.stdout.strip())
            except (OSError, ValueError, subprocess.SubprocessError):
                pass

        try:
            page_size = os.sysconf("SC_PAGE_SIZE")
            physical_pages = os.sysconf("SC_PHYS_PAGES")
            return page_size * physical_pages
        except (AttributeError, OSError, ValueError, subprocess.SubprocessError):
            return 0

    def _memory_usage_percent(self):
        total = self._memory_total_bytes()
        if total <= 0:
            return 0.0
        try:
            if platform.system() == "Darwin":
                result = subprocess.run(
                    ["vm_stat"], check=True, capture_output=True, text=True
                )
                first_line = result.stdout.splitlines()[0]
                page_size = int(first_line.split("page size of ")[1].split(" bytes")[0])
                used_names = {
                    "Pages active",
                    "Pages wired down",
                    "Pages occupied by compressor",
                }
                used_pages = 0
                for line in result.stdout.splitlines()[1:]:
                    name, separator, value = line.partition(":")
                    if separator and name in used_names:
                        used_pages += int(value.strip().rstrip("."))
                return round(min(used_pages * page_size / total * 100, 100), 2)
        except (OSError, ValueError, IndexError, subprocess.SubprocessError):
            return 0.0
        return 0.0


def run_info_process(name, interval, cycles):
    MissionComputer(name).get_mission_computer_info(interval=interval, cycles=cycles)


def run_load_process(name, interval, cycles):
    MissionComputer(name).get_mission_computer_load(interval=interval, cycles=cycles)


def run_sensor_process(name, interval, cycles):
    MissionComputer(name).get_sensor_data(interval=interval, cycles=cycles)


def start_thread_monitor(computer, interval=20, cycles=None):
    """세 메소드를 각각 별도 스레드에서 실행한다."""
    stop_event = threading.Event()
    threads = [
        threading.Thread(
            target=computer.get_mission_computer_info,
            kwargs={"interval": interval, "stop_event": stop_event, "cycles": cycles},
            name="mission-info",
        ),
        threading.Thread(
            target=computer.get_mission_computer_load,
            kwargs={"interval": interval, "stop_event": stop_event, "cycles": cycles},
            name="mission-load",
        ),
        threading.Thread(
            target=computer.get_sensor_data,
            kwargs={"interval": interval, "stop_event": stop_event, "cycles": cycles},
            name="sensor-data",
        ),
    ]
    for thread in threads:
        thread.start()
    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        stop_event.set()
        for thread in threads:
            thread.join()
        print("Sytem stoped....")


def start_process_monitor(interval=20, cycles=None):
    """세 인스턴스와 세 프로세스로 각 모니터 기능을 분리 실행한다."""
    processes = [
        multiprocessing.Process(
            target=run_info_process,
            args=(runComputer1.name, interval, cycles),
            name="mission-info-process",
        ),
        multiprocessing.Process(
            target=run_load_process,
            args=(runComputer2.name, interval, cycles),
            name="mission-load-process",
        ),
        multiprocessing.Process(
            target=run_sensor_process,
            args=(runComputer3.name, interval, cycles),
            name="sensor-data-process",
        ),
    ]
    for process in processes:
        process.start()
    try:
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()
        for process in processes:
            process.join()
        print("Sytem stoped....")


runComputer = MissionComputer("runComputer")
runComputer1 = MissionComputer("runComputer1")
runComputer2 = MissionComputer("runComputer2")
runComputer3 = MissionComputer("runComputer3")


def main():
    # 즉시 검증 가능한 1회 데모. 기본 메소드 간격은 평가 기준대로 20초이다.
    print("===== 멀티스레드 데모 =====")
    start_thread_monitor(runComputer, interval=0, cycles=1)
    print("===== 멀티프로세스 데모 =====")
    start_process_monitor(interval=0, cycles=1)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
