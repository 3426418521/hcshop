"""
订单 API
"""

from .base_api import BaseAPI


class OrderAPI(BaseAPI):
    """订单接口封装"""

    def __init__(self, session=None):
        super().__init__()
        if session:
            self.session = session

    def create_order_from_cart(self):
        """从购物车创建订单"""
        return self.post("/index.php?s=/api/order/create", json={})

    def get_order_list(self, status: str = ""):
        """获取订单列表"""
        params = {}
        if status:
            params["status"] = status
        return self.get("/index.php?s=/api/order/index", params=params)

    def get_order_detail(self, order_id: int):
        """获取订单详情"""
        return self.get("/index.php?s=/api/order/detail", params={
            "id": order_id
        })

    def cancel_order(self, order_id: int):
        """取消订单"""
        return self.post("/index.php?s=/api/order/cancel", json={
            "id": order_id
        })