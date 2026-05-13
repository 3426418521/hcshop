"""
浏览器驱动封装 - 使用本地 ChromeDriver
"""

import os
import logging

from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# 关闭 WebDriver Manager 日志
os.environ['WDM_LOG_LEVEL'] = '0'

logger = logging.getLogger("Hsyuan")

# ============================================
# 本地 ChromeDriver 路径（改成你的路径）
# ============================================
LOCAL_DRIVER = r"D:\chromedriver_win32\chromedriver.exe"


class Browser:
    """浏览器驱动管理类"""

    def __init__(self, browser_type: str = "chrome", headless: bool = False):
        self.browser_type = browser_type.lower()
        self.headless = headless
        self.driver = None

    def _get_chrome_options(self) -> Options:
        """获取 Chrome 配置"""
        options = Options()

        if self.headless:
            options.add_argument("--headless")

        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--ignore-certificate-errors")

        # 禁用自动化检测
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # 禁用密码保存提示
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2
        }
        options.add_experimental_option("prefs", prefs)

        return options

    def _get_firefox_options(self) -> FirefoxOptions:
        """获取 Firefox 配置"""
        options = FirefoxOptions()

        if self.headless:
            options.add_argument("--headless")

        options.add_argument("--width=1920")
        options.add_argument("--height=1080")

        return options

    def get_driver(self):
        """
        获取 WebDriver 实例
        直接使用本地 ChromeDriver，不自动下载
        """
        try:
            if self.browser_type == "chrome":
                options = self._get_chrome_options()

                local_service = (
                    Service(LOCAL_DRIVER) if os.path.exists(LOCAL_DRIVER) else None
                )
                if local_service:
                    logger.info(f"尝试本地 ChromeDriver: {LOCAL_DRIVER}")
                    try:
                        self.driver = webdriver.Chrome(
                            service=local_service, options=options
                        )
                    except SessionNotCreatedException as e:
                        logger.warning(
                            "本地驱动与 Chrome 版本不匹配，改用 Selenium Manager: %s", e
                        )
                        self.driver = webdriver.Chrome(service=Service(), options=options)
                else:
                    logger.info("未找到本地 ChromeDriver，使用 Selenium Manager 自动匹配")
                    self.driver = webdriver.Chrome(service=Service(), options=options)

            elif self.browser_type == "firefox":
                options = self._get_firefox_options()
                service = Service()
                self.driver = webdriver.Firefox(service=service, options=options)

            elif self.browser_type == "edge":
                from selenium.webdriver.edge.service import Service as EdgeService
                from selenium.webdriver.edge.options import Options as EdgeOptions
                options = EdgeOptions()
                options.page_load_strategy = "eager"
                if self.headless:
                    options.add_argument("--headless")
                    options.add_argument("--disable-gpu")
                    options.add_argument("--no-sandbox")
                    options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--window-size=1920,1080")
                service = EdgeService()
                self.driver = webdriver.Edge(service=service, options=options)
            else:
                raise ValueError(f"不支持的浏览器类型: {self.browser_type}")

            # 显式等待由 BasePage 控制；隐式等待与显式混用易拉长失败耗时
            self.driver.implicitly_wait(0)
            self.driver.set_page_load_timeout(120)
            self.driver.set_script_timeout(45)

            logger.info(f"{self.browser_type} 浏览器启动成功")
            return self.driver

        except Exception as e:
            logger.error(f"浏览器启动失败: {e}")
            raise

    def quit(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("浏览器已关闭")


def get_chrome_driver(headless: bool = False):
    """快速获取 Chrome 驱动"""
    browser = Browser("chrome", headless)
    return browser.get_driver()