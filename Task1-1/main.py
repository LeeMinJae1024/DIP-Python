def read_log_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = file.read()
            print(data)

    except FileNotFoundError:
        print("로그 파일을 찾을 수 없습니다.")

    except PermissionError:
        print("파일 접근 권한이 없습니다.")

    except UnicodeDecodeError:
        print("파일 인코딩을 읽을 수 없습니다.")

    except Exception as e:
        print(f"예외 발생 : {e}")


if __name__ == "__main__":
    read_log_file("mission_computer_main.log")