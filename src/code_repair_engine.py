import logging
import ast
import re
import subprocess
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

class CodeRepairEngine:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        self.model = self._initialize_model()
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler('code_repair_engine.log'),
                logging.StreamHandler()
            ]
        )
    
    def _initialize_model(self):
        """初始化修复模型"""
        try:
            model = GPT2LMHeadModel.from_pretrained('gpt2')
            return model
        except Exception as e:
            self.logger.error(f"Model initialization error: {str(e)}")
            return None
            
    def detect_and_fix_errors(self, code, language):
        """检测并修复代码中的错误"""
        try:
            # 分析错误
            errors = self._analyze_code_errors(code, language)
            if not errors:
                self.logger.info("No errors detected.")
                return code
                
            # 尝试修复错误
            fixed_code = self._generate_fix_for_errors(code, errors, language)
            
            # 检查修复是否成功
            if self._test_code(fixed_code, language):
                self.logger.info("Errors fixed successfully.")
                return fixed_code
            else:
                self.logger.error("Failed to fix errors.")
                return self.retry_fixing(fixed_code, language)
        except Exception as e:
            self.logger.error(f"Error fixing process failed: {str(e)}")
            return None
            
    def _analyze_code_errors(self, code, language):
        """分析代码中的错误"""
        errors = []
        try:
            if language == 'python':
                # 使用AST解析Python代码
                try:
                    ast.parse(code)
                except SyntaxError as e:
                    errors.append(str(e))
            elif language == 'javascript':
                # 使用正则表达式检查JavaScript代码
                if not re.match(r'^[\s\S]*;$', code):
                    errors.append("Missing semicolon at the end of the statement.")
            return errors
        except Exception as e:
            self.logger.error(f"Error analysis failed: {str(e)}")
            return errors
    
    def _generate_fix_for_errors(self, code, errors, language):
        """生成修复错误的代码"""
        try:
            fix_prompt = f"以下是一些关于{language}代码的错误：\n{errors}\n请生成修复后的代码：\n{code}"
            inputs = self.tokenizer.encode(fix_prompt, return_tensors='pt')
            outputs = self.model.generate(
                inputs,
                max_length=300,
                num_return_sequences=1,
                temperature=0.7
            )
            fixed_code = self.tokenizer.decode(outputs[0])
            return fixed_code
        except Exception as e:
            self.logger.error(f"Error fix generation failed: {str(e)}")
            return code
    
    def retry_fixing(self, code, language):
        """重试修复代码"""
        max_retries = 5
        for attempt in range(max_retries):
            self.logger.info(f"Retrying fix attempt {attempt + 1}/{max_retries}")
            errors = self._analyze_code_errors(code, language)
            if not errors:
                return code
            
            code = self._generate_fix_for_errors(code, errors, language)
            if self._test_code(code, language):
                return code
        self.logger.error("Max retry attempts reached. Failed to fix errors.")
        return None

    def _test_code(self, code, language):
        """测试修复后的代码"""
        try:
            if language == 'python':
                exec(code)
            elif language == 'javascript':
                with open('test.js', 'w') as f:
                    f.write(code)
                result = subprocess.run(['node', 'test.js'], capture_output=True, text=True)
                if result.returncode != 0:
                    raise RuntimeError(result.stderr)
            return True
        except Exception as e:
            self.logger.error(f"Code test failed: {str(e)}")
            return False

    def download_dependencies(self, dependencies):
        """下载所需的依赖项"""
        try:
            for dep in dependencies:
                subprocess.run(['pip', 'install', dep], check=True)
            self.logger.info("Dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to install dependencies: {str(e)}")