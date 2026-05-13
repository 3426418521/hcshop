from selenium.webdriver.common.by import By
from .base_page import BasePage


class ProductPage(BasePage):
    """商品列表页面对象"""

    # ========== 页面 URL ==========
    PRODUCT_LIST_URL = "/index.php?s=/index/search/index.html"
    CATEGORY_URL = "/index.php?s=/index/search/index/category_id/"

    # ========== 元素定位 ==========
    # 搜索框
    SEARCH_INPUT = (By.XPATH, "//input[contains(@placeholder,'搜索') or contains(@class,'search') or @type='text']")

    # 搜索按钮 - 红色按钮，包含"搜索"文字和放大镜图标
    SEARCH_BUTTON = (By.XPATH,
                     "//button[contains(text(),'搜索') or contains(@class,'search') or contains(@class,'btn')]//i[contains(@class,'search')] | //button[contains(text(),'搜索')]")
    SEARCH_BUTTON_ALT = (By.XPATH,
                         "//a[contains(text(),'搜索') or contains(@class,'search-btn')] | //div[contains(@class,'search')]//button")

    # 分类筛选 - 只保留一级分类
    CATEGORY_FILTER = (By.XPATH, "//div[contains(@class,'category-filter')]")
    CATEGORY_OPTIONS = (By.XPATH, "//div[contains(@class,'category-filter')]//a[contains(@class,'category-option')]")

    # 商品列表 - 根据实际HTML结构: <li class="am-animation-scale-up"><div class="items">...
    PRODUCT_ITEMS = (By.XPATH, "//li[contains(@class,'am-animation-scale-up')]")
    PRODUCT_ITEM = (By.XPATH, "//li[contains(@class,'am-animation-scale-up')]")

    # 商品容器
    ITEM_CONTAINER = (By.XPATH, ".//div[contains(@class,'items')]")

    # 商品链接 - 注意: 链接有target="_blank"，需要处理
    ITEM_LINK = (By.XPATH, ".//a[contains(@class,'am-block')]")

    # 商品图片
    ITEM_IMAGE = (By.XPATH, ".//img[contains(@class,'goods-images')]")

    # 商品标题
    ITEM_TITLE = (By.XPATH, ".//p[contains(@class,'goods-title')]")

    # 商品价格
    ITEM_PRICE = (By.XPATH, ".//p[contains(@class,'price')]//strong")

    # 排序
    SORT_DEFAULT = (By.XPATH, "//a[contains(text(),'综合')]")
    SORT_SALES = (By.XPATH, "//a[contains(text(),'销量')]")
    SORT_PRICE = (By.XPATH, "//a[contains(text(),'价格')]")

    # 分页
    PAGE_NEXT = (By.XPATH, "//a[contains(text(),'下一页')]")
    PAGE_PREV = (By.XPATH, "//a[contains(text(),'上一页')]")
    # 操作按钮 - 根据实际HTML
    # <button class="buy-btn cart-submit buy-btn-second buy-event login-event" title="加入购物车" data-type="cart">
    ADD_CART_BUTTON = (By.XPATH,
                       "//button[contains(@class,'cart-submit') or contains(@class,'buy-event') or @title='加入购物车' or @data-type='cart']")
    ADD_CART_BUTTON_ALT = (By.XPATH, "//button[contains(text(),'加入购物车')]")
    ADD_CART_WITH_ICON = (By.XPATH, "//button[.//i[contains(@class,'opencart')] or .//i[contains(@class,'cart')]]")
    BUY_NOW_BUTTON = (By.XPATH, "//button[contains(text(),'立即购买')]")
    COLLECT_BUTTON = (By.XPATH, "//button[contains(text(),'收藏')]")
    # ========== 页面操作方法 ==========

    def open_product_list(self):
        """打开商品列表页"""
        self.logger.info("打开商品列表页")
        return self.open(self.PRODUCT_LIST_URL)

    def open_category(self, category_id: int):
        """打开指定分类页面"""
        url = f"{self.CATEGORY_URL}{category_id}.html"
        self.logger.info(f"打开分类: {url}")
        return self.open(url)

    def search(self, keywords: str):
        """搜索商品"""
        self.logger.info(f"搜索商品: {keywords}")

        # 先点击搜索框获得焦点
        try:
            search_input = self.find(*self.SEARCH_INPUT)
            search_input.click()
            search_input.clear()
            search_input.send_keys(keywords)
        except Exception as e:
            self.logger.warning(f"通过find输入失败: {e}")
            self.send_keys(*self.SEARCH_INPUT, keywords)

        # 等待一下确保按钮可点击
        self.wait_seconds(0.5)

        # 尝试多种方式点击搜索按钮
        clicked = False
        for btn_locator in [self.SEARCH_BUTTON, self.SEARCH_BUTTON_ALT]:
            try:
                if self.is_element_visible(*btn_locator, timeout=2):
                    self.click(*btn_locator)
                    clicked = True
                    self.logger.info("搜索按钮点击成功")
                    break
            except Exception as e:
                self.logger.debug(f"按钮定位失败: {e}")
                continue

        # 如果按钮点击失败，尝试按回车键提交
        if not clicked:
            self.logger.info("尝试按回车键提交搜索")
            from selenium.webdriver.common.keys import Keys
            search_input = self.find(*self.SEARCH_INPUT)
            search_input.send_keys(Keys.ENTER)

        return self

    def click_first_product(self):
        """点击第一个商品 - 处理target='_blank'在新标签页打开的情况"""
        self.logger.info("点击第一个商品 - 开始查找")

        # 先等待商品列表加载
        self.wait_seconds(2)

        items = []
        try:
            items = self.find_all(*self.PRODUCT_ITEM)
            self.logger.info(f"找到 {len(items)} 个商品")
        except Exception as e:
            self.logger.warning(f"查找商品列表失败: {e}")

        if not items:
            self.logger.warning("未找到商品，尝试备选定位")
            try:
                alt_items = self.driver.find_elements(By.XPATH, "//li[.//img] | //div[contains(@class,'items')]")
                if alt_items:
                    items = alt_items
                    self.logger.info(f"备选定位找到 {len(items)} 个商品")
            except Exception as e:
                self.logger.warning(f"备选定位也失败: {e}")

        if items:
            first_item = items[0]
            self.logger.info("开始点击第一个商品")

            # 找到链接并移除target="_blank"，防止在新标签页打开
            try:
                link = first_item.find_element(*self.ITEM_LINK)
                # 使用JS移除target属性，确保在当前页打开
                self.driver.execute_script("arguments[0].removeAttribute('target');", link)
                self.logger.info("已移除target=_blank属性")

                # 再点击链接
                self.logger.info("点击商品链接")
                link.click()
                self.logger.info("商品链接点击成功")

                # 等待页面加载
                self.wait_seconds(3)
                return self
            except Exception as e:
                self.logger.warning(f"点击链接失败: {e}")

            # 尝试点击商品图片
            try:
                img = first_item.find_element(*self.ITEM_IMAGE)
                self.logger.info("点击商品图片")
                img.click()
                self.wait_seconds(3)
                self.logger.info("商品图片点击成功")
                return self
            except Exception as e:
                self.logger.warning(f"点击图片失败: {e}")

            # 最后尝试JS点击整个商品容器
            try:
                self.logger.info("使用JS点击商品容器")
                self.driver.execute_script("arguments[0].click();", first_item)
                self.wait_seconds(3)
                self.logger.info("JS点击商品成功")
            except Exception as e:
                self.logger.error(f"JS点击也失败: {e}")
        else:
            self.logger.error("最终未找到任何商品元素")

        return self

    def click_product_by_index(self, index: int):
        """点击指定索引的商品"""
        self.logger.info(f"点击第{index}个商品")
        items = self.find_all(*self.PRODUCT_ITEM)
        if 0 <= index < len(items):
            items[index].click()
        return self

    def sort_by(self, sort_type: str = "default"):
        """排序"""
        self.logger.info(f"排序: {sort_type}")
        if sort_type == "sales":
            self.click(*self.SORT_SALES)
        elif sort_type == "price":
            self.click(*self.SORT_PRICE)
        else:
            self.click(*self.SORT_DEFAULT)
        return self

    def select_category(self, category_name: str):
        """按分类名称筛选商品"""
        self.logger.info(f"选择分类: {category_name}")
        locators = [
            (By.XPATH, f"//a[contains(text(),'{category_name}')]"),
            (By.XPATH, f"//li[contains(text(),'{category_name}')]"),
            (By.XPATH, f"//span[contains(text(),'{category_name}')]"),
            (By.XPATH, f"//div[contains(text(),'{category_name}')]"),
        ]
        for locator in locators:
            try:
                if self.is_element_visible(*locator, timeout=2):
                    self.click(*locator)
                    return self
            except:
                continue
        self.logger.warning(f"未找到分类: {category_name}")
        return self

    def is_category_active(self, category_name: str) -> bool:
        """判断指定分类是否被选中"""
        try:
            active_locators = [
                (By.XPATH, f"//a[contains(text(),'{category_name}') and contains(@class,'active')]"),
                (By.XPATH, f"//li[contains(text(),'{category_name}') and contains(@class,'active')]"),
                (By.XPATH, f"//a[contains(text(),'{category_name}') and contains(@class,'selected')]"),
            ]
            for locator in active_locators:
                if self.is_element_visible(*locator, timeout=2):
                    return True
            return False
        except:
            return False

    def click_next_page(self):
        """下一页"""
        if self.is_element_visible(*self.PAGE_NEXT):
            self.click(*self.PAGE_NEXT)
        return self

    # ========== 状态获取 ==========

    def is_product_list_loaded(self) -> bool:
        """列表是否加载"""
        return self.is_element_present(*self.PRODUCT_ITEMS) or self.is_element_present(*self.PRODUCT_ITEM)

    def get_product_count(self) -> int:
        """获取商品数量"""
        try:
            items = self.find_all(*self.PRODUCT_ITEM)
            count = len(items)
            self.logger.info(f"商品数量: {count}")
            return count
        except Exception as e:
            self.logger.warning(f"获取商品数量失败: {e}")
            return 0

    def is_search_result_displayed(self) -> bool:
        """搜索结果是否显示"""
        return self.get_product_count() > 0

    def get_first_product_title(self) -> str:
        """获取第一个商品标题"""
        try:
            items = self.find_all(*self.PRODUCT_ITEM)
            if items:
                return items[0].find_element(*self.ITEM_TITLE).text
            return ""
        except:
            return ""

    def get_first_product_price(self) -> float:
        """获取第一个商品价格"""
        try:
            items = self.find_all(*self.PRODUCT_ITEM)
            if items:
                price_text = items[0].find_element(*self.ITEM_PRICE).text
                import re
                numbers = re.findall(r'\d+\.?\d*', price_text.replace(',', ''))
                return float(numbers[0]) if numbers else 0.0
            return 0.0
        except:
            return 0.0

    def to_detail_page(self):
        """跳转到详情页（点击后调用）"""
        return ProductDetailPage(self.driver)


