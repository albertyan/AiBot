import inspect
import os
import random
import time
from functools import wraps
from typing import Any, Callable, Optional, Type, TypeVar

from utils.log_util import logger

T = TypeVar("T")


def _get_perf_enabled() -> bool:
    """
    判断是否开启耗时统计
    为什么用环境变量：耗时统计通常只在定位问题时开启，用环境变量可以不改代码快速开关。
    """
    value = os.getenv("AIBOT_PERF_ENABLE", "1").strip().lower()
    return value in {"1", "true", "yes", "y", "on"}


def _get_sample_rate() -> float:
    """
    获取采样率（0~1）
    为什么要采样：在高频调用场景下，全量记录会放大 IO，采样能兼顾定位能力与性能开销。
    """
    raw = os.getenv("AIBOT_PERF_SAMPLE_RATE", "1").strip()
    try:
        rate = float(raw)
    except Exception:
        return 1.0
    if rate <= 0:
        return 0.0
    if rate >= 1:
        return 1.0
    return rate


def _should_sample() -> bool:
    """
    判断本次调用是否命中采样
    为什么单独封装：便于在装饰器与中间件中复用，并保持统一的采样策略。
    """
    rate = _get_sample_rate()
    if rate >= 1:
        return True
    if rate <= 0:
        return False
    return random.random() < rate


def perf_enabled() -> bool:
    """
    对外暴露的开关状态
    为什么单独提供：避免业务代码依赖内部实现细节（以下划线开头的函数）。
    """
    return _get_perf_enabled()


def perf_should_sample() -> bool:
    """
    对外暴露的采样判定
    为什么单独提供：让中间件与装饰器复用统一采样策略，避免两套逻辑导致数据不可比。
    """
    return _should_sample()


def timeit(name: Optional[str] = None) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    方法耗时统计装饰器（支持同步/异步）
    为什么用 perf_counter：它是单调递增计时器，更适合测量耗时，避免系统时间被调整带来的误差。
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        qualname = name or getattr(func, "__qualname__", getattr(func, "__name__", "unknown"))

        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any):  # type: ignore[misc]
                if not _get_perf_enabled() or not _should_sample():
                    return await func(*args, **kwargs)
                start = time.perf_counter()
                ok = True
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    ok = False
                    raise e
                finally:
                    cost_ms = (time.perf_counter() - start) * 1000
                    logger.debug(f"[perf] {qualname} cost={cost_ms:.2f}ms ok={ok}")

            return async_wrapper  # type: ignore[return-value]

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any):  # type: ignore[misc]
            if not _get_perf_enabled() or not _should_sample():
                return func(*args, **kwargs)
            start = time.perf_counter()
            ok = True
            try:
                return func(*args, **kwargs)
            except Exception as e:
                ok = False
                raise e
            finally:
                cost_ms = (time.perf_counter() - start) * 1000
                logger.debug(f"[perf] {qualname} cost={cost_ms:.2f}ms ok={ok}")

        return wrapper  # type: ignore[return-value]

    return decorator


def instrument_class(cls: Type[T], prefix: Optional[str] = None) -> Type[T]:
    """
    批量为类方法注入耗时统计
    为什么用“类级别注入”：可以一次性覆盖一个 Service 的所有公开方法，避免逐个手写装饰器导致遗漏。
    """
    for attr_name, attr_value in list(vars(cls).items()):
        if attr_name.startswith("__"):
            continue
        if attr_name.startswith("_"):
            continue
        if isinstance(attr_value, property):
            continue

        qual = f"{prefix}.{attr_name}" if prefix else f"{cls.__name__}.{attr_name}"

        if isinstance(attr_value, staticmethod):
            func = attr_value.__func__
            setattr(cls, attr_name, staticmethod(timeit(qual)(func)))
            continue

        if isinstance(attr_value, classmethod):
            func = attr_value.__func__
            setattr(cls, attr_name, classmethod(timeit(qual)(func)))
            continue

        if callable(attr_value):
            setattr(cls, attr_name, timeit(qual)(attr_value))

    return cls
