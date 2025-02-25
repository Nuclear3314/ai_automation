from code_collector import CodeCollector
from code_analyzer import CodeAnalyzer
import json

def main():
    collector = CodeCollector()
    analyzer = CodeAnalyzer()
    
    # 示例1：收集GitHub代码
    print("Collecting GitHub code...")
    github_code = collector.collect_github_code("username", "repo-name")
    if github_code:
        print(f"Found {len(github_code)} files")
        
    # 示例2：收集Stack Overflow代码
    print("\nCollecting Stack Overflow examples...")
    stackoverflow_code = collector.collect_stackoverflow_code("python")
    if stackoverflow_code:
        print(f"Found {len(stackoverflow_code)} examples")
        
    # 示例3：分析Python代码
    python_code = """
def example_function(x):
    if x > 0:
        return x * 2
    return x

class ExampleClass:
    def __init__(self):
        self.value = 0
        
    def set_value(self, value):
        self.value = value
    """
    
    print("\nAnalyzing Python code...")
    python_analysis = analyzer.analyze_python_code(python_code)
    if python_analysis:
        print("\nPython Analysis Results:")
        print(json.dumps(python_analysis, indent=2))
        
    # 示例4：分析JavaScript代码
    javascript_code = """
function calculateSum(a, b) {
    return a + b;
}

class Calculator {
    constructor() {
        this.result = 0;
    }
    
    add(value) {
        this.result += value;
    }
}

const multiply = (a, b) => a * b;
"""
    
    print("\nAnalyzing JavaScript code...")
    js_analysis = analyzer.analyze_javascript_code(javascript_code)
    if js_analysis:
        print("\nJavaScript Analysis Results:")
        print(json.dumps(js_analysis, indent=2))

if __name__ == "__main__":
    main()