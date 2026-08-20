from data_loader import (load_cpu_data, load_gpu_data, load_motherboard_data, load_ram_data, load_ssd_data, load_psu_data, load_case_data)
from pc_build_recommender import PCBuildRecommender

##함수
def get_budget_mode():
    while True:
        print("\n========== 예산 설정 방식 ==========")
        print("1. 전체 예산으로 자동 설정")
        print("2. 부품별 예산 직접 설정")

        mode = input("선택하세요 (1 또는 2) : ")

        if mode == "1" or mode == "2":
            return mode

        print("1 또는 2를 입력해주세요.")

def get_budget_input(message):
    while True:
        try:
            budget = int(input(message))

            if budget < 0:
                print("예산은 0원 이상으로 입력해주세요.")
                continue

            return budget

        except ValueError:
            print("숫자만 입력해주세요.")

def get_usage_type():
    while True:
        print("\n========== 사용 목적 ==========")
        print("1. 게임")
        print("2. 사무 / 일반 사용")
        print("3. 개발 / 프로그래밍")
        print("4. 영상 편집")

        usage_type = input("사용 목적을 선택하세요 (1~4) : ")

        if usage_type in ["1", "2", "3", "4"]:
            return usage_type

        print("1부터 4까지의 숫자 중 하나를 입력해주세요.")

#사용목적 알고리즘
def allocate_budget(total_budget, usage_type):
    if usage_type == "1":
        # 게임
        budget_ratio = {
            "cpu": 0.20,
            "gpu": 0.35,
            "motherboard": 0.12,
            "ram": 0.08,
            "ssd": 0.08,
            "psu": 0.09,
            "case": 0.08
        }

    elif usage_type == "2":
        # 사무 / 일반 사용
        budget_ratio = {
            "cpu": 0.25,
            "gpu": 0.15,
            "motherboard": 0.15,
            "ram": 0.12,
            "ssd": 0.13,
            "psu": 0.10,
            "case": 0.10
        }

    elif usage_type == "3":
        # 개발 / 프로그래밍
        budget_ratio = {
            "cpu": 0.27,
            "gpu": 0.18,
            "motherboard": 0.13,
            "ram": 0.15,
            "ssd": 0.12,
            "psu": 0.08,
            "case": 0.07
        }

    else:
        # 영상 편집
        budget_ratio = {
            "cpu": 0.25,
            "gpu": 0.28,
            "motherboard": 0.11,
            "ram": 0.13,
            "ssd": 0.10,
            "psu": 0.08,
            "case": 0.05
        }

    budget_allocation = {
        "cpu": int(total_budget * budget_ratio["cpu"]),
        "gpu": int(total_budget * budget_ratio["gpu"]),
        "motherboard": int(
            total_budget * budget_ratio["motherboard"]
        ),
        "ram": int(total_budget * budget_ratio["ram"]),
        "ssd": int(total_budget * budget_ratio["ssd"]),
        "psu": int(total_budget * budget_ratio["psu"]),
        "case": int(total_budget * budget_ratio["case"])
    }

    return budget_allocation

def get_custom_budget():
    budget_allocation = {
        "cpu": get_budget_input("CPU 예산을 입력하세요 : "),
        "gpu": get_budget_input("GPU 예산을 입력하세요 : "),
        "motherboard": get_budget_input("메인보드 예산을 입력하세요 : "),
        "ram": get_budget_input("RAM 예산을 입력하세요 : "),
        "ssd": get_budget_input("SSD 예산을 입력하세요 : "),
        "psu": get_budget_input("PSU 예산을 입력하세요 : "),
        "case": get_budget_input("Case 예산을 입력하세요 : ")
    }

    return budget_allocation

