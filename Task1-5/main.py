"""과정 1 - 문제 5: NumPy로 화성 기지 부품 취약점 분석."""

import os

import numpy as np


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILENAMES = (
    "mars_base_main_parts-001.csv",
    "mars_base_main_parts-002.csv",
    "mars_base_main_parts-003.csv",
)
ATTACHMENT_FILENAMES = (
    "1-5-mars_base_main_parts-001.csv",
    "1-5-mars_base_main_parts-002.csv",
    "1-5-mars_base_main_parts-003.csv",
)
OUTPUT_FILENAME = "parts_to_work_on.csv"

# 평가에서 확인하기 쉬운 ndarray 이름
arr1 = np.empty((0, 2), dtype=str)
arr2 = np.empty((0, 2), dtype=str)
arr3 = np.empty((0, 2), dtype=str)
parts = np.empty((0, 2), dtype=str)
parts2 = np.empty((0, 2), dtype=str)
parts3 = np.empty((0, 0), dtype=str)


def resolve_input_path(index):
    plain_path = os.path.join(BASE_DIR, INPUT_FILENAMES[index])
    attachment_path = os.path.join(BASE_DIR, ATTACHMENT_FILENAMES[index])
    if os.path.exists(plain_path):
        return plain_path
    return attachment_path


def load_parts_file(filename):
    """헤더를 제외한 CSV를 문자열 ndarray로 읽는다."""
    try:
        loaded = np.genfromtxt(
            filename,
            delimiter=",",
            dtype=str,
            encoding="utf-8-sig",
            skip_header=1,
        )
        if loaded.size == 0:
            return np.empty((0, 2), dtype=str)
        return np.atleast_2d(loaded)
    except FileNotFoundError:
        print(f"입력 파일을 찾을 수 없습니다: {filename}")
    except PermissionError:
        print(f"입력 파일 권한이 없습니다: {filename}")
    except (OSError, ValueError) as error:
        print(f"입력 파일을 읽는 중 오류가 발생했습니다: {error}")
    return np.empty((0, 2), dtype=str)


def save_parts_file(filename, data):
    try:
        np.savetxt(
            filename,
            data,
            fmt="%s",
            delimiter=",",
            header="parts,strength",
            comments="",
            encoding="utf-8",
        )
        print(f"작업 대상 부품을 저장했습니다: {filename}")
        return True
    except PermissionError:
        print(f"출력 파일 권한이 없습니다: {filename}")
    except (OSError, ValueError) as error:
        print(f"출력 파일 저장 중 오류가 발생했습니다: {error}")
    return False


def main():
    global arr1, arr2, arr3, parts, parts2, parts3

    arr1 = load_parts_file(resolve_input_path(0))
    arr2 = load_parts_file(resolve_input_path(1))
    arr3 = load_parts_file(resolve_input_path(2))
    if not (arr1.size and arr2.size and arr3.size):
        return

    parts = np.vstack((arr1, arr2, arr3))
    strengths = parts[:, 1].astype(float)
    average_strength = np.mean(strengths)
    parts_to_work_on = parts[strengths < 50]

    print("===== 병합한 부품 목록 =====")
    print(parts)
    print(f"강도 평균: {average_strength:.3f}")
    print("===== 강도 50 미만 작업 대상 =====")
    print(parts_to_work_on)

    output_path = os.path.join(BASE_DIR, OUTPUT_FILENAME)
    if save_parts_file(output_path, parts_to_work_on):
        parts2 = load_parts_file(output_path)
        parts3 = parts2.T
        print("===== parts2 (저장 파일 재읽기) =====")
        print(parts2)
        print("===== parts3 (전치 행렬) =====")
        print(parts3)


if __name__ == "__main__":
    main()
