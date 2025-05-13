from core.converter import Converter

def to_int(value: str, default: int = 0) -> int:
    """
    将字符串转换为整数
    :param value: 要转换的字符串
    :param default: 转换失败时的默认值
    :return: 转换后的整数
    """
    return Converter.to_int(value, default)

def to_float(value: str, default: float = 0.0) -> float:
    """
    将字符串转换为浮点数
    :param value: 要转换的字符串
    :param default: 转换失败时的默认值
    :return: 转换后的浮点数
    """
    return Converter.to_float(value, default)

def to_bool(value: str, default: bool = False) -> bool:
    """
    将字符串转换为布尔值
    :param value: 要转换的字符串
    :param default: 转换失败时的默认值
    :return: 转换后的布尔值
    """
    return Converter.to_bool(value, default)

def to_datetime(value: str, fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    将字符串转换为 datetime 并返回格式化后的字符串
    :param value: 要转换的字符串
    :param fmt: 日期时间格式
    :return: 格式化后的日期时间字符串
    """
    dt = Converter.to_datetime(value, fmt)
    return dt.strftime(fmt) if dt else ''

def to_date(value: str, fmt: str = '%Y-%m-%d') -> str:
    """
    将字符串转换为 date 并返回格式化后的字符串
    :param value: 要转换的字符串
    :param fmt: 日期格式
    :return: 格式化后的日期字符串
    """
    d = Converter.to_date(value, fmt)
    return d.strftime(fmt) if d else ''

def to_time(value: str, fmt: str = '%H:%M:%S') -> str:
    """
    将字符串转换为 time 并返回格式化后的字符串
    :param value: 要转换的字符串
    :param fmt: 时间格式
    :return: 格式化后的时间字符串
    """
    t = Converter.to_time(value, fmt)
    return t.strftime(fmt) if t else ''

def to_list(value: str, sep: str = ',', converter: str = None) -> list:
    """
    将字符串转换为列表
    :param value: 要转换的字符串
    :param sep: 分隔符
    :param converter: 元素转换类型（int/float/bool）
    :return: 转换后的列表
    """
    if not converter:
        return Converter.to_list(value, sep)
    
    if converter == 'int':
        return Converter.to_list(value, sep, Converter.to_int)
    elif converter == 'float':
        return Converter.to_list(value, sep, Converter.to_float)
    elif converter == 'bool':
        return Converter.to_list(value, sep, Converter.to_bool)
    return Converter.to_list(value, sep)

def to_dict(value: str, item_sep: str = ',', kv_sep: str = ':', 
           converter: str = None) -> dict:
    """
    将字符串转换为字典
    :param value: 要转换的字符串
    :param item_sep: 项分隔符
    :param kv_sep: 键值分隔符
    :param converter: 值转换类型（int/float/bool）
    :return: 转换后的字典
    """
    if not converter:
        return Converter.to_dict(value, item_sep, kv_sep)
    
    if converter == 'int':
        return Converter.to_dict(value, item_sep, kv_sep, Converter.to_int)
    elif converter == 'float':
        return Converter.to_dict(value, item_sep, kv_sep, Converter.to_float)
    elif converter == 'bool':
        return Converter.to_dict(value, item_sep, kv_sep, Converter.to_bool)
    return Converter.to_dict(value, item_sep, kv_sep)

def to_hex(value: str, default: int = 0) -> int:
    """
    将十六进制字符串转换为整数
    :param value: 要转换的字符串
    :param default: 转换失败时的默认值
    :return: 转换后的整数
    """
    return Converter.to_hex(value, default)

def to_binary(value: str, default: int = 0) -> int:
    """
    将二进制字符串转换为整数
    :param value: 要转换的字符串
    :param default: 转换失败时的默认值
    :return: 转换后的整数
    """
    return Converter.to_binary(value, default)

def to_octal(value: str, default: int = 0) -> int:
    """
    将八进制字符串转换为整数
    :param value: 要转换的字符串
    :param default: 转换失败时的默认值
    :return: 转换后的整数
    """
    return Converter.to_octal(value, default) 