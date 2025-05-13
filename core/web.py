from typing import Callable, Optional, Dict, Any, List
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from socketserver import ThreadingMixIn
import signal

class Request:
    def __init__(self, handler: BaseHTTPRequestHandler):
        self.method = handler.command
        self.path = handler.path
        self.headers = dict(handler.headers)
        self.body = {}
        
        # 解析请求体
        content_length = int(handler.headers.get('Content-Length', 0))
        if content_length > 0:
            body_data = handler.rfile.read(content_length)
            content_type = handler.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                self.body = json.loads(body_data.decode('utf-8'))
            else:
                # 解析表单数据
                form_data = urllib.parse.parse_qs(body_data.decode('utf-8'))
                self.body = {k: v[0] for k, v in form_data.items()}

class Response:
    def __init__(self, data=None, status_code=200):
        self.data = data
        self.status_code = status_code

    def send(self, handler: BaseHTTPRequestHandler):
        """发送响应"""
        handler.send_response(self.status_code)
        handler.send_header('Content-Type', 'application/json')
        handler.end_headers()
        
        if self.data is not None:
            if isinstance(self.data, (dict, list)):
                handler.wfile.write(json.dumps(self.data).encode('utf-8'))
            else:
                handler.wfile.write(str(self.data).encode('utf-8'))

class WebApp:
    def __init__(self):
        self.routes: Dict[str, Dict[str, Callable]] = {}
        self.middlewares: List[Callable] = []

    def add_route(self, method: str, path: str, handler: Callable):
        """添加路由"""
        if path not in self.routes:
            self.routes[path] = {}
        self.routes[path][method] = handler

    def add_middleware(self, middleware: Callable):
        """添加中间件"""
        self.middlewares.append(middleware)

    def get(self, path: str):
        """GET 路由装饰器"""
        def decorator(func: Callable):
            self.add_route('GET', path, func)
            return func
        return decorator

    def post(self, path: str):
        """POST 路由装饰器"""
        def decorator(func: Callable):
            self.add_route('POST', path, func)
            return func
        return decorator

    def put(self, path: str):
        """PUT 路由装饰器"""
        def decorator(func: Callable):
            self.add_route('PUT', path, func)
            return func
        return decorator

    def delete(self, path: str):
        """DELETE 路由装饰器"""
        def decorator(func: Callable):
            self.add_route('DELETE', path, func)
            return func
        return decorator

class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, app: WebApp, **kwargs):
        self.app = app
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.handle_request('GET')

    def do_POST(self):
        self.handle_request('POST')

    def do_PUT(self):
        self.handle_request('PUT')

    def do_DELETE(self):
        self.handle_request('DELETE')

    def handle_request(self, method: str):
        """处理请求"""
        # 创建请求对象
        request = Request(self)

        # 执行中间件
        for middleware in self.app.middlewares:
            response = middleware(request)
            if response is not None:
                response.send(self)
                return

        # 查找路由处理函数
        path = self.path.split('?')[0]  # 移除查询参数
        if path in self.app.routes and method in self.app.routes[path]:
            handler = self.app.routes[path][method]
            response = handler(request)
            response.send(self)
        else:
            Response('Not Found', 404).send(self)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """支持多线程的 HTTP 服务器"""

def run_server(app: WebApp, host: str = 'localhost', port: int = 8089):
    """启动服务器"""
    server = ThreadedHTTPServer((host, port), lambda *args, **kwargs: RequestHandler(*args, app=app, **kwargs))
    
    def signal_handler(signum, frame):
        print("\n正在关闭服务器...")
        # server.shutdown()
        server.server_close()
        print("服务器已关闭")
        exit(0)
    
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print(f"服务器运行在 http://{host}:{port}")
    print("按 Ctrl+C 可以优雅地关闭服务器")
    server.serve_forever()

# 创建全局应用实例
app = WebApp()

# 导出装饰器
get = app.get
post = app.post
put = app.put
delete = app.delete
add_middleware = app.add_middleware
