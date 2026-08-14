from data_loader import (load_cpu_data, load_gpu_data, load_motherboard_data, load_ram_data, load_ssd_data, load_psu_data, load_case_data)

##함수
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

def recommend_performance_part(part_list, budget):
    available_parts = []

    for part in part_list:
        if part.price <= budget:
            part.value_score = (
                part.performance_score
                / part.price
                * 10000
            )

            available_parts.append(part)

    if len(available_parts) == 0:
        return None

    recommended_part = max(
        available_parts,
        key=lambda part: part.value_score
    )

    return recommended_part



##함수로 csv파일 불러오기
cpu_list = load_cpu_data()
gpu_list = load_gpu_data()
motherboard_list = load_motherboard_data()
ram_list = load_ram_data()
ssd_list = load_ssd_data()
psu_list = load_psu_data()
case_list = load_case_data()


##기능 모음
##CPU 추천 기능
cpu_budget = get_budget_input("\nCPU 예산을 입력하세요 : ")
recommended_cpu = recommend_performance_part(cpu_list, cpu_budget)

if recommended_cpu is None:
    print("예산 내에서 추천할 수 있는 CPU가 없습니다.")
else:
    print("\n========추천 CPU========")
    print("제품명               :", recommended_cpu.name)
    print("가격                 :", recommended_cpu.price, "원")
    print("성능 점수            :", recommended_cpu.performance_score)
    print("가격 대비 성능 점수  :", round(recommended_cpu.value_score, 2))

##메인보드 추천 기능
if recommended_cpu is not None:
    motherboard_budget = get_budget_input("\n메인보드 예산을 입력하세요 : ")

    compatible_motherboards = []

    for motherboard in motherboard_list:
        if (
            motherboard.socket == recommended_cpu.socket
            and motherboard.price <= motherboard_budget
        ):
            compatible_motherboards.append(motherboard)

    if len(compatible_motherboards) == 0:
        recommended_motherboard = None
        print("추천 CPU와 호환되는 메인보드가 예산 내에 없습니다.")

    else:
        recommended_motherboard = min(
            compatible_motherboards,
            key=lambda motherboard: motherboard.price
        )

        print("\n========추천 메인보드========")
        print("제품명       :", recommended_motherboard.name)
        print("가격         :", recommended_motherboard.price, "원")
        print("소켓         :", recommended_motherboard.socket)
        print("메모리 규격  :", recommended_motherboard.memory_type)

##RAM 추천 기능
if recommended_motherboard is not None:
    ram_budget = get_budget_input("\nRAM 예산을 입력하세요 : ")

    compatible_rams = []

    for ram in ram_list:
        if (
            ram.memory_type == recommended_motherboard.memory_type
            and ram.price <= ram_budget
        ):
            compatible_rams.append(ram)

    if len(compatible_rams) == 0:
        recommended_ram = None
        print("추천 메인보드와 호환되는 RAM이 예산 내에 없습니다.")

    else:
        recommended_ram = max(
            compatible_rams,
            key=lambda ram: ram.capacity
        )

        print("\n========추천 RAM========")
        print("제품명       :", recommended_ram.name)
        print("가격         :", recommended_ram.price, "원")
        print("메모리 규격  :", recommended_ram.memory_type)
        print("용량         :", recommended_ram.capacity, "GB")

##SSD 추천 기능
ssd_budget = get_budget_input("\nSSD 예산을 입력하세요 : ")
available_ssds = []

for ssd in ssd_list:
    if ssd.price <= ssd_budget:
        available_ssds.append(ssd)

if len(available_ssds) == 0:
    recommended_ssd = None
    print("예산 내에서 추천할 수 있는 SSD가 없습니다.")

else:
    recommended_ssd = max(
        available_ssds,
        key=lambda ssd: (
            ssd.capacity, -ssd.price
        )
    )

    print("\n========추천 SSD========")
    print("제품명       :", recommended_ssd.name)
    print("가격         :", recommended_ssd.price, "원")
    print("용량         :", recommended_ssd.capacity, "GB")
    print("연결 방식    :", recommended_ssd.interface)

##GPU 추천 기능
gpu_budget = get_budget_input("\nGPU 예산을 입력하세요 : ")
recommended_gpu = recommend_performance_part(gpu_list, gpu_budget)

if recommended_gpu is None:
    print("예산 내에서 추천할 수 있는 GPU가 없습니다.")
else:
    print("\n========추천 GPU========")
    print("제품명               :", recommended_gpu.name)
    print("가격                 :", recommended_gpu.price)
    print("성능 점수            :", recommended_gpu.performance_score)
    print("가격 대비 성능 점수  :", round(recommended_gpu.value_score))

##PSU 추천 기능
if recommended_cpu is not None and recommended_gpu is not None:
    psu_budget = get_budget_input("\n파워서플라이 예산을 입력하세요 : ")

    base_power = (
        recommended_cpu.power
        + recommended_gpu.power
        + 100  #기타 부품 예상 용량 (테스트)
    )

    required_wattage = int(base_power * 1.3)  #여유 용량 30% (테스트)

    print("\n예상 최소 파워 용량 :", required_wattage, "W")

    available_psus = []

    for psu in psu_list:
        if (
            psu.wattage >= required_wattage
            and psu.price <= psu_budget
        ):
            available_psus.append(psu)

    if len(available_psus) == 0:
        recommended_psu = None
        print("필요한 출력과 예산을 만족하는 파워서플라이가 없습니다.")

    else:
        recommended_psu = min(
            available_psus,
            key=lambda psu: (
                psu.wattage,
                psu.price
            )
        )

        print("\n========추천 파워서플라이========")
        print("제품명       :", recommended_psu.name)
        print("가격         :", recommended_psu.price, "원")
        print("정격 출력    :", recommended_psu.wattage, "W")
        print("효율 등급    :", recommended_psu.efficiency)

##케이스 추천 기능
if recommended_motherboard is not None and recommended_gpu is not None:
    case_budget = get_budget_input("\n케이스 예산을 입력하세요 : ")

    compatible_cases = []

    for pc_case in case_list:
        if (
            pc_case.motherboard_size == recommended_motherboard.size
            and pc_case.max_gpu_length >= recommended_gpu.length
            and pc_case.price <= case_budget
        ):
            compatible_cases.append(pc_case)

    if len(compatible_cases) == 0:
        recommended_case = None
        print("추천 부품과 호환되는 케이스가 예산 내에 없습니다.")

    else:
        recommended_case = min(
            compatible_cases,
            key=lambda pc_case: pc_case.price
        )

        print("\n========추천 케이스========")
        print("제품명             :", recommended_case.name)
        print("가격               :", recommended_case.price, "원")
        print("메인보드 지원 규격 :", recommended_case.motherboard_size)
        print("최대 GPU 길이      :", recommended_case.max_gpu_length, "mm")