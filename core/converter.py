import re
from typing import Any, Optional, List, Dict, Tuple, Callable
from datetime import datetime, date, time
from decimal import Decimal

class Converter:
    @staticmethod
    def to_int(value: str, default: Optional[int] = None) -> Optional[int]:
        """
        将字符串转换为整数
        :param value: 要转换的字符串
        :param default: 转换失败时的默认值
        :return: 转换后的整数或默认值
        """
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    @staticmethod
    def to_float(value: str, default: Optional[float] = None) -> Optional[float]:
        """
        将字符串转换为浮点数
        :param value: 要转换的字符串
        :param default: 转换失败时的默认值
        :return: 转换后的浮点数或默认值
        """
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    @staticmethod
    def to_bool(value: str, default: Optional[bool] = None) -> Optional[bool]:
        """
        将字符串转换为布尔值
        :param value: 要转换的字符串
        :param default: 转换失败时的默认值
        :return: 转换后的布尔值或默认值
        """
        if value.lower() in ('true', 'yes', '1', 'on'):
            return True
        elif value.lower() in ('false', 'no', '0', 'off'):
            return False
        return default

    @staticmethod
    def to_decimal(value: str, default: Optional[Decimal] = None) -> Optional[Decimal]:
        """
        将字符串转换为 Decimal
        :param value: 要转换的字符串
        :param default: 转换失败时的默认值
        :return: 转换后的 Decimal 或默认值
        """
        try:
            return Decimal(value)
        except (ValueError, TypeError):
            return default

    @staticmethod
    def to_datetime(value: str, fmt: str = '%Y-%m-%d %H:%M:%S', 
                   default: Optional[datetime] = None) -> Optional[datetime]:
        """
        将字符串转换为 datetime
        :param value: 要转换的字符串
        :param fmt: 日期时间格式
        :param default: 转换失败时的默认值
        :return: 转换后的 datetime 或默认值
        """
        try:
            return datetime.strptime(value, fmt)
        except (ValueError, TypeError):
            return default

    @staticmethod
    def to_date(value: str, fmt: str = '%Y-%m-%d', 
               default: Optional[date] = None) -> Optional[date]:
        """
        将字符串转换为 date
        :param value: 要转换的字符串
        :param fmt: 日期格式
        :param default: 转换失败时的默认值
        :return: 转换后的 date 或默认值
        """
        try:
            return datetime.strptime(value, fmt).date()
        except (ValueError, TypeError):
            return default

    @staticmethod
    def to_time(value: str, fmt: str = '%H:%M:%S', 
               default: Optional[time] = None) -> Optional[time]:
        """
        将字符串转换为 time
        :param value: 要转换的字符串
        :param fmt: 时间格式
        :param default: 转换失败时的默认值
        :return: 转换后的 time 或默认值
        """
        try:
            return datetime.strptime(value, fmt).time()
        except (ValueError, TypeError):
            return default

    @staticmethod
    def to_list(value: str, sep: str = ',', 
               converter: Optional[Callable] = None) -> List[Any]:
        """
        将字符串转换为列表
        :param value: 要转换的字符串
        :param sep: 分隔符
        :param converter: 元素转换函数
        :return: 转换后的列表
        """
        if not value:
            return []
        
        items = [item.strip() for item in value.split(sep)]
        if converter:
            return [converter(item) for item in items]
        return items

    @staticmethod
    def to_dict(value: str, item_sep: str = ',', 
               kv_sep: str = ':', converter: Optional[Callable] = None) -> Dict[str, Any]:
        """
        将字符串转换为字典
        :param value: 要转换的字符串
        :param item_sep: 项分隔符
        :param kv_sep: 键值分隔符
        :param converter: 值转换函数
        :return: 转换后的字典
        """
        if not value:
            return {}
        
        result = {}
        for item in value.split(item_sep):
            if kv_sep not in item:
                continue
            key, val = item.split(kv_sep, 1)
            key = key.strip()
            val = val.strip()
            if converter:
                val = converter(val)
            result[key] = val
        return result

    @staticmethod
    def to_tuple(value: str, sep: str = ',', 
                converter: Optional[Callable] = None) -> Tuple[Any, ...]:
        """
        将字符串转换为元组
        :param value: 要转换的字符串
        :param sep: 分隔符
        :param converter: 元素转换函数
        :return: 转换后的元组
        """
        if not value:
            return tuple()
        
        items = [item.strip() for item in value.split(sep)]
        if converter:
            return tuple(converter(item) for item in items)
        return tuple(items)

    @staticmethod
    def to_set(value: str, sep: str = ',', 
              converter: Optional[Callable] = None) -> set:
        """
        将字符串转换为集合
        :param value: 要转换的字符串
        :param sep: 分隔符
        :param converter: 元素转换函数
        :return: 转换后的集合
        """
        if not value:
            return set()
        
        items = [item.strip() for item in value.split(sep)]
        if converter:
            return {converter(item) for item in items}
        return set(items)

    @staticmethod
    def to_bytes(value: str, encoding: str = 'utf-8', 
                default: Optional[bytes] = None) -> Optional[bytes]:
        """
        将字符串转换为字节
        :param value: 要转换的字符串
        :param encoding: 编码方式
        :param default: 转换失败时的默认值
        :return: 转换后的字节或默认值
        """
        try:
            return value.encode(encoding)
        except (UnicodeEncodeError, AttributeError):
            return default

    @staticmethod
    def to_hex(value: str, default: Optional[int] = None) -> Optional[int]:
        """
        将十六进制字符串转换为整数
        :param value: 要转换的字符串
        :param default: 转换失败时的默认值
        :return: 转换后的整数或默认值
        """
        try:
            return int(value, 16)
        except (ValueError, TypeError):
            return default

    @staticmethod
    def to_binary(value: str, default: Optional[int] = None) -> Optional[int]:
        """
        将二进制字符串转换为整数
        :param value: 要转换的字符串
        :param default: 转换失败时的默认值
        :return: 转换后的整数或默认值
        """
        try:
            return int(value, 2)
        except (ValueError, TypeError):
            return default

    @staticmethod
    def to_octal(value: str, default: Optional[int] = None) -> Optional[int]:
        """
        将八进制字符串转换为整数
        :param value: 要转换的字符串
        :param default: 转换失败时的默认值
        :return: 转换后的整数或默认值
        """
        try:
            return int(value, 8)
        except (ValueError, TypeError):
            return default 