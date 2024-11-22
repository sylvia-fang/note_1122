import time
import datetime
import os
from colorama import Fore, init
import inspect
import functools

now_dir = os.path.dirname(os.path.dirname(__file__))  # 获取主目录路径
now_time = datetime.datetime.now()
str_time = now_time.strftime("%Y-%m-%d")
log_dir = now_dir + '/logs/'


def info_log(text):
    date = time.strftime('%H:%M:%S', time.localtime(time.time()))
    microsecond = datetime.datetime.now().strftime('%f')[:3]
    stack = inspect.stack()  # 获取方法执行的代码路径
    code_path = f"{os.path.basename(stack[1].filename)}:{stack[1].lineno}"
    log_text = "[INFO]{}-{}-{}\n".format(code_path, (date + '.' + microsecond), text)
    print(Fore.GREEN + log_text.strip())
    log_name = "{}_info.log".format(str_time)
    with open(log_dir + log_name, mode="a", encoding="utf-8") as f:
        f.write(log_text)


def error_log(text):
    date = time.strftime('%H:%M:%S', time.localtime(time.time()))
    microsecond = datetime.datetime.now().strftime('%f')[:3]
    stack = inspect.stack()  # 获取方法执行的代码路径
    code_path = f"{os.path.basename(stack[1].filename)}:{stack[1].lineno}"
    log_text = "[ERROR]{}-{}-{}\n".format(code_path, (date + '.' + microsecond), text)
    print(Fore.RED + str(log_text).strip())
    log_name = "{}_error.log".format(str_time)
    with open(log_dir + log_name, "a", encoding="utf-8") as f:
        f.write(log_text)


def warning_log(text):
    date = time.strftime('%H:%M:%S', time.localtime(time.time()))
    microsecond = datetime.datetime.now().strftime('%f')[:3]
    stack = inspect.stack()  # 获取方法执行的代码路径
    code_path = f"{os.path.basename(stack[1].filename)}:{stack[1].lineno}"
    log_text = "[WARN]{}-{}-{}\n".format(code_path, (date + '.' + microsecond), text)
    print(Fore.BLUE + str(log_text).strip())
    log_name = "{}_warn.log".format(str_time)
    with open(log_dir + log_name, "a", encoding="utf-8") as f:
        f.write(log_text)


def log_method_call(func):
    """用例的日志装饰器"""
    @functools.wraps(func)  # 不影响原有变量
    def wrapper(*args, **kwargs):
        info_log("--------------------CASE START---------------------------")
        class_name = args[0].__class__.__name__  # 获取类名
        method_name = func.__name__  # 获取方法名
        docstring = inspect.getdoc(func)  # 获取方法注释
        info_log(f'TestCase: {method_name} of class {class_name}')
        info_log(f"Describe: {docstring}")
        func(*args, **kwargs)
        info_log("--------------------CASE END---------------------------")
        return func

    return wrapper


def case_log_class(cls):
    """用例的日志装饰器类级别"""
    for name, method in inspect.getmembers(cls, inspect.isfunction):
        if name.startswith('testCase'):
            setattr(cls, name, log_method_call(method))
    return cls


if __name__ == '__main__':
    info_log("hello word!!!")
    error_log("error")
    warning_log("timeout")
