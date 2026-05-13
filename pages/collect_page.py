from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from .base_page import BasePage


class CollectPage(BasePage):
    """收藏页面对象"""

    # ========== 页面 URL ==========
    COLLECT_URL = "/index.php?s=/index/usergoodsfavor/index.html"

    # ========== 元素定位 ==========
    # 页面标题
    PAGE_TITLE = (By.XPATH, "//h2[contains(text(),'我的收藏')]")

    # 顶部导航 - 我的收藏下拉菜单
    NAV_MY_COLLECT = (
        By.XPATH,
        "//a[contains(text(),'我的收藏')] | //span[contains(text(),'我的收藏')]/ancestor::a[1]",
    )
    NAV_COLLECT_DROPDOWN = (By.XPATH,
                            "//div[contains(@class,'dropdown') or contains(@class,'menu') or contains(@class,'am-dropdown-content')]")
    NAV_GOODS_COLLECT_LINK = (
        By.XPATH,
        "//a[contains(text(),'商品收藏')] | //li[contains(text(),'商品收藏')]//a",
    )

    # 另一种可能的定位方式
    NAV_MY_COLLECT_MENU = (By.XPATH, "//a[contains(@href,'usergoodsfavor') or contains(text(),'我的收藏')]")
    SUBMENU_GOODS_COLLECT = (By.XPATH, "//a[contains(text(),'商品收藏') or contains(@href,'usergoodsfavor')]")

    # 收藏列表
    COLLECT_ITEMS = (By.XPATH, "//div[contains(@class,'goods-item') or contains(@class,'collect-item')]")
    COLLECT_ITEM = (By.XPATH, "//div[contains(@class,'goods-item') or contains(@class,'collect-item')]")

    # 商品信息（相对路径）
    ITEM_IMAGE = (By.XPATH, ".//img")
    ITEM_TITLE = (By.XPATH, ".//div[contains(@class,'title') or contains(@class,'name')]")
    ITEM_PRICE = (By.XPATH, ".//span[contains(@class,'price')]")

    # 操作按钮（相对路径）
    ITEM_CANCEL = (By.XPATH,
                   ".//a[contains(text(),'取消收藏') or contains(@class,'cancel') or contains(@class,'delete')]")
    ITEM_ADD_CART = (By.XPATH, ".//button[contains(text(),'加入购物车')]")

    # 空状态
    EMPTY_COLLECT = (By.XPATH, "//div[contains(@class,'empty') or contains(text(),'暂无收藏')]")
    GO_SHOPPING = (By.XPATH, "//a[contains(text(),'去逛逛')]")

    # ========== 页面操作方法 ==========

    def open_collect_page(self):
        """打开收藏页"""
        self.logger.info("打开收藏页")
        return self.open(self.COLLECT_URL)

    def hover_and_click_goods_collect(self):
        """
        悬停到'我的收藏'导航，点击'商品收藏'子菜单
        适用于顶部导航需要悬停才能看到子菜单的场景
        """
        self.logger.info("悬停到'我的收藏'导航")

        # 先尝试直接找到"商品收藏"链接并点击（可能不需要悬停）
        try:
            goods_collect = self.find(*self.SUBMENU_GOODS_COLLECT, timeout=3)
            if goods_collect.is_displayed():
                self.logger.info("直接点击'商品收藏'链接")
                goods_collect.click()
                return self
        except:
            pass

        # 需要悬停的情况
        try:
            # 找到"我的收藏"导航元素
            collect_nav = self.find(*self.NAV_MY_COLLECT, timeout=5)

            # 使用 ActionChains 悬停
            actions = ActionChains(self.driver)
            actions.move_to_element(collect_nav).pause(0.5).perform()

            self.logger.info("悬停完成，等待子菜单显示")

            # 等待子菜单中的"商品收藏"出现并点击
            goods_collect = self.find_clickable(*self.SUBMENU_GOODS_COLLECT, timeout=5)
            goods_collect.click()

            self.logger.info("已点击'商品收藏'")
        except Exception as e:
            self.logger.warning(f"悬停点击失败，尝试直接打开URL: {e}")
            # 如果悬停失败，直接打开收藏页面URL
            self.open(self.COLLECT_URL)

        return self

    def hover_nav_collect(self):
        """
        仅悬停到'我的收藏'导航，不点击
        用于验证下拉菜单显示
        """
        self.logger.info("悬停到'我的收藏'导航")
        try:
            collect_nav = self.find(*self.NAV_MY_COLLECT, timeout=5)
            actions = ActionChains(self.driver)
            actions.move_to_element(collect_nav).pause(0.5).perform()
            self.logger.info("悬停完成")
        except Exception as e:
            self.logger.warning(f"悬停失败: {e}")
        return self

    def is_dropdown_visible(self) -> bool:
        """判断下拉菜单是否显示"""
        return self.is_element_visible(*self.NAV_COLLECT_DROPDOWN, timeout=3)

    def cancel_first_collect(self):
        """取消第一个收藏"""
        self.logger.info("取消第一个收藏")
        items = self.find_all(*self.COLLECT_ITEM)
        if items:
            cancel_btn = items[0].find_element(*self.ITEM_CANCEL)
            cancel_btn.click()
        return self

    def cancel_collect_by_index(self, index: int):
        self.logger.info(f"取消第{index}个收藏")
        items = self.find_all(*self.COLLECT_ITEM)
        if 0 <= index < len(items):
            cancel_btn = items[index].find_element(*self.ITEM_CANCEL)
            cancel_btn.click()
        return self

    def add_first_to_cart(self):
        """将第一个收藏加入购物车"""
        self.logger.info("第一个收藏加入购物车")
        items = self.find_all(*self.COLLECT_ITEM)
        if items:
            cart_btn = items[0].find_element(*self.ITEM_ADD_CART)
            cart_btn.click()
        return self

    def click_go_shopping(self):
        """点击去逛逛"""
        self.click(*self.GO_SHOPPING)
        return self

    # ========== 状态获取 ==========

    def is_collect_list_loaded(self) -> bool:
        """收藏列表是否加载"""
        url = self.driver.current_url.lower()
        if "usergoodsfavor" not in url and "favor" not in url:
            return False
        return (
            self.get_collect_count() > 0
            or self.is_element_visible(*self.EMPTY_COLLECT, timeout=5)
            or self.is_element_visible(*self.PAGE_TITLE, timeout=8)
        )

    def get_collect_count(self) -> int:
        """获取收藏数量"""
        try:
            return len(self.driver.find_elements(*self.COLLECT_ITEM))
        except Exception:
            return 0

    def is_empty_state_displayed(self) -> bool:
        """是否显示空状态"""
        return self.is_element_visible(*self.EMPTY_COLLECT, timeout=5) or self.get_collect_count() == 0

    def get_empty_message(self) -> str:
        """获取空状态提示文本"""
        if self.is_element_visible(*self.EMPTY_COLLECT):
            return self.get_text(*self.EMPTY_COLLECT)
        return ""