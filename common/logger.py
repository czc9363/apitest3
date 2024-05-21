import functools
import inspect
import os
from datetime import datetime

from colorama import Fore

from run import DIR


def info(text):
    stack = inspect.stack()
    formatted_time = datetime.now().strftime('%H:%M:%S:%f')[:-3]
    code_path = f"{os.path.basename(stack[1].filename)}:{stack[1].lineno}"
    content = f"[info]{formatted_time}-{code_path} >> {text}"
    print(Fore.LIGHTGREEN_EX + content)
    str_time = datetime.now().strftime("%Y%m%d")
    with open(file=DIR + '\\logs\\' + f"{str_time}_info.log", mode="a", encoding='utf-8') as f:
        f.write(content + "\n")


def step(text):
    stack = inspect.stack()
    formatted_time = datetime.now().strftime('%H:%M:%S:%f')[:-3]
    code_path = f"{os.path.basename(stack[1].filename)}:{stack[1].lineno}"
    content = f"[step]{formatted_time}-{code_path} >> {text}"
    print(Fore.LIGHTCYAN_EX + content)
    str_time = datetime.now().strftime("%Y%m%d")
    with open(file=DIR + '\\logs\\' + f"{str_time}_info.log", mode="a", encoding='utf-8') as f:
        f.write(content + "\n")


def error(text):
    stack = inspect.stack()
    formatted_time = datetime.now().strftime('%H:%M:%S:%f')[:-3]
    code_path = f"{os.path.basename(stack[1].filename)}:{stack[1].lineno}"
    content = f"[ERROR]{formatted_time}-{code_path} >> {text}"
    print(Fore.LIGHTRED_EX + content)
    str_time = datetime.now().strftime("%Y%m%d")
    with open(file=DIR + '\\logs\\' + f"{str_time}_info.log", mode="a", encoding='utf-8') as f:
        f.write(content + "\n")



def case_log_init(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        class_name = args[0].__class__.__name__
        method_name = func.__name__
        docstring = inspect.getdoc(func)  # 获取方法注释
        print(Fore.LIGHTRED_EX + '====================')
        info(f'Class NAME:{class_name}')
        info(f'Method NAME:{method_name}')
        info(f'Test Description:{docstring}')
        func(*args, **kwargs)

    return inner


def class_case_log(cls):
    # 用例的日志装饰器
    for name, method in inspect.getmembers(cls, inspect.isfunction):
        if name.startswith('testCase'):
            setattr(cls, name, case_log_init(method))
    return cls