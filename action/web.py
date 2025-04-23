from typing import Union
from .convert import to_int
from lib import web 
from handler import routes 

def run(host: str = 'localhost', port: Union[str, int] = 8089):
    """启动服务器"""
    port = to_int(port, 8089)  # 如果转换失败，使用默认值 8089
    web.run_server(web.app, host, port) 
