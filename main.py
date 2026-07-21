def read_log_file(filename):
    log_list = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            print("===== 원본 로그 =====")

            for line in file:
                line = line.strip()
                print(line)

                # 콤마 기준으로 분리
                data = line.split(",", 1)

                if len(data) == 2:
                    log_list.append(data)

        return log_list

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        return []

    except PermissionError:
        print("파일 접근 권한이 없습니다.")
        return []

    except Exception as e:
        print("오류 발생 :", e)
        return []


def print_list(log_list):
    print("\n===== 리스트 =====")

    for item in log_list:
        print(item)


def sort_log_list(log_list):
    # 날짜 문자열이 YYYY-MM-DD HH:MM:SS 형식이므로 문자열 정렬만으로 시간순 정렬 가능
    log_list.sort(reverse=True)


def list_to_dict(log_list):
    log_dict = {}

    for i, item in enumerate(log_list, start=1):
        log_dict[str(i)] = {
            "datetime": item[0],
            "log": item[1]
        }

    return log_dict


def save_json(filename, log_dict):

    try:
        with open(filename, "w", encoding="utf-8") as file:

            file.write("{\n")

            keys = list(log_dict.keys())

            for i, key in enumerate(keys):

                value = log_dict[key]

                file.write(f'  "{key}": {{\n')
                file.write(f'    "datetime": "{value["datetime"]}",\n')
                file.write(f'    "log": "{value["log"]}"\n')
                file.write("  }")

                if i != len(keys) - 1:
                    file.write(",")

                file.write("\n")

            file.write("}")


    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

    except PermissionError:
        print("파일 접근 권한이 없습니다.")

    except Exception as e:
        print("오류 발생 :", e)


def main():

    # 1. 로그 읽기 및 리스트 변환
    log_list = read_log_file("mission_computer_main.log")

    # 2. 리스트 출력
    print_list(log_list)

    # 3. 시간 역순 정렬
    sort_log_list(log_list)

    print("\n===== 시간 역순 정렬 =====")
    print_list(log_list)

    # 4. 딕셔너리 변환
    log_dict = list_to_dict(log_list)

    print("\n===== 딕셔너리 =====")
    for key, value in log_dict.items():
        print(key, value)

    # 5. JSON 파일 저장
    save_json("mission_computer_main.json", log_dict)


if __name__ == "__main__":
    main()