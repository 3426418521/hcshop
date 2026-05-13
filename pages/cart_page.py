from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from .base_page import BasePage


class CartPage(BasePage):
    """购物车页面对象"""

    # ========== 页面 URL ==========
    CART_URL = "/index.php?s=/index/cart/index.html"

    # 购物车标题
    CART_TITLE = (By.XPATH, "//h2[contains(text(),'购物车')]")

    # 购物车商品列表
    CART_ITEMS = (By.XPATH, "//div[contains(@class,'cart-item') or contains(@class,'goods-item')]")
    CART_ITEM = (By.XPATH, "//div[contains(@class,'cart-item')]")

    # 商品信息（相对路径）
    ITEM_CHECKBOX = (By.XPATH, ".//input[@type='checkbox' or contains(@class,'check')]")
    ITEM_IMAGE = (By.XPATH, ".//img")
    ITEM_TITLE = (By.XPATH, ".//div[contains(@class,'title') or contains(@class,'name')]")
    ITEM_PRICE = (By.XPATH, ".//span[contains(@class,'price')]")
    # 新增地址按钮

    # 数量输入框 - 根据实际HTML: <input type="number" class="am-form-field" value="1">
    ITEM_QUANTITY_INPUT = (By.XPATH, ".//input[@type='number' or contains(@class,'am-form-field')]")

    # 加号按钮 - 根据实际HTML: <span class="am-input-group-label stock-submit" data-type="add">+</span>
    ITEM_QUANTITY_PLUS = (By.XPATH,
                          ".//span[contains(@class,'stock-submit') and @data-type='add'] | .//span[contains(text(),'+')] | .//button[contains(text(),'+')]")

    # 减号按钮 - 根据实际HTML: <span class="am-input-group-label stock-submit" data-type="min">-</span>
    ITEM_QUANTITY_MINUS = (By.XPATH,
                           ".//span[contains(@class,'stock-submit') and @data-type='min'] | .//span[contains(text(),'-')] | .//button[contains(text(),'-')]")

    ITEM_SUBTOTAL = (By.XPATH, ".//span[contains(@class,'subtotal') or contains(@class,'total')]")
    # 删除按钮 - 根据实际HTML: <a class="am-text-danger submit-delete" data-view="fun" data-value="ViewDeleteBack">删除</a>
    ITEM_DELETE = (By.XPATH,
                   ".//a[contains(@class,'submit-delete') or contains(@class,'am-text-danger') and contains(text(),'删除')] | .//a[contains(text(),'删除') or contains(@class,'delete')]")

    # 全选
    SELECT_ALL = (By.XPATH, "//input[@type='checkbox' and (contains(@class,'all') or contains(@class,'select-all'))]")

    # 底部结算栏
    TOTAL_PRICE = (By.XPATH,
                   "//div[contains(@class,'cart-footer')]//span[contains(@class,'total') or contains(@class,'price')]")
    SETTLEMENT_BUTTON = (By.XPATH, "//button[contains(text(),'去结算') or contains(text(),'结算')]")
    DELETE_SELECTED = (By.XPATH, "//a[contains(text(),'删除选中')]")

    # 空购物车
    EMPTY_CART = (By.XPATH, "//div[contains(@class,'empty') or contains(text(),'购物车是空的')]")
    GO_SHOPPING_BUTTON = (By.XPATH, "//a[contains(text(),'去购物')]")

    # 确认弹窗
    # 确认弹窗
    CONFIRM_BUTTON = (By.XPATH, "//button[contains(text(),'确认') or contains(text(),'确定')]")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(text(),'取消')]")

    # ========== 页面操作方法 ==========

    def open_cart_page(self):
        self.logger.info("打开购物车页面")
        return self.open(self.CART_URL)

    def select_all_items(self):
        self.logger.info("全选商品")
        checkbox = self.find(*self.SELECT_ALL)
        if not checkbox.is_selected():
            checkbox.click()
        return self

    def select_item(self, index: int = 0):
        self.logger.info(f"选择第{index}个商品")
        items = self.find_all(*self.CART_ITEM)
        if 0 <= index < len(items):
            checkbox = items[index].find_element(*self.ITEM_CHECKBOX)
            if not checkbox.is_selected():
                checkbox.click()
        return self

    def increase_first_item_quantity(self):
        self.logger.info("增加第一个商品数量")
        items = self.find_all(*self.CART_ITEM)
        if items:
            plus_btn = items[0].find_element(*self.ITEM_QUANTITY_PLUS)
            plus_btn.click()
        return self

    def decrease_first_item_quantity(self):
        self.logger.info("减少第一个商品数量")
        items = self.find_all(*self.CART_ITEM)
        if items:
            minus_btn = items[0].find_element(*self.ITEM_QUANTITY_MINUS)
            minus_btn.click()
        return self

    def delete_first_item(self):
        """删除第一个商品"""
        self.logger.info("删除第一个商品 - 开始执行")

        # 等待页面确保加载完成
        self.wait_seconds(2)

        # 方式1: 在商品容器内查找删除按钮
        try:
            items = self.find_all(*self.CART_ITEM)
            self.logger.info(f"找到 {len(items)} 个商品容器")
            if items:
                delete_btn = items[0].find_element(*self.ITEM_DELETE)
                self.logger.info("找到删除按钮，准备点击")
                delete_btn.click()
                self.logger.info("删除按钮点击成功（方式1）")
                return self
        except Exception as e:
            self.logger.warning(f"方式1失败: {e}")

        # 方式2: 直接在整个页面查找第一个删除按钮
        try:
            self.logger.info("尝试方式2: 全局查找删除按钮")
            delete_btn = self.driver.find_element(By.XPATH, "//a[contains(@class,'submit-delete')]")
            delete_btn.click()
            self.logger.info("删除按钮点击成功（方式2）")
            return self
        except Exception as e:
            self.logger.warning(f"方式2失败: {e}")

        # 方式3: 使用JS强制点击
        try:
            self.logger.info("尝试方式3: JS强制点击")
            delete_btn = self.driver.find_element(By.XPATH, "//a[contains(text(),'删除') or contains(@class,'delete')]")
            self.driver.execute_script("arguments[0].click();", delete_btn)
            self.logger.info("删除按钮点击成功（方式3 JS）")
            return self
        except Exception as e:
            self.logger.error(f"方式3也失败: {e}")

        self.logger.error("所有方式都失败，未能点击删除")
        return self

    def delete_last_item(self):
        """删除最后一个商品"""
        self.logger.info("删除最后一个商品")
        items = self.find_all(*self.CART_ITEM)
        if items:
            delete_btn = items[-1].find_element(*self.ITEM_DELETE)
            delete_btn.click()
        return self

    def confirm_delete(self):
        """确认删除"""
        self.logger.info("确认删除 - 开始执行")
        self.wait_seconds(2)

        try:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            self.driver.switch_to.alert.accept()
            self.logger.info("已确认浏览器原生弹窗")
            return self
        except TimeoutException:
            pass

        # 方式1: 查找确认按钮并点击
        try:
            if self.is_element_visible(*self.CONFIRM_BUTTON, timeout=5):
                self.click(*self.CONFIRM_BUTTON)
                self.logger.info("确认按钮点击成功（方式1）")
                return self
        except Exception as e:
            self.logger.warning(f"方式1失败: {e}")

        # 方式2: 直接查找并点击
        try:
            confirm_btn = self.driver.find_element(By.XPATH,
                                                   "//button[contains(text(),'确认') or contains(text(),'确定')]")
            confirm_btn.click()
            self.logger.info("确认按钮点击成功（方式2）")
            return self
        except Exception as e:
            self.logger.warning(f"方式2失败: {e}")

        # 方式3: JS点击
        try:
            confirm_btn = self.driver.find_element(By.XPATH,
                                                   "//button[contains(text(),'确认') or contains(text(),'确定')]")
            self.driver.execute_script("arguments[0].click();", confirm_btn)
            self.logger.info("确认按钮点击成功（方式3 JS）")
            return self
        except Exception as e:
            self.logger.warning(f"方式3失败: {e}")

        self.logger.warning("未能找到确认按钮，可能弹窗未出现或已自动确认")
        return self

    def click_settlement(self):
        """点击去结算"""
        self.logger.info("点击去结算")
        self.click(*self.SETTLEMENT_BUTTON)
        return self

    def click_go_shopping(self):
        """点击去购物（空购物车时）"""
        self.click(*self.GO_SHOPPING_BUTTON)
        return self

    # ========== 状态获取 ==========

    def get_cart_item_count(self) -> int:
        try:
            items = self.find_all(*self.CART_ITEM)
            return len(items)
        except:
            return 0

    def get_first_item_quantity(self) -> int:
        try:
            items = self.find_all(*self.CART_ITEM)
            if items:
                qty_input = items[0].find_element(*self.ITEM_QUANTITY_INPUT)
                return int(qty_input.get_attribute("value") or 0)
            return 0
        except:
            return 0

    def get_total_price(self) -> float:
        """
        获取页面显示的总价
        """
        try:
            price_text = self.get_text(*self.TOTAL_PRICE)
            import re
            numbers = re.findall(r'\d+\.?\d*', price_text.replace(',', ''))
            return float(numbers[0]) if numbers else 0.0
        except:
            return 0.0

    def calculate_subtotal(self) -> float:
        total = 0.0
        try:
            items = self.find_all(*self.CART_ITEM)
            for item in items:
                # 获取单价
                price_text = item.find_element(*self.ITEM_PRICE).text
                import re
                price_numbers = re.findall(r'\d+\.?\d*', price_text.replace(',', ''))
                price = float(price_numbers[0]) if price_numbers else 0.0

                # 获取数量
                qty_input = item.find_element(*self.ITEM_QUANTITY_INPUT)
                quantity = int(qty_input.get_attribute("value") or 1)

                total += price * quantity
        except Exception as e:
            self.logger.warning(f"计算小计失败: {e}")

        return round(total, 2)

    def is_cart_loaded(self) -> bool:
        return self.is_element_visible(*self.CART_TITLE) or self.get_cart_item_count() > 0 or self.is_element_visible(
            *self.EMPTY_CART)

    def is_empty_state_displayed(self) -> bool:
        return self.is_element_visible(*self.EMPTY_CART)