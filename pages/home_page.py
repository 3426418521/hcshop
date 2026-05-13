"""
首页面对象
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class HomePage(BasePage):
    """首页面对象"""

    # ========== 页面 URL ==========
    HOME_URL = "/"

    # ========== 元素定位 ==========
    # 顶部主导航
    NAV_HOME = (By.XPATH, "//a[contains(text(),'首页')]")
    NAV_PRACTICE = (By.XPATH, "//a[contains(text(),'练习hc')]")
    NAV_CATEGORY = (By.XPATH, "//a[contains(text(),'商品分类')]")
    NAV_SHOPXO = (By.XPATH, "//a[contains(text(),'ShopXO')]")

    # 左侧一级分类菜单
    CATEGORY_MENU = (By.XPATH, "//div[contains(@class,'category-menu') or contains(@class,'all-category')]")

    # 一级分类列表
    CATEGORY_ITEMS = (By.XPATH, "//ul[contains(@class,'category-list')]//li[contains(@class,'category-item')]")
    CATEGORY_ITEM = (By.XPATH, "//li[contains(@class,'category-item')]")

    # 具体一级分类（根据截图中的实际文本）
    CAT_DIGITAL = (By.XPATH, "//li[contains(text(),'数码办公')]")
    CAT_CLOTHING = (By.XPATH, "//li[contains(text(),'服饰鞋包')]")
    CAT_FOOD = (By.XPATH, "//li[contains(text(),'食品饮料')]")
    CAT_BEAUTY = (By.XPATH, "//li[contains(text(),'个护化妆')]")
    CAT_JEWELRY = (By.XPATH, "//li[contains(text(),'珠宝手表')]")
    CAT_SPORTS = (By.XPATH, "//li[contains(text(),'运动健康')]")
    CAT_CAR = (By.XPATH, "//li[contains(text(),'汽车用品')]")
    CAT_TOYS = (By.XPATH, "//li[contains(text(),'玩具乐器')]")
    CAT_MOM = (By.XPATH, "//li[contains(text(),'母婴用品')]")
    CAT_LIFE = (By.XPATH, "//li[contains(text(),'生活服务')]")

    # 右侧用户信息区
    USER_AVATAR = (By.XPATH, "//div[contains(@class,'user-avatar')]//img")
    WELCOME_TEXT = (By.XPATH, "//span[contains(text(),'您好，欢迎来到')]")
    LOGIN_BUTTON = (By.XPATH, "//a[contains(text(),'登录')]")
    REGISTER_BUTTON = (By.XPATH, "//a[contains(text(),'注册')]")

    # 搜索框
    SEARCH_INPUT = (By.XPATH, "//input[contains(@placeholder,'搜索') or contains(@class,'search-input')]")
    SEARCH_BUTTON = (By.XPATH, "//button[contains(text(),'搜索') or contains(@class,'search-btn')]")

    # 轮播图
    BANNER = (By.XPATH, "//div[contains(@class,'banner') or contains(@class,'slider')]")

    # 商品推荐区标题
    SECTION_DIGITAL = (By.XPATH, "//div[contains(@class,'section-title') and contains(.,'数码办公')]")
    SECTION_GOODS = (By.XPATH, "//div[contains(@class,'goods-list')]//div[contains(@class,'goods-item')]")

    # ========== 页面操作方法 ==========

    def open_home_page(self):
        """打开首页"""
        self.logger.info("打开首页")
        return self.open(self.HOME_URL)

    def click_nav_home(self):
        """点击顶部首页导航"""
        self.logger.info("点击顶部首页")
        self.click(*self.NAV_HOME)
        return self

    def click_nav_category(self):
        """点击顶部商品分类"""
        self.logger.info("点击顶部商品分类")
        self.click(*self.NAV_CATEGORY)
        return self

    def click_category_by_name(self, category_name: str):
        self.logger.info(f"点击分类: {category_name}")
        locator = (By.XPATH, f"//li[contains(text(),'{category_name}')]")
        self.click(*locator)
        return self

    def click_digital(self):
        """点击数码办公"""
        return self.click_category_by_name("数码办公")

    def click_clothing(self):
        """点击服饰鞋包"""
        return self.click_category_by_name("服饰鞋包")

    def click_food(self):
        """点击食品饮料"""
        return self.click_category_by_name("食品饮料")

    def click_beauty(self):
        """点击个护化妆"""
        return self.click_category_by_name("个护化妆")

    def click_jewelry(self):
        """点击珠宝手表"""
        return self.click_category_by_name("珠宝手表")

    def click_sports(self):
        """点击运动健康"""
        return self.click_category_by_name("运动健康")

    def click_car(self):
        """点击汽车用品"""
        return self.click_category_by_name("汽车用品")

    def click_toys(self):
        """点击玩具乐器"""
        return self.click_category_by_name("玩具乐器")

    def click_mom(self):
        """点击母婴用品"""
        return self.click_category_by_name("母婴用品")

    def click_life(self):
        """点击生活服务"""
        return self.click_category_by_name("生活服务")

    def search(self, keywords: str):
        self.logger.info(f"搜索: {keywords}")
        self.send_keys(*self.SEARCH_INPUT, keywords)
        self.click(*self.SEARCH_BUTTON)
        return self

    def click_login(self):
        """点击登录按钮"""
        self.logger.info("点击登录")
        self.click(*self.LOGIN_BUTTON)
        return self

    def click_register(self):
        """点击注册按钮"""
        self.logger.info("点击注册")
        self.click(*self.REGISTER_BUTTON)
        return self

    # ========== 状态获取 ==========

    def is_home_loaded(self) -> bool:
        """首页是否加载完成"""
        return self.is_element_visible(*self.CATEGORY_MENU) or self.is_element_visible(*self.SEARCH_INPUT)

    def get_category_count(self) -> int:
        """获取一级分类数量"""
        try:
            items = self.find_all(*self.CATEGORY_ITEM)
            return len(items)
        except:
            return 0

    def get_category_names(self) -> list:
        """获取所有一级分类名称"""
        try:
            items = self.find_all(*self.CATEGORY_ITEM)
            return [item.text.strip() for item in items]
        except:
            return []

    def is_user_logged_in(self) -> bool:
        """用户是否已登录（检查是否有登录按钮）"""
        return not self.is_element_visible(*self.LOGIN_BUTTON)

    def is_banner_displayed(self) -> bool:
        """轮播图是否显示"""
        return self.is_element_visible(*self.BANNER)

    def is_digital_section_displayed(self) -> bool:
        """数码办公专区是否显示"""
        return self.is_element_visible(*self.SECTION_DIGITAL)