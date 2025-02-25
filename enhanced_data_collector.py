import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import xml.etree.ElementTree as ET
import sqlite3
import pymongo
import redis
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging
import aiohttp
import asyncio
from datetime import datetime

class EnhancedDataCollector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        self.mongo_client = None
        self.redis_client = None
        self.setup_database_connections()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler('enhanced_data_collection.log'),
                logging.StreamHandler()
            ]
        )
        
    def setup_database_connections(self):
        """设置数据库连接"""
        try:
            # MongoDB连接
            self.mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
            # Redis连接
            self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        except Exception as e:
            self.logger.error(f"Database connection error: {str(e)}")
    
    async def collect_api_data(self, api_url, headers=None):
        """异步收集API数据"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=headers) as response:
                    return await response.json()
        except Exception as e:
            self.logger.error(f"API data collection error: {str(e)}")
            return None

    def collect_dynamic_web_data(self, url):
        """使用Selenium收集动态网页数据"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            content = driver.page_source
            driver.quit()
            return BeautifulSoup(content, 'html.parser')
        except Exception as e:
            self.logger.error(f"Dynamic web data collection error: {str(e)}")
            return None

    def parse_xml_feed(self, xml_url):
        """解析XML/RSS源"""
        try:
            response = requests.get(xml_url)
            root = ET.fromstring(response.content)
            return root
        except Exception as e:
            self.logger.error(f"XML parsing error: {str(e)}")
            return None

    def collect_database_data(self, query, db_type='sqlite'):
        """从数据库收集数据"""
        try:
            if db_type == 'sqlite':
                conn = sqlite3.connect('your_database.db')
                data = pd.read_sql_query(query, conn)
                conn.close()
                return data
            elif db_type == 'mongodb':
                if self.mongo_client:
                    db = self.mongo_client['your_database']
                    return list(db.your_collection.find(query))
        except Exception as e:
            self.logger.error(f"Database data collection error: {str(e)}")
            return None

    def cache_data(self, key, data):
        """缓存数据到Redis"""
        try:
            if self.redis_client:
                self.redis_client.setex(key, 3600, json.dumps(data))  # 1小时过期
        except Exception as e:
            self.logger.error(f"Data caching error: {str(e)}")