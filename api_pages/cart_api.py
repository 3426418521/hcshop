"""
购物车 API
"""

from .base_api import BaseAPI


class CartAPI(BaseAPI):
    """购物车接口封装"""

    def __init__(self, session=None):
        super().__init__()
        if session:
            self.session = session

    def add_to_cart(self, goods_id: int, stock: int = 1, spec: str = ""):
        """加入购物车"""
        return self.post("/index.php?s=/api/cart/save", json={
            "goods_id": goods_id,
            "stock": stock,
            "spec": spec
        })

    def get_cart_list(self):
        """获取购物车列表"""
        return self.get("/index.php?s=/api/cart/index")

    def update_quantity(self, cart_id: int, stock: int, goods_id: int = None):
        """修改数量"""
        data = {
            "id": cart_id,
            "stock": stock
        }
        if goods_id is not None:
            data["goods_id"] = goods_id
        return self.post("/index.php?s=/api/cart/stock", json=data)

    def delete_item(self, cart_id: int):
        """删除购物车商品"""
        return self.post("/index.php?s=/api/cart/delete", json={
            "id": cart_id
        })
