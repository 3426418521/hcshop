"""
侧边栏/底部导航页面对象
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class SidebarPage(BasePage):
    """侧边栏导航页面对象"""

    # ========== 元素定位 ==========
    # 底部导航栏（移动端常见）
    BOTTOM_NAV = (By.XPATH, "//div[contains(@class,'bottom-nav') or contains(@class,'tab-bar')]")

    # 导航项
    NAV_HOME = (By.XPATH, "//a[contains(@href,'index') or contains(text(),'首页') or contains(@class,'home')]")
    NAV_CATEGORY = (By.XPATH, "//a[contains(@href,'category') or contains(text(),'分类') or contains(@class,'category')]")
    NAV_CART = (By.XPATH, "//a[contains(@href,'cart') or contains(text(),'购物车') or contains(@class,'cart')]")
    NAV_USER = (By.XPATH, "//a[contains(@href,'user') or contains(text(),'我的') or contains(@class,'user')]")

    # 激活状态
    ACTIVE_HOME = (By.XPATH, "//a[contains(@class,'active') and (contains(@href,'index') or contains(text(),'首页'))]")
    ACTIVE_CATEGORY = (By.XPATH, "//a[contains(@class,'active') and (contains(@href,'category') or contains(text(),'分类'))]")
    ACTIVE_CART = (By.XPATH, "//a[contains(@class,'active') and (contains(@href,'cart') or contains(text(),'购物车'))]")
    ACTIVE_USER = (By.XPATH, "//a[contains(@class,'active') and (contains(@href,'user') or contains(text(),'我的'))]")

    # 购物车数量角标
    CART_BADGE = (By.XPATH, "//span[contains(@class,'badge') and parent::a[contains(@href,'cart')]]")

    # ========== 页面操作方法 ==========

    def click_home(self):
        """点击首页"""
        self.logger.info("点击首页导航")
        try:
            self.click(*self.NAV_HOME, timeout=12)
        except Exception:
            self.js_click(*self.NAV_HOME)
        return self

    def click_category(self):
        """点击分类"""
        self.logger.info("点击分类导航")
        try:
            self.click(*self.NAV_CATEGORY, timeout=12)
        except Exception:
            self.js_click(*self.NAV_CATEGORY)
        return self

    def click_cart(self):
        """点击购物车"""
        self.logger.info("点击购物车导航")
        try:
            self.click(*self.NAV_CART, timeout=12)
        except Exception:
            self.js_click(*self.NAV_CART)
        return self

    def click_user(self):
        """点击我的"""
        self.logger.info("点击我的导航")
        try:
            self.click(*self.NAV_USER, timeout=12)
        except Exception:
            self.js_click(*self.NAV_USER)
        return self

    # ========== 状态获取 ==========

    def is_sidebar_displayed(self) -> bool:
        """侧边栏/底部导航是否显示"""
        return (
            self.is_element_visible(*self.BOTTOM_NAV, timeout=4)
            or self.is_element_visible(*self.NAV_HOME, timeout=8)
            or self.is_element_present(
                By.XPATH, "//header//a[contains(.,'首页')] | //nav//a[contains(.,'首页')]", timeout=4
            )
        )

    def is_home_active(self) -> bool:
        """首页是否选中"""
        return self.is_element_visible(*self.ACTIVE_HOME)

    def is_category_active(self) -> bool:
        """分类是否选中"""
        return self.is_element_visible(*self.ACTIVE_CATEGORY)

    def is_cart_active(self) -> bool:
        """购物车是否选中"""
        return self.is_element_visible(*self.ACTIVE_CART)

    def is_user_active(self) -> bool:
        """我的是否选中"""
        return self.is_element_visible(*self.ACTIVE_USER)

    def get_cart_badge_count(self) -> int:
        """获取购物车角标数量"""
        try:
            if self.is_element_visible(*self.CART_BADGE):
                text = self.get_text(*self.CART_BADGE)
                import re
                numbers = re.findall(r'\d+', text)
                return int(numbers[0]) if numbers else 0
            return 0
        except:
            return 0