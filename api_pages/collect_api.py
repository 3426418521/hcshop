"""
收藏 API
"""

from .base_api import BaseAPI


class CollectAPI(BaseAPI):
    """收藏接口封装"""

    def __init__(self, session=None):
        super().__init__()
        if session:
            self.session = session

    def add_collect(self, goods_id: int, type: str = "goods"):
        """添加收藏"""
        return self.post("/index.php?s=/api/usergoodsfavor/index", json={
            "goods_id": goods_id,
            "type": type
        })

    def get_collect_list(self):
        """获取收藏列表"""
        return self.get("/index.php?s=/api/usergoodsfavor/index")

    def cancel_collect(self, favor_id: int):
        """取消收藏"""
        return self.post("/index.php?s=/api/usergoodsfavor/index", json={
            "id": favor_id,
            "type": "delete"
        })
