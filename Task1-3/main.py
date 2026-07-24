"""과정 1 - 문제 3: 인화 물질 목록 분석.

외부 패키지를 사용하지 않고 CSV를 2차원 배열(중첩 리스트)로 다룬다.
"""

import os
import pickle


SOURCE_FILE = "Mars_Base_Inventory_List.csv"
DANGER_FILE = "Mars_Base_Inventory_danger.csv"
BINARY_FILE = "Mars_Base_Inventory_List.bin"
FLAMMABILITY_COLUMN = 4
DANGER_LIMIT = 0.7


def read_inventory_file(filename):
    """CSV를 [헤더 배열, 데이터 배열] 형태로 읽는다."""
    inventory_array = [[], []]

    try:
        with open(filename, "r", encoding="utf-8-sig") as file:
            header_line = file.readline().strip()
            if not header_line:
                raise ValueError("CSV 파일에 헤더가 없습니다.")

            inventory_array[0] = header_line.split(",")
            for line in file:
                row = line.strip().split(",")
                if len(row) == len(inventory_array[0]):
                    inventory_array[1].append(row)
                elif line.strip():
                    print("형식이 맞지 않는 행을 건너뜁니다:", line.strip())
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {filename}")
    except PermissionError:
        print(f"파일 접근 권한이 없습니다: {filename}")
    except UnicodeDecodeError:
        print(f"파일 인코딩을 읽을 수 없습니다: {filename}")
    except OSError as error:
        print(f"파일을 읽는 중 오류가 발생했습니다: {error}")
    except ValueError as error:
        print(f"CSV 형식 오류: {error}")

    return inventory_array


def flammability_value(row):
    """정렬 중 잘못된 인화성 값은 가장 낮은 값으로 처리한다."""
    try:
        return float(row[FLAMMABILITY_COLUMN])
    except (IndexError, ValueError):
        return -1.0


def sort_by_flammability(records):
    """인화성 지수를 기준으로 높은 순서대로 배열을 정렬한다."""
    records.sort(key=flammability_value, reverse=True)
    return records


def select_dangerous_records(records):
    """인화성 지수가 기준 이상인 행만 별도의 배열로 만든다."""
    dangerous_array = []
    for row in records:
        if flammability_value(row) >= DANGER_LIMIT:
            dangerous_array.append(row)
    return dangerous_array


def print_inventory(title, header, records):
    print(f"\n===== {title} =====")
    print(", ".join(header))
    for row in records:
        print(", ".join(row))


def save_csv(filename, header, records):
    """배열을 위험 물질 CSV로 저장한다."""
    try:
        with open(filename, "w", encoding="utf-8", newline="") as file:
            file.write(",".join(header) + "\n")
            for row in records:
                file.write(",".join(row) + "\n")
        print(f"위험 물질 CSV를 저장했습니다: {filename}")
        return True
    except PermissionError:
        print(f"파일 저장 권한이 없습니다: {filename}")
    except OSError as error:
        print(f"CSV 저장 중 오류가 발생했습니다: {error}")
    return False


def save_binary(filename, inventory_array):
    """정렬된 배열을 실제 바이너리 형식(pickle)으로 저장한다."""
    try:
        with open(filename, "wb") as file:
            pickle.dump(inventory_array, file)
        print(f"이진 파일을 저장했습니다: {filename}")
        return True
    except PermissionError:
        print(f"파일 저장 권한이 없습니다: {filename}")
    except (OSError, pickle.PickleError) as error:
        print(f"이진 파일 저장 중 오류가 발생했습니다: {error}")
    return False


def read_binary(filename):
    """저장한 이진 파일을 다시 읽어 배열로 반환한다."""
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        print(f"이진 파일을 찾을 수 없습니다: {filename}")
    except PermissionError:
        print(f"파일 접근 권한이 없습니다: {filename}")
    except (OSError, pickle.PickleError, EOFError) as error:
        print(f"이진 파일을 읽는 중 오류가 발생했습니다: {error}")
    return [[], []]


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(base_dir, SOURCE_FILE)
    danger_path = os.path.join(base_dir, DANGER_FILE)
    binary_path = os.path.join(base_dir, BINARY_FILE)

    inventory_array = read_inventory_file(source_path)
    header = inventory_array[0]
    records = inventory_array[1]
    if not header or not records:
        return

    print_inventory("원본 목록", header, records)
    sort_by_flammability(records)
    print_inventory("인화성 내림차순 목록", header, records)

    dangerous_records = select_dangerous_records(records)
    print_inventory("인화성 지수 0.7 이상 목록", header, dangerous_records)
    save_csv(danger_path, header, dangerous_records)

    if save_binary(binary_path, inventory_array):
        restored_array = read_binary(binary_path)
        print_inventory("이진 파일에서 다시 읽은 목록", restored_array[0], restored_array[1])


if __name__ == "__main__":
    main()
