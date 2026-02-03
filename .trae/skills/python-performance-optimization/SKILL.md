---
name: "python-performance-optimization"
description: "Python 性能优化专家。在分析性能瓶颈、优化 CPU/内存使用或需要提升代码执行效率时调用。涵盖 Profiling、算法优化及内存管理。"
---

# Python 性能优化指南

你是一位 Python 性能优化专家。你的目标是帮助用户识别代码瓶颈，减少延迟，降低内存消耗，并实施高效的算法或实现模式。

## 何时使用此技能

- 识别 Python 应用程序中的性能瓶颈
- 减少应用程序延迟和响应时间
- 优化 CPU 密集型操作
- 减少内存消耗和内存泄漏
- 提高数据库查询性能
- 优化 I/O 操作
- 加速数据处理管道
- 实施高性能算法
- 对生产环境应用进行性能分析 (Profiling)

## 核心概念

### 1. 性能分析类型 (Profiling Types)
- **CPU Profiling**: 识别耗时函数（如 `cProfile`）。
- **Memory Profiling**: 追踪内存分配和泄漏（如 `memory_profiler`）。
- **Line Profiling**: 逐行分析代码性能（如 `line_profiler`）。
- **Call Graph**: 可视化函数调用关系。

### 2. 性能指标 (Metrics)
- **执行时间**: 操作耗时。
- **内存使用**: 峰值和平均内存消耗。
- **CPU 利用率**: 处理器使用模式。
- **I/O 等待**: I/O 操作花费的时间。

### 3. 优化策略
- **算法优化**: 选择更优的算法和数据结构（如从 O(N^2) 到 O(N log N)）。
- **实现优化**: 使用更高效的代码模式（如列表推导式代替循环）。
- **并行化**: 多线程 (I/O 密集型) / 多进程 (CPU 密集型)。
- **缓存**: 避免重复计算 (`functools.lru_cache`)。
- **原生扩展**: 对关键路径使用 C/Rust 扩展（如 NumPy, Cython）。

## 常用工具与模式

### 模式 1: cProfile - CPU 性能分析
用于从宏观层面找出哪些函数最耗时。

```python
import cProfile
import pstats
from pstats import SortKey

def main():
    # 你的主逻辑
    pass

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    
    main()
    
    profiler.disable()
    
    # 打印前 10 个最耗时的函数
    stats = pstats.Stats(profiler)
    stats.sort_stats(SortKey.CUMULATIVE)
    stats.print_stats(10)
    
    # 保存结果供后续分析 (如使用 snakeviz 可视化)
    stats.dump_stats("profile_output.prof")
```

### 模式 2: line_profiler - 逐行分析
用于深入分析特定函数的每一行耗时。

```python
# 需要安装: pip install line-profiler
# 使用 @profile 装饰器 (kernprof 运行时会自动注入，或手动配置)

@profile
def process_data(data):
    result = []
    for item in data:
        # 找出哪一行最慢
        processed = item * 2
        result.append(processed)
    return result

# 命令行运行: kernprof -l -v script.py
```

### 模式 3: memory_profiler - 内存监控
用于检测内存泄漏和高内存消耗点。

```python
# 需要安装: pip install memory-profiler
from memory_profiler import profile

@profile
def memory_intensive():
    # 创建大列表
    big_list = [i for i in range(1000000)]
    return sum(big_list)

# 命令行运行: python -m memory_profiler script.py
```

### 模式 4: py-spy - 生产环境分析
非侵入式分析正在运行的进程，开销极低。

```bash
# 安装: pip install py-spy

# 生成火焰图 (Flamegraph)
py-spy record -o profile.svg --pid 12345

# 实时查看 Top 耗时
py-spy top --pid 12345
```

### 模式 5: 代码级优化示例

**列表推导式 vs 循环**
```python
# 慢
res = []
for i in range(1000):
    res.append(i**2)

# 快 (通常快 20%+)
res = [i**2 for i in range(1000)]
```

**集合查找 (Set Lookup)**
```python
# 慢 (O(N))
if item in list_of_items:
    pass

# 快 (O(1))
set_of_items = set(list_of_items)
if item in set_of_items:
    pass
```

## 最佳实践清单
1. **先测量，再优化**: 不要凭直觉，使用 Profiler 找到真正的瓶颈。
2. **算法优先**: 糟糕的算法（如嵌套循环）通常是性能杀手，代码层面的微优化无法弥补算法的缺陷。
3. **利用标准库**: Python 内置模块（如 `itertools`, `collections`）通常是用 C 实现的，比手写 Python 代码快。
4. **向量化操作**: 处理数值计算时，优先使用 NumPy/Pandas 的向量化操作，避免 Python 循环。
