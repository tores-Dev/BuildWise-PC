##클래스
#부모
class PCPart:
    def __init__(self, name, brand, price):

        self.name = name
        self.brand = brand
        self.price = price

#중간 부모
class PerformancePart(PCPart):
    def __init__(self, name, brand, price, performance_score, power):
        super().__init__(name, brand, price)

        self.performance_score = performance_score
        self.power = power
        self.value_score = 0

#상속
class CPU(PerformancePart):
    def __init__(self, name, brand, price, socket, performance_score, power):
        super().__init__(name, brand, price, performance_score, power)

        self.socket = socket

class GPU(PerformancePart):
    def __init__(self, name, brand, price, performance_score, power, length):
        super().__init__(name, brand, price, performance_score, power)

        self.length = length

class Motherboard(PCPart):
    def __init__(self, name, brand, price, socket, memory_type, size):
        super().__init__(name, brand, price)

        self.socket = socket
        self.memory_type = memory_type
        self.size = size

class RAM(PCPart):
    def __init__(self, name, brand, price, memory_type, capacity):
        super().__init__(name, brand, price)

        self.memory_type = memory_type
        self.capacity = capacity

class SSD(PCPart):
    def __init__(self, name, brand, price, capacity, interface):
        super().__init__(name, brand, price)

        self.capacity = capacity
        self.interface = interface

class PSU(PCPart):
    def __init__(self, name, brand, price, wattage, efficiency):
        super().__init__(name, brand, price)

        self.wattage = wattage
        self.efficiency = efficiency

class Case(PCPart):
    def __init__(self, name, brand, price, motherboard_size, max_gpu_length):
        super().__init__(name, brand, price)

        self.motherboard_size = motherboard_size
        self.max_gpu_length = max_gpu_length