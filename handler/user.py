from core.web import get, post, put, delete, Request, Response

def register_routes(app):
    """注册用户相关路由"""
    pass

@get('/api/users')
def get_users(request: Request) -> Response:
    """获取用户列表"""
    users = [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'}
    ]
    return Response(users)

@post('/api/users')
def create_user(request: Request) -> Response:
    """创建用户"""
    if not request.body or 'name' not in request.body:
        return Response('Name is required', 400)
    
    # 这里应该将用户保存到数据库
    user = {'id': 3, 'name': request.body['name']}
    return Response(user, 201)

@get('/api/users/<user_id>')
def get_user(request: Request, user_id: str) -> Response:
    """获取单个用户"""
    # 这里应该从数据库获取用户
    user = {'id': int(user_id), 'name': 'User ' + user_id}
    return Response(user)

@put('/api/users/<user_id>')
def update_user(request: Request, user_id: str) -> Response:
    """更新用户"""
    if not request.body or 'name' not in request.body:
        return Response('Name is required', 400)
    
    # 这里应该更新数据库中的用户
    user = {'id': int(user_id), 'name': request.body['name']}
    return Response(user)

@delete('/api/users/<user_id>')
def delete_user(request: Request, user_id: str) -> Response:
    """删除用户"""
    # 这里应该从数据库删除用户
    return Response(None, 204) 