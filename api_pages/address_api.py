"""
收货地址 API
"""

from .base_api import BaseAPI


class AddressAPI(BaseAPI):
    """收货地址接口封装"""

    def __init__(self, session=None):
        super().__init__()
        if session:
            self.session = session

    def get_address_list(self):
        """获取地址列表"""
        return self.get("/index.php?s=/api/useraddress/index")

    def add_address(self, name: str, tel: str, province: str, city: str, 
                    county: str, address: str, is_default: int = 0):
        """添加地址"""
        return self.post("/index.php?s=/api/useraddress/save", json={
            "name": name,
            "tel": tel,
            "province": province,
            "city": city,
            "county": county,
            "address": address,
            "is_default": is_default
        })

    def update_address(self, address_id: int, **kwargs):
        """修改地址"""
        data = {"id": address_id}
        data.update(kwargs)
        return self.post("/index.php?s=/api/useraddress/save", json=data)

    def delete_address(self, address_id: int):
        """删除地址"""
        return self.post("/index.php?s=/api/useraddress/delete", json={
            "id": address_id
        })

    def set_default(self, address_id: int):
        """设置默认地址"""
        return self.post("/index.php?s=/api/useraddress/setdefault", json={
            "id": address_id
        })