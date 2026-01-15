# 示例：条件判断与循环
# 1. if-elif-else 条件判断
score = 85
if score >= 90:
    grade = "优秀"
elif score >= 80:
    grade = "良好"
elif score >= 70:
    grade = "中等"
else:
    grade = "待提高"
print("成绩等级:", grade)

# 复杂条件判断：列表与字典的综合判断
data = {
    "students": [
        {"name": "Alice", "scores": [90, 85, 92]},
        {"name": "Bob", "scores": [78, 82]},
        {"name": "Charlie", "scores": [95, 88, 91, 87]}
    ],
    "threshold": 85
}

# 判断字典中是否存在学生列表且非空
if "students" in data and isinstance(data["students"], list) and len(data["students"]) > 0:
    # 遍历每个学生
    for student in data["students"]:
        # 判断学生字典是否包含 name 和 scores，且 scores 为列表
        if isinstance(student, dict) and "name" in student and "scores" in student and isinstance(student["scores"], list):
            avg_score = sum(student["scores"]) / len(student["scores"])
            # 根据平均分与阈值比较给出评价
            if avg_score >= data["threshold"]:
                print(f"{student['name']} 的平均成绩为 {avg_score:.1f}，表现优秀。")
            else:
                print(f"{student['name']} 的平均成绩为 {avg_score:.1f}，需要继续努力。")
        else:
            print("学生数据格式错误，缺少必要字段或字段类型不正确。")
else:
    print("未找到学生数据或数据为空。")


# Python 3.10+ 支持 match-case（类似 switch-case）
score = 85
match score // 10:
    case 10 | 9:
        grade = "优秀"
    case 8:
        grade = "良好"
    case 7:
        grade = "中等"
    case _:
        grade = "待提高"
print("成绩等级:", grade)


# 2. for 循环：遍历列表
fruits = ["苹果", "香蕉", "橙子"]
print("水果列表:")
for fruit in fruits:
    print(" -", fruit)

# 3. while 循环：计数
count = 1
while count <= 5:
    print("当前计数:", count)
    count += 1

# 4. 嵌套循环：九九乘法表
for i in range(1, 10):  # 外层循环：控制被乘数，从1到9
    for j in range(1, i + 1):
        print(f"{j}×{i}={i*j}", end="\t")
    print()  # 换行