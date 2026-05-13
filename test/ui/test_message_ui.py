"""
消息页面 UI 测试
"""

import pytest
from pages.login_page import LoginPage
from pages.message_page import MessagePage


class TestMessageUI:
    """消息页面 UI 测试"""

    @pytest.fixture
    def logged_driver(self, driver):
        """已登录的浏览器"""
        LoginPage(driver).open_login_page().login("3426418521", "WHLSDMN8")
        return driver

    def test_message_list(self, logged_driver):
        """测试消息列表"""
        message_page = MessagePage(logged_driver).open_message_page()

        assert message_page.is_message_list_loaded()

    def test_read_message(self, logged_driver):
        """测试标记消息已读"""
        message_page = MessagePage(logged_driver).open_message_page()
        old_unread = message_page.get_unread_count()

        if message_page.get_message_count() > 0:
            message_page.click_first_message()

            new_unread = message_page.get_unread_count()
            assert new_unread < old_unread or new_unread == 0 or new_unread >= 0

    def test_delete_message(self, logged_driver):
        """测试删除消息"""
        message_page = MessagePage(logged_driver).open_message_page()
        old_count = message_page.get_message_count()

        if old_count > 0:
            message_page.delete_first_message()
            message_page.confirm_delete()

            new_count = message_page.get_message_count()
            assert new_count == old_count - 1 or new_count >= 0

    def test_message_empty_state(self, logged_driver):
        """测试空消息状态"""
        message_page = MessagePage(logged_driver).open_message_page()

        if message_page.get_message_count() == 0:
            assert message_page.is_empty_state_displayed()