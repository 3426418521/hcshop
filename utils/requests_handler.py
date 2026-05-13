"""
HTTP 请求封装模块
提供统一的请求处理、重试机制、日志记录
"""

import json
import logging
import time
from typing import Dict, Any, Optional, Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger("Hsyuan")


class RequestsHandler:
    """
    HTTP 请求处理器
    封装 requests，提供统一的超时、重试、日志、异常处理
    """

    DEFAULT_TIMEOUT = (5, 30)
    DEFAULT_RETRIES = 3
    RETRY_STATUS_CODES = [500, 502, 503, 504]

    def __init__(
            self,
            base_url: str = "",
            timeout: tuple = DEFAULT_TIMEOUT,
            max_retries: int = DEFAULT_RETRIES,
            retry_status_codes: list = None
    ):
        """
        初始化请求处理器

        Args:
            base_url: 基础 URL，所有请求会自动拼接
            timeout: (连接超时, 读取超时)
            max_retries: 最大重试次数
            retry_status_codes: 需要重试的 HTTP 状态码
        """
        self.base_url = base_url.rstrip("/") if base_url else ""
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_status_codes = retry_status_codes or self.RETRY_STATUS_CODES

        self.session = requests.Session()

        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=self.retry_status_codes,
            allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
        )

        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=10
        )

        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        self.session.headers.update({
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
        })

    def _build_url(self, url: str) -> str:
        """构建完整 URL"""
        if url.startswith("http://") or url.startswith("https://"):
            return url
        return f"{self.base_url}{url}"

    def _log_request(
            self,
            method: str,
            url: str,
            params: Any = None,
            data: Any = None,
            json_data: Any = None,
            headers: Dict = None
    ):
        """记录请求日志"""
        log_data = {
            "method": method,
            "url": url,
            "params": params,
            "data": self._mask_sensitive_data(data),
            "json": self._mask_sensitive_data(json_data),
            "headers": headers
        }
        logger.info(f"➡️  Request: {json.dumps(log_data, ensure_ascii=False, default=str)}")

    def _log_response(self, response: requests.Response, elapsed: float):
        """记录响应日志"""
        try:
            resp_body = response.json()
        except:
            resp_body = response.text[:1000]

        log_data = {
            "status_code": response.status_code,
            "elapsed": f"{elapsed:.3f}s",
            "body": resp_body
        }
        logger.info(f"⬅️  Response: {json.dumps(log_data, ensure_ascii=False, default=str)}")

    def _mask_sensitive_data(self, data: Any) -> Any:
        """脱敏敏感数据"""
        if not data:
            return data

        if isinstance(data, dict):
            masked = {}
            for k, v in data.items():
                if any(sensitive in k.lower() for sensitive in ["password", "pwd", "token", "secret", "auth"]):
                    masked[k] = "******"
                else:
                    masked[k] = v
            return masked

        if isinstance(data, str):
            try:
                json_data = json.loads(data)
                return self._mask_sensitive_data(json_data)
            except:
                return data[:200] if len(data) > 200 else data

        return data

    def request(
            self,
            method: str,
            url: str,
            params: Dict = None,
            data: Any = None,
            json: Any = None,
            headers: Dict = None,
            files: Any = None,
            cookies: Dict = None,
            timeout: tuple = None,
            **kwargs
    ) -> requests.Response:
        """
        发送 HTTP 请求
        """
        full_url = self._build_url(url)
        request_timeout = timeout or self.timeout

        request_headers = {}
        if self.session.headers:
            request_headers.update(self.session.headers)
        if headers:
            request_headers.update(headers)

        self._log_request(method, full_url, params, data, json, request_headers)

        start_time = time.time()

        try:
            response = self.session.request(
                method=method.upper(),
                url=full_url,
                params=params,
                data=data,
                json=json,
                headers=request_headers,
                files=files,
                cookies=cookies,
                timeout=request_timeout,
                **kwargs
            )

            elapsed = time.time() - start_time
            self._log_response(response, elapsed)

            response.raise_for_status()

            return response

        except requests.exceptions.Timeout as e:
            logger.error(f"请求超时: {full_url}, 错误: {e}")
            raise
        except requests.exceptions.ConnectionError as e:
            logger.error(f"连接错误: {full_url}, 错误: {e}")
            raise
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP 错误: {response.status_code}, URL: {full_url}, 响应: {response.text[:500]}")
            raise
        except Exception as e:
            logger.error(f"请求异常: {full_url}, 错误: {e}")
            raise

    def get(self, url: str, **kwargs) -> requests.Response:
        """GET 请求"""
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        """POST 请求"""
        return self.request("POST", url, **kwargs)

    def put(self, url: str, **kwargs) -> requests.Response:
        """PUT 请求"""
        return self.request("PUT", url, **kwargs)

    def delete(self, url: str, **kwargs) -> requests.Response:
        """DELETE 请求"""
        return self.request("DELETE", url, **kwargs)

    def patch(self, url: str, **kwargs) -> requests.Response:
        """PATCH 请求"""
        return self.request("PATCH", url, **kwargs)

    def update_headers(self, headers: Dict[str, str]):
        """更新默认请求头"""
        self.session.headers.update(headers)

    def remove_header(self, key: str):
        """移除请求头"""
        self.session.headers.pop(key, None)

    def get_cookies(self) -> Dict:
        """获取当前 cookies"""
        return dict(self.session.cookies)

    def close(self):
        """关闭 session"""
        self.session.close()
        logger.info("Requests session 已关闭")


def get_handler(base_url: str = "") -> RequestsHandler:
    """快速获取请求处理器"""
    return RequestsHandler(base_url=base_url)


def quick_post(url: str, json_data: Dict = None, data: Dict = None) -> requests.Response:
    """快速 POST 请求"""
    handler = RequestsHandler()
    return handler.post(url, json=json_data, data=data)


def quick_get(url: str, params: Dict = None) -> requests.Response:
    """快速 GET 请求"""
    handler = RequestsHandler()
    return handler.get(url, params=params)