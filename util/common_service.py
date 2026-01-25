from collections import defaultdict
from typing import Callable
from types import MethodType

from util.setter import argsetter

# ==============================
# 全局注册表
# ==============================

# { PageClassName: { method_name: { platform: func } } }
_PLATFORM_REGISTRY = defaultdict(lambda: defaultdict(dict))


# ==============================
# 平台装饰器（负责注册）
# ==============================

def platform_register(*platforms: str):
    """平台方法注册表，支持同一函数命名注册"""

    def decorator(func: Callable):
        qual = func.__qualname__  # LoginPage.input_username
        cls_name, method_name = qual.rsplit(".", 1)

        for p in platforms:
            _PLATFORM_REGISTRY[cls_name][method_name][p] = func

        return func

    return decorator


# ==============================
# Metaclass
# ==============================

class PageMeta(type):
    """平台方法分发，根据传入的test_platform映射回调注册的平台方法"""

    def __call__(cls, *args, **kwargs):
        test_platform = kwargs.pop("test_platform", argsetter.test_platform)
        if not test_platform:
            raise TypeError("test_platform is not be None")

        obj = super().__call__(*args, **kwargs)
        cls._bind_platform_methods(obj, test_platform)
        return obj

    def _bind_platform_methods(cls, obj, test_platform):
        """
        核心逻辑：
        - 沿 MRO 向上查找 registry
        - 子类优先
        """
        collected: dict[str, dict[str, Callable]] = {}

        # MRO: LoginPage -> BasePage -> object
        for base in cls.__mro__:
            name = base.__name__
            methods = _PLATFORM_REGISTRY.get(name)
            if not methods:
                continue

            for method_name, impls in methods.items():
                # 子类已定义则跳过（覆盖）
                if method_name not in collected:
                    collected[method_name] = impls

        # 绑定方法
        for method_name, impls in collected.items():
            func = impls.get(test_platform) or impls.get("default")

            if func is None:
                setattr(
                    obj,
                    method_name,
                    cls._unsupported(method_name, test_platform)
                )
            else:
                setattr(obj, method_name, MethodType(func, obj))

    @staticmethod
    def _unsupported(method, test_platform):
        def wrapper():
            raise NotImplementedError(
                f"{method} 不支持平台: {test_platform}"
            )

        return wrapper


def platform_mapper(*platform, default_key):
    """
    类装饰器：
    在类定义阶段，将类中 dict 属性根据 platform 循环映射为对应 value
    映射优先级：
        1. attr[platform]
        2. attr[default_key]
        3. 保留原 dict
    """

    def resolve_value(key, mapping: dict):
        if key in mapping:
            return mapping[key]
        if default_key in mapping:
            return mapping[default_key]
        return mapping

    def decorator(cls):
        for key in [*platform]:
            for name, attr in cls.__dict__.items():
                if not isinstance(attr, dict):
                    continue

                setattr(cls, name, resolve_value(key, attr))

        return cls

    return decorator
