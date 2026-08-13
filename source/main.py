import csv

with open("data/cpu.csv", "r", encoding="utf-8") as file:
    cpu_data = csv.DictReader(file)

    for cpu in cpu_data:
        print(cpu)