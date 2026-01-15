from collections.abc import Iterable
import math


def learn_function(input_data, target_value=None):
    """
    这是一个函数，用于学习函数的概念。
    """
    # 这里可以添加具体的学习逻辑
    if target_value is not None:
        # 有监督学习
        return f"已学习输入数据与目标值的关系: {input_data} -> {target_value}"
    else:
        # 无监督学习
        return f"已学习输入数据的模式: {input_data}"


def enhanced_learn_function(
    input_data,
    target_value=None,
    *,
    validation_mode=False,
    max_depth=10,
    tolerance_threshold=1e-5,
):
    """
    增强版学习函数，支持异常边界检测与复杂模式识别。
    参数:
        input_data: 任意可迭代对象或张量
        target_value: 监督学习标签，可为None
        validation_mode: 是否启用严格验证
        max_depth: 递归学习深度上限
        tolerance_threshold: 数值差异容忍度
    返回:
        学习结果字典，包含状态、消息与元数据
    """
    # 输入合法性检查
    if input_data is None:
        raise ValueError("输入数据不能为None")
    if max_depth <= 0:
        raise ValueError("最大深度必须为正整数")
    if tolerance_threshold <= 0:
        raise ValueError("容忍阈值必须为正数")

    # 类型与结构验证
    if validation_mode:
        if isinstance(input_data, (str, bytes)):
            raise TypeError("输入数据不能为字符串或字节串")
        if isinstance(input_data, Iterable):
            input_data = list(input_data)
            if any(x is None for x in input_data):
                raise ValueError("输入数据中包含None元素")
            if any(
                math.isnan(float(x)) or math.isinf(float(x))
                for x in input_data
                if isinstance(x, (int, float))
            ):
                raise ValueError("输入数据包含NaN或无穷大")
        if not isinstance(target_value, Iterable) or isinstance(
            target_value, (str, bytes)
        ):
            raise TypeError("目标值必须为可迭代对象或张量")

    # 空输入边界
    if not input_data:
        return {
            "status": "empty_input",
            "message": "检测到空输入，返回默认模式",
            "metadata": {"depth": 0, "type": "empty"},
        }

    # 目标值异常边界
    if target_value is not None:
        if isinstance(target_value, Iterable) and not isinstance(
            target_value, (str, bytes)
        ):
            target_value = list(target_value)
            if len(target_value) != len(input_data):
                raise ValueError("目标值长度与输入数据不一致")
        # 检查目标值中是否有异常数值
        if any(
            math.isnan(float(v)) or math.isinf(float(v))
            for v in target_value
            if isinstance(v, (int, float))
        ):
            raise ValueError("目标值包含NaN或无穷大")

    # 递归深度保护
    def recursive_learning(data, target, depth):
        if depth > max_depth:
            raise RecursionError("超过最大递归深度限制")
        if isinstance(data, list) and len(data) == 1:
            return recursive_learning(data[0], target[0] if target else None, depth + 1)
        return data, target, depth

    try:
        cleaned_data, cleaned_target, actual_depth = recursive_learning(
            input_data, target_value, 0
        )
    except RecursionError as e:
        return {
            "status": "exception",
            "message": str(e),
            "metadata": {"depth": max_depth, "type": "recursion_limit_exceeded"},
        }

    # 核心学习逻辑
    if target_value is not None:
        # 监督学习：检查线性可分性
        if isinstance(cleaned_data, list) and all(
            isinstance(x, (int, float)) for x in cleaned_data
        ):
            mean = sum(cleaned_data) / len(cleaned_data)
            variance = sum((x - mean) ** 2 for x in cleaned_data) / len(cleaned_data)
            if variance < tolerance_threshold:
                return {
                    "status": "success",
                    "message": f"低方差监督学习: 均值={mean:.4f}",
                    "metadata": {
                        "depth": actual_depth,
                        "type": "low_variance_supervised",
                    },
                }
        return {
            "status": "success",
            "message": f"监督学习完成: {cleaned_data} -> {cleaned_target}",
            "metadata": {"depth": actual_depth, "type": "supervised"},
        }
    else:
        # 无监督学习：聚类异常检测
        if isinstance(cleaned_data, list) and len(cleaned_data) > 1:
            sorted_data = sorted(cleaned_data)
            interquartile_range = sorted_data[-1] - sorted_data[0]
            if interquartile_range < tolerance_threshold:
                return {
                    "status": "success",
                    "message": "无监督学习检测到常数模式",
                    "metadata": {
                        "depth": actual_depth,
                        "type": "constant_unsupervised",
                    },
                }
        return {
            "status": "success",
            "message": f"无监督学习完成: 检测到模式于 {cleaned_data}",
            "metadata": {"depth": actual_depth, "type": "unsupervised"},
        }


def calculate_variance(data, *, sample=False, ddof=None):
    """
    计算给定数据的方差。

    参数:
        data: 可迭代对象，包含数值型数据
        sample: 是否计算样本方差（默认False，即计算总体方差）
        ddof: 自由度修正（Delta Degrees of Freedom），
              若提供则覆盖sample参数；样本方差对应ddof=1
    返回:
        方差值（float）
    异常:
        ValueError: 数据为空或长度不足
        TypeError: 数据包含非数值元素
    """
    if not data:
        raise ValueError("输入数据不能为空")

    # 转换为列表并检查数值类型
    try:
        values = [float(x) for x in data]
    except (TypeError, ValueError):
        raise TypeError("所有数据元素必须为数值类型")

    n = len(values)
    if n == 1 and (sample or (ddof is not None and ddof > 0)):
        raise ValueError("样本方差需要至少两个数据点")

    # 确定自由度
    if ddof is None:
        ddof = 1 if sample else 0
    if ddof < 0:
        raise ValueError("ddof不能为负数")
    if n - ddof <= 0:
        raise ValueError("自由度必须为正数")

    mean = sum(values) / n
    squared_diffs = [(x - mean) ** 2 for x in values]
    variance = sum(squared_diffs) / (n - ddof)
    return variance
