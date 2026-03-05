from __future__ import annotations
import json
import os
from typing import Any, Dict, Optional, Type, TypeVar
from loguru import logger
from pydantic import BaseModel, ValidationError
from utils.config_file import get_base_dir

T = TypeVar("T", bound=BaseModel)

class JSONConfigStore:
    """
    配置文件通用基类
    为什么需要基类：抽取加载与保存的通用逻辑，避免每个配置重复实现IO与序列化代码，降低维护成本
    """
    def __init__(self, file_name: str, base_dir: Optional[str] = None):
        # 为什么按用户目录组织：运行时配置应存放于用户目录，避免覆盖仓库中的示例配置
        self.base_dir = base_dir or get_base_dir()
        self.file_path = os.path.join(self.base_dir, file_name)
        # 确保目录存在，防止首次保存失败
        os.makedirs(self.base_dir, exist_ok=True)

    def _read_json(self) -> Dict[str, Any]:
        # 为什么单独封装：统一异常处理与日志，便于排查问题
        if not os.path.exists(self.file_path):
            logger.warning(f"Config not found, use default: {self.file_path}")
            return {}
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Read config failed: {self.file_path}, error: {e}")
            return {}

    def _write_json(self, data: Dict[str, Any]) -> None:
        # 为什么强制UTF-8且美化：便于人工查看与编辑
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"Write config failed: {self.file_path}, error: {e}")
            raise

    @staticmethod
    def _model_to_dict(model: BaseModel) -> Dict[str, Any]:
        # 为什么使用 model_dump：当前项目使用的是 Pydantic v2，直接使用标准导出API更简洁高效
        return model.model_dump(exclude_none=True)

    def load_model(self, model_cls: Type[T], root_key: Optional[str] = None, default: Optional[Dict[str, Any]] = None) -> T:
        """
        加载配置为Pydantic模型
        为什么返回模型：保障配置的结构化与类型安全，避免使用时再做各种判空
        """
        raw = self._read_json()
        payload = raw.get(root_key, raw) if root_key else raw
        if payload in (None, {}, []) and default is not None:
            payload = default
        try:
            return model_cls(**(payload or {}))
        except ValidationError as e:
            logger.error(f"Validation error for {self.file_path}: {e}")
            # 出错时使用默认值兜底，避免全局崩溃
            return model_cls(**(default or {}))

    def save_model(self, model: BaseModel, root_key: Optional[str] = None) -> None:
        """
        将Pydantic模型保存到配置文件
        为什么通过root_key：兼容部分配置文件使用顶层包裹键的结构
        """
        data = self._model_to_dict(model)
        target = self._read_json()
        if root_key:
            target[root_key] = data
        else:
            target = data
        self._write_json(target)
