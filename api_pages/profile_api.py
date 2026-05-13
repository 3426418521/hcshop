from .base_api import BaseAPI


class ProfileAPI(BaseAPI):
    """个人信息接口封装"""

    def __init__(self, session=None):
        super().__init__()
        if session:
            self.session = session

    def get_user_info(self):
        """获取用户信息"""
        return self.get("/index.php?s=/api/user/info")

    def update_user_info(self, **kwargs):
        """更新用户信息"""
        return self.post("/index.php?s=/api/user/save", json=kwargs)

    def update_profile(self, **kwargs):
        """更新用户资料（别名方法）"""
        return self.update_user_info(**kwargs)

    def update_avatar(self, image_path: str):
        """更新头像"""
        try:
            with open(image_path, "rb") as f:
                return self.post("/index.php?s=/api/user/avatar", files={
                    "file": f
                })
        except FileNotFoundError:
            return None

    def change_password(self, old_pwd: str, new_pwd: str, confirm_pwd: str):
        """修改密码"""
        return self.post("/index.php?s=/api/user/password", json={
            "old_pwd": old_pwd,
            "new_pwd": new_pwd,
            "confirm_pwd": confirm_pwd
        })

    def chage_password(self, old_pwd: str, new_pwd: str, confirm_pwd: str):
        """修改密码（兼容旧拼写）"""
        return self.change_password(old_pwd, new_pwd, confirm_pwd)

    def get_balance(self):
        """获取余额"""
        return self.get("/index.php?s=/api/user/balance")
