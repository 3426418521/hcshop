"""个人中心页面对象"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage


class ProfilePage(BasePage):
    """个人中心页面对象"""

    # ========== 页面 URL ==========
    PROFILE_URL = "/index.php?s=/index/user/index.html"          # 个人中心首页（带左侧菜单）
    PERSONAL_URL = "/index.php?s=/index/personal/index.html"     # 个人资料展示页
    EDIT_PROFILE_URL = "/index.php?s=/index/personal/saveinfo.html"  # 编辑基本资料页
    MOBILE_EDIT_URL = "/index.php?s=/index/safety/mobileinfo.html"    # 修改手机号页
    EMAIL_EDIT_URL = "/index.php?s=/index/safety/emailinfo.html"      # 修改邮箱页

    # ========== 个人中心首页 (user/index.html) 定位器 ==========
    # 修改资料链接（位于用户头像区域）
    MODIFY_PROFILE_LINK = (By.XPATH, "//a[contains(@href, '/personal/index.html') and contains(@class, 'am-icon-edit')]")
    USER_AVATAR = (By.XPATH, "//div[contains(@class,'user-avatar')]//img")
    USER_NAME_TOP = (By.XPATH, "//div[contains(@class,'user-name')]/span")
    ORDER_COUNT = (By.XPATH, "//ul[contains(@class,'user-base-icon')]//li/a[p[text()='订单总数']]/p[1]")
    COLLECT_COUNT = (By.XPATH, "//ul[contains(@class,'user-base-icon')]//li/a[p[text()='商品收藏']]/p[1]")
    MY_ORDERS = (By.XPATH, "//a[contains(@href,'/order/index.html')]")
    MY_ADDRESS = (By.XPATH, "//a[contains(@href,'useraddress/index.html') or contains(text(),'我的地址')]")
    MY_COLLECT = (By.XPATH, "//a[contains(@href,'usergoodsfavor/index.html') or contains(text(),'商品收藏')]")

    # ========== 个人资料展示页 (personal/index.html) 定位器 ==========
    PROFILE_SECTION = (By.XPATH, "//div[contains(@class, 'user-content-body')]")
    NICKNAME_VALUE = (By.XPATH, "//div[contains(@class,'user-content-body')]//dl//dt[text()='昵称']/following-sibling::dd")
    GENDER_VALUE = (By.XPATH, "//div[contains(@class,'user-content-body')]//dl//dt[text()='性别']/following-sibling::dd")
    BIRTHDAY_VALUE = (By.XPATH, "//div[contains(@class,'user-content-body')]//dl//dt[text()='生日']/following-sibling::dd")
    PHONE_VALUE = (By.XPATH, "//div[contains(@class,'user-content-body')]//dl//dt[text()='手机号码']/following-sibling::dd")
    EMAIL_VALUE = (By.XPATH, "//div[contains(@class,'user-content-body')]//dl//dt[text()='电子邮箱']/following-sibling::dd")
    EDIT_BASIC_INFO_BTN = (By.XPATH, "//div[contains(@class,'user-content-body')]//legend//a[contains(text(),'编辑')]")
    EDIT_MOBILE_BTN = (By.XPATH, "//dt[text()='手机号码']/following-sibling::dd//a[contains(text(),'修改')]")
    EDIT_EMAIL_BTN = (By.XPATH, "//dt[text()='电子邮箱']/following-sibling::dd//a[contains(text(),'修改')]")

    # ========== 编辑基本资料页 (saveinfo.html) 定位器 ==========
    NICKNAME_INPUT = (By.NAME, "nickname")
    AVATAR_UPLOAD = (By.XPATH, "//input[@type='file' and contains(@name,'avatar')]")
    SAVE_BUTTON = (By.XPATH, "//button[contains(text(),'保存') or contains(text(),'确定')]")
    SUCCESS_TIP = (By.XPATH, "//div[contains(@class,'am-alert-success') or contains(@class,'success')]")

    # ========== 修改手机号页 (mobileinfo.html) 定位器 ==========
    MOBILE_INPUT = (By.NAME, "mobile")
    MOBILE_CAPTCHA_INPUT = (By.NAME, "captcha")
    MOBILE_GET_CAPTCHA_BTN = (By.XPATH, "//button[contains(text(),'获取验证码')]")
    MOBILE_SAVE_BTN = (By.XPATH, "//button[contains(text(),'保存')]")

    # ========== 页面操作方法 ==========

    # --- 个人中心首页操作 ---
    def open_profile_page(self):
        """打开个人中心首页 (user/index.html)"""
        self.logger.info("打开个人中心首页")
        self.open(self.PROFILE_URL)
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'user-base')]"))
        )
        return self

    def click_modify_profile_link(self):
        """点击「修改资料」链接，跳转到个人资料展示页 (personal/index.html)"""
        self.logger.info("点击「修改资料」链接")
        self.click(*self.MODIFY_PROFILE_LINK, timeout=15)
        # 等待资料展示页加载完成
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.PROFILE_SECTION)
        )
        return self

    # --- 个人资料展示页操作 ---
    def open_personal_page_direct(self):
        """直接打开个人资料展示页（不通过点击链接，仅用于快速测试）"""
        self.logger.info("直接打开个人资料展示页")
        self.open(self.PERSONAL_URL)
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.PROFILE_SECTION)
        )
        return self

    def click_edit_basic_info(self):
        """在资料展示页点击「编辑」按钮，进入基本资料编辑页 (saveinfo.html)"""
        self.logger.info("点击编辑基本资料按钮")
        self.click(*self.EDIT_BASIC_INFO_BTN, timeout=15)
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.NICKNAME_INPUT)
        )
        return self

    def click_edit_mobile(self):
        """点击手机号旁边的「修改」链接，进入手机号修改页"""
        self.logger.info("点击修改手机号链接")
        self.click(*self.EDIT_MOBILE_BTN, timeout=15)
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.MOBILE_INPUT)
        )
        return self

    def click_edit_email(self):
        """点击邮箱旁边的「修改」链接，进入邮箱修改页"""
        self.logger.info("点击修改邮箱链接")
        self.click(*self.EDIT_EMAIL_BTN, timeout=15)
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        return self

    # --- 编辑基本资料页操作 ---
    def input_nickname(self, nickname: str):
        """在编辑页输入昵称（清空原内容）"""
        nickname_input = self.find(*self.NICKNAME_INPUT)
        nickname_input.clear()
        nickname_input.send_keys(nickname)
        return self

    def save_profile(self):
        """保存基本资料修改，并等待返回个人资料展示页"""
        self.logger.info("保存资料")
        try:
            self.click(*self.SAVE_BUTTON, timeout=12)
        except Exception:
            self.js_click(*self.SAVE_BUTTON)
        # 等待返回 personal/index.html
        WebDriverWait(self.driver, 15).until(
            lambda d: "personal/index" in d.current_url
        )
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.PROFILE_SECTION)
        )
        return self

    # --- 获取个人资料展示页信息 ---
    def get_nickname_text(self) -> str:
        """获取当前展示的昵称（处理「未填写」情况）"""
        try:
            elem = self.find(*self.NICKNAME_VALUE, timeout=5)
            text = elem.text.strip()
            return "" if text == "未填写" else text
        except Exception:
            return ""

    def get_mobile_text(self) -> str:
        """获取当前展示的手机号"""
        try:
            elem = self.find(*self.PHONE_VALUE, timeout=5)
            return elem.text.strip()
        except Exception:
            return ""

    def get_email_text(self) -> str:
        """获取当前展示的邮箱"""
        try:
            elem = self.find(*self.EMAIL_VALUE, timeout=5)
            return elem.text.strip()
        except Exception:
            return ""

    # --- 个人中心首页其他方法（用于其他测试）---
    def is_avatar_displayed(self) -> bool:
        return self.is_element_visible(*self.USER_AVATAR, timeout=5)

    def get_username_top(self) -> str:
        try:
            return self.get_text(*self.USER_NAME_TOP)
        except Exception:
            return ""

    def get_order_count(self) -> int:
        try:
            text = self.get_text(*self.ORDER_COUNT)
            return int(text) if text.isdigit() else 0
        except Exception:
            return 0

    def click_my_orders(self):
        self.click(*self.MY_ORDERS, timeout=15)
        return self

    def click_my_address(self):
        self.click(*self.MY_ADDRESS, timeout=15)
        return self

    def click_my_collect(self):
        self.click(*self.MY_COLLECT, timeout=15)
        return self