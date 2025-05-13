import os
import sys
import subprocess
import xml.etree.ElementTree as ET
from typing import List, Optional, Dict, Any
from pathlib import Path

class SVNClient:
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        """
        初始化 SVN 客户端
        :param username: SVN 用户名
        :param password: SVN 密码
        """
        self.username = username
        self.password = password
        self._check_svn_installed()

    def _check_svn_installed(self) -> None:
        """
        检查 SVN 是否已安装
        """
        try:
            subprocess.run(['svn', '--version'], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE, 
                         check=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            raise RuntimeError("SVN is not installed or not in PATH")

    def _run_command(self, command: List[str], cwd: Optional[str] = None) -> tuple:
        """
        执行 SVN 命令
        :param command: 命令列表
        :param cwd: 工作目录
        :return: (成功标志, 输出内容)
        """
        try:
            # 添加认证信息
            if self.username and self.password:
                command.extend(['--username', self.username, '--password', self.password])
            
            # 添加非交互式标志
            command.extend(['--non-interactive'])
            
            # 执行命令
            result = subprocess.run(command,
                                  cwd=cwd,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True,
                                  check=True)
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr

    def checkout(self, url: str, path: str, revision: Optional[int] = None) -> bool:
        """
        检出代码
        :param url: SVN 仓库地址
        :param path: 本地路径
        :param revision: 版本号
        :return: 是否成功
        """
        command = ['svn', 'checkout', url, path]
        if revision:
            command.extend(['-r', str(revision)])
        success, _ = self._run_command(command)
        return success

    def update(self, path: str, revision: Optional[int] = None) -> bool:
        """
        更新代码
        :param path: 本地路径
        :param revision: 版本号
        :return: 是否成功
        """
        command = ['svn', 'update', path]
        if revision:
            command.extend(['-r', str(revision)])
        success, _ = self._run_command(command, cwd=path)
        return success

    def commit(self, path: str, message: str) -> bool:
        """
        提交代码
        :param path: 本地路径
        :param message: 提交信息
        :return: 是否成功
        """
        command = ['svn', 'commit', '-m', message, path]
        success, _ = self._run_command(command, cwd=path)
        return success

    def add(self, path: str) -> bool:
        """
        添加文件到版本控制
        :param path: 文件路径
        :return: 是否成功
        """
        command = ['svn', 'add', path]
        success, _ = self._run_command(command, cwd=os.path.dirname(path))
        return success

    def delete(self, path: str) -> bool:
        """
        从版本控制中删除文件
        :param path: 文件路径
        :return: 是否成功
        """
        command = ['svn', 'delete', path]
        success, _ = self._run_command(command, cwd=os.path.dirname(path))
        return success

    def status(self, path: str) -> List[Dict[str, Any]]:
        """
        获取文件状态
        :param path: 路径
        :return: 状态列表
        """
        command = ['svn', 'status', '--xml', path]
        success, output = self._run_command(command, cwd=path)
        if not success:
            return []

        try:
            root = ET.fromstring(output)
            status_list = []
            for entry in root.findall('.//entry'):
                status_list.append({
                    'path': entry.get('path'),
                    'status': entry.find('wc-status').get('item'),
                    'revision': entry.find('wc-status').get('revision')
                })
            return status_list
        except ET.ParseError:
            return []

    def info(self, path: str) -> Optional[Dict[str, Any]]:
        """
        获取文件信息
        :param path: 路径
        :return: 文件信息
        """
        command = ['svn', 'info', '--xml', path]
        success, output = self._run_command(command, cwd=path)
        if not success:
            return None

        try:
            root = ET.fromstring(output)
            entry = root.find('entry')
            if entry is None:
                return None

            return {
                'url': entry.find('url').text,
                'revision': entry.get('revision'),
                'last_changed_rev': entry.find('commit').get('revision'),
                'last_changed_date': entry.find('commit/date').text,
                'last_changed_author': entry.find('commit/author').text
            }
        except (ET.ParseError, AttributeError):
            return None

    def log(self, path: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取提交日志
        :param path: 路径
        :param limit: 日志数量限制
        :return: 日志列表
        """
        command = ['svn', 'log', '--xml', '--limit', str(limit), path]
        success, output = self._run_command(command, cwd=path)
        if not success:
            return []

        try:
            root = ET.fromstring(output)
            log_list = []
            for logentry in root.findall('logentry'):
                log_list.append({
                    'revision': logentry.get('revision'),
                    'author': logentry.find('author').text,
                    'date': logentry.find('date').text,
                    'message': logentry.find('msg').text
                })
            return log_list
        except (ET.ParseError, AttributeError):
            return []

    def diff(self, path: str, revision1: Optional[int] = None, revision2: Optional[int] = None) -> Optional[str]:
        """
        获取文件差异
        :param path: 路径
        :param revision1: 起始版本
        :param revision2: 结束版本
        :return: 差异内容
        """
        command = ['svn', 'diff', path]
        if revision1 and revision2:
            command.extend(['-r', f'{revision1}:{revision2}'])
        elif revision1:
            command.extend(['-r', str(revision1)])
        
        success, output = self._run_command(command, cwd=path)
        return output if success else None

    def list(self, url: str) -> List[str]:
        """
        列出目录内容
        :param url: SVN 仓库地址
        :return: 文件列表
        """
        command = ['svn', 'list', '--xml', url]
        success, output = self._run_command(command)
        if not success:
            return []

        try:
            root = ET.fromstring(output)
            return [entry.text for entry in root.findall('.//name')]
        except ET.ParseError:
            return []

    def mkdir(self, url: str, message: str) -> bool:
        """
        创建目录
        :param url: 目录 URL
        :param message: 提交信息
        :return: 是否成功
        """
        command = ['svn', 'mkdir', '-m', message, url]
        success, _ = self._run_command(command)
        return success

    def move(self, src: str, dst: str, message: str) -> bool:
        """
        移动文件或目录
        :param src: 源路径
        :param dst: 目标路径
        :param message: 提交信息
        :return: 是否成功
        """
        command = ['svn', 'move', '-m', message, src, dst]
        success, _ = self._run_command(command)
        return success

    def copy(self, src: str, dst: str, message: str) -> bool:
        """
        复制文件或目录
        :param src: 源路径
        :param dst: 目标路径
        :param message: 提交信息
        :return: 是否成功
        """
        command = ['svn', 'copy', '-m', message, src, dst]
        success, _ = self._run_command(command)
        return success 