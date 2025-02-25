import requests
from bs4 import BeautifulSoup
import logging
import json
from datetime import datetime
import re
import os

class CodeCollector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler('code_collection.log'),
                logging.StreamHandler()
            ]
        )

    def collect_github_code(self, owner, repo, path=""):
        """从GitHub收集代码"""
        try:
            api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
            response = requests.get(api_url, headers=self.headers)
            if response.status_code == 200:
                contents = response.json()
                if isinstance(contents, list):
                    return [item for item in contents if item['type'] == 'file']
                else:
                    return [contents] if contents['type'] == 'file' else []
            else:
                self.logger.error(f"Failed to collect GitHub code: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"GitHub collection error: {str(e)}")
            return None

    def collect_stackoverflow_code(self, tag, limit=10):
        """从Stack Overflow收集代码示例"""
        try:
            api_url = f"https://api.stackexchange.com/2.3/questions"
            params = {
                'tagged': tag,
                'sort': 'votes',
                'site': 'stackoverflow',
                'pagesize': limit
            }
            response = requests.get(api_url, params=params)
            if response.status_code == 200:
                return response.json()['items']
            else:
                self.logger.error(f"Failed to collect Stack Overflow code: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"Stack Overflow collection error: {str(e)}")
            return None

    def collect_gitlab_code(self, project_id, branch='main'):
        """从GitLab收集代码"""
        try:
            api_url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/tree"
            params = {'ref': branch}
            response = requests.get(api_url, params=params, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Failed to collect GitLab code: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"GitLab collection error: {str(e)}")
            return None

    def collect_npm_package_code(self, package_name):
        """从NPM收集包信息和代码"""
        try:
            api_url = f"https://registry.npmjs.org/{package_name}"
            response = requests.get(api_url)
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Failed to collect NPM package info: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"NPM collection error: {str(e)}")
            return None

    def collect_pypi_package_code(self, package_name):
        """从PyPI收集包信息和代码"""
        try:
            api_url = f"https://pypi.org/pypi/{package_name}/json"
            response = requests.get(api_url)
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Failed to collect PyPI package info: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"PyPI collection error: {str(e)}")
            return None

    def save_code(self, code_data, file_path):
        """保存收集到的代码"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                if isinstance(code_data, dict):
                    json.dump(code_data, f, indent=2)
                else:
                    f.write(str(code_data))
            return True
        except Exception as e:
            self.logger.error(f"Code saving error: {str(e)}")
            return False