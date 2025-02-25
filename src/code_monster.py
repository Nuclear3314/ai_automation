from .learning_engine import CodeLearningEngine
from .code_repair_engine import CodeRepairEngine
import requests
import logging
from datetime import datetime
import threading
import queue
import json
import os

class CodeMonster:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        self.learning_engine = CodeLearningEngine()
        self.code_repair_engine = CodeRepairEngine()
        self.code_queue = queue.Queue()
        self.processed_urls = set()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler('code_monster.log'),
                logging.StreamHandler()
            ]
        )
        
    def start_collecting(self):
        """开始收集代码"""
        # 启动多线程收集器
        collector_thread = threading.Thread(target=self._collect_code)
        processor_thread = threading.Thread(target=self._process_code)
        
        collector_thread.start()
        processor_thread.start()
        
    def _collect_code(self):
        """收集代码的线程"""
        while True:
            try:
                # 从多个源收集代码
                self._collect_from_github()
                self._collect_from_gitlab()
                self._collect_from_stackoverflow()
                # 等待一段时间再继续收集
                time.sleep(3600)  # 每小时收集一次
            except Exception as e:
                self.logger.error(f"Code collection error: {str(e)}")
                
    def _process_code(self):
        """处理代码的线程"""
        while True:
            try:
                # 从队列获取代码
                code_data = self.code_queue.get()
                if code_data is None:
                    continue
                    
                # 学习代码模式
                self.learning_engine.learn_from_code(
                    code_data['code'],
                    code_data['language']
                )
                
                # 标记URL为已处理
                self.processed_urls.add(code_data['url'])
                
            except Exception as e:
                self.logger.error(f"Code processing error: {str(e)}")
                
    def generate_improved_code(self, prompt, language):
        """生成改进的代码"""
        try:
            # 使用学习引擎生成代码
            generated_code = self.learning_engine.generate_code(prompt, language)
            
            if generated_code:
                self.logger.info(f"Successfully generated code for {language}")
                
                # 检测并修复代码中的错误
                fixed_code = self.code_repair_engine.detect_and_fix_errors(generated_code, language)
                
                if fixed_code:
                    self.logger.info(f"Successfully fixed code for {language}")
                    return fixed_code
                else:
                    self.logger.error("Failed to fix code")
                    return None
            else:
                self.logger.error("Failed to generate code")
                return None
                
        except Exception as e:
            self.logger.error(f"Code generation error: {str(e)}")
            return None
            
    def get_learning_status(self):
        """获取学习状态"""
        return {
            'processed_urls': len(self.processed_urls),
            'knowledge_base_size': len(self.learning_engine.code_patterns),
            'supported_languages': list(self.learning_engine.knowledge_base.keys())
        }