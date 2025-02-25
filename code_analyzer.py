import re
import ast
import logging
from collections import Counter
import networkx as nx
from datetime import datetime

class CodeAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler('code_analysis.log'),
                logging.StreamHandler()
            ]
        )

    def analyze_python_code(self, code_str):
        """分析Python代码"""
        try:
            tree = ast.parse(code_str)
            analysis = {
                'functions': self._get_functions(tree),
                'classes': self._get_classes(tree),
                'imports': self._get_imports(tree),
                'complexity': self._calculate_complexity(tree)
            }
            return analysis
        except Exception as e:
            self.logger.error(f"Python code analysis error: {str(e)}")
            return None

    def analyze_javascript_code(self, code_str):
        """分析JavaScript代码"""
        try:
            analysis = {
                'functions': self._find_js_functions(code_str),
                'classes': self._find_js_classes(code_str),
                'imports': self._find_js_imports(code_str),
                'complexity': self._estimate_js_complexity(code_str)
            }
            return analysis
        except Exception as e:
            self.logger.error(f"JavaScript code analysis error: {str(e)}")
            return None

    def _get_functions(self, tree):
        """获取Python函数信息"""
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    'name': node.name,
                    'args': [arg.arg for arg in node.args.args],
                    'line_number': node.lineno
                })
        return functions

    def _get_classes(self, tree):
        """获取Python类信息"""
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append({
                    'name': node.name,
                    'bases': [base.id for base in node.bases if isinstance(base, ast.Name)],
                    'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
                    'line_number': node.lineno
                })
        return classes

    def _get_imports(self, tree):
        """获取Python导入信息"""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports.append(name.name)
                else:
                    module = node.module if node.module else ''
                    for name in node.names:
                        imports.append(f"{module}.{name.name}")
        return imports

    def _calculate_complexity(self, tree):
        """计算代码复杂度"""
        complexity = 1
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.FunctionDef, ast.ClassDef)):
                complexity += 1
        return complexity

    def _find_js_functions(self, code_str):
        """查找JavaScript函数"""
        function_pattern = r'function\s+(\w+)\s*\([^)]*\)'
        arrow_pattern = r'(?:const|let|var)?\s*(\w+)\s*=\s*\([^)]*\)\s*=>'
        functions = []
        
        # 查找普通函数
        for match in re.finditer(function_pattern, code_str):
            functions.append({
                'name': match.group(1),
                'type': 'function'
            })
            
        # 查找箭头函数
        for match in re.finditer(arrow_pattern, code_str):
            functions.append({
                'name': match.group(1),
                'type': 'arrow_function'
            })
            
        return functions

    def _find_js_classes(self, code_str):
        """查找JavaScript类"""
        class_pattern = r'class\s+(\w+)(?:\s+extends\s+(\w+))?\s*{'
        classes = []
        
        for match in re.finditer(class_pattern, code_str):
            classes.append({
                'name': match.group(1),
                'extends': match.group(2) if match.group(2) else None
            })
            
        return classes

    def _find_js_imports(self, code_str):
        """查找JavaScript导入"""
        import_pattern = r'import\s+(?:{[^}]+}|[^;]+)\s+from\s+[\'"]([^\'"]+)[\'"]'
        require_pattern = r'(?:const|let|var)\s+\w+\s*=\s*require\([\'"]([^\'"]+)[\'"]\)'
        
        imports = []
        
        # 查找ES6导入
        for match in re.finditer(import_pattern, code_str):
            imports.append({
                'module': match.group(1),
                'type': 'es6'
            })
            
        # 查找require导入
        for match in re.finditer(require_pattern, code_str):
            imports.append({
                'module': match.group(1),
                'type': 'require'
            })
            
        return imports

    def _estimate_js_complexity(self, code_str):
        """估算JavaScript代码复杂度"""
        complexity = 1
        patterns = [
            r'\bif\b',
            r'\bfor\b',
            r'\bwhile\b',
            r'\bswitch\b',
            r'\bcatch\b',
            r'\bfunction\b',
            r'=>'
        ]
        
        for pattern in patterns:
            complexity += len(re.findall(pattern, code_str))
            
        return complexity