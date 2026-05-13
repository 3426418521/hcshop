"""
页面对象基类
封装所有页面通用的 Selenium 操作方法
"""

import time
import logging
from typing import Tuple, List, Optional, Union
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotVisibleException,
    StaleElementReferenceException
)

logger = logging.getLogger("Hsyuan")
class BasePage:
    """所有页面对象的基类"""
    # 默认超时时间（秒）
    DEFAULT_TIMEOUT = 10
    # 默认轮询间隔（秒）
    DEFAULT_POLL = 0.5
    def __init__(self, driver: WebDriver):
        """
        初始化页面

        Args:
            driver: WebDriver 实例
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT, self.DEFAULT_POLL)
        self.base_url = "http://shop-xo.hctestedu.com"
        self.logger = logging.getLogger(self.__class__.__name__)

    # ==================== 导航方法 ====================

    def open(self, url: str = ""):
        """
        打开页面

        Args:
            url: 相对路径，如 "/index.html"；若以 http(s):// 开头则视为完整 URL

        Returns:
            self，支持链式调用
        """
        url = (url or "").strip()
        if url.startswith("http://") or url.startswith("https://"):
            full_url = url
        else:
            if url and not url.startswith("/"):
                url = "/" + url
            full_url = self.base_url + url
        self.logger.info(f"打开页面: {full_url}")
        self.driver.get(full_url)
        return self

    def refresh(self):
        """刷新页面"""
        self.logger.info("刷新页面")
        self.driver.refresh()
        return self

    def back(self):
        """浏览器后退"""
        self.logger.info("浏览器后退")
        self.driver.back()
        return self

    def forward(self):
        """浏览器前进"""
        self.logger.info("浏览器前进")
        self.driver.forward()
        return self

    def get_title(self) -> str:
        """获取页面标题"""
        return self.driver.title

    def get_url(self) -> str:
        """获取当前 URL"""
        return self.driver.current_url

    # ==================== 元素查找方法 ====================

    def find(self, by: By, value: str, timeout: int = None) -> WebElement:
        """
        显式等待查找单个元素

        Args:
            by: 定位方式
            value: 定位值
            timeout: 自定义超时时间

        Returns:
            WebElement 元素对象
        """
        wait_time = timeout or self.DEFAULT_TIMEOUT
        custom_wait = WebDriverWait(self.driver, wait_time, self.DEFAULT_POLL)

        self.logger.debug(f"查找元素: {by}={value}")
        return custom_wait.until(
            EC.presence_of_element_located((by, value))
        )

    def find_visible(self, by: By, value: str, timeout: int = None) -> WebElement:
        """
        查找可见元素

        Args:
            by: 定位方式
            value: 定位值
            timeout: 自定义超时时间

        Returns:
            WebElement 元素对象
        """
        wait_time = timeout or self.DEFAULT_TIMEOUT
        custom_wait = WebDriverWait(self.driver, wait_time, self.DEFAULT_POLL)

        self.logger.debug(f"查找可见元素: {by}={value}")
        return custom_wait.until(
            EC.visibility_of_element_located((by, value))
        )

    def find_clickable(self, by: By, value: str, timeout: int = None) -> WebElement:

        wait_time = timeout or self.DEFAULT_TIMEOUT
        custom_wait = WebDriverWait(self.driver, wait_time, self.DEFAULT_POLL)

        self.logger.debug(f"查找可点击元素: {by}={value}")
        return custom_wait.until(
            EC.element_to_be_clickable((by, value))
        )

    def find_all(self, by: By, value: str, timeout: int = None) -> List[WebElement]:
        """
        查找所有匹配的元素

        Args:
            by: 定位方式
            value: 定位值
            timeout: 自定义超时时间

        Returns:
            WebElement 列表
        """
        wait_time = timeout or self.DEFAULT_TIMEOUT
        custom_wait = WebDriverWait(self.driver, wait_time, self.DEFAULT_POLL)

        self.logger.debug(f"查找所有元素: {by}={value}")
        return custom_wait.until(
            EC.presence_of_all_elements_located((by, value))
        )

    # ==================== 元素操作方法 ====================

    def click(self, by: By, value: str, timeout: int = None):
        """
        点击元素

        Args:
            by: 定位方式
            value: 定位值
            timeout: 自定义超时时间

        Returns:
            self，支持链式调用
        """
        element = self.find_clickable(by, value, timeout)
        self.logger.info(f"点击元素: {by}={value}")
        element.click()
        return self

    def send_keys(self, by: By, value: str, text: str, clear_first: bool = True, timeout: int = None):
        """
        输入文本

        Args:
            by: 定位方式
            value: 定位值
            text: 输入内容
            clear_first: 是否先清空
            timeout: 自定义超时时间

        Returns:
            self，支持链式调用
        """
        element = self.find_visible(by, value, timeout)

        if clear_first:
            self.logger.info(f"清空并输入: {by}={value}, 内容: {text}")
            element.clear()
        else:
            self.logger.info(f"输入: {by}={value}, 内容: {text}")

        element.send_keys(text)
        return self

    def get_text(self, by: By, value: str, timeout: int = None) -> str:
        """
        获取元素文本

        Args:
            by: 定位方式
            value: 定位值
            timeout: 自定义超时时间

        Returns:
            元素文本内容
        """
        element = self.find_visible(by, value, timeout)
        text = element.text
        self.logger.info(f"获取文本: {by}={value}, 内容: {text}")
        return text

    def get_attribute(self, by: By, value: str, attribute: str, timeout: int = None) -> str:

        element = self.find(by, value, timeout)
        attr_value = element.get_attribute(attribute)
        self.logger.info(f"获取属性: {by}={value}, {attribute}={attr_value}")
        return attr_value

    def clear(self, by: By, value: str, timeout: int = None):

        element = self.find_visible(by, value, timeout)
        self.logger.info(f"清空输入框: {by}={value}")
        element.clear()
        return self

    # ==================== 元素状态判断 ====================

    def is_element_visible(self, by: By, value: str, timeout: int = 3) -> bool:

        try:
            wait = WebDriverWait(self.driver, timeout, self.DEFAULT_POLL)
            wait.until(EC.visibility_of_element_located((by, value)))
            return True
        except TimeoutException:
            return False

    def is_element_present(self, by: By, value: str, timeout: int = 3) -> bool:
        """
        判断元素是否存在（短超时，不抛异常）

        Args:
            by: 定位方式
            value: 定位值
            timeout: 短超时时间

        Returns:
            True/False
        """
        try:
            wait = WebDriverWait(self.driver, timeout, self.DEFAULT_POLL)
            wait.until(EC.presence_of_element_located((by, value)))
            return True
        except TimeoutException:
            return False

    def is_element_clickable(self, by: By, value: str, timeout: int = 3) -> bool:
        """
        判断元素是否可点击（短超时，不抛异常）

        Args:
            by: 定位方式
            value: 定位值
            timeout: 短超时时间

        Returns:
            True/False
        """
        try:
            wait = WebDriverWait(self.driver, timeout, self.DEFAULT_POLL)
            wait.until(EC.element_to_be_clickable((by, value)))
            return True
        except TimeoutException:
            return False

    # ==================== 等待方法 ====================

    def wait_for_element_visible(self, by: By, value: str, timeout: int = None):
        """
        等待元素可见

        Args:
            by: 定位方式
            value: 定位值
            timeout: 超时时间

        Returns:
            self，支持链式调用
        """
        wait_time = timeout or self.DEFAULT_TIMEOUT
        self.logger.info(f"等待元素可见: {by}={value}, 超时: {wait_time}s")
        WebDriverWait(self.driver, wait_time, self.DEFAULT_POLL).until(
            EC.visibility_of_element_located((by, value))
        )
        return self

    def wait_for_element_invisible(self, by: By, value: str, timeout: int = None):
        """
        等待元素不可见

        Args:
            by: 定位方式
            value: 定位值
            timeout: 超时时间

        Returns:
            self，支持链式调用
        """
        wait_time = timeout or self.DEFAULT_TIMEOUT
        self.logger.info(f"等待元素不可见: {by}={value}, 超时: {wait_time}s")
        WebDriverWait(self.driver, wait_time, self.DEFAULT_POLL).until(
            EC.invisibility_of_element_located((by, value))
        )
        return self

    def wait_for_text_present(self, by: By, value: str, text: str, timeout: int = None):
        """
        等待元素包含指定文本

        Args:
            by: 定位方式
            value: 定位值
            text: 期望文本
            timeout: 超时时间

        Returns:
            self，支持链式调用
        """
        wait_time = timeout or self.DEFAULT_TIMEOUT
        self.logger.info(f"等待文本出现: {by}={value}, 文本: {text}")
        WebDriverWait(self.driver, wait_time, self.DEFAULT_POLL).until(
            EC.text_to_be_present_in_element((by, value), text)
        )
        return self

    def wait_seconds(self, seconds: float):
        """
        强制等待（尽量少用）

        Args:
            seconds: 等待秒数

        Returns:
            self，支持链式调用
        """
        self.logger.warning(f"强制等待: {seconds}s")
        time.sleep(seconds)
        return self

    # ==================== JavaScript 操作 ====================

    def js_click(self, by: By, value: str):
        """
        JavaScript 强制点击（用于普通点击失败时）

        Args:
            by: 定位方式
            value: 定位值

        Returns:
            self，支持链式调用
        """
        element = self.find(by, value)
        self.logger.info(f"JS点击: {by}={value}")
        self.driver.execute_script("arguments[0].click();", element)
        return self

    def js_send_keys(self, by: By, value: str, text: str):
        """
        JavaScript 设置输入框值

        Args:
            by: 定位方式
            value: 定位值
            text: 输入内容

        Returns:
            self，支持链式调用
        """
        element = self.find(by, value)
        self.logger.info(f"JS输入: {by}={value}, 内容: {text}")
        self.driver.execute_script("arguments[0].value = arguments[1];", element, text)
        return self

    def js_scroll_to_element(self, by: By, value: str):
        """
        滚动到元素位置

        Args:
            by: 定位方式
            value: 定位值

        Returns:
            self，支持链式调用
        """
        element = self.find(by, value)
        self.logger.info(f"滚动到元素: {by}={value}")
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        return self

    def js_scroll_to_bottom(self):
        """滚动到页面底部"""
        self.logger.info("滚动到页面底部")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        return self

    def js_scroll_to_top(self):
        """滚动到页面顶部"""
        self.logger.info("滚动到页面顶部")
        self.driver.execute_script("window.scrollTo(0, 0);")
        return self

    # ==================== 弹窗处理 ====================

    def accept_alert(self):
        """接受弹窗"""
        self.logger.info("接受弹窗")
        self.driver.switch_to.alert.accept()
        return self

    def dismiss_alert(self):
        """取消弹窗"""
        self.logger.info("取消弹窗")
        self.driver.switch_to.alert.dismiss()
        return self

    def get_alert_text(self) -> str:
        """获取弹窗文本"""
        text = self.driver.switch_to.alert.text
        self.logger.info(f"弹窗文本: {text}")
        return text

    # ==================== 截图方法 ====================

    def take_screenshot(self, filename: str = None) -> bytes:
        """
        截图

        Args:
            filename: 保存文件名（可选）

        Returns:
            截图二进制数据
        """
        screenshot = self.driver.get_screenshot_as_png()

        if filename:
            self.driver.save_screenshot(filename)
            self.logger.info(f"截图保存: {filename}")

        return screenshot

    # ==================== iframe 切换 ====================

    def switch_to_frame(self, by: By, value: str):
        """
        切换到 iframe

        Args:
            by: 定位方式
            value: 定位值

        Returns:
            self，支持链式调用
        """
        element = self.find(by, value)
        self.logger.info(f"切换到iframe: {by}={value}")
        self.driver.switch_to.frame(element)
        return self

    def switch_to_default_content(self):
        """切换回主文档"""
        self.logger.info("切换回主文档")
        self.driver.switch_to.default_content()
        return self

    # ==================== 窗口切换 ====================

    def switch_to_window(self, index: int = -1):
        """
        切换到指定窗口

        Args:
            index: 窗口索引，-1 表示最新窗口

        Returns:
            self，支持链式调用
        """
        handles = self.driver.window_handles
        self.logger.info(f"切换到窗口: {index}, 总窗口数: {len(handles)}")
        self.driver.switch_to.window(handles[index])
        return self

    def close_current_window(self):
        """关闭当前窗口"""
        self.logger.info("关闭当前窗口")
        self.driver.close()
        return self