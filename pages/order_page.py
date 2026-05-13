"""
订单页面对象
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from .base_page import BasePage


class OrderPage(BasePage):
    """订单页面对象"""

    # ========== 页面 URL ==========
    ORDER_LIST_URL = "/index.php?s=/index/order/index.html"
    ORDER_DETAIL_URL = "/index.php?s=/index/order/detail.html"

    # ========== 元素定位 ==========
    # 订单列表
    ORDER_ITEMS = (By.XPATH, "//div[contains(@class,'order-item')]")
    ORDER_ITEM = (
        By.XPATH,
        "//div[contains(@class,'order-item')]"
        " | //ul[contains(@class,'order')]//li"
        " | //div[contains(@class,'order-list')]//div[contains(@class,'items')]",
    )

    # 订单信息（相对路径）
    ORDER_ID = (By.XPATH, ".//span[contains(@class,'order-id') or contains(text(),'订单号')]")
    ORDER_STATUS = (By.XPATH, ".//span[contains(@class,'status')]")
    ORDER_TOTAL = (By.XPATH, ".//span[contains(@class,'total') or contains(@class,'price')]")
    ORDER_DATE = (By.XPATH, ".//span[contains(@class,'date') or contains(@class,'time')]")

    # 订单操作按钮（相对路径）
    PAY_BUTTON = (By.XPATH, ".//button[contains(text(),'付款') or contains(text(),'支付')]")
    CANCEL_BUTTON = (By.XPATH, ".//a[contains(text(),'取消订单') or contains(text(),'取消')]")
    CONFIRM_RECEIVE_BUTTON = (By.XPATH, ".//button[contains(text(),'确认收货')]")
    DELETE_ORDER_BUTTON = (By.XPATH, ".//a[contains(text(),'删除订单')]")
    VIEW_DETAIL_BUTTON = (By.XPATH, ".//a[contains(text(),'查看详情')]")

    # 筛选标签
    TAB_ALL = (By.XPATH, "//li[contains(text(),'全部') or contains(@data-status,'')]")
    TAB_UNPAID = (By.XPATH, "//li[contains(text(),'待付款') or contains(@data-status,'1')]")
    TAB_UNSHIPPED = (By.XPATH, "//li[contains(text(),'待发货') or contains(@data-status,'2')]")
    TAB_UNRECEIVED = (By.XPATH, "//li[contains(text(),'待收货') or contains(@data-status,'3')]")
    TAB_COMPLETED = (By.XPATH, "//li[contains(text(),'已完成') or contains(@data-status,'4')]")

    # 确认弹窗
    CONFIRM_BUTTON = (By.XPATH, "//button[contains(text(),'确认') or contains(text(),'确定')]")
    CANCEL_POPUP_BUTTON = (By.XPATH, "//button[contains(text(),'取消')]")

    # 订单详情页
    DETAIL_ORDER_ID = (By.XPATH, "//span[contains(text(),'订单编号')]/following-sibling::span")
    DETAIL_STATUS = (By.XPATH, "//span[contains(text(),'订单状态')]/following-sibling::span")
    DETAIL_TOTAL = (By.XPATH, "//div[contains(@class,'total')]//span[contains(@class,'price')]")
    DETAIL_ADDRESS = (By.XPATH, "//div[contains(@class,'address')]")
    DETAIL_GOODS_LIST = (By.XPATH, "//div[contains(@class,'goods-list')]//div[contains(@class,'goods-item')]")

    # 订单成功页
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class,'success') or contains(@class,'am-alert-success')]")
    ORDER_SUCCESS_TITLE = (By.XPATH, "//h2[contains(text(),'订单提交成功') or contains(text(),'支付成功')]")

    # ========== 页面操作方法 ==========

    def open_order_list(self):
        """打开订单列表"""
        self.logger.info("打开订单列表")
        return self.open(self.ORDER_LIST_URL)

    def filter_by_status(self, status: str):
        """
        按状态筛选订单

        Args:
            status: all/unpaid/unshipped/unreceived/completed
        """
        self.logger.info(f"筛选订单状态: {status}")
        status_map = {
            "all": self.TAB_ALL,
            "待付款": self.TAB_UNPAID,
            "unpaid": self.TAB_UNPAID,
            "待发货": self.TAB_UNSHIPPED,
            "unshipped": self.TAB_UNSHIPPED,
            "待收货": self.TAB_UNRECEIVED,
            "unreceived": self.TAB_UNRECEIVED,
            "已完成": self.TAB_COMPLETED,
            "completed": self.TAB_COMPLETED,
        }
        tab = status_map.get(status, self.TAB_ALL)
        self.click(*tab, timeout=20)
        return self

    def click_first_order(self):
        """点击第一个订单查看详情"""
        self.logger.info("点击第一个订单")
        items = self.find_all(*self.ORDER_ITEM)
        if items:
            detail_btn = items[0].find_element(*self.VIEW_DETAIL_BUTTON)
            detail_btn.click()
        return self

    def click_pay_first_order(self):
        """点击第一个订单的支付按钮"""
        self.logger.info("点击支付第一个订单")
        items = self.find_all(*self.ORDER_ITEM)
        if items:
            pay_btn = items[0].find_element(*self.PAY_BUTTON)
            pay_btn.click()
        return self

    def click_cancel_first_order(self):
        """点击取消第一个订单"""
        self.logger.info("点击取消第一个订单")
        items = self.find_all(*self.ORDER_ITEM)
        if items:
            cancel_btn = items[0].find_element(*self.CANCEL_BUTTON)
            cancel_btn.click()
        return self

    def confirm_cancel(self):
        """确认取消"""
        self.logger.info("确认取消订单")
        try:
            WebDriverWait(self.driver, 4).until(EC.alert_is_present())
            self.driver.switch_to.alert.accept()
            return self
        except TimeoutException:
            pass
        if self.is_element_visible(*self.CONFIRM_BUTTON, timeout=5):
            try:
                self.click(*self.CONFIRM_BUTTON)
            except Exception:
                self.js_click(*self.CONFIRM_BUTTON)
        return self

    def select_address(self):
        """选择收货地址（下单时）"""
        self.logger.info("选择收货地址")
        return self

    def submit_order(self):
        """提交订单"""
        self.logger.info("提交订单")
        submit_btn = (By.XPATH, "//button[contains(text(),'提交订单') or contains(text(),'确认下单')]")
        self.click(*submit_btn)
        return self

    # ========== 状态获取 ==========

    def is_order_list_loaded(self) -> bool:
        """订单列表是否加载（含空列表页）"""
        if "order" not in self.driver.current_url.lower():
            return False
        try:
            if len(self.driver.find_elements(*self.ORDER_ITEM)) > 0:
                return True
        except Exception:
            pass
        return self.is_element_visible(
            By.XPATH, "//h2[contains(.,'订单') or contains(.,'我的订单')]", timeout=5
        ) or self.is_element_present(
            By.XPATH, "//*[contains(text(),'暂无') and contains(text(),'订单')]", timeout=3
        )

    def get_order_count(self) -> int:
        """获取订单数量"""
        try:
            return len(self.driver.find_elements(*self.ORDER_ITEM))
        except Exception:
            return 0

    def get_first_order_status(self) -> str:
        """获取第一个订单状态"""
        try:
            items = self.find_all(*self.ORDER_ITEM)
            if items:
                return items[0].find_element(*self.ORDER_STATUS).text
            return ""
        except:
            return ""

    def is_order_success(self) -> bool:
        """是否显示订单成功"""
        return self.is_element_visible(*self.SUCCESS_MESSAGE) or self.is_element_visible(*self.ORDER_SUCCESS_TITLE)

    def get_success_message(self) -> str:
        """获取成功提示文本"""
        if self.is_element_visible(*self.SUCCESS_MESSAGE):
            return self.get_text(*self.SUCCESS_MESSAGE)
        if self.is_element_visible(*self.ORDER_SUCCESS_TITLE):
            return self.get_text(*self.ORDER_SUCCESS_TITLE)
        return ""

    def is_detail_loaded(self) -> bool:
        """订单详情是否加载"""
        return self.is_element_visible(*self.DETAIL_ORDER_ID) or self.is_element_visible(*self.DETAIL_STATUS)