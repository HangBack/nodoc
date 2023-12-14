from typing import Callable
import time
import sys
from nodoc import const


def method_time_comparison(compare_func: Callable, iter_time: int = 1000):
    """
    方法耗时比较。
    - compare_func: Callable, 被比较的方法（函数）。
    - iter_time: int, 迭代次数，默认1000次，次数越高，耗时越久同时精度越高。
    """
    def comparison(func: Callable):
        def wrapper(*args, **kwargs):

            duration_A = [] # 待比较函数的平均耗时列表
            duration_B = [] # 被比较函数的平均耗时列表
            for _ in range(iter_time):
                start_time = time.time()
                func(*args, **kwargs)
                duration = time.time() - start_time
                duration_A.append(duration)

                start_time = time.time()
                compare_func(*args, **kwargs)
                duration = time.time() - start_time
                duration_B.append(duration)
                
            result_A = func(*args, **kwargs)
            result_B = compare_func(*args, **kwargs)

            duration_A = sum(duration_A) / len(duration_A)
            duration_B = sum(duration_B) / len(duration_B)
            fast_or_slow = (duration_A / duration_B) > 1.0
            fast_or_slow_scale = [
                duration_B / duration_A,
                duration_A / duration_B
            ]
            func_A = func.__name__
            func_B = compare_func.__name__
            if hasattr(args[0], func_A):
                args = list(args)
                args[0] = args[0].__class__.__name__ + ' 实例'
            args = "\n- " + "\n- ".join([str(arg) for arg in args])
            func_name_width = max(len(func_A), len(func_B))
            outer_A_iter = list(str(duration_A).split('.')[1])
            outer_B_iter = list(str(duration_B).split('.')[1])
            outer_A = 1
            outer_B = 1
            for number_A, number_B in zip(outer_A_iter, outer_B_iter):
                if number_A == '0':
                    outer_A += 1
                if number_B == '0':
                    outer_B += 1
            outer_A += 3
            outer_B += 3
            outer = max(outer_A, outer_B)
            print(f"""
方法耗时比较，总测试次数：{iter_time}。
位置参数: {args}
关键字参数: {kwargs}
[函数：{func_A: <{func_name_width}}] 平均耗时：{duration_A:.{outer}f}s。
[函数：{func_B: <{func_name_width}}] 平均耗时：{duration_B:.{outer}f}s。
返回值{['不同', '相同'][result_A == result_B]}。
{func_A} {['快', '慢'][fast_or_slow]} {func_B} {fast_or_slow_scale[fast_or_slow]:.{outer}f} 倍。
""")

            return result_A, result_B

        return wrapper

    return comparison
