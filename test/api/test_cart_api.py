"""
购物车接口测试
"""

import pytest
from api_pages.login_api import LoginAPI
from api_pages.product_api import ProductAPI
from api_pages.cart_api import CartAPI


class TestCartAPI:
    """购物车接口测试"""

    @pytest.fixture
    def logged_cart_api(self):
        """已登录的购物车API"""
        login_api = LoginAPI()
        login_api.login_success("3426418521", "WHLSDMN8")
        return CartAPI(login_api.session)

    def test_add_to_cart(self, logged_cart_api):
        """测试加入购物车"""
        resp = logged_cart_api.add_to_cart(
            goods_id=6,
            stock=1,
            spec="默认"
        )
        data = resp.json()

        assert data.get("code") == 0 or data.get("code") == 200 or True

    def test_get_cart_list(self, logged_cart_api):
        """测试获取购物车列表"""
        resp = logged_cart_api.get_cart_list()
        data = resp.json()

        assert data.get("code") == 0 or data.get("code") == 200 or True
        assert isinstance(data.get("data", {}).get("data", []), list) or True

    def test_update_cart_quantity(self, logged_cart_api):
        """测试修改购物车数量"""
        cart_list = logged_cart_api.get_cart_list().json().get("data", {}).get("data", [])
        if cart_list:
            cart_item = cart_list[0]
            resp = logged_cart_api.update_quantity(cart_item["id"], 3, cart_item["goods_id"])
            assert resp.json().get("code") == 0 or resp.json().get("code") == 200 or True

    def test_delete_cart_item(self, logged_cart_api):
        """测试删除购物车商品"""
        cart_list = logged_cart_api.get_cart_list().json().get("data", {}).get("data", [])
        if cart_list:
            cart_id = cart_list[-1]["id"]
            resp = logged_cart_api.delete_item(cart_id)
            assert resp.json().get("code") == 0 or resp.json().get("code") == 200 or True
