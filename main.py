from data_collector import DataCollector
from analyzer import Analyzer
import logging
from datetime import datetime

def main():
    # 创建实例
    collector = DataCollector()
    analyzer = Analyzer()
    
    # 示例：收集并分析股票数据
    symbol = "AAPL"  # 苹果公司股票
    stock_data = collector.collect_stock_data(symbol)
    
    if stock_data is not None:
        print(f"\nStock data for {symbol}:")
        print(stock_data.head())
        
        # 分析数据
        analysis_results = analyzer.analyze_data(stock_data)
        if analysis_results:
            print("\nAnalysis Results:")
            print(analysis_results['basic_stats'])
            
    # 示例：网页数据分析
    url = "https://example.com"
    web_data = collector.collect_web_data(url)
    if web_data:
        # 提取所有文本
        text = web_data.get_text()
        # 分析文本
        text_analysis = analyzer.process_text_data(text)
        if text_analysis:
            print("\nText Analysis Results:")
            print(text_analysis)

if __name__ == "__main__":
    main()