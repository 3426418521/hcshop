"""
消息中心页面对象
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from .base_page import BasePage


class MessagePage(BasePage):
    """消息中心页面对象"""

    # ========== 页面 URL ==========
    MESSAGE_URL = "/index.php?s=/index/message/index.html"

    # ========== 元素定位 ==========
    # 页面标题
    PAGE_TITLE = (By.XPATH, "//h2[contains(text(),'消息') or contains(.,'站内信')]")

    # 消息列表
    MESSAGE_ITEMS = (By.XPATH, "//div[contains(@class,'message-item')]")
    MESSAGE_ITEM = (By.XPATH, "//div[contains(@class,'message-item')]")

    # 消息信息（相对路径）
    MSG_TITLE = (By.XPATH, ".//div[contains(@class,'title')]")
    MSG_CONTENT = (By.XPATH, ".//div[contains(@class,'content')]")
    MSG_TIME = (By.XPATH, ".//span[contains(@class,'time')]")
    MSG_UNREAD_TAG = (By.XPATH, ".//span[contains(@class,'unread') or contains(text(),'未读')]")

    # 操作按钮（相对路径）
    MSG_READ = (By.XPATH, ".//a[contains(text(),'标记已读') or contains(@class,'read')]")
    MSG_DELETE = (
        By.XPATH,
        ".//a[contains(text(),'删除') or contains(@class,'delete') or contains(@href,'delete')]",
    )

    # 批量操作
    SELECT_ALL_MSG = (By.XPATH, "//input[@type='checkbox' and contains(@class,'all')]")
    READ_ALL_BUTTON = (By.XPATH, "//button[contains(text(),'全部已读')]")
    DELETE_ALL_BUTTON = (By.XPATH, "//button[contains(text(),'批量删除')]")

    # 未读数量
    UNREAD_COUNT = (By.XPATH, "//span[contains(@class,'unread-count') or contains(@class,'badge')]")

    # 空状态
    EMPTY_MESSAGE = (
        By.XPATH,
        "//div[contains(@class,'empty')] | //*[contains(text(),'暂无消息')] | "
        "//*[contains(text(),'没有') and contains(text(),'消息')]",
    )

    # 确认弹窗
    CONFIRM_BUTTON = (By.XPATH, "//button[contains(text(),'确认') or contains(text(),'确定')]")

    # ========== 页面操作方法 ==========

    def open_message_page(self):
        """打开消息中心"""
        self.logger.info("打开消息中心")
        return self.open(self.MESSAGE_URL)

    def click_first_message(self):
        """点击第一条消息"""
        self.logger.info("点击第一条消息")
        items = self.driver.find_elements(*self.MESSAGE_ITEM)
        if items:
            self.driver.execute_script("arguments[0].click();", items[0])
        return self

    def read_first_message(self):
        """标记第一条已读"""
        self.logger.info("标记第一条已读")
        items = self.driver.find_elements(*self.MESSAGE_ITEM)
        if items:
            read_btn = items[0].find_element(*self.MSG_READ)
            self.driver.execute_script("arguments[0].click();", read_btn)
        return self

    def delete_first_message(self):
        """删除第一条消息"""
        self.logger.info("删除第一条消息")
        items = self.driver.find_elements(*self.MESSAGE_ITEM)
        if items:
            delete_btn = items[0].find_element(*self.MSG_DELETE)
            self.driver.execute_script("arguments[0].click();", delete_btn)
        return self

    def confirm_delete(self):
        """确认删除"""
        self.logger.info("确认删除")
        try:
            WebDriverWait(self.driver, 4).until(EC.alert_is_present())
            self.driver.switch_to.alert.accept()
            return self
        except TimeoutException:
            pass
        if self.is_element_visible(*self.CONFIRM_BUTTON, timeout=4):
            try:
                self.click(*self.CONFIRM_BUTTON)
            except Exception:
                self.js_click(*self.CONFIRM_BUTTON)
        return self

    def click_read_all(self):
        """全部标记已读"""
        self.logger.info("全部标记已读")
        self.click(*self.READ_ALL_BUTTON)
        return self

    # ========== 状态获取 ==========

    def is_message_list_loaded(self) -> bool:
        """消息列表是否加载"""
        if "message" not in self.driver.current_url.lower():
            return False
        if self.get_message_count() > 0:
            return True
        if self.is_element_visible(*self.EMPTY_MESSAGE, timeout=5):
            return True
        if self.is_element_visible(*self.PAGE_TITLE, timeout=8):
            return True
        try:
            txt = self.driver.execute_script("return (document.body && document.body.innerText) || ''")
            if txt and "消息" in txt and len(txt) > 50:
                return True
        except Exception:
            pass
        return self.is_element_present((By.XPATH, "//div[contains(@class,'am-container')]"), timeout=5)

    def get_message_count(self) -> int:
        """获取消息总数"""
        try:
            return len(self.driver.find_elements(*self.MESSAGE_ITEM))
        except Exception:
            return 0

    def get_unread_count(self) -> int:
        """获取未读消息数"""
        try:
            if self.is_element_visible(*self.UNREAD_COUNT):
                count_text = self.get_text(*self.UNREAD_COUNT)
                import re
                numbers = re.findall(r'\d+', count_text)
                return int(numbers[0]) if numbers else 0
            items = self.driver.find_elements(*self.MESSAGE_ITEM)
            unread = 0
            for item in items:
                if item.find_elements(*self.MSG_UNREAD_TAG):
                    unread += 1
            return unread
        except:
            return 0

    def is_empty_state_displayed(self) -> bool:
        """是否空消息列表（无条目即视为空状态，兼容主题未单独做 empty 区块）"""
        if self.get_message_count() == 0:
            return True
        return self.is_element_visible(*self.EMPTY_MESSAGE, timeout=5)