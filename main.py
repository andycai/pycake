import sys
import importlib
from typing import List, Any

def execute_action(action_path: str, func_name: str, args: List[str]) -> Any:
    """
    动态执行指定模块中的函数
    :param action_path: 动作路径（例如：say.hello）
    :param func_name: 函数名
    :param args: 函数参数列表
    :return: 函数执行结果
    """
    try:
        # 构建模块路径
        module_path = f"action.{action_path}"
        
        # 动态导入模块
        module = importlib.import_module(module_path)
        
        # 获取函数
        func = getattr(module, func_name)
        
        # 执行函数
        return func(*args)
    except ImportError as e:
        print(f"Error: Could not find module '{module_path}'. {str(e)}")
        sys.exit(1)
    except AttributeError:
        print(f"Error: Function '{func_name}' not found in module '{module_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error executing function: {str(e)}")
        sys.exit(1)

def main():
    # 检查参数数量
    if len(sys.argv) < 2:
        print("Usage: python main.py <action.function> [args...]")
        print("Example: python main.py say.hello andy")
        print("Example: python main.py web.run_server localhost 8000")
        sys.exit(1)

    # 解析动作路径
    action_parts = sys.argv[1].split('.')
    if len(action_parts) != 2:
        print("Error: Action should be in format 'module.function'")
        sys.exit(1)

    action_path, func_name = action_parts[0], action_parts[1]
    args = sys.argv[2:]  # 获取其余参数

    # 执行动作
    result = execute_action(action_path, func_name, args)
    if result is not None:
        pass
        # print(result)

if __name__ == "__main__":
    main()
