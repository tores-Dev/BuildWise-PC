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

        # 초기화
        self.total_budget = None
        self.usage_type = None
        self.remaining_budget = 0
        self.upgrade_history = []

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

    ##필요 PSU 용량 계산
    def calculate_required_wattage(self, cpu, gpu):
        base_power = cpu.power + gpu.power + 100
        return int(base_power * 1.3)

    ##호환 PSU 찾기
    def find_compatible_psu(self, cpu, gpu):
        required_wattage = self.calculate_required_wattage(cpu, gpu)

        compatible_psus = []

        for psu in self.psu_list:
            if psu.wattage >= required_wattage:
                compatible_psus.append(psu)

        if len(compatible_psus) == 0:
            return None

        return min(
            compatible_psus,
            key=lambda psu: (
                psu.wattage,
                psu.price
            )
        )

    ##호환 Case 찾기
    def find_compatible_case(self, motherboard, gpu):
        compatible_cases = []

        for pc_case in self.case_list:
            if (
                pc_case.motherboard_size == motherboard.size
                and pc_case.max_gpu_length >= gpu.length
            ):
                compatible_cases.append(pc_case)

        if len(compatible_cases) == 0:
            return None

        return min(
            compatible_cases,
            key=lambda pc_case: pc_case.price
        )

    ##빌드 생성
    def create_build(
        self,
        budget_allocation,
        recommendation_strategy,
        total_budget=None,
        usage_type=None
    ):
        self.budget_allocation = budget_allocation
        self.recommendation_strategy = recommendation_strategy
        self.total_budget = total_budget
        self.usage_type = usage_type

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

    ##사용 목적별 업그레이드 우선순위
    def get_usage_weights(self):
        if self.usage_type == "1":
            # 게임
            return {
                "cpu": 1.2,
                "gpu": 2.0,
                "ram": 0.8,
                "ssd": 0.6
            }

        elif self.usage_type == "2":
            # 사무 / 일반
            return {
                "cpu": 1.2,
                "gpu": 0.4,
                "ram": 1.0,
                "ssd": 1.0
            }

        elif self.usage_type == "3":
            # 개발 / 프로그래밍
            return {
                "cpu": 1.5,
                "gpu": 0.6,
                "ram": 1.5,
                "ssd": 1.1
            }

        elif self.usage_type == "4":
            # 영상 편집
            return {
                "cpu": 1.5,
                "gpu": 1.5,
                "ram": 1.3,
                "ssd": 1.1
            }

        return {
            "cpu": 1.0,
            "gpu": 1.0,
            "ram": 1.0,
            "ssd": 1.0
        }

    ##업그레이드 후보 비교 메서드
    def find_best_upgrade(self):
        usage_weights = self.get_usage_weights()
        upgrade_candidates = []

        # CPU 후보
        for cpu in self.cpu_list:
            if (
                self.recommended_cpu is not None
                and cpu.socket == self.recommended_cpu.socket
                and cpu.performance_score > self.recommended_cpu.performance_score
                and cpu.price > self.recommended_cpu.price
            ):
                compatible_psu = self.find_compatible_psu(
                    cpu,
                    self.recommended_gpu
                )

                if compatible_psu is None:
                    continue

                cpu_cost = cpu.price - self.recommended_cpu.price
                psu_cost = max(
                    0,
                    compatible_psu.price - self.recommended_psu.price
                )

                total_cost = cpu_cost + psu_cost

                if total_cost <= self.remaining_budget:
                    improvement = (
                        cpu.performance_score
                        - self.recommended_cpu.performance_score
                    ) / self.recommended_cpu.performance_score

                    score = (
                        improvement
                        * usage_weights["cpu"]
                        / (total_cost / 10000)
                    )

                    upgrade_candidates.append({
                        "type": "cpu",
                        "score": score,
                        "cost": total_cost,
                        "cpu": cpu,
                        "psu": compatible_psu
                    })

        # GPU 후보
        for gpu in self.gpu_list:
            if (
                self.recommended_gpu is not None
                and gpu.performance_score > self.recommended_gpu.performance_score
                and gpu.price > self.recommended_gpu.price
            ):
                compatible_psu = self.find_compatible_psu(
                    self.recommended_cpu,
                    gpu
                )

                compatible_case = self.find_compatible_case(
                    self.recommended_motherboard,
                    gpu
                )

                if compatible_psu is None or compatible_case is None:
                    continue

                gpu_cost = gpu.price - self.recommended_gpu.price

                psu_cost = max(
                    0,
                    compatible_psu.price - self.recommended_psu.price
                )

                case_cost = max(
                    0,
                    compatible_case.price - self.recommended_case.price
                )

                total_cost = gpu_cost + psu_cost + case_cost

                if total_cost <= self.remaining_budget:
                    improvement = (
                        gpu.performance_score
                        - self.recommended_gpu.performance_score
                    ) / self.recommended_gpu.performance_score

                    score = (
                        improvement
                        * usage_weights["gpu"]
                        / (total_cost / 10000)
                    )

                    upgrade_candidates.append({
                        "type": "gpu",
                        "score": score,
                        "cost": total_cost,
                        "gpu": gpu,
                        "psu": compatible_psu,
                        "case": compatible_case
                    })

        # RAM 후보
        for ram in self.ram_list:
            if (
                self.recommended_ram is not None
                and ram.memory_type == self.recommended_ram.memory_type
                and ram.capacity > self.recommended_ram.capacity
                and ram.price > self.recommended_ram.price
            ):
                total_cost = ram.price - self.recommended_ram.price

                if total_cost <= self.remaining_budget:
                    improvement = (
                        ram.capacity - self.recommended_ram.capacity
                    ) / self.recommended_ram.capacity

                    score = (
                        improvement
                        * usage_weights["ram"]
                        / (total_cost / 10000)
                    )

                    upgrade_candidates.append({
                        "type": "ram",
                        "score": score,
                        "cost": total_cost,
                        "ram": ram
                    })

        # SSD 후보
        for ssd in self.ssd_list:
            if (
                self.recommended_ssd is not None
                and ssd.capacity > self.recommended_ssd.capacity
                and ssd.price > self.recommended_ssd.price
            ):
                total_cost = ssd.price - self.recommended_ssd.price

                if total_cost <= self.remaining_budget:
                    improvement = (
                        ssd.capacity - self.recommended_ssd.capacity
                    ) / self.recommended_ssd.capacity

                    score = (
                        improvement
                        * usage_weights["ssd"]
                        / (total_cost / 10000)
                    )

                    upgrade_candidates.append({
                        "type": "ssd",
                        "score": score,
                        "cost": total_cost,
                        "ssd": ssd
                    })

        if len(upgrade_candidates) == 0:
            return None

        return max(
            upgrade_candidates,
            key=lambda candidate: candidate["score"]
        )

    ##업그레이드 적용
    def apply_upgrade(self, upgrade):
        remaining_before = self.remaining_budget

        if upgrade["type"] == "cpu":
            old_part = self.recommended_cpu
            new_part = upgrade["cpu"]

            self.recommended_cpu = new_part
            self.recommended_psu = upgrade["psu"]

        elif upgrade["type"] == "gpu":
            old_part = self.recommended_gpu
            new_part = upgrade["gpu"]

            self.recommended_gpu = new_part
            self.recommended_psu = upgrade["psu"]
            self.recommended_case = upgrade["case"]

        elif upgrade["type"] == "ram":
            old_part = self.recommended_ram
            new_part = upgrade["ram"]

            self.recommended_ram = new_part

        elif upgrade["type"] == "ssd":
            old_part = self.recommended_ssd
            new_part = upgrade["ssd"]

            self.recommended_ssd = new_part

        self.remaining_budget -= upgrade["cost"]

        self.upgrade_history.append({
            "type": upgrade["type"],
            "old_part": old_part.name,
            "new_part": new_part.name,
            "cost": upgrade["cost"],
            "score": upgrade["score"],
            "remaining_before": remaining_before,
            "remaining_after": self.remaining_budget
        })

    ##전체 업그레이드
    def upgrade_build(self):
        if self.total_budget is None:
            return

        if not self.is_complete_build():
            return

        self.upgrade_history = []

        current_total_price = self.calculate_total_price()
        self.remaining_budget = self.total_budget - current_total_price

        while True:
            best_upgrade = self.find_best_upgrade()

            if best_upgrade is None:
                break

            self.apply_upgrade(best_upgrade)