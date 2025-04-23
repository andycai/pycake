from typing import List, Optional
from lib.svn import SVNClient

def checkout(url: str, path: str, revision: Optional[int] = None) -> bool:
    """
    检出 SVN 仓库
    :param url: SVN 仓库地址
    :param path: 本地路径
    :param revision: 版本号（可选）
    :return: 是否成功
    """
    client = SVNClient()
    return client.checkout(url, path, revision)

def update(path: str, revision: Optional[int] = None) -> bool:
    """
    更新 SVN 仓库
    :param path: 本地路径
    :param revision: 版本号（可选）
    :return: 是否成功
    """
    client = SVNClient()
    return client.update(path, revision)

def commit(path: str, message: str) -> bool:
    """
    提交更改
    :param path: 本地路径
    :param message: 提交信息
    :return: 是否成功
    """
    client = SVNClient()
    return client.commit(path, message)

def status(path: str) -> List[dict]:
    """
    获取文件状态
    :param path: 本地路径
    :return: 状态列表
    """
    client = SVNClient()
    return client.status(path)

def info(path: str) -> Optional[dict]:
    """
    获取文件信息
    :param path: 本地路径
    :return: 文件信息
    """
    client = SVNClient()
    return client.info(path)

def log(path: str, limit: int = 10) -> List[dict]:
    """
    获取提交日志
    :param path: 本地路径
    :param limit: 日志数量限制
    :return: 日志列表
    """
    client = SVNClient()
    return client.log(path, limit)

def diff(path: str, revision1: Optional[int] = None, revision2: Optional[int] = None) -> Optional[str]:
    """
    获取文件差异
    :param path: 本地路径
    :param revision1: 起始版本（可选）
    :param revision2: 结束版本（可选）
    :return: 差异内容
    """
    client = SVNClient()
    return client.diff(path, revision1, revision2)

def list(url: str) -> List[str]:
    """
    列出目录内容
    :param url: SVN 仓库地址
    :return: 文件列表
    """
    client = SVNClient()
    return client.list(url)

def mkdir(url: str, message: str) -> bool:
    """
    创建目录
    :param url: 目录 URL
    :param message: 提交信息
    :return: 是否成功
    """
    client = SVNClient()
    return client.mkdir(url, message)

def move(src: str, dst: str, message: str) -> bool:
    """
    移动文件或目录
    :param src: 源路径
    :param dst: 目标路径
    :param message: 提交信息
    :return: 是否成功
    """
    client = SVNClient()
    return client.move(src, dst, message)

def copy(src: str, dst: str, message: str) -> bool:
    """
    复制文件或目录
    :param src: 源路径
    :param dst: 目标路径
    :param message: 提交信息
    :return: 是否成功
    """
    client = SVNClient()
    return client.copy(src, dst, message)
 