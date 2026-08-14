import csv
from pc_parts import (CPU, GPU, Motherboard, RAM, SSD, PSU, Case)


##함수
def load_cpu_data():
    cpu_list = []

    with open("data/cpu.csv", "r", encoding="utf-8") as file:
        cpu_data = csv.DictReader(file)

        for row in cpu_data:
            cpu = CPU(
                row["name"],
                row["brand"],
                int(row["price"]),
                row["socket"],
                int(row["performance_score"]),
                int(row["power"])
            )

            cpu_list.append(cpu)

    return cpu_list

def load_gpu_data():
    gpu_list = []

    with open("data/gpu.csv", "r", encoding="utf-8") as file:
        gpu_data = csv.DictReader(file)

        for row in gpu_data:
            gpu = GPU(
                row["name"],
                row["brand"],
                int(row["price"]),
                int(row["performance_score"]),
                int(row["power"]),
                int(row["length"])
            )

            gpu_list.append(gpu)

    return gpu_list

def load_motherboard_data():
    motherboard_list = []

    with open("data/motherboard.csv", "r", encoding="utf-8") as file:
        motherboard_data = csv.DictReader(file)

        for row in motherboard_data:
            motherboard = Motherboard(
                row["name"],
                row["brand"],
                int(row["price"]),
                row["socket"],
                row["memory_type"],
                row["size"]
            )

            motherboard_list.append(motherboard)

    return motherboard_list

def load_ram_data():
    ram_list = []

    with open("data/ram.csv", "r", encoding="utf-8") as file:
        ram_data = csv.DictReader(file)

        for row in ram_data:
            ram = RAM(
                row["name"],
                row["brand"],
                int(row["price"]),
                row["memory_type"],
                int(row["capacity"])
            )

            ram_list.append(ram)

    return ram_list

def load_ssd_data():
    ssd_list = []

    with open("data/ssd.csv", "r", encoding="utf-8") as file:
        ssd_data = csv.DictReader(file)

        for row in ssd_data:
            ssd = SSD(
                row["name"],
                row["brand"],
                int(row["price"]),
                int(row["capacity"]),
                row["interface"]
            )

            ssd_list.append(ssd)

    return ssd_list

def load_psu_data():
    psu_list = []

    with open("data/psu.csv", "r", encoding="utf-8") as file:
        psu_data = csv.DictReader(file)

        for row in psu_data:
            psu = PSU(
                row["name"],
                row["brand"],
                int(row["price"]),
                int(row["wattage"]),
                row["efficiency"]
            )

            psu_list.append(psu)

    return psu_list

def load_case_data():
    case_list = []

    with open("data/case.csv", "r", encoding="utf-8") as file:
        case_data = csv.DictReader(file)

        for row in case_data:
            pc_case = Case(
                row["name"],
                row["brand"],
                int(row["price"]),
                row["motherboard_size"],
                int(row["max_gpu_length"])
            )

            case_list.append(pc_case)

    return case_list