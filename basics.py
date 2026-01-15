# Python 基础语法速览

# 1. 变量与基本数据类型 (无需声明类型，自动推导)
name = "Python Learner"  # 字符串
age = 1  # 整数
is_ready = True  # 布尔值
skills = ["Linux", "Network", "Database"]  # 列表 (List)
config = {"host": "localhost", "port": 8080}  # 字典 (Dictionary)

print(f"Hello, {name}! 准备好开始学习了吗? {is_ready}")

# 2. 控制流
if "Python" in skills:
    print("你已经懂 Python 了？")
else:
    print("正在添加 Python 到技能树...")
    skills.append("Python")

# 循环
print("当前技能:")
for skill in skills:
    print(f"- {skill}")

# 3. 函数 (Function)
def greet(user_name: str, greeting: str = "Welcome") -> str:
    """
    这是一个带有类型提示的函数。
    类型提示(Type Hints)在现代 Python 开发中非常重要。
    """
    return f"{greeting}, {user_name}!"

message = greet(name)
print(message)

# 4. 类与对象 (面向对象编程)
class WebServer:
    def __init__(self, name: str, port: int):
        self.name = name
        self.port = port
        self.is_running = False

    def start(self):
        self.is_running = True
        print(f"[{self.name}] 服务已启动，监听端口: {self.port}")

    def stop(self):
        self.is_running = False
        print(f"[{self.name}] 服务已停止")

# 实例化并使用类
my_server = WebServer("MyFirstApp", 8000)
my_server.start()