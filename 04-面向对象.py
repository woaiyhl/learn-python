# 面向对象知识点示例：封装、继承、多态、抽象、类与对象、构造方法、属性、方法、命名规范
# 命名规范：类名使用 PascalCase，变量/方法名使用 snake_case，常量使用 UPPER_SNAKE_CASE，避免中文

import math
from abc import ABC, abstractmethod

# 常量定义
MAX_SPEED = 120
DEFAULT_COLOR = "white"


# 抽象基类：交通工具
class Vehicle(ABC):
    """抽象基类，定义交通工具的通用行为"""

    def __init__(self, brand: str, color: str = DEFAULT_COLOR):
        self._brand = brand  # 受保护变量，品牌
        self._color = color  # 受保护变量，颜色
        self._speed = 0  # 受保护变量，当前速度

    # 受保护方法：检查速度合法性
    def _validate_speed(self, speed: int) -> bool:
        return 0 <= speed <= MAX_SPEED

    # 公有方法：加速
    def accelerate(self, increment: int) -> None:
        new_speed = self._speed + increment
        if self._validate_speed(new_speed):
            self._speed = new_speed
        else:
            raise ValueError("Speed out of range")

    # 公有方法：获取品牌
    def get_brand(self) -> str:
        return self._brand

    # 公有方法：获取颜色
    def get_color(self) -> str:
        return self._color

    # 公有方法：获取速度
    def get_speed(self) -> int:
        return self._speed

    # 抽象方法：计算油耗（子类必须实现）
    @abstractmethod
    def calculate_fuel_consumption(self, distance: float) -> float:
        pass

    # 魔术方法：字符串表示
    def __str__(self) -> str:
        return f"{self._brand} vehicle, color={self._color}, speed={self._speed} km/h"


# 子类：汽车
class Car(Vehicle):
    """继承自 Vehicle，表示汽车"""

    def __init__(self, brand: str, color: str = DEFAULT_COLOR, seats: int = 5):
        super().__init__(brand, color)
        self._seats = seats  # 私有变量，座位数
        self._engine_started = False

    # 公有方法：启动引擎
    def start_engine(self) -> None:
        self._engine_started = True

    # 公有方法：停止引擎
    def stop_engine(self) -> None:
        self._engine_started = False
        self._speed = 0

    # 重写抽象方法：计算油耗
    def calculate_fuel_consumption(self, distance: float) -> float:
        # 假设每公里油耗 0.08 升
        return distance * 0.08

    # 魔术方法：字符串表示
    def __str__(self) -> str:
        return f"Car: {super().__str__()}, seats={self._seats}"


# 子类：自行车
class Bicycle(Vehicle):
    """继承自 Vehicle，表示自行车"""

    def __init__(self, brand: str, color: str = DEFAULT_COLOR, bike_type: str = "road"):
        super().__init__(brand, color)
        self._bike_type = bike_type  # 山地车、公路车等

    # 重写抽象方法：自行车无油耗，返回 0
    def calculate_fuel_consumption(self, distance: float) -> float:
        return 0.0

    # 公有方法：获取自行车类型
    def get_bike_type(self) -> str:
        return self._bike_type

    # 魔术方法：字符串表示
    def __str__(self) -> str:
        return f"Bicycle: {super().__str__()}, type={self._bike_type}"


# 多态示例：统一处理不同交通工具
def show_vehicle_info(vehicle: Vehicle) -> None:
    """多态：接收任意 Vehicle 子类对象"""
    print(vehicle)
    print(f"Fuel for 100km: {vehicle.calculate_fuel_consumption(100):.2f} L")


# 类变量与类方法示例
class MathUtils:
    """工具类，演示类变量与类方法"""

    PI = 3.141592653589793

    @classmethod
    def circle_area(cls, radius: float) -> float:
        return cls.PI * radius**2

    @staticmethod
    def add(a: float, b: float) -> float:
        return a + b


# 主程序入口
if __name__ == "__main__":
    # 创建对象
    my_car = Car("Toyota", "red", 5)
    my_bike = Bicycle("Giant", "blue", "mountain")

    # 使用对象方法
    my_car.accelerate(60)
    print("Car current speed:", my_car.get_speed())

    # 多态调用
    show_vehicle_info(my_car)
    show_vehicle_info(my_bike)

    # 使用类方法
    print("Circle area (r=5):", MathUtils.circle_area(5))
