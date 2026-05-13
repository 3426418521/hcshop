"""
登录 API
"""

from .base_api import BaseAPI


class LoginAPI(BaseAPI):
    """登录接口封装"""

    def login(self, accounts: str, pwd: str, type_: str = "username"):
        """调用登录接口"""
        return self.post("/index.php?s=/api/user/login", json={
            "accounts": accounts,
            "pwd": pwd,
            "type": type_
        })

    def login_success(self, accounts: str, pwd: str):
        """登录；若响应含 token 则写入请求头，否则依赖会话 Cookie"""
        resp = self.login(accounts, pwd)
        data = resp.json()
        if data.get("code") == 0:
            token = (data.get("data") or {}).get("token")
            if token:
                self.session.headers.update({"token": token})
        return resp

    def logout(self):
        """退出登录"""
        return self.get("/index.php?s=/api/user/logout")

    def is_logged_in(self) -> bool:
        """检查是否已登录"""
        try:
            resp = self.get("/index.php?s=/api/user/info")
            data = resp.json()
            return data.get("code") == 0
        except:
            return False