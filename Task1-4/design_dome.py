"""과정 1 - 문제 4: 화성 기지 반구형 돔 설계 계산기."""

import math


MARS_GRAVITY_RATIO = 0.38
MATERIAL_DENSITIES = {
    "유리": 2.4,
    "알루미늄": 2.7,
    "탄소강": 7.85,
}

# 평가 기준에서 요구한 전역 변수
material = "유리"
diameter = 10.0
thickness = 1.0
area = 0.0
weight = 0.0


def sphere_area(diameter=10, material="유리", thickness=1):
    """반구형 돔의 전체 표면적과 화성 기준 무게를 계산한다.

    전체 표면적은 곡면(2πr²)과 바닥(πr²)을 더한 3πr²를 사용한다.
    밀도는 g/cm³, 입력 지름은 m, 두께는 cm이며 결과 무게는 화성 중력
    비율을 반영한 kgf 상당값이다.
    """
    global area, weight

    try:
        diameter_value = float(diameter)
        thickness_value = float(thickness)
    except (TypeError, ValueError) as error:
        raise ValueError("지름과 두께에는 숫자를 입력해야 합니다.") from error

    if diameter_value <= 0 or thickness_value <= 0:
        raise ValueError("지름과 두께는 0보다 커야 합니다.")
    if material not in MATERIAL_DENSITIES:
        available = ", ".join(MATERIAL_DENSITIES)
        raise ValueError(f"재질은 다음 중 하나여야 합니다: {available}")

    globals()["material"] = material
    globals()["diameter"] = diameter_value
    globals()["thickness"] = thickness_value
    radius = diameter_value / 2
    area = 3 * math.pi * radius**2
    shell_volume = area * (thickness_value / 100)
    earth_mass = MATERIAL_DENSITIES[material] * 1000 * shell_volume
    weight = earth_mass * MARS_GRAVITY_RATIO
    return area, weight


def format_result():
    return (
        f"재질 ⇒ {material}, 지름 ⇒ {diameter:.3f} m, "
        f"두께 ⇒ {thickness:.3f} cm, 면적 ⇒ {area:.3f} m², "
        f"무게 ⇒ {weight:.3f} kg"
    )


def read_value(prompt, default):
    value = input(prompt).strip()
    return default if not value else value


def main():
    global material, diameter, thickness

    print("화성 기지 반구형 돔 설계 계산기 (종료: q)")
    while True:
        try:
            selected_material = read_value(
                "재질 [유리/알루미늄/탄소강, 기본 유리]: ", "유리"
            )
            if selected_material.lower() in {"q", "quit", "exit"}:
                print("계산을 종료합니다.")
                break

            selected_diameter = read_value("지름(m, 기본 10): ", "10")
            selected_thickness = read_value("두께(cm, 기본 1): ", "1")
            material = selected_material
            diameter = float(selected_diameter)
            thickness = float(selected_thickness)
            sphere_area(diameter, material, thickness)
            print(format_result())
        except (EOFError, KeyboardInterrupt):
            print("\n계산을 종료합니다.")
            break
        except ValueError as error:
            print(f"입력 오류: {error}")


if __name__ == "__main__":
    main()
