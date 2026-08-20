class PCBuildRecommender:
    def __init__(
        self,
        cpu_list,
        gpu_list,
        motherboard_list,
        ram_list,
        ssd_list,
        psu_list,
        case_list
    ):
        # 사용할 수 있는 전체 부품 데이터
        self.cpu_list = cpu_list
        self.gpu_list = gpu_list
        self.motherboard_list = motherboard_list
        self.ram_list = ram_list
        self.ssd_list = ssd_list
        self.psu_list = psu_list
        self.case_list = case_list

        # 추천 조건
        self.budget_allocation = None
        self.recommendation_strategy = None

        # 추천 결과
        self.recommended_cpu = None
        self.recommended_gpu = None
        self.recommended_motherboard = None
        self.recommended_ram = None
        self.recommended_ssd = None
        self.recommended_psu = None
        self.recommended_case = None

    ##CPU/GPU 공통 추천 메서드
    def recommend_performance_part(
        self,
        part_list,
        budget
    ):
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

        if self.recommendation_strategy == "performance":
            recommended_part = max(
                available_parts,
                key=lambda part: part.performance_score
            )

        else:
            recommended_part = max(
                available_parts,
                key=lambda part: part.value_score
            )

        return recommended_part

    ##CPU추천
    def recommend_cpu(self):
        self.recommended_cpu = (
            self.recommend_performance_part(
                self.cpu_list,
                self.budget_allocation["cpu"]
            )
        )

    ##GPU추천
    def recommend_gpu(self):
        self.recommended_gpu = (
            self.recommend_performance_part(
                self.gpu_list,
                self.budget_allocation["gpu"]
            )
        )

    ##메인보드 추천
    def recommend_motherboard(self):
        if self.recommended_cpu is None:
            return

        compatible_motherboards = []

        for motherboard in self.motherboard_list:
            if (
                motherboard.socket
                == self.recommended_cpu.socket
                and motherboard.price
                <= self.budget_allocation["motherboard"]
            ):
                compatible_motherboards.append(
                    motherboard
                )

        if len(compatible_motherboards) == 0:
            self.recommended_motherboard = None
            return

        self.recommended_motherboard = min(
            compatible_motherboards,
            key=lambda motherboard: motherboard.price
        )

    ##RAM추천
    def recommend_ram(self):
        if self.recommended_motherboard is None:
            return

        compatible_rams = []

        for ram in self.ram_list:
            if (
                ram.memory_type
                == self.recommended_motherboard.memory_type
                and ram.price
                <= self.budget_allocation["ram"]
            ):
                compatible_rams.append(ram)

        if len(compatible_rams) == 0:
            self.recommended_ram = None
            return

        self.recommended_ram = max(
            compatible_rams,
            key=lambda ram: ram.capacity
        )

    ##SSD추천
    def recommend_ssd(self):
        available_ssds = []

        for ssd in self.ssd_list:
            if (
                ssd.price
                <= self.budget_allocation["ssd"]
            ):
                available_ssds.append(ssd)

        if len(available_ssds) == 0:
            self.recommended_ssd = None
            return

        self.recommended_ssd = max(
            available_ssds,
            key=lambda ssd: (
                ssd.capacity,
                -ssd.price
            )
        )

    ##PSU추천
    def recommend_psu(self):
        if (
            self.recommended_cpu is None
            or self.recommended_gpu is None
        ):
            return

        base_power = (
            self.recommended_cpu.power
            + self.recommended_gpu.power
            + 100
        )

        required_wattage = int(
            base_power * 1.3
        )

        available_psus = []

        for psu in self.psu_list:
            if (
                psu.wattage >= required_wattage
                and psu.price
                <= self.budget_allocation["psu"]
            ):
                available_psus.append(psu)

        if len(available_psus) == 0:
            self.recommended_psu = None
            return

        self.recommended_psu = min(
            available_psus,
            key=lambda psu: (
                psu.wattage,
                psu.price
            )
        )

    ##케이스 추천
    def recommend_case(self):
        if (
            self.recommended_motherboard is None
            or self.recommended_gpu is None
        ):
            return

        compatible_cases = []

        for pc_case in self.case_list:
            if (
                pc_case.motherboard_size
                == self.recommended_motherboard.size
                and pc_case.max_gpu_length
                >= self.recommended_gpu.length
                and pc_case.price
                <= self.budget_allocation["case"]
            ):
                compatible_cases.append(
                    pc_case
                )

        if len(compatible_cases) == 0:
            self.recommended_case = None
            return

        self.recommended_case = min(
            compatible_cases,
            key=lambda pc_case: pc_case.price
        )

    ##빌드 생성
    def create_build(
        self,
        budget_allocation,
        recommendation_strategy
    ):
        self.budget_allocation = budget_allocation
        self.recommendation_strategy = (
            recommendation_strategy
        )

        self.recommend_cpu()
        self.recommend_gpu()
        self.recommend_motherboard()
        self.recommend_ram()
        self.recommend_ssd()
        self.recommend_psu()
        self.recommend_case()

    ##추천 결과 리스트
    def get_recommended_parts(self):
        return [
            self.recommended_cpu,
            self.recommended_gpu,
            self.recommended_motherboard,
            self.recommended_ram,
            self.recommended_ssd,
            self.recommended_psu,
            self.recommended_case
        ]

    ##완성 여부 검사
    def is_complete_build(self):
        for part in self.get_recommended_parts():
            if part is None:
                return False

        return True

    ##총 가격 계산
    def calculate_total_price(self):
        total_price = 0

        for part in self.get_recommended_parts():
            if part is not None:
                total_price += part.price

        return total_price