def print_final_build(
    recommended_cpu,
    recommended_gpu,
    recommended_motherboard,
    recommended_ram,
    recommended_ssd,
    recommended_psu,
    recommended_case,
    total_price
):
    print("\n========== 최종 추천 PC 견적 ==========")

    if recommended_cpu is not None:
        print("CPU          :", recommended_cpu.name)

    if recommended_gpu is not None:
        print("GPU          :", recommended_gpu.name)

    if recommended_motherboard is not None:
        print("Motherboard  :", recommended_motherboard.name)

    if recommended_ram is not None:
        print("RAM          :", recommended_ram.name)

    if recommended_ssd is not None:
        print("SSD          :", recommended_ssd.name)

    if recommended_psu is not None:
        print("PSU          :", recommended_psu.name)

    if recommended_case is not None:
        print("Case         :", recommended_case.name)

    print()
    print("총 가격      :", format(total_price, ","), "원")
    print("=======================================")

def print_missing_parts(
    recommended_cpu,
    recommended_gpu,
    recommended_motherboard,
    recommended_ram,
    recommended_ssd,
    recommended_psu,
    recommended_case
):
    print("\n추천되지 않은 부품:")

    if recommended_cpu is None:
        print("- CPU")

    if recommended_gpu is None:
        print("- GPU")

    if recommended_motherboard is None:
        print("- Motherboard")

    if recommended_ram is None:
        print("- RAM")

    if recommended_ssd is None:
        print("- SSD")

    if recommended_psu is None:
        print("- PSU")

    if recommended_case is None:
        print("- Case")

def print_budget_allocation(budget_allocation):
    print("\n========== 자동 배정 예산 ==========")
    print(
        "CPU          :",
        format(budget_allocation["cpu"], ","),
        "원"
    )
    print(
        "GPU          :",
        format(budget_allocation["gpu"], ","),
        "원"
    )
    print(
        "Motherboard  :",
        format(budget_allocation["motherboard"], ","),
        "원"
    )
    print(
        "RAM          :",
        format(budget_allocation["ram"], ","),
        "원"
    )
    print(
        "SSD          :",
        format(budget_allocation["ssd"], ","),
        "원"
    )
    print(
        "PSU          :",
        format(budget_allocation["psu"], ","),
        "원"
    )
    print(
        "Case         :",
        format(budget_allocation["case"], ","),
        "원"
    )
    print("====================================")

##함수로 csv파일 불러오기
cpu_list = load_cpu_data()
gpu_list = load_gpu_data()
motherboard_list = load_motherboard_data()
ram_list = load_ram_data()
ssd_list = load_ssd_data()
psu_list = load_psu_data()
case_list = load_case_data()

##빌드 생성
recommender = PCBuildRecommender(
    cpu_list,
    gpu_list,
    motherboard_list,
    ram_list,
    ssd_list,
    psu_list,
    case_list
)

##기능 모음
budget_mode = get_budget_mode()

if budget_mode == "1":
    total_budget = get_budget_input(
        "전체 PC 예산을 입력하세요 : "
    )

    usage_type = get_usage_type()

    budget_allocation = allocate_budget(
        total_budget,
        usage_type
    )

    recommendation_strategy = "performance"

    print_budget_allocation(
        budget_allocation
    )

else:
    budget_allocation = get_custom_budget()

    recommendation_strategy = "value"

##부품 추천 기능
recommender.create_build(
    budget_allocation,
    recommendation_strategy
)

recommended_cpu = recommender.recommended_cpu
recommended_gpu = recommender.recommended_gpu
recommended_motherboard = (
    recommender.recommended_motherboard
)
recommended_ram = recommender.recommended_ram
recommended_ssd = recommender.recommended_ssd
recommended_psu = recommender.recommended_psu
recommended_case = recommender.recommended_case

##추천된 부품들 검사
if recommender.is_complete_build():
    total_price = (
        recommender.calculate_total_price()
    )

    print_final_build(
        recommended_cpu,
        recommended_gpu,
        recommended_motherboard,
        recommended_ram,
        recommended_ssd,
        recommended_psu,
        recommended_case,
        total_price
    )

else:
    print("\n완성된 PC 견적을 만들 수 없습니다.")

    print_missing_parts(
        recommended_cpu,
        recommended_gpu,
        recommended_motherboard,
        recommended_ram,
        recommended_ssd,
        recommended_psu,
        recommended_case
    )

    print("\n각 부품의 예산이나 호환 조건을 확인해주세요.")