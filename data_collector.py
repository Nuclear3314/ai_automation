import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from datetime import datetime

class DataCollector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler('data_collection.log'),
                logging.StreamHandler()
            ]
        )
    
    def collect_web_data(self, url):
        """从网页收集数据"""
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return BeautifulSoup(response.text, 'html.parser')
            else:
                self.logger.error(f"Failed to collect data from {url}, status code: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"Error collecting data from {url}: {str(e)}")
            return None
            
    def collect_stock_data(self, symbol):
        """收集股票数据"""
        try:
            import yfinance as yf
            stock = yf.Ticker(symbol)
            return stock.history(period="1mo")
        except Exception as e:
            self.logger.error(f"Error collecting stock data for {symbol}: {str(e)}")
            return None