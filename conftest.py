"""
pytest 全局配置和 fixture
提供 UI/API 测试的基础环境
"""

import os
import sys
import json
import logging

import pytest

# 把项目根目录加入路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from selenium import webdriver
from utils.browser import Browser
from utils.requests_handler import RequestsHandler

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("Hsyuan")

# 项目配置
BASE_URL = "http://shop-xo.hctestedu.com"
API_BASE_URL = f"{BASE_URL}/index.php?s="


# ==================== API 测试 Fixture ====================

@pytest.fixture(scope="session")
def api_handler():
    """
    全局 API 请求处理器
    整个测试会话共享一个 session
    """
    handler = RequestsHandler(base_url=API_BASE_URL)
    logger.info(f"API 处理器初始化完成，基础URL: {API_BASE_URL}")

    yield handler

    handler.close()


@pytest.fixture(scope="session")
def api_token(api_handler):
    """
    登录获取 Token，供后续 API 测试使用
    """
    login_data = {
        "accounts": "3426418521",
        "pwd": "WHLSDMN8",
        "type": "username"
    }

    resp = api_handler.post("/api/user/login", json=login_data)
    data = resp.json()
    assert data.get("code") == 0, f"登录失败: {data.get('msg')}"

    payload = data.get("data") or {}
    token = payload.get("token")
    user_info = {
        "token": token,
        "user_id": payload.get("id"),
        "username": payload.get("username"),
    }

    if token:
        api_handler.update_headers({"token": token})
    else:
        api_handler.remove_header("token")
    logger.info(f"用户登录成功: {user_info.get('username') or login_data['accounts']}")

    yield user_info


@pytest.fixture
def auth_api_handler(api_handler, api_token):
    """
    每个测试用例一个已认证的 API 处理器
    有 token 时写入请求头；否则沿用登录后的 Cookie 会话
    """
    if api_token.get("token"):
        api_handler.update_headers({"token": api_token["token"]})
    else:
        api_handler.remove_header("token")
    yield api_handler


# ==================== UI 测试 Fixture ====================

@pytest.fixture
def driver():
    """
    每个 UI 测试用例一个浏览器实例
    测试结束后自动关闭
    """
    browser = None

    try:
        headless = os.environ.get("SHOPXO_HEADLESS", "").strip() in ("1", "true", "yes")
        browser = Browser(browser_type="edge", headless=headless)
        driver = browser.get_driver()
        logger.info("Edge 浏览器启动成功")

        yield driver

    finally:
        if browser and browser.driver:
            browser.quit()
            logger.info("浏览器已关闭")


@pytest.fixture
def headless_driver():
    """无头模式浏览器（用于 CI/CD）"""
    browser = None

    try:
        browser = Browser(browser_type="edge", headless=True)
        driver = browser.get_driver()
        logger.info("无头 Edge 启动成功")

        yield driver

    finally:
        if browser and browser.driver:
            browser.quit()


@pytest.fixture
def logged_driver(driver):
    """
    已登录的浏览器
    自动执行登录操作
    """
    from pages.login_page import LoginPage

    login_page = LoginPage(driver).open_login_page()
    login_page.login("3426418521", "WHLSDMN8")

    assert login_page.is_login_success(), "登录失败"
    logger.info("浏览器登录成功")

    yield driver


# ==================== 失败处理钩子 ====================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    测试失败时自动截图
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = None

        for fixture_name in ["driver", "logged_driver", "headless_driver"]:
            if fixture_name in item.funcargs:
                driver = item.funcargs[fixture_name]
                break

        if driver:
            try:
                screenshot_path = os.path.join(BASE_DIR, "screenshots", f"{item.name}.png")
                os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
                driver.save_screenshot(screenshot_path)
                logger.info(f"失败截图保存: {screenshot_path}")
            except Exception as e:
                logger.warning(f"截图失败: {e}")


# ==================== 测试数据 Fixture ====================

@pytest.fixture(scope="session")
def test_data():
    """从 YAML 加载测试数据"""
    import yaml

    data_file = os.path.join(BASE_DIR, "data", "test_data.yaml")

    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data
    else:
        logger.warning(f"测试数据文件不存在: {data_file}")
        return {}


# ==================== 会话级初始化和清理 ====================

@pytest.fixture(scope="session", autouse=True)
def session_setup_teardown():
    """
    整个测试会话的初始化和清理
    autouse=True 自动执行
    """
    logger.info("=" * 50)
    logger.info("测试会话开始")
    logger.info(f"基础URL: {BASE_URL}")
    logger.info("=" * 50)

    yield

    logger.info("=" * 50)
    logger.info("测试会话结束")
    logger.info("=" * 50)