"""
API 请求基类
"""

import requests


class BaseAPI:
    """API 基类"""

    def __init__(self, base_url: str = "http://shop-xo.hctestedu.com"):
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, path: str, **kwargs):
        """GET 请求"""
        url = f"{self.base_url}{path}"
        return self.session.get(url, **kwargs)

    def post(self, path: str, **kwargs):
        """POST 请求"""
        url = f"{self.base_url}{path}"
        return self.session.post(url, **kwargs)

    def put(self, path: str, **kwargs):
        """PUT 请求"""
        url = f"{self.base_url}{path}"
        return self.session.put(url, **kwargs)

    def delete(self, path: str, **kwargs):
        """DELETE 请求"""
        url = f"{self.base_url}{path}"
        return self.session.delete(url, **kwargs)