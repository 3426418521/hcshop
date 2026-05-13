from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from .base_page import BasePage
class LoginPage(BasePage):
    LOGIN_URL="/index.php?s=/index/user/logininfo.html"
    TAB_ACCOUNT=(By.XPATH,"//li[contains(text(),'帐号密码')]")
    TAB_EMAIL = (By.XPATH, "//li[contains(text(),'邮箱验证码')]")
    TAB_PHONE = (By.XPATH, "//li[contains(text(),'手机验证码')]")
    # 账号密码登录表单
    USERNAME_INPUT = (By.NAME, "accounts")
    PASSWORD_INPUT = (By.NAME, "pwd")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(@class,'am-btn') and contains(text(),'登录')]")
    REGISTER_LINK = (By.XPATH, "//a[contains(text(),'注册')]")
    FORGET_PASSWORD_LINK = (By.XPATH, "//a[contains(text(),'忘记密码')]")

    # 错误提示
    ERROR_MESSAGE = (By.XPATH, "//div[contains(@class,'am-alert')]")

    # 登录成功后的元素
    USER_AVATAR = (By.XPATH, "//div[contains(@class,'user-avatar') or contains(@class,'avatar')]")
    USER_NAME_DISPLAY = (By.XPATH, "//span[contains(@class,'username') or contains(@class,'nickname')]")
    LOGOUT_LINK = (By.XPATH, "//a[contains(@href,'logout') or contains(@href,'loginout')]")
    USER_CENTER_LINK = (By.XPATH, "//a[contains(@href,'/user/index') or contains(@href,'user/index')]")
    def open_login_page(self):
        self.logger.info("打开登陆页面")
        return self.open(self.LOGIN_URL)
    def switch_tab(self,tab_type:str="account"):
        self.logger.info(f"切换登录方式: {tab_type}")
        if tab_type == "account":
            self.click(*self.TAB_ACCOUNT)
        elif tab_type == "email":
            self.click(*self.TAB_EMAIL)
        elif tab_type == "phone":
            self.click(*self.TAB_PHONE)
        return self

    def input_username(self, username: str):
        """输入用户名"""
        self.send_keys(*self.USERNAME_INPUT, username)
        return self

    def input_password(self, password: str):
        """输入密码"""
        self.send_keys(*self.PASSWORD_INPUT, password)
        return self
    def click_login_button(self):
        self.click(*self.LOGIN_BUTTON)
        return self
    def click_register(self):
        self.click(*self.REGISTER_LINK)
        return self
    def click_forget_password(self):
        self.click(*self.FORGET_PASSWORD_LINK)
        return self

    def login(self, username: str, password: str):
        self.logger.info(f"执行登录: username={username}")
        return self.input_username(username).input_password(password).click_login_button()
    def get_error_message(self)->str:
        if self.is_element_visible(*self.ERROR_MESSAGE):
            return self.get_text(*self.ERROR_MESSAGE)
        return ""

    def is_error_message_displayed(self) -> bool:
        """是否有错误提示"""
        return self.is_element_visible(*self.ERROR_MESSAGE)

    def is_login_success(self) -> bool:
        """判断是否登录成功（多数主题会跳转到非 logininfo 页面）"""
        try:
            WebDriverWait(self.driver, 15, poll_frequency=0.5).until(
                lambda d: "logininfo" not in d.current_url.lower()
            )
            return True
        except TimeoutException:
            pass
        if self.is_element_visible(*self.USER_AVATAR, timeout=3):
            return True
        if self.is_element_visible(*self.USER_NAME_DISPLAY, timeout=3):
            return True
        if self.is_element_visible(*self.LOGOUT_LINK, timeout=3):
            return True
        if self.is_element_visible(*self.USER_CENTER_LINK, timeout=3):
            return True
        # 如果URL已变化或页面包含用户相关元素，也认为登录成功
        if "user" in self.driver.current_url.lower():
            return True
        if "index" in self.driver.current_url.lower() and "login" not in self.driver.current_url.lower():
            return True
        return False

    def get_displayed_username(self) -> str:
        """获取登录后显示的用户名"""
        if self.is_element_visible(*self.USER_NAME_DISPLAY):
            return self.get_text(*self.USER_NAME_DISPLAY)
        return ""

    def is_username_input_displayed(self) -> bool:
        """用户名输入框是否显示"""
        return self.is_element_visible(*self.USERNAME_INPUT)

    def is_password_input_displayed(self) -> bool:
        """密码输入框是否显示"""
        return self.is_element_visible(*self.PASSWORD_INPUT)

    def is_login_button_displayed(self) -> bool:
        """登录按钮是否显示"""
        return self.is_element_visible(*self.LOGIN_BUTTON)

    def logout(self):
        """退出登录"""
        self.logger.info("执行退出登录")
        if self.is_element_visible(*self.LOGOUT_LINK, timeout=3):
            self.click(*self.LOGOUT_LINK)
        else:
            self.open("/index.php?s=/index/user/logout.html")
        self.wait_seconds(2)
        return self

    def is_logged_in(self) -> bool:
        """检查当前是否已登录"""
        return self.is_element_visible(*self.USER_AVATAR, timeout=3) or \
            self.is_element_visible(*self.USER_NAME_DISPLAY, timeout=3) or \
            self.is_element_visible(*self.LOGOUT_LINK, timeout=3)