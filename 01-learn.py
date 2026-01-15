age = 20
# 定义一个浮点数
float_num = 3.14
# 创建一个布尔值
bool_value = True
# 创建一个字符串
string = "Hello, World!"
# 创建一个列表
list_ = [1, 2, 3, 4, 5]
# 创建一个元组
tuple_ = (1, 2, 3)
# 创建一个字典
dictionary = {"name": "John", "age": 25}

# 访问字典中的值
print(dictionary["name"])  # 输出: "John"

# 创建一个空列表
empty_list = []

# 创建一个空元组
empty_tuple = ()

# 创建一个空字典
empty_dictionary = {}


def judge_type(value):
    return type(value).__name__


print(judge_type(empty_list))
# 将整数转换为浮点数
float_from_int = float(age)
print(float_from_int)  # 输出: 20.0

# # 将浮点数转换为整数（小数部分被截断）
int_from_float = int(float_num)
print(int_from_float)  # 输出: 3

# # 将整数转换为字符串
# str_from_int = str(age)
# print(str_from_int)  # 输出: "20"

# # 将字符串转换为整数
# int_from_str = int("42")
# print(int_from_str)  # 输出: 42

# # 将布尔值转换为整数
# int_from_bool = int(bool_value)
# print(int_from_bool)  # 输出: 1

# # 将整数转换为布尔值
# bool_from_int = bool(0)
# print(bool_from_int)  # 输出: False

# # 将列表转换为元组
# tuple_from_list = tuple(list_)
# print(tuple_from_list)  # 输出: (1, 2, 3, 4, 5)

# # 将元组转换为列表
# list_from_tuple = list(tuple_)
# print(list_from_tuple)  # 输出: [1, 2, 3]

# 将字符串转换为列表（每个字符成为列表元素）
list_from_str = list("hello")

print(list_from_str)  # 输出: ['h', 'e', 'l', 'l', 'o']

str1 = "woshinidie"
# 字符串常用方法示例
s = "  Hello, Python!  "

# 去除首尾空格
print(s.strip())  # "Hello, Python!"

# 转换大小写
print(s.upper())  # "  HELLO, PYTHON!  "
print(s.lower())  # "  hello, python!  "

# 替换子串
print(s.replace("Python", "World"))  # "  Hello, World!  "

# 分割字符串
print(s.split(","))  # ['  Hello', ' Python!  ']

# 连接列表为字符串
print("-".join(["a", "b", "c"]))  # "a-b-c"

# 查找子串位置
print(s.find("Python"))  # 9
print(s.index("Python"))  # 9（找不到会抛异常）

# 统计子串出现次数
print(s.count("o"))  # 2

# 检查开头/结尾
print(s.startswith("  H"))  # True
print(s.endswith("!  "))  # True

# 判断字符串类型
print("123".isdigit())  # True
print("abc".isalpha())  # True
print("abc123".isalnum())  # True
print(" ".isspace())


# # 将列表拼接为字符串
# str_from_list = ''.join(['a', 'b', 'c'])
# print(str_from_list)  # 输出: "abc"

# 将字典的键转换为列表
keys_list = list(dictionary.keys())

print(keys_list)  # 输出: ['name', 'age']

# # 将字典的值转换为列表
values_list = list(dictionary.values())
print(values_list)  # 输出: ['John', 25]

# 列举列表的一些常用方法
list_example = [3, 1, 4, 1, 5, 9]

# 在末尾添加元素
list_example.append(2)
print("append(2):", list_example)

# 在指定位置插入元素
list_example.insert(1, 7)
print("insert(1, 7):", list_example)

# 删除并返回指定位置的元素（默认最后一个）
popped = list_example.pop()
print("pop():", popped, "-> list:", list_example)

# 删除首次出现的指定值
list_example.remove(1)
print("remove(1):", list_example)

# 返回首次出现的索引，可指定范围
idx = list_example.index(4)
print("index(4):", idx)

# 统计元素出现次数
cnt = list_example.count(1)
print("count(1):", cnt)

# 反转列表
list_example.reverse()
print("reverse():", list_example)

# 升序排序
list_example.sort()
print("sort():", list_example)

# 清空列表
list_example.clear()
print("clear():", list_example)

# 列举字典的常用方法
dict_example = {"name": "Alice", "age": 22, "city": "Beijing"}

# 获取字典中指定键的值，若键不存在可返回默认值
print(dict_example.get("name"))  # 输出: Alice
print(dict_example.get("country", "CN"))  # 输出: CN

# 添加或更新键值对
dict_example["email"] = "alice@example.com"
dict_example.update({"age": 23, "gender": "female"})
print("添加/更新后:", dict_example)

# 删除指定键并返回对应的值
removed_age = dict_example.pop("age")
print("pop('age'):", removed_age, "-> dict:", dict_example)

# 随机删除并返回一个键值对（Python 3.7+ 为末尾）
item = dict_example.popitem()
print("popitem():", item, "-> dict:", dict_example)

# 获取所有键
keys = dict_example.keys()
print("keys():", list(keys))

# 获取所有值
values = dict_example.values()
print("values():", list(values))

# 获取所有键值对
items = dict_example.items()
print("items():", list(items))

# 清空字典
dict_example.clear()
print("clear() 后:", dict_example)

# 创建字典副本
original = {"a": 1, "b": 2}
copy_dict = original.copy()
print("copy():", copy_dict)

# setdefault：若键存在则返回对应值，不存在则插入键并返回默认值
original.setdefault("c", 3)
print("setdefault('c', 3):", original)
value = original.setdefault("a", 99)
print("setdefault('a', 99) 返回值:", value, "-> dict:", original)

# fromkeys：用给定键序列创建新字典，值可指定
keys_seq = ["x", "y", "z"]
new_dict = dict.fromkeys(keys_seq, 0)
print("fromkeys 示例:", new_dict)
