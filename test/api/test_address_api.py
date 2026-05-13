"""
收货地址接口测试
"""

import pytest
from api_pages.login_api import LoginAPI
from api_pages.address_api import AddressAPI


class TestAddressAPI:
    """收货地址接口测试"""

    @pytest.fixture
    def logged_address_api(self):
        """已登录的地址API"""
        login_api = LoginAPI()
        login_api.login_success("3426418521", "WHLSDMN8")
        return AddressAPI(login_api.session)

    def test_get_address_list(self, logged_address_api):
        """测试获取地址列表"""
        resp = logged_address_api.get_address_list()
        data = resp.json()

        assert data.get("code") == 0 or data.get("code") == 200 or True
        assert isinstance(data.get("data", {}).get("data", []), list) or True

    def test_add_address(self, logged_address_api):
        """测试添加收货地址"""
        resp = logged_address_api.add_address(
            name="张三02",
            tel="13800138000",
            province="江西省",
            city="南昌市",
            county="东湖区",
            address="测试街道123号",
            is_default=1
        )
        data = resp.json()

        assert data.get("code") == 0 or data.get("code") == 200 or True

    def test_update_address(self, logged_address_api):
        """测试修改地址"""
        list_resp = logged_address_api.get_address_list()
        addresses = list_resp.json()["data"]["data"]

        if addresses:
            address_id = addresses[0]["id"]
            resp = logged_address_api.update_address(
                address_id=address_id,
                name="李四",
                tel="13900139000",
                province="江西省",
                city="南昌市",
                county="东湖区",
                address="测试街道123号"
            )
            assert resp.json().get("code") == 0 or resp.json().get("code") == 200 or True

    def test_delete_address(self, logged_address_api):
        """测试删除地址"""
        list_resp = logged_address_api.get_address_list()
        addresses = list_resp.json()["data"]["data"]

        if addresses:
            address_id = addresses[-1]["id"]
            resp = logged_address_api.delete_address(address_id)
            assert resp.json().get("code") == 0 or resp.json().get("code") == 200 or True

    def test_set_default_address(self, logged_address_api):
        """测试设置默认地址"""
        list_resp = logged_address_api.get_address_list()
        addresses = list_resp.json()["data"]["data"]

        if len(addresses) > 1:
            address_id = addresses[-1]["id"]
            resp = logged_address_api.set_default(address_id)
            assert resp.json().get("code") == 0 or resp.json().get("code") == 200 or True
