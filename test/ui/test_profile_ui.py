"""个人中心页面 UI 测试"""

import pytest
import time
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage


class TestProfileUI:
    """个人中心页面 UI 测试"""

    @pytest.fixture
    def logged_driver(self, driver):
        LoginPage(driver).open_login_page().login("3426418521", "WHLSDMN8")
        time.sleep(2)
        return driver

    def test_profile_info_display(self, logged_driver):
        """测试个人资料展示页基本信息显示（直接打开方式）"""
        profile_page = ProfilePage(logged_driver)
        profile_page.open_personal_page_direct()  # 直接打开，不经过点击链接

        assert profile_page.get_nickname_text() is not None, "昵称字段缺失"
        assert profile_page.get_mobile_text() is not None, "手机号字段缺失"
        assert profile_page.get_email_text() is not None, "邮箱字段缺失"

    def test_edit_nickname(self, logged_driver):
        """测试修改昵称（完整用户路径：首页 → 点击修改资料 → 点击编辑 → 修改 → 保存）"""
        profile_page = ProfilePage(logged_driver)

        # 1. 打开个人中心首页
        profile_page.open_profile_page()
        # 2. 点击「修改资料」链接进入个人资料展示页
        profile_page.click_modify_profile_link()

        old_nickname = profile_page.get_nickname_text()
        new_nickname = f"测试昵称_{int(time.time())}"

        # 3. 点击「编辑」按钮进入编辑页
        profile_page.click_edit_basic_info()
        # 4. 修改昵称并保存
        profile_page.input_nickname(new_nickname)
        profile_page.save_profile()

        # 5. 验证修改成功（仍在个人资料展示页）
        current_nickname = profile_page.get_nickname_text()
        assert current_nickname == new_nickname, f"昵称修改失败，期望: {new_nickname}, 实际: {current_nickname}"

        # 6. 恢复原昵称（可选）
        if old_nickname:
            profile_page.click_edit_basic_info()
            profile_page.input_nickname(old_nickname)
            profile_page.save_profile()
            assert profile_page.get_nickname_text() == old_nickname, "恢复原昵称失败"

    def test_navigate_to_order(self, logged_driver):
        """测试从个人中心首页跳转到订单页"""
        profile_page = ProfilePage(logged_driver).open_profile_page()
        profile_page.click_my_orders()
        assert "order" in logged_driver.current_url.lower(), "未跳转到订单页"

    def test_navigate_to_address(self, logged_driver):
        """测试从个人中心首页跳转到地址页"""
        profile_page = ProfilePage(logged_driver).open_profile_page()
        profile_page.click_my_address()
        assert "address" in logged_driver.current_url.lower() or "useraddress" in logged_driver.current_url, "未跳转到地址页"

    def test_navigate_to_collect(self, logged_driver):
        """测试从个人中心首页跳转到收藏页"""
        profile_page = ProfilePage(logged_driver).open_profile_page()
        profile_page.click_my_collect()
        assert "favor" in logged_driver.current_url.lower() or "usergoodsfavor" in logged_driver.current_url, "未跳转到收藏页"

    def test_order_count_display(self, logged_driver):
        """测试订单总数显示为非负数"""
        profile_page = ProfilePage(logged_driver).open_profile_page()
        count = profile_page.get_order_count()
        assert isinstance(count, int) and count >= 0, f"订单总数显示异常: {count}"