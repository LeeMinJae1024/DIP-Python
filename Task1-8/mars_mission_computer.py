"""과정 1 - 문제 8: 시스템 정보와 부하를 확인하는 미션 컴퓨터."""

import json
import os
import platform
import subprocess


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "setting.txt")


class MissionComputer:
    def __init__(self):
        self.env_values = {
            "mars_base_internal_temperature": None,
            "mars_base_external_temperature": None,
            "mars_base_internal_humidity": None,
            "mars_base_external_illuminance": None,
            "mars_base_internal_co2": None,
            "mars_base_internal_oxygen": None,
        }

    def get_mission_computer_info(self):
        """운영체계, CPU, 메모리 정보를 JSON으로 출력하고 반환한다."""
        try:
            info = {
                "operating_system": platform.system(),
                "operating_system_version": platform.release(),
                "cpu_type": platform.processor() or platform.machine(),
                "cpu_core_count": os.cpu_count(),
                "memory_size_bytes": self._memory_total_bytes(),
            }
        except (OSError, subprocess.SubprocessError) as error:
            info = {"error": f"시스템 정보를 가져오지 못했습니다: {error}"}

        filtered_info = self._filter_settings(info)
        print(json.dumps(filtered_info, ensure_ascii=False, indent=2))
        return filtered_info

    def get_mission_computer_load(self):
        """CPU와 메모리 사용량을 JSON으로 출력하고 반환한다."""
        try:
            load = {
                "cpu_usage_percent": self._cpu_usage_percent(),
                "memory_usage_percent": self._memory_usage_percent(),
            }
        except (OSError, subprocess.SubprocessError) as error:
            load = {"error": f"시스템 부하를 가져오지 못했습니다: {error}"}

        filtered_load = self._filter_settings(load)
        print(json.dumps(filtered_load, ensure_ascii=False, indent=2))
        return filtered_load

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
            except (OSError, subprocess.SubprocessError, ValueError):
                pass

        try:
            page_size = os.sysconf("SC_PAGE_SIZE")
            physical_pages = os.sysconf("SC_PHYS_PAGES")
            return page_size * physical_pages
        except (AttributeError, OSError, ValueError):
            return 0

    @staticmethod
    def _cpu_usage_percent():
        cpu_count = os.cpu_count() or 1
        try:
            one_minute_load = os.getloadavg()[0]
            return round(min(one_minute_load / cpu_count * 100, 100), 2)
        except OSError:
            return 0.0

    def _memory_usage_percent(self):
        total = self._memory_total_bytes()
        if total <= 0:
            return 0.0

        if platform.system() == "Darwin":
            try:
                result = subprocess.run(
                    ["vm_stat"], check=True, capture_output=True, text=True
                )
                page_size = self._vm_page_size(result.stdout)
                pages = self._vm_used_pages(result.stdout)
                return round(min(pages * page_size / total * 100, 100), 2)
            except (OSError, subprocess.SubprocessError, ValueError, IndexError):
                return 0.0
        return 0.0

    @staticmethod
    def _vm_page_size(vm_stat_output):
        first_line = vm_stat_output.splitlines()[0]
        return int(first_line.split("page size of ")[1].split(" bytes")[0])

    @staticmethod
    def _vm_used_pages(vm_stat_output):
        used_names = {
            "Pages active",
            "Pages wired down",
            "Pages occupied by compressor",
        }
        pages = 0
        for line in vm_stat_output.splitlines()[1:]:
            name, separator, value = line.partition(":")
            if separator and name in used_names:
                pages += int(value.strip().rstrip("."))
        return pages

    @staticmethod
    def _selected_setting_keys():
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
                keys = [
                    line.strip()
                    for line in file
                    if line.strip() and not line.lstrip().startswith("#")
                ]
            return keys or None
        except FileNotFoundError:
            return None
        except (OSError, UnicodeDecodeError) as error:
            print(f"setting.txt를 읽지 못했습니다: {error}")
            return None

    def _filter_settings(self, values):
        selected_keys = self._selected_setting_keys()
        if selected_keys is None:
            return values
        return {key: values[key] for key in selected_keys if key in values}


runComputer = MissionComputer()


def main():
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()


if __name__ == "__main__":
    main()
