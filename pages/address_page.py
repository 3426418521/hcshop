
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage


class AddressPage(BasePage):
    """收货地址页面对象"""

    # ========== 页面 URL ==========
    ADDRESS_DIRECT_URL = "/index.php?s=/index/useraddress/index.html"
    PROFILE_URL = "/index.php?s=/index/user/index.html"

    # ========== 元素定位 ==========
    # 页面标题（不同主题文案可能为「我的地址」或「收货地址」）
    PAGE_TITLE = (By.XPATH, "//*[contains(text(),'我的地址') or contains(text(),'收货地址')]")

    # 个人中心左侧菜单 - 我的地址链接
    SIDEBAR_MY_ADDRESS = (
        By.XPATH,
        "//a[contains(@href,'useraddress/index.html') and (contains(text(),'我的地址') or contains(text(),'收货地址'))]"
    )

    # 地址列表（根据实际 HTML：<ul class="address-list"><li id="data-list-xxx">）
    ADDRESS_ITEMS = (By.XPATH, "//ul[@class='address-list']/li[contains(@id,'data-list-')]")
    ADDRESS_ITEM = (By.XPATH, "//ul[@class='address-list']/li[contains(@id,'data-list-')]")

    # 地址信息（相对 li 路径，根据实际 HTML 修正）
    ADDRESS_NAME = (By.XPATH, ".//span[@class='user']")
    ADDRESS_PHONE = (By.XPATH, ".//span[@class='phone']")
    ADDRESS_DETAIL = (By.XPATH, ".//span[@class='street']")  # 详细地址
    ADDRESS_DEFAULT_TAG = (
        By.XPATH,
        ".//span[contains(@class,'am-badge-success') or contains(@class,'badge')]"
        "[contains(.,'默认')] | .//*[contains(@class,'default')][contains(.,'默认')]",
    )

    # 操作按钮（相对 li 路径，根据实际 HTML 修正）
    EDIT_BUTTON = (By.XPATH, ".//a[contains(@class,'address-submit-save') and contains(text(),'编辑')]")
    DELETE_BUTTON = (By.XPATH, ".//a[contains(@class,'address-submit-delete')]")
    SET_DEFAULT_BUTTON = (By.XPATH, ".//a[contains(@class,'address-default-submit')]")

    # 新增地址按钮（必须是 button 标签，排除编辑用的 a 标签）
    ADD_ADDRESS_BUTTON = (
        By.XPATH,
        "//button[contains(@class,'address-submit-save') and @data-popup-title='新增地址']"
    )

    # 地址表单
    FORM_ALIAS = (By.NAME, "alias")
    FORM_NAME = (By.NAME, "name")
    FORM_TEL = (By.NAME, "tel")
    FORM_ADDRESS = (By.NAME, "address")
    FORM_IS_DEFAULT = (By.XPATH, "//input[@type='checkbox' and contains(@name,'default')]")

    # 保存按钮
    SAVE_BUTTON = (By.XPATH, "//button[contains(text(),'保存') or contains(text(),'确定')]")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(text(),'取消')]")

    # 确认弹窗
    # 在 AddressPage 类中修改 CONFIRM_DELETE 定位器
    CONFIRM_DELETE = (
        By.XPATH,
        "//span[contains(@class,'am-modal-btn') and (@data-am-modal-confirm='' or text()='确定' or text()='确认')] | //button[contains(text(),'确认') or contains(text(),'确定')]"
    )

    def _wait_address_shell_loaded(self, timeout: int = 15):
        """等待地址页关键壳子（新增按钮或标题）出现"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.ADD_ADDRESS_BUTTON)
            )
        except TimeoutException:
            WebDriverWait(self.driver, 8).until(
                EC.presence_of_element_located(self.PAGE_TITLE)
            )

    # ========== 页面操作方法 ==========

    def open_address_page_direct(self):
        """直接打开地址管理页（需已登录），并等待列表/表单入口就绪"""
        self.logger.info("直接打开地址管理页")
        last_err = None
        for attempt in range(2):
            try:
                self.open(self.ADDRESS_DIRECT_URL)
                WebDriverWait(self.driver, 25).until(
                    lambda d: "useraddress" in d.current_url
                )
                WebDriverWait(self.driver, 20).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
                self._wait_address_shell_loaded(20)
                self.logger.info("地址管理页已就绪")
                return self
            except TimeoutException as e:
                last_err = e
                self.logger.warning(f"打开地址页等待超时，重试第{attempt + 1}次: {e}")
                try:
                    self.driver.refresh()
                except Exception:
                    pass
        raise last_err

    def open_address_page_from_profile(self):
        """从个人中心导航进入我的地址"""
        self.logger.info("从个人中心进入我的地址")

        self.open(self.PROFILE_URL)
        self.click(*self.SIDEBAR_MY_ADDRESS, timeout=25)

        # 等待 URL 跳转
        WebDriverWait(self.driver, 15).until(
            lambda d: "useraddress/index" in d.current_url
        )
        self.logger.info(f"页面已跳转至: {self.driver.current_url}")

        # 等待 document 加载完成，再给前端框架 1 秒渲染
        WebDriverWait(self.driver, 15).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(1)

        # 只要求按钮或标题出现在 DOM 中
        self._wait_address_shell_loaded(15)
        self.logger.info("新增地址按钮已加载到 DOM，页面准备就绪")

        return self

    def click_add_address(self):
        """
        点击新增地址按钮
        关键修复：使用 self.driver.find_element / WebDriverWait 获取原生 WebElement，
        绝对不能使用 self.wait_for_element_visible()（它返回 AddressPage self 用于链式调用）
        """
        self.logger.info("点击新增新地址")

        # 直接拿原生 WebElement
        btn = self.driver.find_element(*self.ADD_ADDRESS_BUTTON)

        # 滚动到视口中央
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)

        # JS 点击最稳，绕过 AmazeUI 对 button[type="button"] 的事件拦截
        self.driver.execute_script("arguments[0].click();", btn)
        self.logger.info("已执行 JS 点击新增地址按钮")

        # 等待弹窗/iframe
        self._wait_for_address_modal()

        return self

    def _wait_for_address_modal(self, timeout: int = 10):
        """等待新增/编辑地址的表单弹窗出现"""
        iframe_xpath = "//iframe[contains(@src,'useraddress/saveinfo')]"
        try:
            iframe = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, iframe_xpath))
            )
            self.logger.info("检测到地址表单 iframe，切换进入")
            self.driver.switch_to.frame(iframe)

            # 关键：等 iframe 内部 document 完全加载
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.NAME, "name"))
            )

            # 给 chosen-select 插件留初始化时间
            time.sleep(1)
            self.logger.info("iframe 内表单已加载")
            return
        except TimeoutException:
            self.logger.info("未检测到 iframe，继续在主页面查找")

        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.NAME, "name"))
        )
        self.logger.info("主页面表单已加载")

    def _set_select_by_text(self, select_name: str, text: str, retries: int = 5):
        """通过 JavaScript 直接设置 <select> 的值并触发 change 事件（带重试）"""
        script = """
            var name = arguments[0], text = arguments[1];
            var select = document.querySelector('select[name="' + name + '"]');
            if (!select) return 'select_not_found';
            var options = Array.from(select.options);
            var target = options.find(opt => opt.text.trim() === text);
            if (!target) {
                var allTexts = options.map(opt => opt.text.trim()).join(', ');
                return 'option_not_found:' + text + '|available:' + allTexts;
            }
            select.value = target.value;
            select.dispatchEvent(new Event('change', {bubbles: true}));
            if (window.jQuery) { jQuery(select).trigger('change'); }
            return 'success';
        """
        for i in range(retries):
            result = self.driver.execute_script(script, select_name, text)
            if 'success' in str(result):
                self.logger.info(f"通过 JS 设置 {select_name} = {text}")
                return self
            if i < retries - 1:
                self.logger.warning(f"第{i + 1}次设置 {select_name} 失败，0.5秒后重试...")
                time.sleep(0.5)

        if 'select_not_found' in str(result):
            raise RuntimeError(f"页面中未找到 <select name='{select_name}'>")
        available = str(result).split('|available:')[-1] if '|available:' in str(result) else 'unknown'
        raise RuntimeError(f"<select name='{select_name}'> 中未找到选项文本: {text}。可用选项: {available}")
    def _wait_for_select_populated(self, select_name: str, timeout: int = 5):
        """等待联动下拉框加载完数据（options.length > 1，即不止空占位选项）"""
        script = """
            var select = document.querySelector('select[name="' + arguments[0] + '"]');
            return select && select.options.length > 1;
        """
        end = time.time() + timeout
        while time.time() < end:
            if self.driver.execute_script(script, select_name):
                self.logger.info(f"<select name='{select_name}'> 选项已加载")
                return True
            time.sleep(0.5)
        raise TimeoutError(f"等待 <select name='{select_name}'> 联动数据加载超时（{timeout}s）")

    def select_province(self, province: str):
        """选择省份，并等待城市联动数据加载"""
        self.logger.info(f"选择省份: {province}")
        self._set_select_by_text("province", province)
        self._wait_for_select_populated("city")
        return self

    def select_city(self, city: str):
        """选择城市，并等待区/县联动数据加载"""
        self.logger.info(f"选择城市: {city}")
        self._set_select_by_text("city", city)
        self._wait_for_select_populated("county")
        return self

    def select_county(self, county: str):
        """选择区/县（页面对应 name='county'）"""
        self.logger.info(f"选择区/县: {county}")
        self._set_select_by_text("county", county)
        return self

    # ---------- 表单填写 ----------

    def fill_address_form(self, name: str, phone: str, province: str = "", city: str = "", district: str = "",
                          detail: str = "", alias: str = "", is_default: bool = False):
        """
        填写地址表单。
        注：district 参数对应页面中的 county（区/县）。
        """
        self.logger.info(f"填写地址: {name}, {detail}")

        if alias:
            self.send_keys(*self.FORM_ALIAS, alias)

        self.send_keys(*self.FORM_NAME, name)
        self.send_keys(*self.FORM_TEL, phone)

        if province:
            self.select_province(province)
        if city:
            self.select_city(city)
        if district:
            self.select_county(district)

        if detail and self.is_element_present(*self.FORM_ADDRESS, timeout=2):
            self.send_keys(*self.FORM_ADDRESS, detail)

        if is_default:
            checkbox = self.find(*self.FORM_IS_DEFAULT)
            if not checkbox.is_selected():
                checkbox.click()

        return self

    def fill_name(self, name: str):
        """填写姓名"""
        self.send_keys(*self.FORM_NAME, name)
        return self

    def save_address(self):
        """保存地址（保存后切回主页面并刷新列表，避免 SPA 未更新 DOM 导致计数不准）"""
        self.logger.info("保存地址")
        try:
            self.click(*self.SAVE_BUTTON)
        except Exception:
            self.js_click(*self.SAVE_BUTTON)

        time.sleep(1.0)

        try:
            self.driver.switch_to.default_content()
            self.logger.info("已切回主页面")
        except Exception as e:
            self.logger.warning(f"切回主页面时异常: {e}")

        self._wait_address_shell_loaded(15)
        self.logger.info("主页面已重新加载")

        self.driver.refresh()
        WebDriverWait(self.driver, 15).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        self._wait_address_shell_loaded(15)
        self.logger.info("已刷新地址列表页")

        return self

    # ---------- 地址列表操作 ----------

    def click_edit_first_address(self):
        """编辑第一个地址"""
        self.logger.info("编辑第一个地址")
        items = self.find_all(*self.ADDRESS_ITEM)
        if items:
            edit_btn = items[0].find_element(*self.EDIT_BUTTON)
            self.driver.execute_script("arguments[0].click();", edit_btn)
            self._wait_for_address_modal()
        return self

    def delete_last_address(self):
        """删除最后一个地址"""
        self.logger.info("删除最后一个地址")
        items = self.find_all(*self.ADDRESS_ITEM)
        if items:
            delete_btn = items[-1].find_element(*self.DELETE_BUTTON)
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", delete_btn)
            time.sleep(0.3)
            self.driver.execute_script("arguments[0].click();", delete_btn)
        time.sleep(0.8)
        return self

    # 修改 _click_layer_confirm 方法，增加对 AmazeUI span 确定按钮的匹配
    def _click_layer_confirm(self) -> bool:
        """尝试点击常见弹层上的「确定/确认」"""
        xpaths = [
            # 优先匹配 AmazeUI 的 span 确定按钮（带 data-am-modal-confirm 属性）
            "//span[contains(@class,'am-modal-btn') and @data-am-modal-confirm='']",
            "//span[contains(@class,'am-modal-btn') and (text()='确定' or text()='确认')]",
            # 保留原有 xpaths 作为 fallback
            "//div[contains(@class,'am-modal-active')]//button[contains(.,'确定')]",
            "//div[contains(@class,'am-modal-active')]//button[contains(.,'确认')]",
            "//div[contains(@class,'am-modal-active')]//a[contains(.,'确定')]",
            "//div[contains(@class,'am-modal')]//button[contains(@class,'am-modal-btn')]",
            "//button[contains(@class,'am-btn-danger') and (contains(.,'确定') or contains(.,'确认'))]",
            "//div[contains(@class,'layui-layer')]//a[contains(.,'确定')]",
        ]
        for xp in xpaths:
            try:
                el = WebDriverWait(self.driver, 4).until(
                    EC.element_to_be_clickable((By.XPATH, xp))
                )
                self.driver.execute_script("arguments[0].click();", el)
                self.logger.info(f"已点击弹层确认: {xp[:50]}...")
                return True
            except TimeoutException:
                continue
            except Exception:
                continue
        return False

    def confirm_delete(self):
        """确认删除（兼容浏览器原生 confirm 与 AmazeUI / Layui 弹层）"""
        self.logger.info("确认删除")
        confirmed = False
        try:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            self.driver.switch_to.alert.accept()
            self.logger.info("已确认浏览器原生弹窗")
            confirmed = True
        except TimeoutException:
            pass
        if not confirmed and self.is_element_visible(*self.CONFIRM_DELETE, timeout=2):
            try:
                self.click(*self.CONFIRM_DELETE, timeout=5)
            except Exception:
                self.js_click(*self.CONFIRM_DELETE)
            confirmed = True
        if not confirmed:
            confirmed = self._click_layer_confirm()
        if confirmed:
            time.sleep(0.5)
            try:
                self.driver.switch_to.default_content()
            except Exception:
                pass
            self.driver.refresh()
            WebDriverWait(self.driver, 15).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            self._wait_address_shell_loaded(15)
        return self

    def set_default_address(self, index: int):
        """设置指定地址为默认"""
        self.logger.info(f"设置第{index}个地址为默认")
        items = self.find_all(*self.ADDRESS_ITEM)
        if 0 <= index < len(items):
            default_btn = items[index].find_element(*self.SET_DEFAULT_BUTTON)
            try:
                self.driver.execute_script("arguments[0].click();", default_btn)
            except Exception:
                default_btn.click()
            try:
                WebDriverWait(self.driver, 3).until(EC.alert_is_present())
                self.driver.switch_to.alert.accept()
            except TimeoutException:
                pass
            time.sleep(0.5)
            self.driver.refresh()
            WebDriverWait(self.driver, 15).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            self._wait_address_shell_loaded(15)
            deadline = time.time() + 12
            while time.time() < deadline and not self.is_default_address(index):
                time.sleep(0.4)
        return self

    # ========== 状态获取 ==========

    def get_address_count(self) -> int:
        """获取地址数量（确保在主页面上下文）"""
        # 安全切回主页面
        try:
            self.driver.switch_to.default_content()
        except Exception:
            pass

        try:
            items = self.find_all(*self.ADDRESS_ITEM)
            count = len(items)
            self.logger.info(f"当前地址数量: {count}")
            return count
        except Exception:
            self.logger.warning("获取地址数量失败，返回 0")
            return 0

    def get_first_address_name(self) -> str:
        """获取第一个地址的姓名"""
        try:
            items = self.find_all(*self.ADDRESS_ITEM)
            if items:
                return items[0].find_element(*self.ADDRESS_NAME).text
            return ""
        except Exception:
            return ""

    def is_default_address(self, index: int) -> bool:
        """指定索引是否是默认地址"""
        try:
            items = self.find_all(*self.ADDRESS_ITEM)
            if 0 <= index < len(items):
                row = items[index]
                if row.find_elements(*self.ADDRESS_DEFAULT_TAG):
                    return True
                return "默认" in (row.text or "")
            return False
        except Exception:
            return False

    def is_address_page_loaded(self) -> bool:
        """地址页面是否加载完成"""
        if "useraddress" not in self.driver.current_url:
            return False
        return self.is_element_present(*self.ADD_ADDRESS_BUTTON, timeout=10) or self.is_element_present(
            *self.PAGE_TITLE, timeout=5
        )