class ProductDetailPage(BasePage):
    """商品详情页面对象"""

    # ========== 元素定位 ==========
    PRODUCT_TITLE = (By.XPATH, "//h1[contains(@class,'goods-title') or contains(@class,'title')]")
    PRODUCT_PRICE = (By.XPATH, "//span[contains(@class,'price') or contains(@class,'am-text-danger')]")
    PRODUCT_STOCK = (By.XPATH, "//span[contains(text(),'库存')]")

    # 数量
    QUANTITY_INPUT = (By.XPATH, "//input[contains(@class,'quantity') or @type='number']")
    QUANTITY_PLUS = (By.XPATH, "//button[contains(text(),'+')]")
    QUANTITY_MINUS = (By.XPATH, "//button[contains(text(),'-')]")

    # 操作按钮
    ADD_CART_BUTTON = (By.XPATH, "//button[contains(text(),'加入购物车') or contains(@class,'cart')]")
    ADD_CART_BUTTON_ALT = (By.XPATH, "/html/body/div[4]/div[2]/div[2]/div/div[3]/div[2]/button[2]")
    ADD_CART_WITH_ICON = (By.XPATH, "//button[.//i[contains(@class,'cart')] or .//span[contains(text(),'购物车')]]")
    BUY_NOW_BUTTON = (By.XPATH, "//button[contains(text(),'立即购买')]")
    COLLECT_BUTTON = (By.XPATH, "//button[contains(text(),'收藏')]")

    # 商品详情
    TAB_DETAIL = (By.XPATH, "//li[contains(text(),'商品详情')]")
    TAB_COMMENT = (By.XPATH, "//li[contains(text(),'商品评论')]")

    # ========== 页面操作方法 ==========

    def set_quantity(self, quantity: int):
        """设置数量"""
        self.send_keys(*self.QUANTITY_INPUT, str(quantity))
        return self

    def increase_quantity(self):
        """增加数量"""
        self.click(*self.QUANTITY_PLUS)
        return self

    def decrease_quantity(self):
        """减少数量"""
        self.click(*self.QUANTITY_MINUS)
        return self

    def add_to_cart(self):
        """加入购物车"""
        self.logger.info("点击加入购物车")

        # 尝试多种方式点击加入购物车
        clicked = False
        for locator in [self.ADD_CART_BUTTON, self.ADD_CART_BUTTON_ALT, self.ADD_CART_WITH_ICON]:
            try:
                if self.is_element_visible(*locator, timeout=3):
                    self.click(*locator)
                    clicked = True
                    self.logger.info("加入购物车按钮点击成功")
                    break
            except Exception as e:
                self.logger.debug(f"加入购物车按钮定位失败: {e}")
                continue

        # 如果都失败了，尝试JS点击
        if not clicked:
            try:
                btn = self.driver.find_element(By.XPATH,
                                               "//button[contains(@class,'cart-submit') or @data-type='cart']")
                self.driver.execute_script("arguments[0].click();", btn)
                self.logger.info("使用JS点击加入购物车")
            except Exception as e:
                self.logger.warning(f"加入购物车点击失败: {e}")

        return self

    def buy_now(self):
        """立即购买"""
        self.logger.info("点击立即购买")
        self.click(*self.BUY_NOW_BUTTON)
        return self

    def click_collect(self):
        """点击收藏"""
        self.logger.info("点击收藏")
        self.click(*self.COLLECT_BUTTON)
        return self

    # ========== 状态获取 ==========

    def is_detail_loaded(self) -> bool:
        """详情页是否加载"""
        return self.is_element_visible(*self.PRODUCT_TITLE)

    def get_product_title(self) -> str:
        """获取标题"""
        return self.get_text(*self.PRODUCT_TITLE)

    def get_product_price(self) -> float:
        """获取价格"""
        price_text = self.get_text(*self.PRODUCT_PRICE)
        import re
        numbers = re.findall(r'\d+\.?\d*', price_text.replace(',', ''))
        return float(numbers[0]) if numbers else 0.0

    def is_add_cart_button_displayed(self) -> bool:
        """加购按钮是否显示"""
        return self.is_element_visible(*self.ADD_CART_BUTTON)

    def is_collected(self) -> bool:
        """是否已收藏"""
        try:
            btn = self.find(*self.COLLECT_BUTTON)
            return "已收藏" in btn.text or "active" in (btn.get_attribute("class") or "")
        except:
            return False