"""
消息 API
"""

from .base_api import BaseAPI


class MessageAPI(BaseAPI):
    """消息接口封装"""

    def __init__(self, session=None):
        super().__init__()
        if session:
            self.session = session

    def get_message_list(self):
        """获取消息列表"""
        return self.get("/index.php?s=/api/message/index")

    def get_unread_count(self):
        """获取未读消息数"""
        return self.get("/index.php?s=/api/message/unread")

    def read_message(self, msg_id: int):
        """标记已读"""
        return self.post("/index.php?s=/api/message/read", json={
            "id": msg_id
        })

    def delete_message(self, msg_id: int):
        """删除消息"""
        return self.post("/index.php?s=/api/message/delete", json={
            "id": msg_id
        })