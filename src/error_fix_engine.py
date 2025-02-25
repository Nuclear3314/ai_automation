import logging
import ast
import re
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

class ErrorFixEngine:
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
                logging.FileHandler('error_fix_engine.log'),
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
                return None
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
                except SyntaxError as e