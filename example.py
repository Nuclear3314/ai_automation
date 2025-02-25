from src.code_monster import CodeMonster

def main():
    # 创建代码怪物实例
    monster = CodeMonster()
    
    # 启动自动收集进程
    monster.start_collecting()
    
    # 示例：生成Python代码
    python_prompt = """
    创建一个函数，用于处理列表数据并返回统计信息
    """
    python_code = monster.generate_improved_code(python_prompt, 'python')
    if python_code:
        print("Generated Python Code:")
        print(python_code)
        
    # 示例：生成JavaScript代码
    js_prompt = """
    创建一个异步函数，用于处理API请求
    """
    js_code = monster.generate_improved_code(js_prompt, 'javascript')
    if js_code:
        print("\nGenerated JavaScript Code:")
        print(js_code)
        
    # 查看学习状态
    status = monster.get_learning_status()
    print("\nLearning Status:")
    print(json.dumps(status, indent=2))

if __name__ == "__main__":
    main()